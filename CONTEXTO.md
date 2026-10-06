# Contexto del proyecto

Este proyecto es un trabajo práctico de **Probabilidad y Estadística**. Tiene una API pequeña en FastAPI, diez ejercicios y una interfaz web estática. La prioridad es que los resultados respeten las consignas de la materia y que el código sea fácil de entender y mantener, sin sobreingeniería.

## Estructura

- `main.py`: API FastAPI. Expone `GET /api/ejercicios` y `GET /api/ejercicios/{n}`, carga los módulos de ejercicios y sirve la carpeta `static/`.
- `estadistica.py`: funciones estadísticas compartidas y formato de bloques, tablas y gráficos.
- `ejercicios/ej01.py` a `ejercicios/ej10.py`: datos, enunciados y resolución de cada ejercicio.
- `static/index.html`: interfaz web; muestra los resultados y gráficos con Chart.js.
- `static/js.js` y `static/style.css`: están vacíos actualmente. No dupliques ni traslades código allí sin una necesidad concreta.
- `requirements.txt`: dependencias Python: FastAPI, Uvicorn y pandas.

## Convenciones del proyecto

- Cada ejercicio expone `TITULO`, `ENUNCIADO` y `resolver()`.
- Los resultados se devuelven como bloques con subtítulo, columnas, filas, gráfico opcional y notas. La API y la interfaz dependen de ese formato.
- Reutiliza `estadistica.py` para cálculos compartidos y conserva la estructura existente. Evita agregar capas, dependencias o configuraciones que no resuelvan una necesidad real.
- Escribe en español claro los textos visibles y las explicaciones. Describe las fórmulas y decisiones estadísticas de forma que puedan vincularse con lo visto en clase.
- Distingue población de muestra: el código usa `ddof=0` (divisor `N`) para población y `ddof=1` (divisor `n - 1`) para muestra.
- `percentil(datos, p)` ordena los datos y aplica la convención del TP: posición `p*n/100`; si es entera, promedia el dato de esa posición y el siguiente; si no, toma el dato siguiente según el índice de la implementación. No sustituyas esta regla por la convención predeterminada de una biblioteca sin revisar la consigna.
- Para datos agrupados, conserva los límites, amplitudes, frecuencias y marcas de clase definidos por el ejercicio. Las bibliotecas pueden usar convenciones diferentes a las del curso.
- Mantén visibles las suposiciones e inconsistencias del material. No inventes datos ni ajustes resultados en silencio.
- Si un caso límite afecta un cálculo solicitado —por ejemplo, una división por cero—, trátalo explícitamente y explícalo; no ocultes el problema con un valor predeterminado.

## Supuestos conocidos

- **Ejercicio 9:** el material no especifica qué medidas calcular, así que el código asume las mismas que el ejercicio 7. La última clase es abierta («12 y más»); su marca `15` se obtiene de `1725 / 115`, y se usa amplitud `3` para los cálculos agrupados. Son decisiones asumidas para este ejercicio, no datos universales.
- **Ejercicio 10:** el enunciado indica 200 observaciones de razonamiento cuantitativo, pero el material disponible contiene 195. No inventes las cinco observaciones faltantes.

## Ejecución y comprobación

Instala las dependencias con `pip install -r requirements.txt` y ejecuta la aplicación desde la raíz con `uvicorn main:app --reload`. La documentación automática de FastAPI está en `/docs`.

El proyecto no tiene una suite de pruebas automatizada configurada. Para cambios estadísticos, comprueba resultados con ejemplos manuales pequeños y con la convención indicada por la consigna. Para cambios en la API o interfaz, verifica el listado de ejercicios, un ejercicio simple y los ejercicios agrupados o con gráficos afectados.
