# TP1 — Estadística descriptiva y análisis de variables

## Alcance y criterio de lectura

**Comprobado en el repositorio:** el TP1 tiene diez módulos en [`ejercicios/`](../../ejercicios/), cada uno con `TITULO`, `ENUNCIADO` y `resolver()`. No hay un PDF de TP1 en [`docs/`](../../docs/); por eso las consignas que siguen son transcripciones de la constante `ENUNCIADO` del código, no transcripciones verificadas del apunte original. Los datos, resultados y procedimientos se reproducen desde los resolvers. La interfaz incluye además ejemplos de clasificación de variables y un glosario en [`static/index.html`](../../static/index.html).

En los diez módulos, `TITULO` es el rótulo genérico “Ejercicio N”. Los nombres descriptivos de los encabezados de este documento identifican el tema a partir del `ENUNCIADO`; no se presentan como títulos transcritos de un PDF inexistente.

**Interpretación didáctica:** las medidas describen el conjunto que el ejercicio declara como población o muestra. Los métodos y convenciones efectivamente usados se explican abajo; no deben reemplazarse automáticamente por las convenciones por defecto de otro programa estadístico.

## Convenciones y fórmulas compartidas

El helper [`estadistica.py`](../../estadistica.py) concentra las medidas descriptivas comunes:

- **Media:** \(\bar x=\sum_i x_i/n\). Para una tabla agrupada, se aproxima con \(\bar x=\sum_j m_j f_j/N\), donde \(m_j\) es la marca de clase y \(f_j\) su frecuencia.
- **Mediana:** valor central de los datos ordenados; si hay cantidad par, se promedian los dos valores centrales.
- **Moda:** valor o categoría más frecuente. El helper informa todas las modas si hay empate y “No hay” si cada valor aparece una sola vez.
- **Rango:** máximo menos mínimo.
- **Varianza y desvío:** `Series.std(ddof=0)` usa divisor \(N\) para población; `ddof=1` usa \(n-1\) para muestra. El helper informa la varianza como el cuadrado de ese desvío. Para datos agrupados calcula directamente las desviaciones de las marcas respecto de la media con el mismo divisor.
- **Coeficiente de variación:** \(CV=100\,s/\bar x\), usando el desvío correspondiente a población o muestra.
- **Percentil programado:** se ordenan \(n\) datos y se calcula \(pos=pn/100\). Si `pos` es entero, se promedian las observaciones en las posiciones `pos` y `pos+1` (contadas desde 1); si no es entero, se usa el elemento cuyo índice base cero es la parte entera de `pos`. Es la convención propia de [`percentil()`](../../estadistica.py), no `Series.quantile()`.
- **Cuantil agrupado:** \(L+\frac{qN-F_{\text{anterior}}}{f_{\text{clase}}}h\), con límite inferior \(L\), frecuencia acumulada anterior \(F_{\text{anterior}}\), frecuencia de clase \(f_{\text{clase}}\) y amplitud \(h\).
- **Moda agrupada:** \(L+\frac{d_1}{d_1+d_2}h\), donde \(d_1\) y \(d_2\) comparan la frecuencia modal con las frecuencias vecinas.
- **Asimetría de Pearson:** con moda única, \((\bar x-\text{moda})/s\); sin moda única, \(3(\bar x-\text{mediana})/s\).
- **Asimetría de Bowley:** \((Q_3+Q_1-2Q_2)/(Q_3-Q_1)\); si \(Q_3=Q_1\), el programa devuelve 0.
- **Interpretación programada de asimetría:** valor mayor que 0,05 se etiqueta positiva; menor que −0,05, negativa; entre ambos umbrales, aproximadamente simétrica. La etiqueta del programa es una regla de presentación.

Para datos agrupados, la media, varianza, cuantiles y moda son aproximaciones derivadas de marcas de clase e interpolación. No equivalen necesariamente a calcular las medidas sobre los datos individuales.

## Clasificación de variables incluida en la interfaz

La sección “Clasificación de variables” de [`static/index.html`](../../static/index.html) usa estos ejemplos:

