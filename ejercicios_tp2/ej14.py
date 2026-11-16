from fractions import Fraction as F

from probabilidad import bloque_bayes, bloque_resolucion, fila, total

TITULO = "Ejercicio 14 – Bayes (urnas y monedas)"
ENUNCIADO = ("Urna I: un cajón con moneda de oro y otro con moneda de plata. Urna II: oro en ambos cajones. "
             "Se elige una urna al azar y luego un cajón al azar; la moneda es de oro. "
             "¿Probabilidad de que provenga de la urna II?")


def resolver():
    tabla, p_o = total([F(1, 2), F(1, 2)], [F(1, 2), F(1)])
    tabla.index = ["Urna I", "Urna II"]
    p_ii_o = tabla.loc["Urna II", "P(Hi)·P(E/Hi)"] / p_o
    filas = [
        fila("P(O) = P(I)·P(O/I) + P(II)·P(O/II)", "(1/2)(1/2) + (1/2)(1) = 1/4 + 1/2", p_o),
        fila("P(II/O) = P(II)·P(O/II) / P(O)", "(1/2) / (3/4)", p_ii_o),
    ]
    return [bloque_bayes(tabla, "Urna (Hi)"),
            bloque_resolucion(filas, notas=["O: la moneda encontrada es de oro (en la tabla, E = O)."])]
