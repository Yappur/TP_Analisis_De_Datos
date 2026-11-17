from distribuciones import (bloque_comparacion, bloque_distribucion, bloque_resolucion, binomial, fila,
                            num, poisson, prob)

TITULO = "Ejercicio 21 – Aproximación de Poisson a la binomial (accidentes)"
ENUNCIADO = ("La probabilidad de un accidente en cualquier día es 0,005 y los accidentes son independientes. "
             "En un período de 400 días: a) probabilidad de que ocurra un accidente en un día (exactamente 1 día con "
             "accidente); b) probabilidad de que ocurra un accidente a lo sumo en tres días.")
N, PROB = 400, 0.005


def resolver():
    lam = N * PROB
    b, p = binomial(N, PROB), poisson(lam, 10)
    xb, xp = b["x"], p["x"]
    filas = [
        fila("λ = n·p = 400 · 0,005", "n grande y p chico", lam, porcentaje=False),
        fila("a) P(X = 1) ≈ e^(−2)·2¹ / 1!", "2·e^(−2)", prob(p, xp == 1)),
        fila("b) P(X ≤ 3) ≈ e^(−2)·(1 + 2 + 2 + 4/3)", "P(0) + P(1) + P(2) + P(3)", prob(p, xp <= 3)),
    ]
    comparacion = [
        ["a) P(X = 1)", "400·0,005·0,995³⁹⁹  vs  2·e^(−2)", num(prob(b, xb == 1)), num(prob(p, xp == 1))],
        ["b) P(X ≤ 3)", "Σ x=0..3", num(prob(b, xb <= 3)), num(prob(p, xp <= 3))],
    ]
    return [bloque_resolucion(filas, notas=["X: días con accidente en 400 días ~ B(400; 0,005) ≈ Poisson(λ = 2)."]),
            bloque_comparacion(comparacion, N, PROB),
            bloque_distribucion("X ≈ Poisson(λ = 2)", p, {"a) = 1": xp == 1, "b) ≤ 3": xp <= 3})]