1. **Cantidad de hermanos:** cuantitativa discreta; se cuentan unidades enteras.
2. **Género musical preferido:** cualitativa nominal; son categorías sin orden.
3. **Estatura:** cuantitativa continua; puede tomar valores reales dentro de un intervalo.
4. **Satisfacción con las clases:** cualitativa ordinal; las categorías tienen orden.
5. **Tiempo de carrera:** cuantitativa continua.
6. **Medio de transporte:** cualitativa nominal.
7. **Temperatura diaria:** cuantitativa continua.

En cada tarjeta la interfaz propone población, variable, clasificación, elemento unitario y dimensiones temporal y espacial. Cuando dice “ejemplo”, esos detalles son ilustrativos y no deben confundirse con datos de una medición real.

## Ejercicios

### Ejercicio 1 — Ingresos a Instagram

- **Enunciado en código:** “Cantidad de veces que ingresaron a Instagram en un día (20 alumnos). Calcular P10 y P90.”
- **Objetivo y conceptos:** resumir una variable cuantitativa discreta con medidas de centro, dispersión, cuartiles, asimetría y percentiles.
- **Procedimiento y resultados:** \(n=20\). Con la convención del programa, \(P_{10}\) promedia los valores ordenados 2.º y 3.º, ambos 0; \(P_{90}\) promedia el 18.º y 19.º, ambos 3. Salida: media 1,55; mediana 1,5; modas 1 y 2; rango 4; varianza poblacional 1,2475; desvío 1,1169; \(CV=72,06\%\); \(Q_1=1\), \(Q_2=1,5\), \(Q_3=2\); Pearson 0,134; Bowley 0; \(P_{10}=0\), \(P_{90}=3\). Frecuencias para 0–4: 4, 6, 6, 3, 1.
- **Interpretación:** Pearson se clasifica positiva y Bowley aproximadamente simétrica con el umbral implementado. Como hay dos modas, Pearson usa la fórmula basada en la mediana.
- **Implementación:** [`ej01.py`](../../ejercicios/ej01.py) llama a `resolver_simple(..., poblacion=True)`; el helper construye la serie, obtiene las medidas y genera barras de frecuencia.

### Ejercicio 2 — Me gusta en videos

- **Enunciado en código:** “Cantidad de me gusta de 30 videos de programación en sus primeras 100 visualizaciones. Calcular el decil 40 (P40).”
- **Objetivo:** resumir los datos y obtener el percentil 40. Un decil 4 equivale a \(P_{40}\).
- **Procedimiento y resultados:** \(pos=40·30/100=12\), entero; se promedian las observaciones ordenadas 12.ª y 13.ª, ambas 2. Salida: media 3,0667; mediana 2,5; moda 1; rango 8; varianza poblacional 5,1289; desvío 2,2647; \(CV=73,85\%\); cuartiles 1, 2,5 y 4; Pearson 0,913; Bowley 0; \(P_{40}=2\). Frecuencias para 0–8: 2, 7, 6, 5, 3, 2, 1, 2, 2.
- **Interpretación:** Pearson positiva; Bowley aproximadamente simétrica según el criterio del programa.
- **Implementación:** [`ej02.py`](../../ejercicios/ej02.py) delega a `resolver_simple` como población y variable discreta.

### Ejercicio 3 — Errores de programación

- **Enunciado en código:** “Cantidad de errores cada 10 horas de programación de 30 estudiantes. Calcular cuartil 2, decil 50 y percentil 50 (los tres coinciden con la mediana).”
- **Objetivo:** mostrar la equivalencia entre \(Q_2\), \(D_5\), \(P_{50}\) y la mediana.
- **Procedimiento y resultados:** \(pos=50·30/100=15\); se promedian las observaciones 15.ª y 16.ª, ambas 23. Por lo tanto, \(Q_2=D_5=P_{50}=\) mediana \(=23\). Salida: media 23,2333; moda 21; rango 8; varianza poblacional 5,6456; desvío 2,376; \(CV=10,23\%\); \(Q_1=21\), \(Q_3=25\); Pearson 0,94; Bowley 0. Frecuencias para 20–28: 4, 6, 2, 5, 4, 3, 3, 1, 2.
- **Interpretación:** Pearson se clasifica positiva y Bowley aproximadamente simétrica.
- **Implementación:** [`ej03.py`](../../ejercicios/ej03.py) pide \(P_{50}\); `resolver_simple` también presenta \(Q_2\) como medida general.

