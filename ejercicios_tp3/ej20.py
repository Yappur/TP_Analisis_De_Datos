from distribuciones import bloque_distribucion, bloque_resolucion, fila, poisson, prob

TITULO = "Ejercicio 20 – Poisson (intentos de login fallidos)"
ENUNCIADO = ("El servidor registra una media de 1,2 intentos fallidos de inicio de sesión por hora. Probabilidad de "
             "que en una hora normal ocurran más de 3 intentos fallidos.")
LAMBDA = 1.2


def resolver():
    t = poisson(LAMBDA, 8)
    x = t["x"]
    marcas = {"> 3": x > 3}
    p3 = prob(t, x <= 3)
    filas = [
        fila("P(X ≤ 3) = e^(−1,2)·(1 + 1,2 + 1,2²/2 + 1,2³/6)", "e^(−1,2) · 3,208", p3),
        fila("P(X > 3) = 1 − P(X ≤ 3)", f"1 − {p3:.6f}", 1 - p3),
    ]
    return [bloque_distribucion("X ~ Poisson(λ = 1,2 intentos/hora)", t, marcas),
            bloque_resolucion(filas, notas=["«Más de 3» no incluye el 3: x = 4, 5, …"])]
