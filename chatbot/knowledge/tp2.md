# TP2 — Probabilidad

## Alcance y fuentes

Este documento describe los ejercicios 1–17 de [`ejercicios_tp2/`](../../ejercicios_tp2/) y los contrasta con [`TP 2 PROBABILIDAD 2026.pdf`](../../docs/TP%202%20PROBABILIDAD%202026.pdf). Los valores de entrada y salidas enumerados se comprobaron en los módulos Python. Las páginas 2–3 incluyen imágenes con datos del diagrama/las tablas de algunos ejercicios: cuando no es posible leer esos elementos como texto, se distingue expresamente el dato que usa el código de su verificación contra el original.

**Convención de certeza:** “consigna” resume lo legible en el PDF; “código” describe fielmente los datos y cálculos ejecutables; “interpretación” explica el resultado. No se suplen datos ausentes.

## Conceptos y fórmulas

- **Espacio muestral \(S\):** conjunto de resultados posibles del experimento.
- **Suceso \(A\):** subconjunto del espacio muestral.
- **Complemento \(A'\):** resultados de \(S\) que no están en \(A\); \(P(A')=1-P(A)\).
- **Intersección \(A\cap B\):** ocurren ambos sucesos.
- **Unión \(A\cup B\):** ocurre al menos uno.
- **Diferencia \(A-B\):** ocurre \(A\), pero no \(B\); equivale a \(A\cap B'\).
- **Excluyentes:** \(A\cap B=\varnothing\).
- **Complementarios:** son excluyentes y además \(A\cup B=S\). Por eso todo par complementario es excluyente, pero no todo par excluyente es complementario.
- **Regla de Laplace:** para resultados equiprobables, \(P(A)=|A|/|S|\).
- **Probabilidad condicional:** \(P(A\mid B)=P(A\cap B)/P(B)\), si \(P(B)>0\).
- **Independencia:** \(P(A\cap B)=P(A)P(B)\); equivalentemente, \(P(A\mid B)=P(A)\) cuando la condicional está definida.
- **Partición:** sucesos mutuamente excluyentes cuya unión cubre \(S\).
- **Probabilidad total:** para una partición \(H_i\), \(P(E)=\sum_iP(H_i)P(E\mid H_i)\).
- **Bayes:** \(P(H_i\mid E)=P(H_i)P(E\mid H_i)/P(E)\).
- **Distribución discreta válida:** todos los valores \(P(x)\) son no negativos y suman 1.

El proyecto usa `Fraction` para conservar razones exactas y mostrarlas como fracciones además de su decimal cuando corresponde. Los helpers que implementan conteo de Laplace, marginales, probabilidad total y Bayes están en [`probabilidad.py`](../../probabilidad.py).

## Resoluciones

### Ejercicio 1 — Espacio muestral

- **Consigna:** proponer espacios muestrales para (a) extraer una carta; (b) contar defectuosos en 500 artículos; (c) lanzar dos monedas; (d) lanzar moneda y dado; (e) medir el intervalo entre llegadas a una cola.
- **Conceptos:** espacio finito, discreto y continuo.
- **Resolución:** (a) las 52 cartas; (b) \(\{0,1,\ldots,500\}\), 501 resultados; (c) \(\{CC,CX,XC,XX\}\); (d) \(\{C1,\ldots,C6,X1,\ldots,X6\}\), 12 pares; (e) tiempos no negativos \([0,+\infty)\), continuo no numerable.
- **Implementación:** [`ej01.py`](../../ejercicios_tp2/ej01.py) arma una baraja/pares de resultados y usa `RangeIndex(0, 501)` para el número de defectuosos. Un `DataFrame` sirve como representación, no cambia el modelo probabilístico.
- **Fuente:** PDF, p. 1.

### Ejercicio 2 — Sucesos y operaciones

- **Consigna:** con una moneda y un dado, \(A=\) cara y \(B=\) resultado impar; enumerar \(A\), \(A\cap B\), \(B'\), \((A\cap B)'\), \(A'\cap B\) y \(A-B\).
- **Resolución:** \(A=\{C1,\ldots,C6\}\); \(A\cap B=\{C1,C3,C5\}\); \(B'=\{C2,C4,C6,X2,X4,X6\}\); \((A\cap B)'=\{C2,C4,C6,X1,\ldots,X6\}\); \(A'\cap B=\{X1,X3,X5\}\); \(A-B=\{C2,C4,C6\}\).
- **Procedimiento:** construir los 12 pares posibles y filtrar cada conjunto según sus propiedades.
- **Implementación:** [`ej02.py`](../../ejercicios_tp2/ej02.py) usa una tabla, máscaras booleanas y `.loc` para seleccionar filas. La operación de conjuntos se refleja en las condiciones de las máscaras.
- **Fuente:** PDF, p. 1.

### Ejercicio 3 — Complementarios y mutuamente excluyentes

- **Consigna:** evaluar si dos sucesos complementarios son mutuamente excluyentes y si dos sucesos mutuamente excluyentes necesariamente son complementarios.
- **Resolución:** (a) verdadero, porque \(A\cap A'=\varnothing\). (b) falso: la exclusión solo exige intersección vacía; no garantiza que \(A\cup B=S\). Contraejemplo usado: \(\{1\}\) y \(\{2\}\) dentro de los resultados de un dado.
- **Implementación:** [`ej03.py`](../../ejercicios_tp2/ej03.py) usa conjuntos y máscaras para comparar intersección y unión.
- **Fuente:** PDF, p. 1.

### Ejercicio 4 — Laplace con y sin sustitución

- **Consigna:** hay 10 artículos sin defecto y 6 defectuosos; hallar la probabilidad de que, al elegir dos, exactamente uno sea sin defecto, distinguiendo con reposición y sin reposición.
- **Con reposición:** hay dos órdenes favorables. \(2(10/16)(6/16)=120/256=15/32=0,46875\).
- **Sin reposición:** \(2(10/16)(6/15)=120/240=1/2=0,5\). Comprobación combinatoria: \(\binom{10}{1}\binom{6}{1}/\binom{16}{2}=60/120=1/2\).
- **Interpretación:** al reponer el primer artículo, la composición del lote y la probabilidad del segundo ensayo se mantienen; sin reposición, el denominador cambia.
- **Implementación:** [`ej04.py`](../../ejercicios_tp2/ej04.py) enumera pares ordenados, aplica Laplace y verifica el caso sin reposición por combinaciones. Usa `Fraction` para los cocientes exactos.
- **Fuente:** PDF, p. 1.

### Ejercicio 5 — Dos cartas sucesivas

- **Consigna:** expresar el espacio de dos extracciones de una baraja de 52 cartas y calcular cinco eventos: primera carta no diez de trébol ni as; primera as y segunda no as; al menos un diamante; palos distintos; segunda carta no figura.
- **Supuestos del código:** extracción sin reposición y pares ordenados; las figuras son J, Q y K.
- **Espacio y resultados:** \(52·51=2652\) pares ordenados. Probabilidades, en el orden de los incisos: \(47/52\approx0,9038\); \(16/221\approx0,0724\); \(15/34\approx0,4412\); \(13/17\approx0,7647\); \(10/13\approx0,7692\).
- **Procedimiento:** contar pares favorables; para “al menos un diamante” se puede interpretar por complemento de “ningún diamante”.
- **Implementación:** [`ej05.py`](../../ejercicios_tp2/ej05.py) construye las cartas con `baraja()`, hace el producto cruzado con `merge(how="cross")`, quita pares de una misma carta y aplica máscaras/Laplace.
- **Cautela:** “sucesivamente” no explicita en la frase resumida si se devuelve la carta; el código adopta sin reposición, lectura habitual.
- **Fuente:** PDF, p. 1.

### Ejercicio 6 — Probabilidad condicional en un dado

- **Datos:** \(A=\{1,2,3\}\), \(B=\{1,2\}\), \(C=\{4,5,6\}\).
- **Consigna y fórmula:** hallar \(P(A\mid B)\), \(P(B\mid A)\), \(P(A\mid C)\), \(P(B\mid C)\) y decidir si \(A\) y \(B\) son independientes. Se usa \(P(E\mid F)=P(E\cap F)/P(F)\).
- **Resultados:** \(P(A\mid B)=1\), \(P(B\mid A)=2/3\), \(P(A\mid C)=0\), \(P(B\mid C)=0\). Además \(P(A)P(B)=1/6\) y \(P(A\cap B)=1/3\), por lo que \(A,B\) no son independientes.
- **Interpretación:** \(B\subset A\), así que, dado \(B\), necesariamente ocurre \(A\).
- **Implementación:** [`ej06.py`](../../ejercicios_tp2/ej06.py) combina una función condicional con conteo de Laplace sobre máscaras.
- **Fuente:** PDF, p. 1.

### Ejercicio 7 — Dos dados y condicional

- **Consigna:** lanzar un dado rojo y uno negro; hallar \(P(\text{suma}=7)\) y \(P(\text{suma}=7\mid\text{rojo}=2)\).
- **Procedimiento:** hay 36 pares equiprobables. Seis suman 7, por lo que \(P=6/36=1/6\). Si el rojo vale 2, quedan seis resultados equiprobables para el negro y solo el 5 produce suma 7: \(1/6\).
- **Interpretación:** las dos probabilidades coinciden; en este experimento esos sucesos son independientes.
- **Implementación:** [`ej07.py`](../../ejercicios_tp2/ej07.py) genera el producto cartesiano de los dos dados y aplica máscaras de Laplace.
- **Fuente:** PDF, p. 1.

### Ejercicio 8 — Independencia y exclusión (diagrama)

- **Consigna:** decidir cinco afirmaciones sobre \(A,B,C\) y sus probabilidades marginales/conjuntas.
- **Datos que usa el código:** \(P(A)=1/4\), \(P(B)=1/2\), \(P(C)=1/6\), \(P(A\cap B)=1/8\), \(P(A\cap C)=1/12\), \(P(B\cap C)=0\).
- **Resultados:** (a) A y B excluyentes: falso; (b) A y B independientes: verdadero, pues \(1/8=(1/4)(1/2)\); (c) independencia mutua de A, B y C: falso; (d) A y C independientes: falso, pues \(1/12\ne1/24\); (e) A y B independientes: verdadero.
- **Implementación:** [`ej08.py`](../../ejercicios_tp2/ej08.py) representa razones con `Fraction` y compara valores exactos.
- **Límite:** los datos se transcriben del diagrama usado por el código; el PDF presenta ese gráfico como imagen y no fue posible corroborar visualmente todas sus cifras en la extracción textual.
- **Fuente:** PDF, p. 1.

### Ejercicio 9 — Tabla de probabilidades conjuntas

- **Consigna:** a partir de una tabla de clientes clasificados por sexo y residencia, hallar la probabilidad de suburbios, de mujer en ciudad y de hombre.
- **Tabla codificada:** filas suburbios/ciudad y columnas masculino/femenino: suburbios \((0,17;0,67)\), ciudad \((0,04;0,12)\). Marginales: suburbios 0,84; ciudad 0,16; masculino 0,21; femenino 0,79; total 1.
- **Resultados:** \(P(\text{suburbios})=0,84\); \(P(\text{mujer y ciudad})=0,12\); \(P(\text{hombre})=0,21\).
- **Implementación:** [`ej09.py`](../../ejercicios_tp2/ej09.py) organiza la tabla en `DataFrame` y usa `con_totales()` para agregar marginales.
- **Verificación:** el PDF contiene la tabla como imagen; los cálculos coinciden con los datos codificados, pero la transcripción original de las celdas no se pudo comprobar independientemente.
- **Fuente:** PDF, p. 2.

### Ejercicio 10 — Pedidos por línea y género

- **Consigna:** sobre 1000 pedidos, calcular probabilidades de mujer, línea 1, mujer y línea 1, línea 1 dado mujer, y decidir independencia.
- **Datos codificados:** masculino: 132 y 147; femenino: 516 y 205 (línea 1 y otra línea, según el arreglo del código). Totales: masculino 279, femenino 721; línea 1 648, otra línea 352.
- **Resultados:** \(P(\text{mujer})=0,721\); \(P(\text{línea 1})=0,648\); conjunta \(P(\text{mujer}\cap\text{línea 1})=0,516\); \(P(\text{línea 1}\mid\text{mujer})=516/721\approx0,7157\). El producto de marginales es 0,467208, distinto de 0,516: no son independientes.
- **Implementación:** [`ej10.py`](../../ejercicios_tp2/ej10.py) crea una tabla de contingencia con marginales, usa `Fraction` y compara conjunta con el producto.
- **Discrepancia textual:** el código denomina “cara” a la línea 1, mientras la descripción del PDF la presenta como línea relativamente cara. La probabilidad se calcula sobre “línea 1”; no se altera por esa etiqueta.
- **Verificación:** la tabla fuente del PDF es imagen; los valores no se pudieron corroborar directamente contra ella.
- **Fuente:** PDF, p. 2.

### Ejercicio 11 — Probabilidad total (despertador)

- **Datos/consigna:** el reloj suena con probabilidad 0,7; si suena, despertar a tiempo tiene probabilidad 0,8; si no suena, 0,30. Hallar la probabilidad de llegar a tiempo.
- **Fórmula y desarrollo:** para los casos \(S\) y \(S'\), \(P(T)=P(S)P(T\mid S)+P(S')P(T\mid S')=0,7·0,8+0,3·0,3=0,65\).
- **Interpretación y supuesto:** el módulo identifica “despertarse a tiempo” con “llegar a tiempo”. La equivalencia no está explicitada en la consigna y debe comunicarse como supuesto.
- **Implementación:** [`ej11.py`](../../ejercicios_tp2/ej11.py) llama a `total()` y presenta la tabla ponderada.
- **Fuente:** PDF, pp. 2–3.

### Ejercicio 12 — Probabilidad total y Bayes (sucursales)

- **Datos:** cuotas de producción A/B/C de 0,30/0,50/0,20; defectuosidad condicional 0,10/0,30/0,25.
- **Consigna:** hallar probabilidad de defecto y probabilidad de que un producto defectuoso provenga de B.
- **Desarrollo:** \(P(D)=0,30·0,10+0,50·0,30+0,20·0,25=0,03+0,15+0,05=0,23\). Por Bayes, \(P(B\mid D)=0,50·0,30/0,23=15/23\approx0,6522\).
- **Implementación:** [`ej12.py`](../../ejercicios_tp2/ej12.py) compone `total()` y `bloque_bayes()`; `Fraction` conserva la posterior exacta.
- **Fuente:** PDF, p. 2.

### Ejercicio 13 — Bayes (cheques con fecha adelantada)

- **Datos:** clientes con fondos suficientes cometen el error con probabilidad 0,001; clientes insuficientes son 1% y siempre cometen el error.
- **Consigna:** dado que se observa un cheque con fecha adelantada, hallar la probabilidad de fondos insuficientes.
- **Desarrollo:** \(P(F)=0,99·0,001+0,01·1=0,01099\). Entonces \(P(I\mid F)=0,01/0,01099=1000/1099\approx0,9099\), aproximadamente 90,99%.
- **Interpretación:** aunque la proporción inicial de clientes insuficientes es 1%, el error observado es mucho más probable bajo esa hipótesis.
- **Implementación:** [`ej13.py`](../../ejercicios_tp2/ej13.py) calcula primero la probabilidad total y luego Bayes.
- **Fuente:** PDF, pp. 2–3.

### Ejercicio 14 — Bayes (urnas y monedas)

- **Consigna:** se elige al azar una de dos urnas y luego un cajón; una urna contiene oro y plata, la otra dos monedas de oro. Dado que se obtuvo oro, hallar la probabilidad de haber elegido la urna II.
- **Desarrollo:** \(P(O)=\frac12·\frac12+\frac12·1=\frac34\). Bayes: \(P(II\mid O)=(\frac12·1)/(\frac34)=2/3\).
- **Implementación:** [`ej14.py`](../../ejercicios_tp2/ej14.py) presenta una tabla de probabilidad total y posterior de Bayes.
- **Fuente:** PDF, p. 3.

### Ejercicio 15 — Distribuciones de probabilidad en un dado

- **Consigna:** verificar si D1, D2 y D3 son distribuciones válidas y, con D1, hallar \(P(A)\), \(P(B')\), \(P(C)\), \(P(D)\) para los sucesos definidos en el ejercicio.
- **Criterio:** cada valor debe ser no negativo y la suma debe ser 1. Con D1 uniforme: \(A=\) par, \(B=\{x\le4\}\), \(C=A\cap B\), \(D=B-A\).
- **Datos y resultados:** D1 es uniforme; D2 \((1/12,1/6,1/6,1/6,1/6,3/12)\); D3 \((0,1/6,1/6,1/6,1/6,2/6)\). Las tres cumplen los dos criterios. Con D1, \(P(A)=1/2\); \(P(B')=1/3\); \(P(C)=1/3\); \(P(D)=1/3\).
- **Implementación:** [`ej15.py`](../../ejercicios_tp2/ej15.py) usa `DataFrame`, `Fraction`, máscaras, sumas y `barras()` para la representación gráfica.
- **Fuente:** PDF, p. 3.

### Ejercicio 16 — Tabla de probabilidad, condicional e independencia

- **Consigna:** encuesta a 1000 adultos cruzando carga del préstamo con presencia de un hijo en la universidad; hallar marginales, conjunta, condicionales e independencia.
- **Datos codificados:** con hijo: 0,35; 0,08; 0,01. Sin hijo: 0,25; 0,20; 0,11. Marginal de “con hijo” 0,44; marginal de carga muy alta 0,60; total 1.
- **Resultados:** \(P(D)=0,44\); \(P(A)=0,60\); \(P(A\cap D)=0,35\); \(P(A\mid D)=0,35/0,44\approx0,7955\); \(P(D\mid A)=0,35/0,60\approx0,5833\). Como \(P(A)P(D)=0,264\ne0,35\), los sucesos no son independientes.
- **Implementación:** [`ej16.py`](../../ejercicios_tp2/ej16.py) crea la tabla de proporciones y añade totales marginales con `con_totales()`.
- **Verificación:** los valores de la tabla son del código; la tabla del PDF se presenta como imagen y no se pudieron comprobar visualmente.
- **Fuente:** PDF, p. 3.

### Ejercicio 17 — Independencia (clasificación de cafés)

- **Consigna:** ordenar al azar X, Y, Z; \(A=\) X está por encima de Y; \(B,C,D=\) X queda primero, segundo o tercero. Decidir independencia de A con B, C y D.
- **Procedimiento:** las seis permutaciones son equiprobables. \(P(A)=1/2\); cada posición de X tiene probabilidad \(1/3\). \(P(A\cap B)=1/3\), que no es \(1/2·1/3=1/6\): no independientes. \(P(A\cap C)=1/6=1/6\): independientes. \(P(A\cap D)=0\ne1/6\): no independientes.
- **Implementación:** [`ej17.py`](../../ejercicios_tp2/ej17.py) usa `permutations("XYZ")`, identifica posiciones y compara razones exactas con `Fraction`.
- **Fuente:** PDF, p. 3.

## Glosario existente en la interfaz

El glosario original está en [`static/tp2.html`](../../static/tp2.html). Sus definiciones, conservadas aquí, son:

- **Espacio muestral:** conjunto de todos los resultados posibles; un suceso es un subconjunto.
- **Regla de Laplace:** favorables dividido por posibles cuando los resultados son equiprobables.
- **Axiomas:** \(P(A)\ge0\), \(P(S)=1\) y aditividad para sucesos disjuntos; de ellos se obtiene \(P(A')=1-P(A)\).
- **Complementarios y excluyentes:** los excluyentes tienen intersección vacía; los complementarios además cubren \(S\).
- **Probabilidad condicional:** probabilidad de A dado B, \(P(A\mid B)=P(A\cap B)/P(B)\), con \(P(B)>0\).
- **Independencia:** la conjunta coincide con el producto de marginales.
- **Probabilidad total:** suma ponderada de las condicionales sobre una partición.
- **Teorema de Bayes:** obtiene una probabilidad posterior a partir de una condicional, prior y evidencia.
- **Distribución discreta:** asignación no negativa de probabilidades cuya suma es 1.

## Implementación de probabilidad y datos

- [`probabilidad.py`](../../probabilidad.py) contiene `baraja`, `dado`, `laplace`, `texto_laplace`, `fraccion`, `con_totales`, `total` y `bloque_bayes`, además de helpers de filas/tablas. `laplace` cuenta una máscara booleana y divide por la cantidad de resultados; `total` pondera condicionales; `bloque_bayes` agrega las probabilidades posteriores.
- En los ejercicios aparecen `DataFrame`/`Series`, `MultiIndex.from_product`, `RangeIndex`, `merge(how="cross")`, `.loc`, `.sum()`, `.apply()`, máscaras booleanas y operaciones de conjuntos. Los DataFrames representan espacios muestrales o tablas de contingencia; las fórmulas de probabilidad las determina el código.
- `Fraction` permite conservar razones como \(15/32\), \(15/23\) o \(2/3\) sin error de redondeo durante la operación.
- Los bloques de salida se convierten en JSON y en Excel mediante los mecanismos compartidos de [`estadistica.py`](../../estadistica.py) y [`exportar_excel.py`](../../exportar_excel.py); la explicación de extremo a extremo está en [`programacion.md`](./programacion.md).

## Límites y supuestos que el chatbot debe preservar

1. Los resultados de los ejercicios 9, 10 y 16 se validaron respecto de los datos del código, pero no contra las celdas incrustadas como imagen en el PDF. El diagrama del ejercicio 8 también requiere lectura visual para confirmar todos sus valores.
2. En el ejercicio 5 se interpreta la extracción sucesiva como sin reposición; las figuras se consideran J, Q y K.
3. En el ejercicio 11 se supone que despertarse a tiempo equivale a llegar a tiempo.
4. No hay un glosario separado en `chatbot/knowledge`; las definiciones de este documento incorporan el glosario que ya estaba en la página web.