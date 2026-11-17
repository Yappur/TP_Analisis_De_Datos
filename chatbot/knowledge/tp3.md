# TP3 — Variables aleatorias discretas y distribuciones

## Alcance y fuentes

El TP3 contiene 25 módulos en [`ejercicios_tp3/`](../../ejercicios_tp3/) y su consigna está en [`TP 3_2026.pdf`](../../docs/TP%203_2026.pdf), de cuatro páginas. Se revisó cada `resolver()` y se compararon enunciados legibles con el código. Los números que siguen reflejan las salidas actuales del programa, incluidos los cambios de los ejercicios 2, 5 y 11. Cuando el PDF tiene datos gráficos no recuperados como texto, se distingue el resultado condicionado a los datos del código.

## Glosario y fórmulas

El glosario de [`static/tp3.html`](../../static/tp3.html) incluye:

- **Variable aleatoria discreta:** asigna un número a cada resultado; toma valores aislados.
- **Función de masa de probabilidad (FMP):** \(f(x)=P(X=x)\), con \(f(x)\ge0\) y \(\sum_x f(x)=1\).
- **Esperanza:** promedio ponderado \(E(X)=\sum_x x f(x)\). Para una función \(g\), \(E[g(X)]=\sum_xg(x)f(x)\).
- **Varianza y desvío:** \(V(X)=E(X^2)-[E(X)]^2\), \(\sigma=\sqrt{V(X)}\).
- **Exactamente, al menos, como máximo y menos de:** exactamente \(k\): \(X=k\); al menos: \(X\ge k\); como máximo/a lo sumo: \(X\le k\); menos de \(k\): \(X\le k-1\).
- **Binomial:** \(n\) ensayos independientes, probabilidad de éxito constante \(p\); \(P(X=x)=\binom nx p^x(1-p)^{n-x}\), \(E=np\), \(V=np(1-p)\).
- **Poisson:** cuenta eventos en un intervalo con media \(\lambda\); \(P(X=x)=e^{-\lambda}\lambda^x/x!\), \(E=V=\lambda\). Al cambiar la duración del intervalo, la media cambia proporcionalmente.
- **Aproximación Poisson a binomial:** para \(n\) grande y \(p\) pequeño se usa \(\lambda=np\). El helper documenta como regla práctica \(n\ge20\) y \(p\le0,05\); en los ejercicios comparativos se muestra también la binomial exacta.
- **Geométrica:** \(X\) es el número de ensayos hasta el primer éxito; \(P(X=x)=(1-p)^{x-1}p\), \(E(X)=1/p\).

En las tablas de la interfaz, el símbolo ✓ marca los valores de \(x\) que se suman para el inciso.

## Ejercicios

### Ejercicio 1 — FMP válida (loot boxes)

- **Consigna:** hallar la probabilidad faltante de un ítem legendario dadas las probabilidades 0,60, 0,25 y 0,12.
- **Conceptos y procedimiento:** una FMP debe ser no negativa y sumar 1. \(p_{\text{faltante}}=1-(0,60+0,25+0,12)=0,03\).
- **Resultado e interpretación:** la probabilidad faltante es 0,03 y la suma queda 1; la distribución es válida.
- **Implementación:** [`ej01.py`](../../ejercicios_tp3/ej01.py) organiza valores y masa en un `DataFrame`, calcula la diferencia y muestra la tabla. PDF, p. 1.

### Ejercicio 2 — Esperanza y varianza (boletos de avión)

- **Consigna y discrepancia:** el PDF define una distribución para \(X\), el número de boletos vendidos, con \(X=6,\ldots,10\) y probabilidades 0,25; 0,35; 0,25; 0,10; 0,05. La pregunta se refiere a pasajeros que se presentan al vuelo. Son variables distintas si puede haber ausencias.
- **Cálculo que sí permiten los datos:** \(E(X)=\sum xf(x)=7,35\); \(E(X^2)=55,25\); \(V(X)=55,25-7,35^2=1,2275\); \(\sigma\approx1,107926\). Estos momentos describen boletos vendidos, no asistencia.
- **Límite:** no se proporciona un modelo/probabilidad de asistencia; por lo tanto, la cantidad esperada de pasajeros presentes no puede deducirse. La nota actual del código lo explicita, sin inventar datos.
- **Implementación:** [`ej02.py`](../../ejercicios_tp3/ej02.py) construye la tabla de masa y llama a `momentos()`. PDF, p. 1.

