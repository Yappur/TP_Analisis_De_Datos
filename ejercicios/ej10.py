import re
import pandas as pd
from estadistica import bloque, barras, percentil, r, tipo_asimetria

TITULO = "Ejercicio 10"
ENUNCIADO = ("a) Lenguajes de programación de 78 estudiantes. "
             "b) Dispersión de la prueba de comprensión lectora (Software vs Programación). "
             "c) Estadística descriptiva del razonamiento cuantitativo (como en Excel). "
             "Nota: el PDF muestra 195 valores en (c), aunque el enunciado dice 200.")

TEXTO = """Python - Cobol - PHP - C++ - Cobol - PHP - SQL - SQL - Python - Python – C++ – SQL - Cobol - PHP -
Python - C++- PHP - Cobol - Python - PHP - Cobol - SQL - Python - C++- Python - Python - C++ - PHP
- SQL - SQL – Cobol – Cobol- Java - Cobol - Java - Cobol - PHP - C++ - SQL - SQL - Python - C++ -
Cobol-Cobol - Python -C++ - SQL - Cobol - C++ - SQL - Python - SQL - C++ - Python - Cobol - Cobol
-Java - C++ - Java - Cobol - SQL- Cobol - Java - Cobol - C++ - SQL – PHP - Cobol - Cobol - PHP -Java
- C++ - Java - PHP - C++ -Java - PHP -Java"""

SOFTWARE = [3.0, 3.7, 2.5, 2.2, 3.5, 3.0, 2.7, 3.8, 3.8, 2.2, 2.5, 3.8,
            3.3, 2.8, 2.7, 3.5, 2.2, 2.7, 2.2, 2.3, 2.3, 2.3, 2.0, 3.8,
            2.7, 2.2, 3.2, 2.5, 3.7, 2.3, 3.5, 2.2, 2.0, 2.5, 3.0, 2.8,
            3.8, 2.3, 3.0, 2.0, 2.3, 3.7, 2.7, 2.2, 2.3, 2.7, 2.7, 2.2,
            3.3, 2.0, 3.0, 2.2, 2.3, 2.3, 3.5, 2.8, 3.0, 3.0, 2.2, 4.0]

PROGRAMACION = [3.8, 3.5, 2.7, 2.2, 3.0, 2.0, 3.5, 3.7, 2.0, 3.8, 2.0, 2.5,
                2.7, 2.0, 2.7, 3.8, 2.3, 3.2, 3.7, 3.3, 3.3, 2.2, 2.3, 2.5,
                2.0, 2.7, 3.0, 3.8, 3.3, 3.8, 2.7, 2.3, 2.2, 3.5, 3.5, 2.5,
                2.5, 2.7, 3.2, 3.3, 2.3, 2.2, 2.3, 3.0, 3.5, 3.5, 2.2, 2.7,
                2.2, 2.7, 2.5, 3.8, 2.7, 2.2, 2.3, 2.5, 2.7, 2.7, 2.2, 3.8]

# 13 filas x 15 columnas = 195 valores. Si el profesor pasa los 5 faltantes, se agregan acá.
RAZONAMIENTO = [
    1.8, 3.8, 3.3, 1.3, 1.3, 2.3, 3.5, 2.5, 2.0, 1.5, 2.5, 3.3, 3.5, 2.5, 1.5,
    3.5, 3.5, 2.0, 4.3, 3.5, 3.8, 3.3, 2.3, 2.5, 2.8, 3.3, 1.5, 2.0, 1.5, 1.5,
    3.5, 2.8, 1.5, 1.8, 1.0, 4.3, 3.8, 1.8, 4.0, 2.0, 0.3, 2.8, 2.3, 3.0, 3.0,
    3.5, 2.5, 1.8, 1.8, 2.0, 3.0, 3.0, 2.5, 2.5, 3.3, 2.3, 1.5, 2.3, 2.0, 2.0,
    3.3, 2.3, 3.0, 2.3, 3.0, 2.8, 3.8, 3.3, 3.0, 2.8, 4.0, 1.8, 2.3, 1.5, 3.0,
    2.8, 2.8, 1.5, 1.5, 1.5, 2.5, 2.8, 4.0, 1.5, 1.0, 3.3, 2.0, 2.8, 1.8, 1.9,
    3.0, 2.8, 2.8, 2.5, 3.5, 1.8, 1.3, 3.3, 0.8, 3.0, 2.5, 2.5, 2.5, 2.5, 4.0,
    1.5, 1.3, 2.0, 2.0, 2.3, 1.8, 3.0, 3.5, 2.3, 1.8, 2.5, 4.0, 1.3, 1.8, 3.0,
    2.8, 2.8, 2.0, 2.3, 2.3, 3.0, 2.0, 3.0, 2.8, 1.5, 3.3, 2.0, 2.8, 1.8, 2.8,
    1.5, 3.3, 4.0, 1.3, 2.3, 3.5, 3.0, 2.3, 2.8, 3.0, 2.3, 2.0, 3.5, 1.5, 3.0,
    3.8, 4.0, 2.3, 2.3, 2.0, 2.0, 1.5, 3.8, 4.0, 4.0, 2.8, 2.8, 3.0, 1.3, 3.3,
    0.8, 2.5, 2.5, 2.5, 2.8, 2.0, 2.0, 3.3, 4.5, 0.8, 1.8, 3.3, 3.3, 4.0, 3.3,
    3.0, 2.3, 2.0, 2.8, 2.3, 4.0, 2.5, 2.0, 3.0, 2.8, 1.3, 2.0, 0.8, 2.5, 3.0,
]


