"""Diccionario de sinónimos editable.

Cómo funciona:
    Antes de buscar, cada CLAVE que aparece en la pregunta se REEMPLAZA por su VALOR.
    Si querés conservar la palabra original, incluila también en el valor
    (ej.: "promedio": "promedio media").

Reglas para editarlo:
    - Podés escribir con tildes y mayúsculas: todo se normaliza al cargar.
    - Las claves de varias palabras ("tp 1", "desvio estandar") se aplican antes
      que las de una sola, así "desvio estandar" no se rompe por la regla "desvio".
    - Se reemplazan palabras completas: "media" no toca "mediana".
"""

SINONIMOS: dict[str, str] = {
    # ---------- Nombres de los TP (activan el filtro por TP en search.py) ----------
    "tp 1": "tp1",
    "tp n 1": "tp1",
    "tp nro 1": "tp1",
    "trabajo practico 1": "tp1",
    "trabajo practico uno": "tp1",
    "primer tp": "tp1",
    "tp 2": "tp2",
    "tp n 2": "tp2",
    "tp nro 2": "tp2",
    "trabajo practico 2": "tp2",
    "trabajo practico dos": "tp2",
    "segundo tp": "tp2",
    "tp 3": "tp3",
    "tp n 3": "tp3",
    "tp nro 3": "tp3",
    "trabajo practico 3": "tp3",
    "trabajo practico tres": "tp3",
    "tercer tp": "tp3",

    # ---------- Ejercicios ----------
    "ej": "ejercicio",
    "ejer": "ejercicio",
    "punto": "ejercicio",
    "problema": "ejercicio",

    # ---------- Estadística descriptiva (TP1) ----------
    "promedio": "promedio media",
    "media aritmetica": "media",
    # En tp1.md se escribe "desvío estándar", así que llevamos todo a esa forma.
    "desviacion estandar": "desvio estandar",
    "desviacion tipica": "desvio estandar",
    "sd": "desvio estandar",
    "cv": "coeficiente variacion",
    "valor mas repetido": "moda",
    "valor central": "mediana",
    "dispersion": "dispersion varianza desvio rango",
    "cuartil": "cuartil cuartiles",
    "percentil": "percentil percentiles",
    "asimetria": "asimetria sesgo",
    "frecuencias": "frecuencia tabla frecuencias",
    "grafico": "grafico histograma",

    # ---------- Probabilidad (TP2) ----------
    "condicionada": "condicional",
    "bayes": "bayes teorema",
    "laplace": "laplace regla",
    "eventos": "sucesos",
    "evento": "suceso",
    "incompatibles": "excluyentes",
    "disjuntos": "excluyentes",
    "complemento": "complemento complementarios",

    # ---------- Variables aleatorias (TP3) ----------
    "esperanza matematica": "esperanza",
    "valor esperado": "esperanza",
    "fmp": "funcion probabilidad",
    "funcion de masa": "funcion probabilidad",
    "binomiales": "binomial",
    "poison": "poisson",

    # ---------- Programación / arquitectura ----------
    "se programo": "programacion lenguaje bibliotecas",
    "programo": "programacion lenguaje bibliotecas",
    "programaron": "programacion lenguaje bibliotecas",
    "programado": "programacion lenguaje bibliotecas",
    "codigo": "codigo programacion implementacion",
    "excel": "excel openpyxl",
    "planilla": "excel",
    "backend": "fastapi api",
    "endpoint": "ruta api",
    "endpoints": "rutas api",
    "frontend": "frontend html javascript",
    "carpetas": "carpetas organizacion archivos",
    "estructura": "estructura organizacion carpetas",
    "librerias": "bibliotecas dependencias",
    "bot": "chatbot",
}
