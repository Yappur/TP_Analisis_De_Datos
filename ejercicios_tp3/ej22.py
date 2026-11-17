from distribuciones import (bloque_comparacion, bloque_distribucion, bloque_resolucion, binomial, fila,
                            num, poisson, prob)

TITULO = "Ejercicio 22 – Aproximación de Poisson (artículos con burbujas)"
ENUNCIADO = ("En promedio 1 de cada 1000 artículos de vidrio tiene una o más burbujas. Probabilidad de que una "
             "muestra aleatoria de 8000 tenga menos de 7 artículos con burbujas.")
N, PROB = 8000, 1 / 1000


def resolver():
    lam = N * PROB
    b, p = binomial(N, PROB, x_max=30), poisson(lam, 20)
    filas = [
        fila("λ = n·p = 8000 · 0,001", "", lam, porcentaje=False),
        fila("P(X < 7) = P(X ≤ 6) ≈ Σ x=0..6 e^(−8)·8^x / x!", "Poisson acumulada hasta 6", prob(p, p["x"] < 7)),
    ]
    comparacion = [["P(X < 7)", "Σ x=0..6", num(prob(b, b["x"] < 7)), num(prob(p, p["x"] < 7))]]
    return [bloque_resolucion(filas, notas=["«Menos de 7» no incluye el 7."]),
            bloque_comparacion(comparacion, N, PROB),
            bloque_distribucion("X ≈ Poisson(λ = 8)", p, {"< 7": p["x"] < 7})]
