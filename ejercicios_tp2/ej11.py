from fractions import Fraction as F

from probabilidad import bloque_bayes, bloque_resolucion, fila, total

TITULO = "Ejercicio 11 – Probabilidad total (despertador)"
ENUNCIADO = ("Un despertador suena a la hora deseada con probabilidad 0,7. Si suena, la probabilidad de que la "
             "persona se despierte es 0,8; si no suena, la probabilidad de que se despierte a tiempo es 0,30. "
             "¿Cuál es la probabilidad de que llegue a tiempo al trabajo?")


def resolver():
    tabla, p_t = total([F("0.7"), F("0.3")], [F("0.8"), F("0.3")])
    tabla.index = ["S: suena", "S': no suena"]
    filas = [fila("P(T) = P(S)·P(T/S) + P(S')·P(T/S')", "0.7 · 0.8 + 0.3 · 0.3 = 0.56 + 0.09", p_t)]
    return [bloque_bayes(tabla, "Hipótesis", decimal=True, bayes=False),
            bloque_resolucion(filas, notas=[
                "T: llega a tiempo. Se considera que despertarse a tiempo equivale a llegar a tiempo.",
                "S y S' forman una partición: P(S') = 1 − 0,7 = 0,3."])]
