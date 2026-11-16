from fractions import Fraction as F

import pandas as pd
from estadistica import barras, bloque, r
from probabilidad import bloque_resolucion, conjunto, fila, fraccion

TITULO = "Ejercicio 15 – Distribuciones de probabilidad en un dado"
ENUNCIADO = ("Experimento «tiro de un dado» con las distribuciones D1, D2 y D3 de la tabla. "
             "a) Analizar si las Di son distribuciones de probabilidad. "
             "b) Con D1: A = {x / x es par}, B = {x / x ≤ 4}, C = A ∩ B, D = B − A. Calcular P(A), P(Bᶜ), P(C), P(D).")

U = [1, 2, 3, 4, 5, 6]
DISTRIBUCIONES = pd.DataFrame({
    "D1": [F(1, 6)] * 6,
    "D2": [F(1, 12), F(1, 6), F(1, 6), F(1, 6), F(1, 6), F(3, 12)],
    "D3": [F(0), F(1, 6), F(1, 6), F(1, 6), F(1, 6), F(2, 6)],
}, index=U)


def resolver():
    d = DISTRIBUCIONES
    tabla = [[str(x)] + [fraccion(v) for v in d.loc[x]] for x in U]
    tabla.append(["Σ P(x)"] + [fraccion(d[c].sum()) for c in d.columns])
    grafico = barras(U, {c: [r(v) for v in d[c]] for c in d.columns})
    grafico["eje"] = "Probabilidad"

    analisis = [[c, "Sí" if (d[c] >= 0).all() else "No", fraccion(d[c].sum()),
                 "Sí" if (d[c] >= 0).all() and d[c].sum() == 1 else "No"] for c in d.columns]

    p = d["D1"]
    x = pd.Series(U, index=U)
    A, B = x % 2 == 0, x <= 4
    C, D = A & B, B & ~A
    filas = [
        fila(f"P(A), A = {conjunto(x[A])}", "3 · 1/6", p[A].sum()),
        fila(f"P(Bᶜ), Bᶜ = {conjunto(x[~B])}", "1 − P(B) = 1 − 4/6", p[~B].sum()),
        fila(f"P(C), C = A ∩ B = {conjunto(x[C])}", "2 · 1/6", p[C].sum()),
        fila(f"P(D), D = B − A = {conjunto(x[D])}", "2 · 1/6", p[D].sum()),
    ]
    return [
        bloque("Distribuciones dadas", ["x"] + list(d.columns), tabla, grafico),
        bloque("a) Condiciones: P(x) ≥ 0 y Σ P(x) = 1", ["Distribución", "Todas P(x) ≥ 0", "Σ P(x)",
                                                          "¿Es distribución?"], analisis,
               notas=["D2: 1/12 + 4·(1/6) + 3/12 = 1/12 + 8/12 + 3/12 = 1.",
                      "D3: P(1) = 0 está permitido (suceso imposible); 0 + 4/6 + 2/6 = 1.",
                      "Las tres cumplen los axiomas, por lo tanto las tres son distribuciones de probabilidad."]),
        bloque_resolucion(filas, subtitulo="b) Sucesos con D1"),
    ]
