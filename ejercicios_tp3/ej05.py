from fractions import Fraction as Fr

import pandas as pd
from distribuciones import bloque_resolucion, bloque_tabla, fila

TITULO = "Ejercicio 5 – Constante de normalización"
ENUNCIADO = ("Determinar el valor de c para que f(x) = c·(x² + 1), x = 0, 1, 2, 3, "
             "sea la distribución de probabilidad de la v.a. X.")


def resolver():
    t = pd.DataFrame({"x": range(4)})
    t["x² + 1"] = t["x"] ** 2 + 1
    suma = int(t["x² + 1"].sum())
    c = Fr(1, suma)
    t["f(x) = c·(x² + 1)"] = [c * v for v in t["x² + 1"]]
    filas = [
        fila("Σ c·(x² + 1) = 1", "c·(1 + 2 + 5 + 10) = 1  →  18·c = 1", 1, porcentaje=False),
        fila("c = 1 / 18", f"c = {c}", c, porcentaje=False),
    ]
    return [bloque_resolucion(filas),
            bloque_tabla("Distribución resultante (c = 1/18)", t,
                         notas=["Con c = 1/18 todas las f(x) son ≥ 0 y suman 1."])]
