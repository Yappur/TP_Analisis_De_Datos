# Manual de programación — Probabilidad y Estadística

## Alcance y estado comprobado

Esta guía describe el código presente en el repositorio. La aplicación resuelve y visualiza TP1, TP2 y TP3 con Python/FastAPI y un frontend HTML, CSS y JavaScript. También existe una integración de chatbot RAG en [`chatbot/`](../): un router HTTP, un servicio que recupera evidencia de cinco Markdown permitidos, índice JSON local y cliente web. Su uso requiere configurar un proveedor de IA compatible; esta documentación no contiene claves ni tokens.

## Lenguaje, bibliotecas y dependencias

| Tecnología | Uso comprobado |
|---|---|
| Python | Ejercicios, cálculos, API y exportación de Excel. |
| FastAPI | Rutas JSON, páginas y descargas. |
| Uvicorn | Servidor de desarrollo indicado en comentarios y documentación: `uvicorn main:app --reload`. |
| pandas | `DataFrame`/`Series`, máscaras, tablas de contingencia, frecuencias, acumuladas, resúmenes y agrupación. |
| openpyxl | Creación y formato de libros, hojas, celdas, gráficos de barras y configuración de impresión. |
| JavaScript vanilla | Solicitudes `fetch`, menú de ejercicios, tablas, temas y gráficos del navegador. |
| Chart.js 4.4.1 | Gráficos de barras en el frontend, cargado desde jsDelivr en las páginas HTML. |
| `urllib`, `json`, `hashlib`, `asyncio`, `threading`, `math` | HTTP compatible con API OpenAI, almacenamiento/lectura JSON, huellas de documentos, ejecución asíncrona y coseno del RAG. Son módulos estándar de Python. |
| Pydantic | Modelos y validación de solicitudes/respuestas de chat; se importa desde el stack FastAPI. |
| HTML y CSS vanilla | Páginas semánticas, glosarios, clasificación de variables y diseño adaptable. |

Las dependencias Python declaradas directamente están en [`requirements.txt`](../../requirements.txt): `fastapi`, `uvicorn`, `pandas` y `openpyxl`. `importlib`, `pathlib`, `fractions`, `itertools`, `urllib`, `json`, `hashlib`, `asyncio`, `threading` y `math` son módulos de la biblioteca estándar. No se usa SciPy ni un SDK dedicado de chatbot; el servicio usa HTTP estándar. Chart.js se carga desde la página y no figura en `requirements.txt`.

## Organización de los archivos fuente

