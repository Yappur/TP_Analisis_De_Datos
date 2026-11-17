from math import sqrt

from distribuciones import bloque_distribucion, bloque_resolucion, binomial, fila, prob

TITULO = "Ejercicio 12 – Binomial, esperanza y varianza (tests en CI/CD)"
ENUNCIADO = ("Una suite de 15 tests independientes; cada test pasa con probabilidad 0,90 (0,10 de falso negativo). "
             "a) Si se requiere que pasen al menos 14 de los 15, probabilidad de aprobación automática. "
             "b) Valor esperado. c) Varianza y desviación estándar.")
N, PROB = 15, 0.9


def resolver():
    t = binomial(N, PROB)
    x = t["x"]
    marcas = {"a) ≥ 14": x >= 14}
    pa = prob(t, marcas["a) ≥ 14"])
    e, v = N * PROB, N * PROB * (1 - PROB)
    filas = [
        fila("a) P(X ≥ 14) = P(14) + P(15)", "15·0,9¹⁴·0,1 + 0,9¹⁵", pa),
        fila("b) E(X) = n·p", "15 · 0,9", e, porcentaje=False),
        fila("c) V(X) = n·p·q", "15 · 0,9 · 0,1", v, porcentaje=False),
        fila("   σ = √(n·p·q)", f"√{v:.2f}", sqrt(v), porcentaje=False),
    ]
    aprob = [
        fila("E(A) = p_A", "aprobación como ensayo de Bernoulli", pa, porcentaje=False),
        fila("V(A) = p_A·(1 − p_A)", f"{pa:.6f} · {1 - pa:.6f}", pa * (1 - pa), porcentaje=False),
        fila("σ = √V(A)", "", sqrt(pa * (1 - pa)), porcentaje=False),
    ]
    return [bloque_distribucion("X ~ B(n = 15, p = 0,9): tests que pasan", t, marcas),
            bloque_resolucion(filas, notas=[
                "b) y c) se calculan sobre X (tests que pasan): en promedio pasan 13,5 tests de 15."]),
            bloque_resolucion(aprob, subtitulo="Complemento: aprobación A ~ Bernoulli(p = P(X ≥ 14))", notas=[
                "Si «valor esperado de que el código sea aprobado» se lee como la variable A = 1 (aprobado) / 0 "
                "(rechazado), su esperanza es la probabilidad del inciso a)."])]
