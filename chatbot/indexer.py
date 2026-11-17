"""Indexador: convierte los archivos Markdown de `knowledge/` en una lista de secciones.

Este módulo NO busca nada: solo lee, corta y prepara el texto.
La búsqueda vive en `search.py`.

Recorrido:
    1. leer_secciones() abre cada .md de la carpeta knowledge/.
    2. _dividir_en_secciones() lo corta en cada título ## o ###.
    3. Cada sección guarda su texto ORIGINAL (para devolverlo literal al usuario)
       y una versión NORMALIZADA (para comparar contra la pregunta).
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

# Carpeta donde están los 5 Markdown. Si algún día los movés, cambiá solo esta línea.
CARPETA_KNOWLEDGE = Path(__file__).resolve().parent / "knowledge"

# Nombre "lindo" para los archivos que no son de un TP (se usa en la fuente: "📄 Programación · ...").
NOMBRES_ARCHIVO = {
    "programacion": "Programación",
    "arquitectura": "Arquitectura",
}

# ---------------------------------------------------------------------------
# Stopwords: palabras tan comunes que no ayudan a distinguir un tema de otro.
# Están escritas YA normalizadas (minúsculas y sin tildes), porque se comparan
# después de normalizar. Podés agregar o quitar palabras libremente.
# ---------------------------------------------------------------------------
STOPWORDS = set("""
a al algo algun alguna algunas alguno algunos ante antes aqui asi aun
cada como con contra cual cuales cualquier cuando cuanto cuanta cuantos cuantas
de del desde donde dos e el ella ellas ello ellos en entre era eran es esa esas
ese eso esos esta estaba estado estan estar este esto estos estoy fue fueron
ha habia han hasta hay la las le les lo los mas me mi mis mucho muy
nada ni no nos nosotros o otra otras otro otros para pero poco por porque
puede pueden que quien quienes se sea segun ser si sido siempre sin sobre
su sus tal tambien tan tanto te tiene tienen todo todos tu tus un una unas uno unos
usted y ya yo
hola buenas buen dia porfa favor gracias quiero queria necesito saber decime
deci dame explicame explica explicar mostrame muestra mostrar contame cuenta
significa significado define definicion definir dice entiendo ayuda ayudame
podes podrias puedo hace hacer hacen hizo calcula calcular calculo
""".split())
# Nota: dejamos "calculo" en stopwords porque casi todas las secciones calculan
# algo; si querés que pese, sacalo de la lista.


def normalizar(texto: str) -> str:
    """Pasa a minúsculas, quita tildes y signos, y colapsa espacios.

    Ejemplo: "¿Qué es la Desviación Estándar?" -> "que es la desviacion estandar"
    La ñ también se convierte en n (es lo esperable al escribir rápido sin tildes).
    """
    texto = unicodedata.normalize("NFD", texto.lower())
    # Las letras con tilde se descomponen en letra + marca; acá descartamos la marca.
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    # Todo lo que no sea letra o número se vuelve espacio.
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    return texto.strip()


def sin_stopwords(texto_normalizado: str) -> str:
    """Quita las stopwords de un texto que ya pasó por normalizar()."""
    return " ".join(p for p in texto_normalizado.split() if p not in STOPWORDS)


def preparar(texto: str) -> str:
    """Atajo: normalizar + quitar stopwords. Es la forma en que se compara todo."""
    return sin_stopwords(normalizar(texto))


@dataclass
class Seccion:
    """Una porción de un .md que empieza en un título ## o ###."""
    archivo: str                 # "tp2.md"
    tp: str                      # "TP2", "Programación", ...
    titulo: str                  # "Ejercicio 4 — Laplace con y sin sustitución"
    contenido: str               # Markdown literal, con los bloques de código intactos
    palabras_clave: list[str] = field(default_factory=list)
    padre: str = ""              # título ## que contiene a este ### (contexto para buscar)
    documento: str = ""          # título # del archivo (ej.: "TP2 — Probabilidad")

    @property
    def etiqueta(self) -> str:
        """Texto único que identifica la sección: "TP2 · Ejercicio 4 — Laplace…"."""
        return f"{self.tp} · {self.titulo}"

    # Versiones normalizadas: se calculan una vez y se reutilizan en cada búsqueda.
    @property
    def titulo_norm(self) -> str:
        return preparar(self.titulo)

    @property
    def claves_norm(self) -> str:
        return preparar(" ".join(self.palabras_clave))

    def texto_indexable(self) -> str:
        """Lo que ve TF-IDF. El título y las palabras clave van DOS veces para pesar más."""
        partes = [
            self.titulo, self.titulo,
            " ".join(self.palabras_clave), " ".join(self.palabras_clave),
            self.padre, self.documento, self.tp,
            self.contenido,
        ]
        return preparar(" ".join(partes))