def lenguajes():
    datos = pd.Series(re.findall(r"Python|Cobol|PHP|C\+\+|SQL|Java", TEXTO))
    f = datos.value_counts()
    filas = [[l, int(n), r(n / len(datos), 3), r(n / len(datos) * 100, 2)] for l, n in f.items()]
    return [bloque(f"a) Lenguajes de programación (n = {len(datos)})",
                   ["Lenguaje", "f", "fr", "%"], filas,
                   barras(f.index, {"Frecuencia": f.values}),
                   [f"Variable cualitativa nominal: solo tiene sentido la moda ({', '.join(datos.mode())})."])]


def comprension():
    grupos = {"Desarrollo de Software": SOFTWARE, "Programación": PROGRAMACION}
    medidas = {}
    for nombre, datos in grupos.items():
        s = pd.Series(datos)
        q1, q3 = percentil(s, 25), percentil(s, 75)
        medidas[nombre] = [r(s.mean()), r(s.max() - s.min()), r(q3 - q1),
                           r(s.var(ddof=0)), r(s.std(ddof=0)),
                           r(s.std(ddof=0) / s.mean() * 100, 2)]
    nombres = list(grupos)
    nombres_medidas = ["Media", "Rango", "Rango intercuartil", "Varianza", "Desvío estándar", "CV (%)"]
    filas = [[m] + [medidas[n][i] for n in nombres] for i, m in enumerate(nombres_medidas)]

    cv = {n: medidas[n][-1] for n in nombres}
    mayor = max(cv, key=cv.get)
    if abs(cv[nombres[0]] - cv[nombres[1]]) < 1:
        nota = "Los CV son casi iguales: la dispersión relativa es prácticamente la misma."
    else:
        nota = f"Mayor dispersión relativa en {mayor} (CV = {cv[mayor]}%)."

    valores = sorted(set(SOFTWARE) | set(PROGRAMACION))
    series = {n: pd.Series(d).value_counts().reindex(valores, fill_value=0) for n, d in grupos.items()}
    return [bloque("b) Comprensión lectora (población: todos los aspirantes)",
                   ["Medida"] + nombres, filas,
                   barras([f"{v:g}" for v in valores], series), [nota])]


def razonamiento():
    s = pd.Series(RAZONAMIENTO)
    filas = [["Media", r(s.mean())], ["Error típico", r(s.sem())], ["Mediana", r(s.median())],
             ["Moda", ", ".join(f"{m:g}" for m in s.mode())],
             ["Desviación estándar", r(s.std())], ["Varianza de la muestra", r(s.var())],
             ["Curtosis", r(s.kurt())], ["Coeficiente de asimetría", r(s.skew())],
             ["Rango", r(s.max() - s.min())], ["Mínimo", r(s.min())], ["Máximo", r(s.max())],
             ["Suma", r(s.sum())], ["Cuenta", int(s.count())]]
    conteo = pd.cut(s, bins=10).value_counts(sort=False)
    etiquetas = [f"{i.left:.2f} a {i.right:.2f}" for i in conteo.index]
    return [bloque("c) Razonamiento cuantitativo (estadística descriptiva)", ["Medida", "Valor"], filas,
                   barras(etiquetas, {"Frecuencia": conteo.values}),
                   [f"Asimetría {tipo_asimetria(s.skew())}; curtosis {r(s.kurt(), 3)} "
                    f"({'más plana' if s.kurt() < 0 else 'más apuntada'} que la normal)."])]


def resolver():
    return lenguajes() + comprension() + razonamiento()