| Archivo o carpeta | Responsabilidad |
|---|---|
| [`main.py`](../../main.py) | Crea la instancia FastAPI, valida números de ejercicio, carga módulos dinámicamente, define rutas y sirve páginas estáticas. |
| [`ejercicios/`](../../ejercicios/) | Diez resoluciones del TP1. |
| [`ejercicios_tp2/`](../../ejercicios_tp2/) | Diecisiete resoluciones del TP2. |
| [`ejercicios_tp3/`](../../ejercicios_tp3/) | Veinticinco resoluciones del TP3. |
| [`estadistica.py`](../../estadistica.py) | Bloques JSON, gráficos, redondeo, estadística descriptiva, percentiles, asimetría y medidas para datos agrupados. |
| [`probabilidad.py`](../../probabilidad.py) | Helpers de cartas/dados, regla de Laplace, fracciones, tablas marginales, probabilidad total y Bayes. |
| [`distribuciones.py`](../../distribuciones.py) | Distribuciones binomial, Poisson y geométrica, sumas de eventos y momentos discretos. |
| [`exportar_excel.py`](../../exportar_excel.py) | Exporta un módulo de ejercicio a un libro `.xlsx`; incluye formatos, hojas, tablas auxiliares y gráficos. |
| [`generar_excel.py`](../../generar_excel.py) | Genera un libro TP1 consolidado, con una hoja de resumen y una hoja por ejercicio. |
| [`static/index.html`](../../static/index.html) | Página TP1, tarjetas de variables y glosario TP1. |
| [`static/tp2.html`](../../static/tp2.html), [`static/tp3.html`](../../static/tp3.html) | Páginas TP2/TP3, glosarios y `data-api` de cada TP. |
| [`static/js.js`](../../static/js.js) | Lógica compartida de carga, renderizado, tema y gráficos. |
| [`static/style.css`](../../static/style.css) | Diseño visual, temas claro/oscuro y puntos de adaptación móvil. |
| [`static/chatbot.js`](../../static/chatbot.js) | Cliente del panel flotante del chatbot: salud, consultas, render Markdown acotado y fuentes. |
| [`docs/`](../../docs/) | PDFs de TP2 y TP3; no se encontró un PDF de TP1. |
| [`chatbot/router.py`](../router.py) | Modelos Pydantic, límites de petición y rutas `/api/chat`. |
| [`chatbot/assistant.py`](../assistant.py) | Configuración, carga de fuentes permitidas, indexación y recuperación RAG, verificación de evidencia y generación de respuesta. |
| [`chatbot/prompts.py`](../prompts.py) | Instrucción del sistema del asistente. |
| [`chatbot/README.md`](../README.md) | Configuración y operación del chatbot. |
| [`chatbot/knowledge/`](.) | Los cinco Markdown que el indexador permite como únicas fuentes. |
| [`tests/test_chatbot.py`](../../tests/test_chatbot.py) | Pruebas unitarias del allowlist, chunking, abstención, validación y autenticación de reindexación. |
| [`.env.example`](../../.env.example) | Nombres de variables de configuración con valores vacíos o no sensibles. |

Cada ejercicio sigue el contrato: constantes `TITULO` y `ENUNCIADO`, y `resolver()` que devuelve una lista de bloques. Un bloque suele incluir subtítulo, columnas, filas, notas y, opcionalmente, un gráfico. Los cálculos específicos están en el módulo del ejercicio; el código común se reutiliza cuando existe.

No hay clases en los módulos de ejercicios. La mayoría declara solo `resolver()` además de sus constantes; excepciones relevantes: TP1 [`ej10.py`](../../ejercicios/ej10.py) separa `lenguajes()`, `comprension()` y `razonamiento()`; TP2 [`ej06.py`](../../ejercicios_tp2/ej06.py) define `condicional()`, TP2 [`ej02.py`](../../ejercicios_tp2/ej02.py) usa una función local `fila()` y [`ej08.py`](../../ejercicios_tp2/ej08.py) una función local `indep()`; TP3 [`ej02.py`](../../ejercicios_tp3/ej02.py) define `r6()`, [`ej04.py`](../../ejercicios_tp3/ej04.py) usa la función local `p()` y [`ej23.py`](../../ejercicios_tp3/ej23.py) usa una expresión `lambda` local. También hay lambdas en algunos cálculos TP2. Los demás ejercicios no declaran clases ni helpers nombrados adicionales según el inventario de los módulos.

Detalles de esas excepciones:

- TP1 `lenguajes()` no recibe argumentos: lee el texto global del módulo, extrae categorías, calcula conteos, frecuencias relativas, porcentajes y moda; retorna una lista de un bloque con tabla y gráfico. `comprension()` tampoco recibe argumentos: usa las listas globales de dos carreras, calcula medidas y CV, y retorna un bloque comparativo con gráfico. `razonamiento()` calcula estadísticos descriptivos de los datos globales y un histograma de diez intervalos; retorna un bloque. Las tres funciones son llamadas por `resolver()` en [`ej10.py`](../../ejercicios/ej10.py).
- TP2 `condicional(evento,dado_que)` recibe dos máscaras booleanas alineadas al espacio muestral y devuelve una `Fraction` con \(P(E\mid F)\), dividiendo Laplace de la intersección por Laplace de la condición; requiere que el denominador sea positivo. La función local `fila(inciso,definicion,mascara)` del ejercicio 2 devuelve una lista con inciso, definición, conjunto seleccionado y cantidad. La función local `indep(x,y)` del ejercicio 8 recibe nombres de eventos y devuelve si la probabilidad conjunta almacenada coincide con el producto de marginales. Se complementan con helpers de [`probabilidad.py`](../../probabilidad.py).
- TP3 `r6(x)` del ejercicio 2 convierte a float, redondea a seis decimales y devuelve texto para mostrar operandos; no calcula momentos. La función local `p(m)` del ejercicio 4 suma las masas seleccionadas por una máscara. En el ejercicio 23, `en_rango` es una lambda que recibe una tabla y produce la máscara \(6\le x\le8\); se aplica a la tabla binomial y Poisson para compararlas.