### Ejercicio 4 — Errores de carga

- **Enunciado en código:** “Cantidad de errores en la carga de datos de 40 operadores. Pearson, Bowley, decil 60 (P60) y cuartil 3 (P75).”
- **Objetivo:** calcular asimetría y cuantiles de una variable discreta.
- **Procedimiento y resultados:** \(P_{60}\): \(pos=24\), se promedian los valores 24.º y 25.º, resultado 3. \(P_{75}\): \(pos=30\), se promedian el 30.º y 31.º, resultado 4. Salida: media 2,75; mediana 3; moda 3; rango 6; varianza poblacional 2,7875; desvío 1,6696; \(CV=60,71\%\); cuartiles 2, 3 y 4; Pearson −0,15; Bowley 0; \(P_{60}=3\), \(P_{75}=4\). Frecuencias para 0–6: 6, 3, 8, 9, 7, 6, 1.
- **Interpretación:** Pearson negativa; Bowley aproximadamente simétrica.
- **Implementación:** [`ej04.py`](../../ejercicios/ej04.py) usa `resolver_simple` como población.

### Ejercicio 5 — Libros leídos

- **Enunciado en código:** “Cantidad de libros leídos por 50 personas en la feria del libro. Pearson, Bowley, centil 80 (P80) y cuartil 1 (P25).”
- **Objetivo y procedimiento:** para \(P_{80}\), \(pos=40\), entero, se promedian los valores 40.º y 41.º: 5,5. Para \(P_{25}\), \(pos=12,5\), se toma el elemento de índice 12 (13.º ordenado): 2.
- **Resultados:** media 3,62; mediana 3; moda 2; rango 9; varianza poblacional 4,9156; desvío 2,2171; \(CV=61,25\%\); cuartiles 2, 3 y 5; Pearson 0,731; Bowley 0,333; \(P_{80}=5,5\), \(P_{25}=2\). Frecuencias para 0–9: 1, 7, 11, 9, 7, 5, 4, 2, 2, 2.
- **Interpretación:** ambos coeficientes indican asimetría positiva según las fórmulas implementadas.
- **Implementación:** [`ej05.py`](../../ejercicios/ej05.py) usa `resolver_simple` como población.

### Ejercicio 6 — Materias aprobadas

- **Enunciado en código:** “Cantidad de materias aprobadas por 40 estudiantes de abogacía. Percentil 95, cuartil 3 y tipo de asimetría.”
- **Objetivo y procedimiento:** \(P_{95}\): posición 38, entero; promedio de los valores 38.º y 39.º = 6. \(Q_3=P_{75}\): posición 30; promedio del 30.º y 31.º = 5.
- **Resultados:** media 3,7; mediana 4; moda 5; rango 6; varianza poblacional 2,76; desvío 1,6613; \(CV=44,9\%\); cuartiles 2,5, 4 y 5; Pearson −0,783; Bowley −0,2; \(P_{95}=6\), \(P_{75}=5\). Frecuencias para 0–6: 2, 2, 6, 7, 8, 9, 6.
- **Interpretación:** los dos coeficientes indican asimetría negativa. “Tipo de asimetría” se comunica en las notas de esos coeficientes.
- **Implementación:** [`ej06.py`](../../ejercicios/ej06.py) llama a `resolver_simple` como población.

### Ejercicio 7 — Espera del autobús

- **Enunciado en código:** “Minutos de espera del autobús en 30 días laborales. Distribución de frecuencias con h = 4, Pearson y Bowley.”
- **Objetivo:** agrupar una variable cuantitativa continua y calcular medidas agrupadas.
- **Procedimiento:** clases \([0,4),[4,8),[8,12),[12,16),[16,20)\); frecuencias 6, 4, 13, 4, 3; acumuladas 6, 10, 23, 27, 30; marcas 2, 6, 10, 14, 18. La opción de muestra usa divisor \(30-1\). La mediana cae en \([8,12)\): \(8+[(15-10)/13]·4=9,538\). \(Q_1=5,5\); \(Q_3=11,846\); la clase modal es \([8,12)\) y la moda interpolada es 10.
- **Resultados:** media 9,2; varianza muestral 23,614; desvío 4,859; \(CV=52,82\%\); Pearson −0,165; Bowley −0,273.
- **Interpretación:** ambos índices se clasifican negativos; las medidas son estimaciones a partir de clases, frecuencias y marcas.
- **Implementación:** [`ej07.py`](../../ejercicios/ej07.py) calcula frecuencias por máscaras de intervalos y usa `resolver_agrupado` con amplitud 4 y `poblacion=False`.

