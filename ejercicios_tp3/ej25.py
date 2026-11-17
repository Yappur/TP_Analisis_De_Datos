from distribuciones import P, bloque_resolucion, bloque_tabla, fila, geometrica

TITULO = "Ejercicio 25 – Geométrica: costo esperado de un experimento"
ENUNCIADO = ("Cada experimento cuesta $1000. Si falla, hay un costo adicional de $300 antes de intentar de nuevo. "
             "La probabilidad de éxito en cada ensayo es 0,2, los ensayos son independientes y se repiten hasta el "
             "primer éxito. ¿Cuál es el costo esperado del procedimiento completo?")
PROB, COSTO, ADICIONAL = 0.2, 1000, 300


def resolver():
    e_x = 1 / PROB
    costo_esperado = (COSTO + ADICIONAL) * e_x - ADICIONAL

    # Verificación numérica con pandas: Σ C(x)·P(X = x) (la cola después de x = 200 es despreciable)
    t = geometrica(PROB, 200)
    t["C(x) = 1300x − 300"] = (COSTO + ADICIONAL) * t["x"] - ADICIONAL
    t["C(x)·P(X = x)"] = t["C(x) = 1300x − 300"] * t[P]
    verificacion = t["C(x)·P(X = x)"].sum()
    assert abs(verificacion - costo_esperado) < 1e-6

    filas = [
        fila("X ~ Geométrica(p = 0,2): ensayos hasta el 1.er éxito", "P(X = x) = 0,8^(x−1)·0,2", PROB),
        fila("E(X) = 1 / p", "1 / 0,2", e_x, porcentaje=False),
        ["C(X) = 1000·X + 300·(X − 1) = 1300·X − 300", "X ensayos pagados y X − 1 fracasos con costo extra",
         "—", "—"],
        fila("E[C(X)] = 1300·E(X) − 300", "1300 · 5 − 300", costo_esperado, porcentaje=False),
        fila("Verificación: Σ C(x)·P(X = x)", "suma con pandas, x = 1..200", verificacion, porcentaje=False),
    ]
    vista = t.head(10)[["x", P, "C(x) = 1300x − 300", "C(x)·P(X = x)"]]
    return [bloque_resolucion(filas, notas=[f"Costo esperado del procedimiento completo: ${costo_esperado:.0f}."]),
            bloque_tabla("Primeros valores de la distribución geométrica", vista, totales=False,
                         notas=["La distribución sigue para x = 11, 12, …; en la verificación se suman hasta x = 200."])]