## Helpers estadísticos: `estadistica.py`

- **`r(x, decimales=4)`**: convierte el valor a `float` y lo redondea para salida/JSON. Recibe un número y retorna un número.
- **`bloque(subtitulo, columnas, filas, grafico=None, notas=())`**: empaqueta contenido de resolución como diccionario. Es el contrato compartido entre ejercicios, API y frontend.
- **`barras(etiquetas, series)`**: convierte etiquetas y series a valores numéricos simples que JSON y Chart.js pueden consumir.
- **`percentil(datos, p)`**: construye una `Series`, ordena y aplica la convención del proyecto: posición \(pn/100\), promedia dos observaciones si es entera y si no toma el índice base cero correspondiente. No llama `Series.quantile()`.
- **`tipo_asimetria(valor)`**: clasifica por los cortes de 0,05 y −0,05 como positiva, negativa o aproximadamente simétrica.
- **`pearson_bowley(...)`**: calcula los dos coeficientes de asimetría; Pearson cambia de fórmula según haya una sola moda y Bowley controla el caso \(Q_3=Q_1\).
- **`interpretar(pearson,bowley)`**: forma notas textuales de interpretación.
- **`resolver_simple(datos,poblacion=True,percentiles=(),continuo=False)`**: convierte los datos en `Series`; calcula media, mediana, moda, rango, varianza, desvío, CV, cuartiles, coeficientes y percentiles solicitados. `poblacion` selecciona `ddof=0` o `ddof=1`; `continuo` elige histograma con `pd.cut` en lugar de barras por valor. Retorna una lista de bloques.
- **`resolver_agrupado(tabla,h,poblacion=True)`**: recibe tabla con etiqueta, límite inferior `li`, frecuencia `f` y marca de clase, y amplitud `h`. Calcula acumuladas, media, varianza/desvío, cuantiles interpolados y moda agrupada; devuelve tabla de frecuencia y bloque de medidas.

**Pandas en TP1:** `Series`/`DataFrame`, `sort_values`, `reset_index`, `iloc`, `mean`, `median`, `std`, `var`, `value_counts`, `sort_index`, `max`, `min`, `cumsum`, `sum`, `idxmax`, `copy`, `mode`, `sem`, `kurt`, `skew`, `count`, `reindex`, `items`, `index`, `values` y `cut`. En el ejercicio 7 se cuentan intervalos con comparaciones vectorizadas y `.sum()`; en el 10 se calculan frecuencias/porcentajes y medidas con métodos de pandas.

**Pandas en TP2:** `DataFrame` y `Series`; `MultiIndex.from_product`, `RangeIndex`, `merge(how="cross")`; `map`, `astype`, `loc`, `reset_index`, `isin`, `sum`, `copy`, `apply`, `all`; y acceso a `columns`, `index` y `values`, además de máscaras booleanas. Se usan para construir espacios muestrales, filtrar eventos, contar casos y presentar tablas.

**Pandas en TP3:** `DataFrame`; selección de columnas, máscaras, `loc`, `iloc`, `sum`, `cumsum`, `copy`, `values`, `astype(object)`, `head(10)` y `columns`. Se usan para construir distribuciones, acumular masas y seleccionar los valores que corresponden a cada inciso. Los nombres citados son métodos/atributos de pandas, no funciones de probabilidad.

## Helpers de probabilidad: `probabilidad.py`

