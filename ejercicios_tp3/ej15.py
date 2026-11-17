from distribuciones import bloque_distribucion, bloque_resolucion, fila, poisson, prob

TITULO = "Ejercicio 15 – Poisson (tráfico de un API Gateway)"
ENUNCIADO = ("En horas pico el servidor recibe en promedio 4,5 peticiones HTTP por segundo y procesa como máximo 7 "
             "por segundo. Probabilidad exacta de que en un segundo ocurran: a) exactamente 4 peticiones; "
             "b) ninguna petición; c) más de 7 peticiones (saturación). Se escala si P(X > 7) supera el 5%.")
LAMBDA = 4.5


def resolver():
    t = poisson(LAMBDA, 14)
    x = t["x"]
    marcas = {"a) = 4": x == 4, "b) = 0": x == 0, "c) > 7": x > 7}
    p_hasta_7 = prob(t, x <= 7)
    p_sat = 1 - p_hasta_7
    filas = [
        fila("a) P(X = 4) = e^(−4,5)·4,5⁴ / 4!", "0,011109 · 410,0625 / 24", prob(t, marcas["a) = 4"])),
        fila("b) P(X = 0) = e^(−4,5)", "e^(−4,5)·4,5⁰ / 0!", prob(t, marcas["b) = 0"])),
        fila("   P(X ≤ 7) = Σ x=0..7 e^(−4,5)·4,5^x / x!", "probabilidad acumulada", p_hasta_7),
        fila("c) P(X > 7) = 1 − P(X ≤ 7)", f"1 − {p_hasta_7:.6f}", p_sat),
    ]
    decision = "SÍ se debe levantar el contenedor clon" if p_sat > 0.05 else "NO hace falta escalar"
    return [bloque_distribucion("X ~ Poisson(λ = 4,5 peticiones/segundo)", t, marcas,
                                notas=["La tabla se corta en x = 14; P(X > 7) se calcula por complemento, "
                                       "porque X puede tomar infinitos valores."]),
            bloque_resolucion(filas, notas=[
                f"P(X > 7) = {p_sat * 100:.2f}% > 5% → {decision} (Auto-scaling)."])]