### Ejercicio 3 — Esperanza de una función g(X)

- **Consigna:** con la distribución del número de autos que pasan por un lavadero, el pago se modela como \(g(X)=2X-1\); hallar el pago esperado.
- **Procedimiento:** \(E[g(X)]=\sum(2x-1)f(x)=2E(X)-1\). El código obtiene \(E(X)=6,833333\), por lo que \(E[g(X)]=38/3\approx12,6667\).
- **Resultado e interpretación:** pago esperado aproximadamente \$12,67 según la escala monetaria implícita en el enunciado.
- **Implementación:** [`ej03.py`](../../ejercicios_tp3/ej03.py) crea columnas \(g(x)\) y \(g(x)f(x)\) con pandas y suma la última. PDF, p. 1.

### Ejercicio 4 — Verificar una función de probabilidad

- **Consigna:** verificar \(f(x)=(x+2)/25,\ x=1,\ldots,5\), y hallar cuatro probabilidades.
- **Validez:** las masas son \(3/25,4/25,5/25,6/25,7/25\), todas no negativas y con suma 1.
- **Resultados:** \(P(X>1)=0,88\); \(P(X<5)=0,72\); \(P(X\le3)=0,48\); \(P(1\le X\le4)=0,72\). Los signos estrictos excluyen los extremos correspondientes.
- **Implementación:** [`ej04.py`](../../ejercicios_tp3/ej04.py) construye la tabla de \(f(x)\), usa máscaras booleanas y suma las masas seleccionadas. PDF, p. 1.

### Ejercicio 5 — Constante de normalización

- **Consigna:** hallar \(c\) para que \(f(x)=c(x^2+1)\), \(x=0,1,2,3\), sea una FMP.
- **Desarrollo:** \(1+2+5+10=18\); la normalización exige \(18c=1\), luego \(c=1/18\). Las masas son \(1/18,2/18,5/18,10/18\) y suman 1.
- **Resultado e implementación:** [`ej05.py`](../../ejercicios_tp3/ej05.py) muestra \(c=1/18\). Se corrigió la fila de la igualdad de normalización para que su resultado sea **1** (antes mostraba 18, que era la suma de los términos \(x^2+1\), no el resultado de la igualdad).
- **Fuente:** PDF, p. 1.

### Ejercicio 6 — Constante k y probabilidades (peticiones fallidas)

- **Consigna según el código:** \(X=0,\ldots,4\), con probabilidades 0,45; 0,30; 0,15; \(k\); 0,03; hallar \(k\), \(P(X=2)\), \(P(X<3)\), \(P(X\ge2)\).
- **Desarrollo:** \(k=1-(0,45+0,30+0,15+0,03)=0,07\). Resultados: \(P(X=2)=0,15\); \(P(X<3)=0,90\); \(P(X\ge2)=0,25\).
- **Implementación:** [`ej06.py`](../../ejercicios_tp3/ej06.py) completa la masa faltante, selecciona intervalos con condiciones booleanas y suma.
- **Límite de verificación:** la tabla del PDF no se recupera en la extracción textual; los valores anteriores son los que usa el módulo. PDF, p. 1.

### Ejercicio 7 — Probabilidades, esperanza y varianza (errores en código)

- **Datos:** \(f(0,\ldots,4)=(0,46;0,32;0,16;0,05;0,01)\).
- **Resultados:** \(P(X<3)=0,94\); \(P(1<X<4)=0,21\); \(P(X>2)=0,06\). \(E(X)=0,83\); \(E(X^2)=1,57\); \(V(X)=1,57-0,83^2=0,8811\); \(\sigma\approx0,938669\).
- **Interpretación:** el intervalo \(1<X<4\) es estricto, así que solo incluye 2 y 3.
- **Implementación:** [`ej07.py`](../../ejercicios_tp3/ej07.py) genera columnas \(x f(x)\) y \(x^2f(x)\), filtra por máscaras y calcula momentos. PDF, p. 2.