- **`es_decimal_exacto(x)`**: identifica si el denominador de una `Fraction` solo tiene factores 2 y 5 y es apto para una presentación decimal finita.
- **`fraccion(x)`**: convierte fracciones a texto exacto, o decimal cuando corresponde; los flotantes se redondean para presentación.
- **`fila(planteo,calculo,valor)`**: genera una fila con fórmula, sustitución, texto del resultado y decimal.
- **`laplace(casos)`**: para una serie booleana, retorna favorables / posibles como `Fraction`.
- **`texto_laplace(casos)`**: presenta el conteo `favorables / posibles`.
- **`conjunto(elementos)`**: transforma resultados en notación de conjunto o vacío.
- **`baraja()` y `dado()`**: devuelven `DataFrame` de cartas y caras posibles.
- **`con_totales(tabla)`**: copia una tabla de contingencia y añade sumas por filas y columnas, incluidos los totales marginales.
- **`bloque_tabla(...)` y `bloque_resolucion(...)`**: serializan una tabla o una resolución como bloque compartido.
- **`total(probabilidades,condicionales)`**: devuelve una tabla con \(P(H_i)\), \(P(E\mid H_i)\), su producto y la suma total \(P(E)\).
- **`bloque_bayes(tabla,nombre_hipotesis,decimal=False,bayes=True)`**: calcula y agrega \(P(H_i\mid E)\) sobre la tabla de probabilidad total; `bayes=False` presenta solo total. El parámetro `decimal` controla cómo representa decimales en el texto.

Este módulo usa pandas para espacios muestrales y tablas; `Fraction` para precisión exacta; `itertools.product` para combinaciones de resultados; y `merge(how="cross")` en el ejercicio de cartas.

## Distribuciones discretas: `distribuciones.py`

- **`num(v)`**, **`en_porcentaje(v)`**, **`texto(v)`**, **`coma(x)`**: redondeo y formato de número/fracción/porcentaje para las tablas.
- **`fila(...,porcentaje=True)`**: genera una fila; si `porcentaje=False`, omite la columna porcentual para esperanza, varianza, costo u otras magnitudes no probabilísticas.
- **`binomial(n,p,x_max=None)`**: devuelve un DataFrame \(x,P(X=x),P(X\le x)\). Para \(n\le1000\) evalúa \(\binom nx p^x(1-p)^{n-x}\); para \(n\) grande usa la recurrencia entre masas para evitar coeficientes que exceden la representación numérica.
- **`poisson(lam,x_max)`**: evalúa \(e^{-\lambda}\lambda^x/x!\) desde 0 hasta el máximo y agrega la acumulada.
- **`geometrica(p,x_max)`**: evalúa \((1-p)^{x-1}p\) desde \(x=1\) hasta el máximo.
- **`prob(tabla,mascara)`**: suma la columna de masa para los valores seleccionados.
- **`bloque_distribucion(...)`**: crea una tabla de masa/acumulada, marca incisos y agrega datos de gráfico.
- **`bloque_comparacion(filas,n,p,notas=())`**: arma la presentación binomial exacta vs aproximación Poisson con \(\lambda=np\).
- **`momentos(x,f)`**: devuelve tabla de \(x f(x)\), \(x^2f(x)\), \(E(X)\), \(V(X)=E(X^2)-E(X)^2\) y \(\sigma\).
- **`bloque_tabla(...)`**: prepara una tabla y, opcionalmente, agrega la fila \(\Sigma\).

La masa/acumulada se implementa en Python y pandas; `math.comb`, `exp`, `factorial` y `sqrt` son de la biblioteca estándar. La tabla puede truncarse para presentación; un complemento como “más de k” se calcula en el ejercicio con la acumulada/total y no debe confundirse con una suma parcial incompleta.

## API FastAPI: `main.py`

La aplicación se crea como `app = FastAPI(...)`. `BASE` apunta a la carpeta del proyecto; los rangos disponibles son 1–10, 1–17 y 1–25.

