from fractions import Fraction as F

from probabilidad import bloque_bayes, bloque_resolucion, fila, total

TITULO = "Ejercicio 12 – Probabilidad total y Bayes (sucursales)"
ENUNCIADO = ("Un artículo proviene de las sucursales A (30%), B (50%) y C (20%). La probabilidad de que sea "
             "defectuoso es 0,10 si proviene de A, 0,30 si proviene de B y 0,25 si proviene de C. "
             "a) Probabilidad de que un artículo al azar sea defectuoso. "
             "b) Si es defectuoso, probabilidad de que provenga de la sucursal B.")


def resolver():
    tabla, p_d = total([F("0.3"), F("0.5"), F("0.2")], [F("0.10"), F("0.30"), F("0.25")])
    tabla.index = ["A", "B", "C"]
    p_b_d = tabla.loc["B", "P(Hi)·P(E/Hi)"] / p_d
    filas = [
        fila("a) P(D) = Σ P(Hi)·P(D/Hi)", "0.3·0.10 + 0.5·0.30 + 0.2·0.25 = 0.03 + 0.15 + 0.05", p_d),
        fila("b) P(B/D) = P(B)·P(D/B) / P(D)", "0.15 / 0.23", p_b_d),
    ]
    return [bloque_bayes(tabla, "Sucursal (Hi)", decimal=True),
            bloque_resolucion(filas, notas=["D: el artículo es defectuoso (en la tabla, E = D)."])]
