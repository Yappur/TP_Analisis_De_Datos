from distribuciones import (bloque_comparacion, bloque_distribucion, bloque_resolucion, binomial, fila,
                            num, poisson, prob)

TITULO = "Ejercicio 23 – Aproximación de Poisson, media y varianza (declaraciones de impuestos)"
ENUNCIADO = ("Una persona de cada 1000 comete un error numérico en su declaración de impuestos. Se examinan 10000 "
             "formas al azar. Probabilidad de que 6, 7 u 8 formas contengan un error. Calcular la media y la varianza.")
N, PROB = 10000, 1 / 1000


def resolver():
    lam = N * PROB
    b, p = binomial(N, PROB, x_max=30), poisson(lam, 22)
    en_rango = lambda t: (t["x"] >= 6) & (t["x"] <= 8)
    filas = [
        fila("λ = n·p = 10000 · 0,001", "", lam, porcentaje=False),
        fila("P(6 ≤ X ≤ 8) ≈ P(6) + P(7) + P(8)", "e^(−10)·(10⁶/6! + 10⁷/7! + 10⁸/8!)", prob(p, en_rango(p))),
        fila("Media: μ = n·p = λ", "10000 · 0,001", lam, porcentaje=False),
        fila("Varianza (Poisson): σ² = λ", "10", lam, porcentaje=False),
        fila("Varianza (binomial exacta): σ² = n·p·q", "10000 · 0,001 · 0,999", N * PROB * (1 - PROB),
             porcentaje=False),
    ]
    comparacion = [["P(6 ≤ X ≤ 8)", "P(6) + P(7) + P(8)", num(prob(b, en_rango(b))), num(prob(p, en_rango(p)))]]
    return [bloque_resolucion(filas, notas=["En Poisson la media y la varianza son iguales (λ = 10); "
                                            "la binomial exacta da 9,99, casi lo mismo."]),
            bloque_comparacion(comparacion, N, PROB),
            bloque_distribucion("X ≈ Poisson(λ = 10)", p, {"6 ≤ x ≤ 8": en_rango(p)})]