- **`cargar(n,paquete="ejercicios",numeros=NUMEROS)`**: verifica que `n` esté en el rango permitido y carga `paquete.ejNN` con `importlib`. Si no está permitido, lanza `HTTPException(404, "Ejercicio inexistente")`.
- **`listar()`**: `GET /api/ejercicios`; devuelve número y título del TP1.
- **`ver(n)`**: `GET /api/ejercicios/{n}`; carga el módulo y devuelve número, título, enunciado, enlace Excel y `resolver()`.
- **`registrar_tp(tp,paquete,numeros,carpeta_excel,exportador)`**: crea rutas equivalentes para un TP, reutilizando carga, lista y resolución.

Rutas de TP2: `GET /api/tp2/ejercicios`, `GET /api/tp2/ejercicios/{n}`, `GET /api/tp2/excel/{n}` y `GET /tp2`. Para TP3, cambian `tp2` por `tp3`. También están las rutas de TP1 `GET /api/ejercicios` y `/api/ejercicios/{n}`; `/` sirve el `index.html` por `StaticFiles`.

La respuesta del endpoint individual tiene la forma:

```json
{
  "numero": 1,
  "titulo": "…",
  "enunciado": "…",
  "excel_url": "…",
  "bloques": [
    {
      "subtitulo": "…",
      "columnas": ["…"],
      "filas": [["…"]],
      "grafico": null,
      "notas": []
    }
  ]
}
```

Los valores reales varían por ejercicio; `grafico` puede ser nulo o un objeto con etiquetas y series. FastAPI serializa estos objetos como JSON.

## Generación de Excel

### Exportación por ejercicio — `exportar_excel.py`

`exportar(modulo,carpeta,anchos,formato_numerico)` recibe un módulo con `TITULO`, `ENUNCIADO`, `__file__` y `resolver()`. Crea un `Workbook`, una hoja titulada “Ejercicio N”, escribe título/enunciado y recorre los bloques para agregar subtítulos, encabezados, celdas, notas y, si hay gráfico, tabla auxiliar y `BarChart`.

- `escribir_fila()` escribe celdas con bordes, alineación y estilo opcional de encabezado.
- `escribir_texto()` combina A:E, habilita ajuste de línea y estima altura.
- `agregar_grafico()` crea un `BarChart`, asigna series/categorías con `Reference` y lo ubica a la derecha de la tabla.
- `escribir_bloque()` agrega tabla, notas, tabla auxiliar para gráfico y mantiene espacio para que los bloques no se solapen.
- `configurar_hoja()` define anchos, oculta la cuadrícula y configura impresión horizontal a una página de ancho.
- `formatear_numeros()` aplica formatos numéricos del TP3 a valores flotantes no enteros.
- `exportar_tp2()` y `exportar_tp3()` seleccionan carpeta y anchos específicos; TP3 aplica formato numérico.
- `numeros_disponibles()` detecta módulos con patrón `ejNN.py`.
- Como CLI admite todos los ejercicios, números seleccionados o `--tp2`/`--tp3`. Ejemplo: `python exportar_excel.py --tp3 8 15`.

Una hoja de TP2/TP3 contiene título, enunciado y bloques. Los gráficos de Excel dependen de una tabla auxiliar de datos escrita en la hoja. La librería usada es `openpyxl`.

### Libro consolidado TP1 — `generar_excel.py`

`cargar_ejercicios()` busca archivos `ejNN.py` de TP1 y los importa. `generar_excel()` crea `excel/ejercicios.xlsx`, con hoja “Resumen” (número/título) y una hoja por ejercicio. `escribir_fila`, `escribir_bloque` y `ajustar_columnas` escriben contenido y formato. Este script es independiente del endpoint de TP1.

**Diferencia de endpoints:** `main.py` usa enlaces externos predefinidos para el Excel de TP1; no registra una ruta local `/api/excel/{n}`. TP2/TP3 sí tienen rutas de descarga local. Sus endpoints devuelven el archivo si ya existe y solo llaman al exportador si falta; no regeneran automáticamente un libro existente tras un cambio en el código.