### Ejercicio 8 — Tiempos de CPU

- **Enunciado en código:** “Tiempos de CPU (segundos) de 30 trabajos tomados al azar (muestra). Percentil 15, cuartil 1, coeficiente de variación y tipo de asimetría.”
- **Objetivo:** describir una muestra continua con medidas, percentiles e histograma.
- **Procedimiento y resultados:** \(P_{15}\) tiene posición 4,5 y el programa toma el quinto dato ordenado: 0,47. \(P_{25}\) tiene posición 7,5 y toma el octavo: 0,75. Salida: media 1,6803; mediana 1,305; sin moda; rango 4,73; varianza muestral 1,6806; desvío 1,2964; \(CV=77,15\%\); cuartiles 0,75, 1,305 y 2,41; Pearson 0,869; Bowley 0,331; histograma con frecuencias 8, 10, 4, 3, 3, 2.
- **Interpretación:** asimetría positiva según ambos coeficientes. El percentil sigue la regla discreta programada aunque los datos sean tiempos continuos.
- **Implementación:** [`ej08.py`](../../ejercicios/ej08.py) usa `resolver_simple` como muestra y `continuo=True`; el histograma se construye con `pd.cut`.

### Ejercicio 9 — Niños atendidos por edad

- **Enunciado disponible:** el texto del módulo describe niños atendidos por edad y señala que asume las mismas medidas del ejercicio 7 porque no identifica en el código qué medidas pediría el PDF. También informa que la clase “12 y más” contiene 115 personas cuya suma de edades es 1725.
- **Objetivo:** mostrar una distribución agrupada y medidas calculadas desde la tabla suministrada.
- **Procedimiento:** clases \([0,3),[3,6),[6,9),[9,12)\) y “12 y más”; frecuencias 5080, 4551, 3000, 955, 115; acumuladas 5080, 9631, 12631, 13586, 13701; marcas 1,5; 4,5; 7,5; 10,5; 15. La última marca se obtiene como \(1725/115=15\). El código usa población y amplitud 3. Por ejemplo, \(Q_1=0+(3425,25/5080)·3=2,023\); la mediana es 4,167 y \(Q_3=6,645\).
- **Resultados:** \(N=13701\); media 4,551; mediana 4,167; moda 2,717; varianza poblacional 8,74; desvío 2,956; \(CV=64,96\%\); Pearson 0,62; Bowley 0,072.
- **Límite:** no hay PDF de TP1 para cotejar el pedido original. La clase final es abierta; su marca se deriva de la suma de edades y el código usa amplitud 3. El significado de las medidas calculadas es una suposición documentada en el código y en [`SKILL.md`](../../SKILL.md), no una verificación del enunciado original.
- **Implementación:** [`ej09.py`](../../ejercicios/ej09.py) construye una tabla agrupada y llama a `resolver_agrupado`.

### Ejercicio 10 — Lenguajes, comprensión lectora y razonamiento cuantitativo

- **Enunciado disponible:** el módulo organiza tres incisos: (a) lenguajes de programación en estudiantes; (b) dispersión de comprensión lectora entre Software y Programación; (c) descriptiva de razonamiento cuantitativo. Es una síntesis del código, no una transcripción cotejada con un PDF de TP1.

#### 10.a — Lenguajes de programación

El programa analiza 78 respuestas. Frecuencias y porcentajes: Cobol 19 (24,36%), C++ 14 (17,95%), SQL 13 (16,67%), Python 12 (15,38%), PHP 11 (14,10%) y Java 9 (11,54%). La moda es Cobol. La variable es cualitativa nominal: el código cuenta categorías, no calcula promedios numéricos de sus nombres. El conteo y el cálculo de porcentajes se implementan en [`ej10.py`](../../ejercicios/ej10.py).

#### 10.b — Comprensión lectora

El código trata ambas listas como poblaciones (`ddof=0`) y compara media, rango, rango intercuartílico, varianza, desvío y coeficiente de variación.

