from fractions import Fraction
from itertools import product

import pandas as pd
from probabilidad import bloque_resolucion, fila, laplace, texto_laplace

TITULO = "Ejercicio 4 – Laplace con y sin sustitución"
ENUNCIADO = ("Un lote tiene 10 artículos sin defecto y 6 con defecto. Se escogen 2. Probabilidad de que "
             "exactamente uno sea sin defecto: a) con sustitución; b) sin sustitución.")
BUENOS, DEFECTUOSOS = 10, 6


def resolver():
    lote = ["B"] * BUENOS + ["D"] * DEFECTUOSOS  # B = sin defecto, D = defectuoso
    n = len(lote)

    # Pares ordenados de artículos (i, j): con sustitución se permite i = j
    con = pd.DataFrame(product(range(n), repeat=2), columns=["i", "j"])
    sin = con[con["i"] != con["j"]]
    exactamente_uno = lambda df: (df["i"].map(lote.__getitem__) == "B") != (df["j"].map(lote.__getitem__) == "B")

    p_con = laplace(exactamente_uno(con))
    p_sin = laplace(exactamente_uno(sin))
    assert p_con == 2 * Fraction(10, 16) * Fraction(6, 16)
    assert p_sin == 2 * Fraction(10, 16) * Fraction(6, 15)

    filas = [
        fila("a) P = P(BD) + P(DB) (con sustitución)", "2 · (10/16) · (6/16) = 120/256", p_con),
        fila("   Verificación por conteo (pares ordenados)", texto_laplace(exactamente_uno(con)), p_con),
        fila("b) P = P(BD) + P(DB) (sin sustitución)", "2 · (10/16) · (6/15) = 120/240", p_sin),
        fila("   Con combinaciones", "C(10,1)·C(6,1) / C(16,2) = 60/120", p_sin),
    ]
    return [bloque_resolucion(filas, notas=[
        "Total de artículos: 16 (10 sin defecto + 6 con defecto).",
        "Con sustitución las extracciones son independientes; sin sustitución el denominador baja a 15."])]
