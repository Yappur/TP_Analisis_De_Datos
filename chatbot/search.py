"""Motor de búsqueda local por palabras clave.

No genera texto: elige UNA sección de los .md y la devuelve tal cual.

Puntaje de cada sección (cuanto más alto, mejor):

    puntaje = similitud coseno TF-IDF                 (0 a 1: cuánto se parece el vocabulario)
            + PESO_TITULO  * cobertura del título     (qué parte de la pregunta está en el título)
            + PESO_CLAVES  * cobertura de claves      (ídem con la línea "Palabras clave: ...")
            + PESO_FUZZY   * parecido difuso título   (rapidfuzz.partial_ratio, tolera tipeos)
            + PESO_CONTENIDO * cobertura del texto    (qué parte de la pregunta aparece en la sección)
            + PESO_DEFINICION si la pregunta pide una definición ("qué es...") y la sección
              es un glosario o una lista de conceptos/fórmulas

El último término existe porque las secciones largas (glosarios, fórmulas) tienen un
coseno bajo aunque contengan la palabra buscada; así "mediana" o "curtosis" se encuentran.
Una pregunta fuera de tema ("capital de Francia") tiene cobertura 0 y no lo aprovecha.

Después, el puntaje se multiplica por la proporción de palabras de la pregunta que
existen en los .md. Si preguntás "datos del clima en Tucumán", solo "datos" existe:
el puntaje se reduce a un tercio y la pregunta queda fuera.

Si el mejor puntaje no llega a UMBRAL, se responde "No tengo información...".
Para calibrar los números de abajo, corré:  python -m chatbot.probar
"""
from __future__ import annotations

import re
import threading
from dataclasses import dataclass

from rapidfuzz import fuzz, process
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from chatbot.indexer import Seccion, leer_secciones, normalizar, sin_stopwords
from chatbot.sinonimos import SINONIMOS

# ---------------------------------------------------------------------------
# Parámetros ajustables
# ---------------------------------------------------------------------------
UMBRAL = 0.15              # puntaje mínimo para considerar que hay respuesta
UMBRAL_SUGERENCIA = 0.08   # puntaje mínimo para ofrecer una sección como sugerencia
MAX_SUGERENCIAS = 2

PESO_TITULO = 0.35
PESO_CLAVES = 0.25
PESO_FUZZY = 0.15
PESO_CONTENIDO = 0.15
PESO_DEFINICION = 0.15

# Preguntas de definición y secciones que las responden mejor (comparación ya normalizada).
_RE_DEFINICION = re.compile(r"\b(que es|que son|que significa|significado|definicion|defini|concepto)\b")
TITULOS_DE_DEFINICION = {"glosario", "conceptos", "formulas", "convenciones", "clasificacion"}
FUZZY_MINIMO = 75          # partial_ratio por debajo de esto no suma nada
CORRECCION_MINIMA = 85     # parecido mínimo para corregir una palabra mal escrita

MENSAJE_SIN_RESULTADO = (
    "No tengo información sobre eso en el proyecto. Probá preguntar sobre los TPs, "
    "el glosario o la programación."
)

# "tp1", "tp2", "tp3" en la pregunta (ya normalizada y con sinónimos aplicados)
_RE_TP = re.compile(r"\btp([0-9]+)\b")


@dataclass
class Resultado:
    encontrado: bool
    titulo: str = ""
    tp: str = ""
    archivo: str = ""
    respuesta_md: str = MENSAJE_SIN_RESULTADO
    sugerencias: list[str] | None = None
    puntaje: float = 0.0          # no se envía al navegador; lo usa probar.py
    consulta: str = ""            # pregunta tal como quedó después de procesarla

    def a_dict(self) -> dict:
        """Formato exacto que devuelve POST /api/chat."""
        return {
            "encontrado": self.encontrado,
            "titulo": self.titulo,
            "tp": self.tp,
            "archivo": self.archivo,
            "respuesta_md": self.respuesta_md,
            "sugerencias": self.sugerencias or [],
        }


def _compilar_sinonimos(diccionario: dict[str, str]) -> list[tuple[re.Pattern, str]]:
    """Convierte el diccionario en expresiones regulares, de la clave más larga a la más corta."""
    reglas = []
    for clave, valor in diccionario.items():
        clave_n, valor_n = normalizar(clave), normalizar(valor)
        if clave_n:
            reglas.append((clave_n, valor_n))
    reglas.sort(key=lambda par: len(par[0]), reverse=True)
    # \b asegura palabras completas: la regla "media" no toca "mediana".
    return [(re.compile(rf"\b{re.escape(c)}\b"), v) for c, v in reglas]


