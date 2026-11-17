from distribuciones import bloque_distribucion, bloque_resolucion, fila, poisson, prob

TITULO = "Ejercicio 16 – Poisson (accidentes de tránsito)"
ENUNCIADO = ("En promedio ocurren tres accidentes por mes en una intersección. Probabilidad de que en un mes "
             "dado: a) ocurran exactamente cinco; b) ocurran menos de tres; c) ocurran al menos dos.")
LAMBDA = 3


def resolver():
    t = poisson(LAMBDA, 12)
    x = t["x"]
    marcas = {"a) = 5": x == 5, "b) < 3": x < 3, "c) ≥ 2": x >= 2}
    p01 = prob(t, x <= 1)
    filas = [
        fila("a) P(X = 5) = e^(−3)·3⁵ / 5!", "0,049787 · 243 / 120", prob(t, marcas["a) = 5"])),
        fila("b) P(X < 3) = P(0) + P(1) + P(2)", "e^(−3)·(1 + 3 + 9/2)", prob(t, marcas["b) < 3"])),
        fila("c) P(X ≥ 2) = 1 − [P(0) + P(1)]", f"1 − e^(−3)·(1 + 3) = 1 − {p01:.6f}", 1 - p01),
    ]
    return [bloque_distribucion("X ~ Poisson(λ = 3 accidentes/mes)", t, marcas,
                                notas=["c) se calcula por complemento (la tabla se corta en x = 12)."]),
            bloque_resolucion(filas)]
