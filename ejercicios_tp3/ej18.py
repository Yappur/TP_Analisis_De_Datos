from distribuciones import bloque_distribucion, bloque_resolucion, fila, poisson, prob

TITULO = "Ejercicio 18 – Poisson con cambio de intervalo (cola de mensajes)"
ENUNCIADO = ("Ingresan en promedio λ = 12 mensajes de pago por minuto a una cola. a) Tasa promedio esperada en 30 "
             "segundos. b) Tasa promedio en 10 segundos. c) Con el intervalo de 10 segundos, probabilidad de recibir "
             "exactamente 2 mensajes y de recibir al menos 1 mensaje.")
LAMBDA_MINUTO = 12


def resolver():
    l30 = LAMBDA_MINUTO * 30 / 60
    l10 = LAMBDA_MINUTO * 10 / 60
    t = poisson(l10, 10)
    x = t["x"]
    marcas = {"= 2": x == 2, "≥ 1": x >= 1}
    p0 = prob(t, x == 0)
    filas = [
        fila("a) λ₃₀ = 12 · (30/60)", "12 mensajes/min · 0,5 min", l30, porcentaje=False),
        fila("b) λ₁₀ = 12 · (10/60)", "12 mensajes/min · 1/6 min", l10, porcentaje=False),
        fila("c1) P(X = 2) = e^(−2)·2² / 2!", "2·e^(−2)", prob(t, marcas["= 2"])),
        fila("c2) P(X ≥ 1) = 1 − P(X = 0)", f"1 − e^(−2) = 1 − {p0:.6f}", 1 - p0),
    ]
    return [bloque_resolucion(filas, notas=["La media de Poisson es proporcional a la longitud del intervalo."]),
            bloque_distribucion("X ~ Poisson(λ = 2 mensajes cada 10 segundos)", t, marcas,
                                notas=["«Al menos 1» se calcula por complemento."])]
