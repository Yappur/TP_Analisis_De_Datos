from fractions import Fraction as F

from probabilidad import bloque_bayes, bloque_resolucion, fila, total

TITULO = "Ejercicio 13 – Bayes (cheques con fecha adelantada)"
ENUNCIADO = ("Los clientes con fondos suficientes firman cheques con fecha adelantada por error una vez cada mil; "
             "los que tienen fondos insuficientes siempre lo hacen, y son el 1% del total. Un cajero recibe un "
             "cheque con fecha adelantada: ¿probabilidad de que provenga de un cliente con dinero insuficiente?")


def resolver():
    tabla, p_f = total([F("0.99"), F("0.01")], [F(1, 1000), F(1)])
    tabla.index = ["S: suficiente", "I: insuficiente"]
    p_i_f = tabla.loc["I: insuficiente", "P(Hi)·P(E/Hi)"] / p_f
    filas = [
        fila("P(F) = P(S)·P(F/S) + P(I)·P(F/I)", "0.99 · 0.001 + 0.01 · 1 = 0.00099 + 0.01", p_f),
        fila("P(I/F) = P(I)·P(F/I) / P(F)", "0.01 / 0.01099", p_i_f),
    ]
    return [bloque_bayes(tabla, "Cliente (Hi)", decimal=True),
            bloque_resolucion(filas, notas=[
                "F: el cheque tiene fecha adelantada (en la tabla, E = F).",
                f"Aunque solo el 1% tiene fondos insuficientes, ante un cheque adelantado la probabilidad "
                f"sube a ≈ {float(p_i_f) * 100:.2f}%."])]
