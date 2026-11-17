from distribuciones import bloque_distribucion, bloque_resolucion, binomial, fila, prob

TITULO = "Ejercicio 8 – Binomial (fallas en llamadas a una API)"
ENUNCIADO = ("Cada petición a una API de pagos falla con probabilidad 0,15, de forma independiente. Se envía un lote "
             "de 8 peticiones. Probabilidad exacta de que: a) no falle ninguna; b) fallen exactamente 2; "
             "c) el lote falle por completo porque ocurren más de 5 fallas.")
N, PROB = 8, 0.15


def resolver():
    t = binomial(N, PROB)
    x = t["x"]
    marcas = {"a) = 0": x == 0, "b) = 2": x == 2, "c) > 5": x > 5}
    filas = [
        fila("a) P(X = 0) = C(8,0)·0,15⁰·0,85⁸", "0,85⁸", prob(t, marcas["a) = 0"])),
        fila("b) P(X = 2) = C(8,2)·0,15²·0,85⁶", "28 · 0,0225 · 0,85⁶", prob(t, marcas["b) = 2"])),
        fila("c) P(X > 5) = P(6) + P(7) + P(8)", "28·0,15⁶·0,85² + 8·0,15⁷·0,85 + 0,15⁸",
             prob(t, marcas["c) > 5"])),
    ]
    return [bloque_distribucion("X ~ B(n = 8, p = 0,15): número de peticiones fallidas", t, marcas),
            bloque_resolucion(filas, notas=[
                "Binomial: n = 8 ensayos independientes, éxito = «la petición falla», p = 0,15 constante.",
                "«Más de 5» no incluye el 5: x = 6, 7, 8."])]