## Frontend: HTML, JavaScript y CSS

### HTML

- [`static/index.html`](../../static/index.html) contiene navegación, presentación, menú/contenedor dinámico, siete tarjetas de clasificación de variables y glosario TP1.
- [`static/tp2.html`](../../static/tp2.html) y [`static/tp3.html`](../../static/tp3.html) contienen navegación, glosario estático y contenedores de ejercicios. Cada una declara su endpoint en `body[data-api]`.
- Las páginas cargan [`static/style.css`](../../static/style.css), [`static/js.js`](../../static/js.js) y Chart.js desde CDN con `defer`.
- No se usa motor de plantillas como Jinja en el código examinado; FastAPI sirve archivos estáticos y JSON.

### JavaScript (`static/js.js`)

- **`inicializarTema()`** lee el tema guardado en `localStorage` o respeta `prefers-color-scheme`; configura el botón y persiste cambios.
- **`actualizarBotonTema()`** actualiza `aria-pressed` y el texto accesible del control.
- **`limpiarGraficos()`** destruye instancias anteriores de Chart.js antes de volver a dibujar.
- **`tabla(columnas,filas)`** genera el marcado HTML de una tabla.
- **`cargarMenu()`** hace `fetch` al endpoint de lista definido por `data-api`, crea botones y muestra el primer ejercicio.
- **`mostrar(numero)`** actualiza selección, pide el JSON del ejercicio, compone título/enunciado/enlace Excel, agrega tablas/notas/canvas y construye gráficos Chart.js si está cargado.
- El `catch` al final de `cargarMenu()` muestra un mensaje genérico si falla la carga inicial.

El contrato `bloques` conecta los resolvers Python con el navegador: `columnas` y `filas` se vuelven celdas; `notas` se vuelven una lista; `grafico.etiquetas` y `grafico.series` alimentan Chart.js. El enlace `excel_url` lleva al libro.

### CSS (`static/style.css`)

Usa variables CSS para paletas de tema claro y oscuro; `data-theme="dark"` cambia los tokens. Define navegación fija, jerarquía tipográfica, paneles, tablas con scroll horizontal, tarjetas, gráficos y glosarios. Los media queries reducen columnas/espaciado para pantallas menores de 980px y 620px; `prefers-reduced-motion` reduce animaciones. El botón de tema se maneja en JavaScript; CSS refleja el estado visual.

## Manejo de errores y validaciones comprobables

- El control principal de número inexistente es `cargar()`, que genera HTTP 404. La tabla de rutas de TP2/TP3 también restringe cada número mediante sus rangos.
- En el CLI del exportador, un módulo inexistente se informa y se continúa con los pedidos siguientes. `PermissionError` al guardar produce un mensaje para cerrar el Excel y volver a intentar.
- El frontend muestra “No se pudieron cargar los ejercicios” ante fallo de carga de la lista; no hay un manejador separado en el código para cada petición individual.
- Hay pruebas unitarias en [`tests/test_chatbot.py`](../../tests/test_chatbot.py), ejecutables con `python -m unittest discover -s tests -v`. Prueban el allowlist, errores por documentos faltantes, separación Markdown, abstención, metadatos de fuentes, validación de mensaje, token administrativo y estado sin configuración. En esta revisión se ejecutaron los 52 resolvers (10+17+25) y se comprobó su serialización JSON; no se ejecutó una llamada en vivo al proveedor externo.
- La salida de distribución redondea solo al presentar; el cálculo mantiene precisión de Python. TP2 utiliza `Fraction` donde el modelo permite cocientes exactos.

## Recorrido desde una operación hasta la pantalla

1. El usuario abre `/`, `/tp2` o `/tp3`; FastAPI sirve el HTML correspondiente.
2. `js.js` lee `data-api` (TP1 usa `/api/ejercicios`) y solicita la lista.
3. La lista informa números/títulos y el navegador crea el menú.
4. Al elegir un ejercicio, el navegador solicita el endpoint individual.
5. FastAPI importa `ejNN.py`, ejecuta `resolver()` y devuelve el resultado como JSON.
6. El navegador pinta enunciado, bloques, tablas, notas y gráficos.
7. El usuario puede seguir `excel_url`; TP2/TP3 descargan un libro local existente o generan uno si falta; TP1 usa un enlace externo.

