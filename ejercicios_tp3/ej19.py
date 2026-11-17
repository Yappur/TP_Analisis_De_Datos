from distribuciones import bloque_distribucion, bloque_resolucion, fila, poisson, prob

TITULO = "Ejercicio 19 – Poisson (errores por página)"
ENUNCIADO = ("Una secretaria comete dos errores por página, en promedio. Probabilidad de que en la siguiente "
             "página cometa: a) cuatro o más errores; b) ningún error.")
LAMBDA = 2


def resolver():
    t = poisson(LAMBDA, 10)
    x = t["x"]
    marcas = {"a) ≥ 4": x >= 4, "b) = 0": x == 0}
    p3 = prob(t, x <= 3)
    filas = [
        fila("   P(X ≤ 3) = e^(−2)·(1 + 2 + 2 + 4/3)", "P(0) + P(1) + P(2) + P(3)", p3),
        fila("a) P(X ≥ 4) = 1 − P(X ≤ 3)", f"1 − {p3:.6f}", 1 - p3),
        fila("b) P(X = 0) = e^(−2)", "e^(−2)·2⁰ / 0!", prob(t, marcas["b) = 0"])),
    ]
    return [bloque_distribucion("X ~ Poisson(λ = 2 errores/página)", t, marcas,
                                notas=["«Cuatro o más» = X ≥ 4, por complemento."]),
            bloque_resolucion(filas)]