class Buscador:
    """Guarda el índice TF-IDF en memoria. Se construye una sola vez al iniciar la app."""

    def __init__(self, secciones: list[Seccion]):
        if not secciones:
            raise ValueError("No se encontró ninguna sección en los archivos Markdown.")
        self.secciones = secciones
        self._reglas_sinonimos = _compilar_sinonimos(SINONIMOS)

        # TfidfVectorizer: cada sección se convierte en un vector de pesos por palabra.
        #  - ngram_range=(1, 2): palabras sueltas y pares ("desviacion estandar").
        #  - token_pattern acepta tokens de 1 carácter para no perder números ("ejercicio 5").
        #  - sublinear_tf: una palabra repetida 20 veces no pesa 20 veces más.
        #  El texto ya llega normalizado y sin stopwords desde indexer.preparar().
        self.vectorizador = TfidfVectorizer(
            ngram_range=(1, 2),
            token_pattern=r"(?u)\b\w+\b",
            sublinear_tf=True,
            lowercase=False,
        )
        self.matriz = self.vectorizador.fit_transform(s.texto_indexable() for s in secciones)

        # Vocabulario de palabras sueltas: contra esto se corrigen los errores de tipeo.
        self.vocabulario = sorted(t for t in self.vectorizador.vocabulary_ if " " not in t)
        self._vocab_set = set(self.vocabulario)

        # Atajo para coincidencias exactas (cuando el usuario toca una sugerencia o un tema).
        self._por_etiqueta = {normalizar(s.etiqueta): i for i, s in enumerate(secciones)}

        # Precalculado para no repetirlo en cada pregunta.
        self._titulos = [set(s.titulo_norm.split()) for s in secciones]
        self._claves = [set(s.claves_norm.split()) for s in secciones]
        self._palabras = [set(s.texto_indexable().split()) for s in secciones]
        self._es_glosario = [bool(t & TITULOS_DE_DEFINICION) for t in self._titulos]

    # ------------------------------------------------------------------
    # Paso 1: preparar la pregunta
    # ------------------------------------------------------------------
    def _aplicar_sinonimos(self, texto: str) -> str:
        for patron, reemplazo in self._reglas_sinonimos:
            texto = patron.sub(reemplazo, texto)
        return re.sub(r"\s+", " ", texto).strip()

    def _corregir(self, palabra: str) -> str:
        """Si la palabra no existe en los .md, busca la más parecida ("varianca" -> "varianza")."""
        if palabra in self._vocab_set or len(palabra) < 4 or palabra.isdigit():
            return palabra
        mejor = process.extractOne(palabra, self.vocabulario, scorer=fuzz.ratio,
                                   score_cutoff=CORRECCION_MINIMA)
        return mejor[0] if mejor else palabra

    def procesar_pregunta(self, pregunta: str) -> tuple[str, str | None, bool]:
        """Devuelve (consulta lista para buscar, TP a filtrar o None, ¿pide una definición?)."""
        normal = normalizar(pregunta)
        definicion = bool(_RE_DEFINICION.search(normal))   # se mira ANTES de quitar stopwords
        texto = self._aplicar_sinonimos(normal)
        tp = _RE_TP.search(texto)
        filtro = f"TP{tp.group(1)}" if tp else None
        palabras = [self._corregir(p) for p in sin_stopwords(texto).split()]
        return " ".join(palabras), filtro, definicion

    # ------------------------------------------------------------------
    # Paso 2: puntuar las secciones
    # ------------------------------------------------------------------
    def _puntajes(self, consulta: str, filtro: str | None,
                  definicion: bool = False) -> list[tuple[float, int]]:
        palabras = set(consulta.split())
        # "tp1", "tp2"... ya se usan como filtro; no deben bajar la cobertura del título.
        palabras_tema = {p for p in palabras if not _RE_TP.fullmatch(p)} or palabras

        # Proporción de palabras que existen en algún .md (1.0 = todas conocidas).
        conocidas = sum(1 for p in palabras_tema if p in self._vocab_set) / len(palabras_tema)

        vector = self.vectorizador.transform([consulta])
        cosenos = linear_kernel(vector, self.matriz).ravel()  # coseno (los vectores ya están normalizados)

        resultados = []
        for i, seccion in enumerate(self.secciones):
            if filtro and seccion.tp != filtro:
                continue

            puntaje = float(cosenos[i])

            # Bonus por título: proporción de palabras de la pregunta que están en el título.
            en_titulo = len(palabras_tema & self._titulos[i]) / len(palabras_tema)
            puntaje += PESO_TITULO * en_titulo

            # Bonus por palabras clave declaradas en el .md.
            if self._claves[i]:
                en_claves = len(palabras_tema & self._claves[i]) / len(palabras_tema)
                puntaje += PESO_CLAVES * en_claves

            # Bonus por cobertura: todas las palabras de la pregunta aparecen en la sección.
            en_texto = len(palabras_tema & self._palabras[i]) / len(palabras_tema)
            puntaje += PESO_CONTENIDO * en_texto

            # Bonus para glosarios cuando se pregunta "qué es...", solo si el término aparece.
            if definicion and self._es_glosario[i] and en_texto == 1:
                puntaje += PESO_DEFINICION

            # Bonus difuso: tolera palabras pegadas, cortadas o con errores contra el título.
            if len(consulta) >= 4:
                parecido = fuzz.partial_ratio(consulta, seccion.titulo_norm)
                if parecido > FUZZY_MINIMO:
                    puntaje += PESO_FUZZY * (parecido - FUZZY_MINIMO) / (100 - FUZZY_MINIMO)

            resultados.append((puntaje * conocidas, i))

        resultados.sort(reverse=True)
        return resultados

    # ------------------------------------------------------------------
    # Paso 3: armar la respuesta
    # ------------------------------------------------------------------
    def _resultado(self, i: int, puntaje: float, consulta: str, sugerencias: list[str]) -> Resultado:
        s = self.secciones[i]
        return Resultado(encontrado=True, titulo=s.titulo, tp=s.tp, archivo=s.archivo,
                         respuesta_md=s.contenido, sugerencias=sugerencias,
                         puntaje=round(puntaje, 3), consulta=consulta)

    def buscar(self, pregunta: str) -> Resultado:
        # Coincidencia exacta con "TP2 · Ejercicio 4 — ..." (botones de sugerencias y temas).
        exacta = self._por_etiqueta.get(normalizar(pregunta))
        if exacta is not None:
            consulta = self.secciones[exacta].titulo_norm
            vecinos = [i for _, i in self._puntajes(consulta, self.secciones[exacta].tp) if i != exacta]
            sugerencias = [self.secciones[i].etiqueta for i in vecinos[:MAX_SUGERENCIAS]]
            return self._resultado(exacta, 1.0, consulta, sugerencias)

        consulta, filtro, definicion = self.procesar_pregunta(pregunta)
        if not consulta:
            return Resultado(encontrado=False, consulta=consulta)

        ranking = self._puntajes(consulta, filtro, definicion)
        if not ranking or ranking[0][0] < UMBRAL:
            mejor = ranking[0][0] if ranking else 0.0
            return Resultado(encontrado=False, puntaje=round(mejor, 3), consulta=consulta)

        mejor_puntaje, mejor = ranking[0]
        sugerencias = [self.secciones[i].etiqueta
                       for p, i in ranking[1:1 + MAX_SUGERENCIAS] if p >= UMBRAL_SUGERENCIA]
        return self._resultado(mejor, mejor_puntaje, consulta, sugerencias)

    def temas(self) -> dict[str, list[str]]:
        """Títulos agrupados por TP, en el orden en que aparecen en los archivos."""
        agrupados: dict[str, list[str]] = {}
        for s in self.secciones:
            agrupados.setdefault(s.tp, []).append(s.titulo)
        return agrupados


# ---------------------------------------------------------------------------
# Instancia única compartida por toda la app
# ---------------------------------------------------------------------------
_buscador: Buscador | None = None
_candado = threading.Lock()


def cargar() -> Buscador:
    """Lee los .md y construye el índice. Se llama desde el lifespan de main.py."""
    global _buscador
    with _candado:
        _buscador = Buscador(leer_secciones())
    return _buscador


def obtener() -> Buscador:
    """Devuelve el buscador; si todavía no se cargó (ej.: en tests), lo carga."""
    return _buscador or cargar()


def buscar(pregunta: str) -> Resultado:
    return obtener().buscar(pregunta)


def temas() -> dict[str, list[str]]:
    return obtener().temas()
