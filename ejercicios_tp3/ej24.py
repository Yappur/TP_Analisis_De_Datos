from distribuciones import (bloque_comparacion, bloque_resolucion, binomial, fila, num, poisson, prob)

TITULO = "Ejercicio 24 – Binomial: media, varianza y P(X = 0) (diodos)"
ENUNCIADO = ("Un tablero tiene 200 diodos y la probabilidad de que falle alguno es 0,03. a) Número promedio de "
             "fallas. b) Varianza. c) El tablero funciona si no tiene diodos defectuosos: probabilidad de que funcione.")
N, PROB = 200, 0.03


def resolver():
    b, p = binomial(N, PROB), poisson(N * PROB, 20)
    p0 = prob(b, b["x"] == 0)
    filas = [
        fila("a) μ = n·p", "200 · 0,03", N * PROB, porcentaje=False),
        fila("b) σ² = n·p·q", "200 · 0,03 · 0,97", N * PROB * (1 - PROB), porcentaje=False),
        fila("c) P(X = 0) = 0,97²⁰⁰", "C(200,0)·0,03⁰·0,97²⁰⁰", p0),
    ]
    comparacion = [["c) P(X = 0)", "0,97²⁰⁰  vs  e^(−6)", num(p0), num(prob(p, p["x"] == 0))]]
    return [bloque_resolucion(filas, notas=["X: diodos que fallan ~ B(200; 0,03)."]),
            bloque_comparacion(comparacion, N, PROB, notas=[
                "El resultado de c) se informa con la binomial exacta; la aproximación de Poisson con λ = 6 "
                "da un valor muy cercano."])]