### Ejercicio 8 — Binomial (fallas en llamadas a una API)

- **Consigna:** 8 llamadas independientes; cada una falla con \(p=0,15\). Hallar ninguna falla, exactamente 2 fallas y más de 5 fallas.
- **Modelo:** \(X\sim B(8,0,15)\), donde \(X\) cuenta fallas.
- **Resultados:** \(P(X=0)=0,272491\); \(P(X=2)=0,237604\); \(P(X>5)=0,0002423\), suma de \(x=6,7,8\).
- **Implementación:** [`ej08.py`](../../ejercicios_tp3/ej08.py) usa `binomial()`, una máscara por inciso y `prob()` para sumar la masa. PDF, p. 2.

### Ejercicio 9 — Binomial (campaña telefónica)

- **Consigna:** 25 llamadas, probabilidad de inscripción \(p=1/20=0,05\); hallar al menos dos inscripciones.
- **Modelo y procedimiento:** \(X\sim B(25,0,05)\). Por complemento, \(P(X\ge2)=1-P(0)-P(1)\).
- **Resultados:** \(P(0)=0,277390\), \(P(1)=0,364986\), \(P(X\ge2)=0,357624\) (35,76%).
- **Implementación:** [`ej09.py`](../../ejercicios_tp3/ej09.py) construye la tabla binomial y aplica la máscara \(x\ge2\). PDF, p. 2.

### Ejercicio 10 — Binomial (tiros libres)

- **Consigna:** 14 tiros, encesta con \(p=0,70\); calcular al menos 7 encestes, entre 3 y 6 fallas inclusive, todas fallas y todos encestes.
- **Modelo:** \(X\sim B(14,0,70)\) cuenta encestes; para las fallas se usa \(Y=14-X\).
- **Resultados en el orden de los incisos:** 0,968531; 0,745882; \(4,783\times10^{-8}\); 0,006782.
- **Implementación:** [`ej10.py`](../../ejercicios_tp3/ej10.py) calcula los eventos con máscaras de rango y complementos sobre la tabla binomial. PDF, p. 2.

### Ejercicio 11 — Binomial (billetes de lotería)

- **Consigna:** de 500 billetes, 200 recuperan al menos el costo; se compran 5; calcular la probabilidad de ganar al menos el costo de 3.
- **Modelo exacto:** se seleccionan billetes de un conjunto finito sin reposición, por lo que el número de ganadores sigue una hipergeométrica. \(P(X\ge3)=\sum_{k=3}^{5}\binom{200}{k}\binom{300}{5-k}/\binom{500}{5}=0,316744\).
- **Aproximación:** la binomial con \(n=5,p=200/500=0,4\) da 0,317440.
- **Resultado actual:** la fila principal de [`ej11.py`](../../ejercicios_tp3/ej11.py) es el resultado hipergeométrico exacto; el valor binomial se mantiene explícitamente como aproximación. La diferencia es pequeña, pero no nula.
- **Fuente:** PDF, p. 2. [`SKILL.md`](../../SKILL.md) contiene una descripción previa que todavía presenta la binomial como método principal; para este ejercicio debe prevalecer el código actual.

### Ejercicio 12 — Binomial, esperanza y varianza (tests en CI/CD)

- **Consigna:** 15 tests independientes, cada uno pasa con \(p=0,90\); se aprueba con al menos 14. Se piden esperanza, varianza y desvío asociados a la aprobación.
- **Variable de conteo:** \(X=\) número de tests que pasan. \(E(X)=np=13,5\), \(V(X)=np(1-p)=1,35\), \(\sigma\approx1,161895\), y \(P(X\ge14)=0,549043\).
- **Variable indicadora:** el módulo incluye también \(A=1\) si se aprueba y 0 si no. \(E(A)=P(A=1)=0,549043\); \(V(A)=p_A(1-p_A)=0,247595\); \(\sigma_A\approx0,497589\).
- **Interpretación:** cantidad de tests que pasan y resultado binario de aprobación son variables distintas; el código informa ambos análisis.
- **Implementación:** [`ej12.py`](../../ejercicios_tp3/ej12.py) usa la tabla binomial y cálculos de momentos. PDF, pp. 2–3.