## Chatbot académico: RAG y rutas

La integración se distribuye entre [`chatbot/router.py`](../router.py), [`chatbot/assistant.py`](../assistant.py), [`chatbot/prompts.py`](../prompts.py), [`static/chatbot.js`](../../static/chatbot.js) y el montaje de router en [`main.py`](../../main.py). Las únicas fuentes configuradas son `tp1.md`, `tp2.md`, `tp3.md`, `programacion.md` y `arquitectura.md`; no se rastrea el resto del repositorio.

### Configuración

`_env(name,default="")` lee primero el entorno del proceso y luego busca la variable en `.env` de la raíz, sin dependencia dotenv. `_settings()` lee el proveedor compatible con API OpenAI, modelo de generación, modelo de embeddings, `top_k` y umbral de similitud. Los valores ajustables se listan por nombre en [`.env.example`](../../.env.example); la clave y el token administrativo se mantienen en el servidor y no deben copiarse a esta documentación.

Variables configurables: `CHATBOT_API_BASE_URL`, `CHATBOT_API_KEY`, `CHATBOT_MODEL`, `CHATBOT_EMBEDDING_MODEL`, `CHATBOT_TOP_K`, `CHATBOT_SIMILARITY_THRESHOLD` y `CHATBOT_REINDEX_TOKEN`. El endpoint base predeterminado es compatible con `/embeddings` y `/chat/completions`. No hay un SDK del proveedor; `_request_json()` usa `urllib.request`, JSON y bearer authorization.

### Construcción del índice y recuperación

- **`_request_json(path,body,settings,timeout=35)`**: codifica JSON, hace POST al proveedor y devuelve el objeto JSON. Convierte fallos HTTP/red/timeout/JSON en `ChatbotError` y registra el tipo de error sin exponer la credencial.
- **`_embed(texts,settings)`**: valida clave y modelo de embeddings, solicita vectores para una lista de textos y ordena la respuesta por índice. Retorna listas de flotantes.
- **`_category(filename)`**: asigna a cada nombre de Markdown su categoría TP1, TP2, TP3, Programación o Arquitectura.
- **`_load_documents()`**: exige que existan todos los nombres de `ALLOWED_FILES` y lee únicamente esos cinco UTF-8. Si falta uno, falla con el nombre; ignora cualquier otro Markdown.
- **`_split_markdown(filename,markdown)`**: divide por encabezados y párrafos, preserva bloques de código y agrupa fragmentos de aproximadamente 650 tokens estimados como longitud/4, con solapamiento de hasta 320 caracteres. Deduplica sección/texto y retorna sección y contenido.
- **`build_or_update_index(force=False)`**: requiere clave y modelo de embeddings, calcula SHA-256 por documento y reutiliza fragmentos existentes si el contenido y el modelo no cambiaron. Si se fuerza o un hash cambió, vuelve a fragmentar y solicita embeddings en grupos de hasta 64. Escribe versión/modelo/chunks en un temporal y lo renombra como `chatbot/vector_db/index.json`. Retorna cantidad indexada y cantidad de documentos actualizados.
- **`_cosine(left,right)`**: calcula similitud coseno y retorna 0 si el denominador es cero.
- **`retrieve(message)`**: construye índice si falta; si existe, compara hashes/modelo y actualiza documentos obsoletos. Genera embedding de consulta, ordena fragmentos por coseno y retorna los mejores `top_k` junto con el vector.

El índice se genera localmente y está excluido de Git; los Markdown son su fuente de verdad. Una consulta puede actualizar el índice incrementalmente cuando detecta cambios. Cambiar el modelo de embeddings requiere reindexar.

### Evidencia y respuesta

