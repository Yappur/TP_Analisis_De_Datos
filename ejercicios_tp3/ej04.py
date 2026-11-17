from fractions import Fraction as Fr

import pandas as pd
from estadistica import bloque
from distribuciones import bloque_resolucion, fila, texto

TITULO = "Ejercicio 4 – Verificar una función de probabilidad"
ENUNCIADO = ("Verificar si f(x) = (x + 2)/25 para x = 1, 2, 3, 4, 5 puede ser función de probabilidad. "
             "Calcular: a) P(X > 1)  b) P(X < 5)  c) P(X ≤ 3)  d) P(1 ≤ X ≤ 4).")


def resolver():
    t = pd.DataFrame({"x": range(1, 6)})
    t["f(x)"] = [Fr(x + 2, 25) for x in t["x"]]
    x, f = t["x"], t["f(x)"]

    incisos = {"a": x > 1, "b": x < 5, "c": x <= 3, "d": (x >= 1) & (x <= 4)}
    filas_tabla = [[int(xi), f"({xi} + 2)/25", texto(fi)] + ["✓" if m.iloc[i] else "" for m in incisos.values()]
                   for i, (xi, fi) in enumerate(zip(x, f))]
    filas_tabla.append(["Σ", "", texto(f.sum()), "", "", "", ""])

    def p(m):
        return f[m].sum()

    filas = [
        fila("Condiciones: f(x) ≥ 0 y Σ f(x) = 1", "(3 + 4 + 5 + 6 + 7)/25 = 25/25", f.sum(), porcentaje=False),
        fila("a) P(X > 1) = 1 − f(1)", f"1 − 3/25 = {p(incisos['a'])}", p(incisos["a"])),
        fila("b) P(X < 5) = 1 − f(5)", f"1 − 7/25 = {p(incisos['b'])}", p(incisos["b"])),
        fila("c) P(X ≤ 3) = f(1) + f(2) + f(3)", f"(3 + 4 + 5)/25 = {p(incisos['c'])}", p(incisos["c"])),
        fila("d) P(1 ≤ X ≤ 4) = f(1) + … + f(4)", f"(3 + 4 + 5 + 6)/25 = {p(incisos['d'])}", p(incisos["d"])),
    ]
    return [bloque("Función de probabilidad", ["x", "f(x)", "Valor", "a", "b", "c", "d"], filas_tabla,
                   notas=["Todas las f(x) son positivas y suman 1: SÍ es función de probabilidad.",
                          "✓ = valores de x que se suman en ese inciso."]),
            bloque_resolucion(filas)]