### Ejercicio 13 — Binomial (filtro de spam)

- **Consigna:** se consideran 10 correos efectivamente spam, con detección del 80%; hallar la probabilidad de filtrar menos de 7.
- **Modelo y resultado:** \(X\sim B(10,0,8)\); \(P(X<7)=P(X\le6)=0,120874\). El 7 no se incluye.
- **Implementación:** [`ej13.py`](../../ejercicios_tp3/ej13.py) suma la masa para \(x\le6\).
- **Ambigüedad terminológica:** el PDF usa “precisión” para la capacidad de detectar spam; precisión técnica y sensibilidad/tasa de detección no son necesariamente lo mismo. El cálculo supone \(p=0,8\) como tasa de detección. PDF, p. 3.

### Ejercicio 14 — Binomial (chips defectuosos)

- **Consigna:** muestra de 20 chips, probabilidad de defecto 0,10; calcular a lo sumo 3 defectuosos, al menos 2 y ninguno.
- **Modelo y resultados:** \(X\sim B(20,0,10)\). \(P(X\le3)=0,867047\); \(P(X\ge2)=0,608253\); \(P(X=0)=0,121577\).
- **Implementación:** [`ej14.py`](../../ejercicios_tp3/ej14.py) usa máscaras inclusivas para \(X\le3\) y \(X\ge2\). PDF, p. 3.

### Ejercicio 15 — Poisson (tráfico de un API Gateway)

- **Consigna:** tasa media 4,5 peticiones por segundo y capacidad 7; calcular \(P(X=4)\), \(P(X=0)\) y la saturación \(X>7\); decidir si escalar cuando supera 5%.
- **Modelo y resultados:** \(X\sim Pois(4,5)\); \(P(4)=0,189808\), \(P(0)=0,011109\), \(P(X\le7)=0,913414\), por lo que \(P(X>7)=0,086586\).
- **Interpretación:** 8,66% supera el umbral indicado de 5%, por lo que el código recomienda escalar.
- **Implementación:** [`ej15.py`](../../ejercicios_tp3/ej15.py) usa `poisson()`, complemento para saturación y columna de marcas. PDF, p. 3.

### Ejercicio 16 — Poisson (accidentes de tránsito)

- **Consigna:** media de 3 accidentes por mes; hallar exactamente 5, menos de 3 y al menos 2.
- **Resultados:** para \(X\sim Pois(3)\), \(P(X=5)=0,100819\); \(P(X<3)=P(X\le2)=0,423190\); \(P(X\ge2)=0,800852\).
- **Implementación:** [`ej16.py`](../../ejercicios_tp3/ej16.py) suma masas según las condiciones. PDF, p. 3.

### Ejercicio 17 — Poisson (ataques de virus)

- **Consigna y resultado:** tasa media 0,4 virus por semana; la probabilidad de cero ataques la semana próxima es \(P(0)=e^{-0,4}=0,670320\), es decir, aproximadamente 67,03%.
- **Implementación:** [`ej17.py`](../../ejercicios_tp3/ej17.py) usa la distribución Poisson con \(\lambda=0,4\). PDF, p. 3.

### Ejercicio 18 — Poisson con cambio de intervalo (cola de mensajes)

- **Consigna:** tasa de 12 mensajes por minuto; hallar las medias para 30 y 10 segundos y, para 10 segundos, exactamente 2 y al menos 1 mensaje.
- **Procedimiento:** escalar la tasa por duración: \(\lambda_{30}=12·0,5=6\); \(\lambda_{10}=12·(10/60)=2\).
- **Resultados:** con \(Pois(2)\), \(P(X=2)=0,270671\); \(P(X\ge1)=1-P(0)=0,864665\).
- **Implementación:** [`ej18.py`](../../ejercicios_tp3/ej18.py) construye las tablas Poisson para cada intervalo. PDF, pp. 3–4.