def _tp_desde_archivo(nombre: str) -> str:
    """tp1.md -> "TP1";  programacion.md -> "Programación";  otro.md -> "Otro"."""
    base = Path(nombre).stem.lower()
    coincidencia = re.search(r"tp\s*_?(\d+)", base)
    if coincidencia:
        return f"TP{coincidencia.group(1)}"
    return NOMBRES_ARCHIVO.get(base, base.replace("_", " ").capitalize())


# Reconoce una línea "Palabras clave: a, b, c" (también con negrita: **Palabras clave:**)
_RE_CLAVES = re.compile(r"^\s*[*_]*\s*palabras\s+clave\s*:?\s*[*_]*\s*:?\s*(.+)$", re.IGNORECASE)
# Reconoce títulos de nivel 1, 2 o 3: "# ...", "## ...", "### ..."
_RE_TITULO = re.compile(r"^(#{1,3})\s+(.+?)\s*#*\s*$")
# Reconoce la apertura/cierre de un bloque de código: ``` o ~~~
_RE_FENCE = re.compile(r"^\s*(```|~~~)")


def _dividir_en_secciones(texto: str, archivo: str) -> list[Seccion]:
    """Corta un Markdown en secciones ## / ###.

    Detalles importantes:
    - Un "## Algo" dentro de un bloque de código NO es un título (por eso seguimos
      si estamos dentro de ``` ... ```).
    - Los títulos #### y más profundos quedan DENTRO de la sección ### que los contiene.
    - Si un ## no tiene texto propio (solo sub-secciones ###), no se guarda vacío.
    """
    tp = _tp_desde_archivo(archivo)
    documento = ""
    padre = ""
    secciones: list[Seccion] = []
    actual: dict | None = None
    dentro_de_codigo = False

    def cerrar():
        if actual is None:
            return
        lineas = actual["lineas"]
        claves: list[str] = []
        limpias = []
        for linea in lineas:
            m = _RE_CLAVES.match(linea) if not claves else None
            if m:
                # "media, promedio; esperanza" -> ["media", "promedio", "esperanza"]
                claves = [c.strip(" *_.") for c in re.split(r"[,;]", m.group(1)) if c.strip(" *_.")]
            else:
                limpias.append(linea)
        contenido = "\n".join(limpias).strip()
        if contenido:
            secciones.append(Seccion(
                archivo=archivo, tp=tp, titulo=actual["titulo"], contenido=contenido,
                palabras_clave=claves, padre=actual["padre"], documento=documento,
            ))

    for linea in texto.splitlines():
        if _RE_FENCE.match(linea):
            dentro_de_codigo = not dentro_de_codigo
        titulo = None if dentro_de_codigo else _RE_TITULO.match(linea)

        if titulo:
            nivel, texto_titulo = len(titulo.group(1)), titulo.group(2).strip()
            if nivel == 1:
                documento = texto_titulo
                continue
            cerrar()
            if nivel == 2:
                padre = texto_titulo
                actual = {"titulo": texto_titulo, "padre": "", "lineas": []}
            else:  # nivel 3
                actual = {"titulo": texto_titulo, "padre": padre, "lineas": []}
        elif actual is not None:
            actual["lineas"].append(linea)
        # El texto antes del primer ## (introducción del archivo) se ignora a propósito.

    cerrar()
    return secciones


def leer_secciones(carpeta: Path | None = None) -> list[Seccion]:
    """Lee todos los .md de la carpeta y devuelve la lista completa de secciones."""
    carpeta = carpeta or CARPETA_KNOWLEDGE
    if not carpeta.is_dir():
        raise FileNotFoundError(f"No existe la carpeta de conocimiento: {carpeta}")

    secciones: list[Seccion] = []
    for ruta in sorted(carpeta.glob("*.md")):
        # utf-8-sig tolera archivos guardados con BOM desde el Bloc de notas de Windows.
        texto = ruta.read_text(encoding="utf-8-sig")
        secciones.extend(_dividir_en_secciones(texto, ruta.name))
    return secciones
