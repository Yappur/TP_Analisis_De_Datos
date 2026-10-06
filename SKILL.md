# Guía de trabajo: Probabilidad y Estadística

Esta guía sirve a cualquier persona o asistente que trabaje en este TP. El objetivo es resolver correctamente lo pedido por la materia con código sencillo, documentado y fácil de verificar.

## Antes de cambiar código

1. Lee la consigna y el módulo del ejercicio afectado. Si el cálculo es compartido, revisa `estadistica.py`; si afecta cómo se muestran los resultados, revisa `main.py` y `static/index.html`.
2. Identifica los datos disponibles, qué se pide calcular y si corresponden a población o muestra. No completes información ausente por suposición.
3. Confirma la convención estadística de la consigna. Hay distintas definiciones válidas para percentiles y cálculos con intervalos agrupados; no las sustituyas implícitamente por las de una biblioteca.
4. Realiza el cambio más pequeño que resuelva el pedido y mantenga el formato existente.
5. Explica en español las fórmulas, elecciones o limitaciones que no sean obvias.

## Organización y formatos

- Implementa cada ejercicio en `ejercicios/ejNN.py` y conserva `TITULO`, `ENUNCIADO` y `resolver()`.
- Coloca en `estadistica.py` únicamente lógica que sea compartida o que corresponda a sus helpers actuales.
- Mantén la salida como bloques compatibles con la API: subtítulo, columnas, filas, gráfico opcional y notas.
- Conserva el formato de datos que consume la interfaz y devuelve valores numéricos compatibles con JSON.
- No incorpores frameworks, dependencias ni abstracciones nuevas para resolver un ejercicio aislado.

## Criterios estadísticos de este TP

- `resolver_simple` calcula medidas para datos sin agrupar. `poblacion=True` usa `ddof=0`; `poblacion=False` usa `ddof=1`.
- `percentil(datos, p)` ordena los datos y usa la posición `p*n/100`: cuando es entera, promedia el valor de esa posición y el siguiente; cuando no es entera, toma el siguiente valor según el índice usado en la implementación.
- `resolver_agrupado` usa una tabla con `etiqueta`, `li`, `f` y `marca`, además de la amplitud `h`. Conserva las clases y marcas indicadas en el ejercicio.
- `tipo_asimetria` considera aproximadamente simétricos los valores entre `-0.05` y `0.05`. `pearson_bowley` aplica las fórmulas compartidas existentes.
- No asumas que pandas u otra biblioteca tiene la misma convención que el apunte. Si la consigna pide otra fórmula, confirma su efecto y documenta la decisión.

## Supuestos que no se deben ocultar

- En el ejercicio 9, las medidas se asumen a partir del ejercicio 7 porque el enunciado no las especifica. La clase «12 y más» es abierta, su marca se calcula como `1725 / 115 = 15` y se usa amplitud `3` para las medidas agrupadas.
- En el ejercicio 10, hay 195 observaciones disponibles para razonamiento cuantitativo, aunque el enunciado menciona 200. No inventes los cinco datos faltantes.
- Si aparece otra discrepancia entre consigna, datos y resultado, descríbela y conserva la trazabilidad; no alteres datos para forzar un resultado.

## Verificación

- Comprueba los cálculos con un ejemplo pequeño cuyo resultado puedas calcular manualmente.
- Verifica que `resolver()` mantenga la estructura de salida esperada y que la respuesta de la API siga siendo consumible por la interfaz.
- Para probar la aplicación, desde la raíz ejecuta `uvicorn main:app --reload`; consulta `/api/ejercicios` y el endpoint del ejercicio afectado.
- No hay una suite automatizada configurada actualmente. No agregues una infraestructura de pruebas salvo que el cambio o el pedido lo requiera.