### Ejercicio 19 — Poisson (errores por página)

- **Consigna:** media de 2 errores por página; calcular cuatro o más y ningún error.
- **Resultados:** \(P(X\ge4)=1-P(X\le3)=0,142877\); \(P(X=0)=0,135335\), para \(X\sim Pois(2)\).
- **Implementación:** [`ej19.py`](../../ejercicios_tp3/ej19.py) obtiene el evento de cola por complemento. PDF, p. 4.

### Ejercicio 20 — Poisson (intentos de login fallidos)

- **Consigna y procedimiento:** media 1,2 intentos fallidos por hora; “más de 3” corresponde a \(X\ge4\), calculado como complemento de \(X\le3\).
- **Resultado:** \(P(X>3)=0,033769\).
- **Implementación:** [`ej20.py`](../../ejercicios_tp3/ej20.py) utiliza `poisson(1.2, ...)` y complemento. PDF, p. 4.

### Ejercicio 21 — Aproximación de Poisson a la binomial (accidentes)

- **Consigna:** 400 días independientes con probabilidad diaria 0,005; pregunta por un accidente “en un día” y por a lo sumo tres días con accidente.
- **Interpretación del código:** en (a) calcula exactamente un día con accidente entre los 400, no la probabilidad de accidente en un día particular.
- **Aproximación y comparación:** \(\lambda=np=400·0,005=2\). Poisson: \(P(X=1)=0,270671\), \(P(X\le3)=0,857123\). Binomial exacta: 0,270669 y 0,857577, respectivamente.
- **Ambigüedad:** “en un día” puede leerse como la probabilidad diaria 0,005 o como exactamente uno entre 400 días. El código adopta la segunda lectura; no se debe ocultar la ambigüedad.
- **Implementación:** [`ej21.py`](../../ejercicios_tp3/ej21.py) compara Poisson y binomial exacta. PDF, p. 4.

### Ejercicio 22 — Aproximación de Poisson (artículos con burbujas)

- **Consigna:** 8.000 artículos con probabilidad de defecto 0,001; hallar menos de 7 defectuosos.
- **Modelo:** \(\lambda=np=8\); “menos de 7” significa \(X\le6\).
- **Resultados:** Poisson \(P(X\le6)=0,313374\); binomial exacta 0,313252.
- **Implementación:** [`ej22.py`](../../ejercicios_tp3/ej22.py) muestra ambas columnas. PDF, p. 4.

### Ejercicio 23 — Aproximación de Poisson, media y varianza (declaraciones de impuestos)

- **Consigna:** 10.000 formularios, error con probabilidad 0,001; probabilidad de exactamente 6, 7 u 8 errores, media y varianza.
- **Procedimiento:** \(\lambda=np=10\). Poisson \(P(6\le X\le8)=0,265734\); binomial exacta 0,265716. La media Poisson es 10 y su varianza 10; la varianza binomial es \(np(1-p)=9,99\).
- **Interpretación:** los modelos dan probabilidades muy próximas, pero la aproximación no es idéntica a la binomial.
- **Implementación:** [`ej23.py`](../../ejercicios_tp3/ej23.py) compara las probabilidades y los momentos. PDF, p. 4.

### Ejercicio 24 — Binomial: media, varianza y P(X = 0) (diodos)

- **Consigna:** 200 diodos con probabilidad de falla 0,03; hallar media, varianza y probabilidad de que el tablero funcione (ningún diodo falla).
- **Resultados:** \(E(X)=np=6\); \(V(X)=np(1-p)=5,82\); \(P(X=0)=0,97^{200}=0,002261\). La aproximación Poisson con \(\lambda=6\) da 0,002479.
- **Implementación:** [`ej24.py`](../../ejercicios_tp3/ej24.py) informa la binomial exacta y su aproximación Poisson. PDF, p. 4.

### Ejercicio 25 — Geométrica: costo esperado de un experimento