| Grupo | Media | Rango | RIC | Varianza poblacional | Desvío | CV |
|---|---:|---:|---:|---:|---:|---:|
| Software | 2,7817 | 2 | 0,95 | 0,3432 | 0,5858 | 21,06% |
| Programación | 2,8283 | 1,8 | 1,1 | 0,353 | 0,5942 | 21,01% |

El programa concluye que la dispersión relativa es prácticamente igual porque los CV son muy cercanos. El inciso se titula “dispersión”, aunque la tabla también presenta medias.

#### 10.c — Razonamiento cuantitativo

El código contiene 195 observaciones (13×15); su comentario indica que el enunciado del PDF habría mencionado 200. No agrega los cinco valores faltantes.

Resultados calculados con los métodos pandas usados en el módulo: media 2,5421; error típico 0,0599; mediana 2,5; moda 2,8; desvío muestral 0,8362; varianza muestral 0,6993; curtosis −0,5181; asimetría −0,0006; rango 4,2; mínimo 0,3; máximo 4,5; suma 495,7; cantidad 195. El histograma de diez intervalos tiene frecuencias 1, 6, 25, 14, 40, 41, 21, 27, 17, 3.

La asimetría se clasifica aproximadamente simétrica según el umbral del helper; la curtosis negativa se interpreta en el comentario del programa como una distribución más plana que la normal. `Series.sem()`, `.kurt()` y `.skew()` se usan con sus parámetros por defecto; no se documenta una convención alternativa en el módulo.

## Glosario TP1 de la interfaz

Las siguientes definiciones condensan el glosario que existe en [`static/index.html`](../../static/index.html); conservan su sentido.

- **Población:** conjunto completo que se quiere estudiar.
- **Muestra:** parte seleccionada de una población.
- **Variable:** característica observada en cada elemento.
- **Cualitativa nominal:** categorías sin orden natural.
- **Cuantitativa discreta:** valores contables, normalmente enteros.
- **Cuantitativa continua:** mediciones que pueden tomar valores dentro de un intervalo.
- **Frecuencia absoluta \(f\):** cantidad de veces que aparece un valor o clase.
- **Frecuencia relativa:** proporción del total, \(f/n\).
- **Frecuencia acumulada \(F\):** suma de las frecuencias hasta un valor o intervalo.
- **Distribución de frecuencias:** organización de valores o intervalos con sus frecuencias.
- **Media:** promedio; en datos agrupados se ponderan las marcas por sus frecuencias.
- **Mediana:** valor central de los datos ordenados.
- **Moda:** valor o categoría con mayor frecuencia.
- **Rango:** máximo menos mínimo.
- **Varianza:** medida de dispersión construida con desviaciones al cuadrado respecto de la media.
- **Desvío estándar:** raíz de la varianza; queda expresado en las unidades originales.
- **Coeficiente de variación:** desvío dividido por media, multiplicado por 100; compara dispersión relativa.
- **Cuartiles, deciles y percentiles:** cuantiles que dividen los datos ordenados en 4, 10 y 100 partes. \(P_{25}=Q_1\), \(P_{50}=Q_2\) y \(P_{75}=Q_3\).
- **Asimetría:** describe la dirección de la cola de la distribución.
- **Pearson y Bowley:** medidas de asimetría; Pearson usa media, moda o mediana y desvío; Bowley usa cuartiles.
- **Error típico:** `Series.sem()` estima la variabilidad de la media muestral; el glosario lo expresa como desvío dividido por la raíz del tamaño de datos.
- **Curtosis:** medida de forma que el glosario relaciona con qué tan apuntada o plana es la distribución respecto de una normal.

## Fuentes de implementación

- Ejercicios: [`ejercicios/`](../../ejercicios/).
- Medidas, percentiles, asimetría, gráficos y bloques: [`estadistica.py`](../../estadistica.py).
- Interfaz, tarjetas de clasificación y glosario: [`static/index.html`](../../static/index.html), [`static/js.js`](../../static/js.js) y [`static/style.css`](../../static/style.css).
- Convenciones y supuestos documentados por el proyecto: [`SKILL.md`](../../SKILL.md). Ese archivo no sustituye al PDF original, que no está disponible para TP1.