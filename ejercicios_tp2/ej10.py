from fractions import Fraction

import pandas as pd
from probabilidad import bloque_resolucion, bloque_tabla, con_totales, fila

TITULO = "Ejercicio 10 – Pedidos por línea y género"
ENUNCIADO = ("Encuesta de 1000 pedidos por línea de productos (1 cara, 2 barata) y género. Se elige un pedido: "
             "a) P(A), A: el consumidor es mujer; b) P(B), B: el pedido es de la línea 1; "
             "c) P(línea 1 y mujer); d) P(línea 1 / mujer); e) ¿A y B son independientes?")

TABLA = pd.DataFrame({"Línea 1": [132, 516], "Línea 2": [147, 205]}, index=["Masculino", "Femenino"])


def resolver():
    t = con_totales(TABLA)
    n = int(t.loc["Total", "Total"])
    pA = Fraction(int(t.loc["Femenino", "Total"]), n)
    pB = Fraction(int(t.loc["Total", "Línea 1"]), n)
    pAB = Fraction(int(t.loc["Femenino", "Línea 1"]), n)

    filas = [
        fila("a) P(A) = mujeres / total", f"{t.loc['Femenino', 'Total']} / {n}", pA),
        fila("b) P(B) = línea 1 / total", f"{t.loc['Total', 'Línea 1']} / {n}", pB),
        fila("c) P(A ∩ B)", f"{t.loc['Femenino', 'Línea 1']} / {n}", pAB),
        fila("d) P(B/A) = P(A ∩ B) / P(A)", f"0.516 / 0.721 = 516 / 721", pAB / pA),
        fila("e) P(A) · P(B)", "0.721 · 0.648", pA * pB),
        fila("   P(A ∩ B)", "0.516", pAB),
    ]
    return [bloque_tabla("Tabla de frecuencias con totales", t, "Sexo", 0),
            bloque_resolucion(filas, notas=[
                f"e) P(A ∩ B) = 0.516 ≠ P(A)·P(B) = {float(pA * pB):.4f} → A y B NO son independientes "
                f"(también P(B/A) ≈ {float(pAB / pA):.4f} ≠ P(B) = 0.648)."])]