- **Consigna:** cada ensayo cuesta \$1.000, cada fallo suma \$300, éxito con \(p=0,2\), ensayos independientes hasta el primero.
- **Modelo y desarrollo:** \(X\sim Geom(0,2)\), \(E(X)=1/p=5\). El costo total para \(X\) ensayos es \(C(X)=1000X+300(X-1)=1300X-300\). Por linealidad, \(E[C]=1300·5-300=\$6.200\).
- **Interpretación:** costo medio de largo plazo, no costo garantizado de cada corrida.
- **Implementación:** [`ej25.py`](../../ejercicios_tp3/ej25.py) usa `geometrica()` y suma una tabla truncada hasta \(x=200\) como verificación numérica; la esperanza se obtiene también algebraicamente. PDF, p. 4.

## Implementación compartida

[`distribuciones.py`](../../distribuciones.py) define:

- `binomial(n,p,x_max=None)`: genera un `DataFrame` con \(x\), \(P(X=x)\) y \(P(X\le x)\). Para \(n\le1000\) usa coeficientes combinatorios directos; para \(n\) grande usa la recurrencia \(P(x+1)=P(x)\frac{n-x}{x+1}\frac{p}{1-p}\).
- `poisson(lam,x_max)`: evalúa \(e^{-\lambda}\lambda^x/x!\) para \(x=0,\ldots,x_{\max}\) y acumula con `cumsum()`.
- `geometrica(p,x_max)`: evalúa \((1-p)^{x-1}p\) para \(x=1,\ldots,x_{\max}\).
- `prob(tabla,mascara)`: suma las masas seleccionadas.
- `momentos(x,f)`: crea productos \(xf(x)\) y \(x^2f(x)\), y retorna tabla, esperanza, varianza y desvío.
- `bloque_distribucion`, `bloque_resolucion`, `bloque_tabla`, `bloque_comparacion`: presentan tablas, acumuladas, marcas por inciso, gráficos o comparación exacta/aproximada. Son formato de salida, no modelos probabilísticos nuevos.

Las tablas utilizan `DataFrame`, máscaras booleanas, `.loc`, `.sum()`, `.cumsum()`, `.copy()`, `.iloc` y columnas seleccionadas. Los cálculos de probabilidad se implementan con Python (`math.comb`, `exp`, `factorial`, `sqrt`) y no con SciPy. Para cifras pequeñas el formato muestra hasta 6 decimales o 4 cifras significativas según el tamaño.

## Discrepancias, supuestos y vigencia

1. **Ejercicio 2:** la distribución corresponde a boletos vendidos, mientras la pregunta pide asistencia. El código actual señala que la asistencia no se puede determinar; no imputar ausencias.
2. **Ejercicio 5:** se corrigió el resultado de la igualdad de normalización a 1; \(c\) sigue siendo \(1/18\).
3. **Ejercicio 11:** la hipergeométrica exacta 0,316744 es principal y 0,317440 es aproximación binomial.
4. **Ejercicio 12:** “esperanza de aprobación” puede referirse al indicador binario o al conteo de tests; el módulo muestra ambos.
5. **Ejercicio 13:** la interpretación de “precisión” como tasa de detección está supuesta.
6. **Ejercicio 21(a):** la redacción permite más de una lectura; el código usa “exactamente uno en 400 días”.
7. **Ejercicio 6:** las cifras de entrada no se pudieron verificar contra el texto extraído del PDF.
8. [`SKILL.md`](../../SKILL.md) no se actualizó con los cambios previos de los ejercicios 2 y 11 y conserva supuestos antiguos; para describir la resolución vigente prevalece el módulo actual. Es una inconsistencia documental no resuelta en esta tarea.
9. En el repositorio, los Excel de TP3 02, 05 y 11 tienen fecha de modificación 16/11/2026, anterior a las correcciones de los módulos del 17/11/2026. No se inspeccionó su contenido celda por celda. La ruta de descarga sirve un archivo existente sin regenerarlo, por lo que estos libros pueden estar desactualizados; se pueden regenerar con `python exportar_excel.py --tp3 2 5 11`.