- **`_evidence_is_sufficient(message,relevant,settings)`**: presenta pregunta y fragmentos recuperados a un evaluador, solicita JSON con `sufficient=true/false` y temperatura 0; si el formato no es válido, interpreta insuficiencia.
- **`answer(message)`**: exige configuración completa; recupera fragmentos y descarta los que estén debajo del umbral. Si no queda evidencia o el evaluador la considera insuficiente, retorna la abstención fija y fuentes vacías. Si hay evidencia, invoca el modelo con `SYSTEM_PROMPT`, consulta y fragmentos marcados como contenido no confiable; retorna `answer` y fuentes únicas (`file`, `category`, `section`).
- **`health()`**: informa estado, disponibilidad del índice, configuración del modelo y documentos faltantes; no hace una llamada de generación.
- **`ChatRequest`**: esquema Pydantic; `message` es obligatorio, de 1 a 2000 caracteres; valida que no contenga solo espacios y lo recorta.
- **`ChatResponse`, `Source`, `HealthResponse`**: tipan respuesta, referencias documentales y diagnóstico de disponibilidad.

La instrucción en `prompts.py` exige español, respuesta fundamentada solo en fragmentos y abstención si no hay evidencia suficiente. La recuperación y revisión de evidencia reducen respuestas fuera de alcance, pero no garantizan matemáticamente que un modelo generativo nunca cometa errores.

### Rutas y errores del chatbot

- **`POST /api/chat`** recibe `{"message":"..."}` y devuelve `{"answer":"...","sources":[...]}`. Ejecuta `assistant.answer` en un hilo, limita trabajo concurrente con `Semaphore(4)` y espera hasta 50 segundos. Timeout: 504; configuración/proveedor no disponible: 503; fallo inesperado: 500 con mensaje genérico y registro en servidor.
- **`GET /api/chat/health`** retorna `status`, `index_ready`, `model_configured` y `missing_documents`.
- **`POST /api/chat/reindex`** exige `X-Chatbot-Admin-Token`, compara con `hmac.compare_digest`, fuerza reindexación y espera hasta 180 segundos. Token no configurado: 503; no autorizado: 403; timeout: 504; error de configuración: 503.

El router se incluye en `main.py` antes de montar `StaticFiles`, para que el catch-all no intercepte estas rutas.

### Cliente del chatbot

`static/chatbot.js` controla botón flotante, panel, sugerencias, formulario y estado de salud. `submitQuestion()` publica JSON a `/api/chat`, muestra el mensaje, indicador de escritura, respuesta, fuentes o acción de reintento; Enter envía y Shift+Enter agrega línea. “Nueva conversación” limpia el panel local; no hay historial enviado al servidor ni memoria conversacional.

`renderMarkdown()` permite un subconjunto de Markdown (código, matemáticas como texto, negrita, cursiva y listas). Escapa el texto externo antes de insertar etiquetas permitidas; los mensajes del usuario y las fuentes se insertan como `textContent`. La vista consulta `/api/chat/health`. El panel es adaptable y tiene etiquetas/estados accesibles en HTML; CSS usa los tokens de tema y reduce animación cuando el sistema lo solicita.

### Pruebas y limitaciones

`tests/test_chatbot.py` contiene pruebas `unittest` con mocks para evitar llamadas reales al proveedor. Incluye allowlist de cinco documentos, documentos faltantes, preservación de encabezados/código en fragmentos, abstención fuera de alcance, fuentes, revisión de evidencia, validación de texto, token de reindexación y estado no configurado. No verifica embeddings reales ni una llamada en vivo al proveedor; tampoco sustituye la verificación visual/manual del navegador.

## Documentación de conocimiento del chatbot

Los Markdown [`tp1.md`](./tp1.md), [`tp2.md`](./tp2.md), [`tp3.md`](./tp3.md), este manual y [`arquitectura.md`](./arquitectura.md) forman el allowlist leído por el RAG. El nombre y orden están definidos en `assistant.py`; añadir una fuente al repositorio no la incluye automáticamente.