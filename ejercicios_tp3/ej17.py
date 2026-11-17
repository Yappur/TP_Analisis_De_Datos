from math import exp

from distribuciones import bloque_distribucion, bloque_resolucion, fila, poisson, prob

TITULO = "Ejercicio 17 – Poisson (ataques de virus)"
ENUNCIADO = ("El sistema de cómputo de una universidad fue atacado por virus a una tasa promedio de 0,4 por semana. "
             "Suponiendo Poisson, probabilidad de no ser atacada durante la semana siguiente.")
LAMBDA = 0.4


def resolver():
    t = poisson(LAMBDA, 5)
    marcas = {"= 0": t["x"] == 0}
    p0 = prob(t, marcas["= 0"])
    assert abs(p0 - exp(-LAMBDA)) < 1e-15
    return [bloque_distribucion("X ~ Poisson(λ = 0,4 virus/semana)", t, marcas),
            bloque_resolucion([fila("P(X = 0) = e^(−0,4)·0,4⁰ / 0!", "e^(−0,4)", p0)])]
