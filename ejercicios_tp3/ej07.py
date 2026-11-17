import pandas as pd
from distribuciones import P, bloque_distribucion, bloque_resolucion, bloque_tabla, fila, momentos, prob

TITULO = "Ejercicio 7 – Probabilidades, esperanza y varianza (errores en código)"
ENUNCIADO = ("X: número de errores en un módulo de código, con f(0)=0,46; f(1)=0,32; f(2)=0,16; f(3)=0,05; "
             "f(4)=0,01. a) P(X < 3)  b) P(1 < X < 4)  c) P(X > 2)  d) Valor esperado del número de errores. "
             "e) Varianza y desviación estándar.")

X = [0, 1, 2, 3, 4]
FX = [0.46, 0.32, 0.16, 0.05, 0.01]


def resolver():
    t = pd.DataFrame({"x": X, P: FX})
    t["P(X ≤ x)"] = t[P].cumsum()
    x = t["x"]
    marcas = {"a) < 3": x < 3, "b) 1 < x < 4": (x > 1) & (x < 4), "c) > 2": x > 2}
    m, e, v, s = momentos(X, FX)
    e2 = m["x²·f(x)"].sum()

    filas = [
        fila("a) P(X < 3) = f(0) + f(1) + f(2)", "0,46 + 0,32 + 0,16", prob(t, marcas["a) < 3"])),
        fila("b) P(1 < X < 4) = f(2) + f(3)", "0,16 + 0,05", prob(t, marcas["b) 1 < x < 4"])),
        fila("c) P(X > 2) = f(3) + f(4)", "0,05 + 0,01", prob(t, marcas["c) > 2"])),
        fila("d) E(X) = Σ x·f(x)", "0·0,46 + 1·0,32 + 2·0,16 + 3·0,05 + 4·0,01", e, porcentaje=False),
        fila("e) V(X) = E(X²) − [E(X)]²", f"{e2:.2f} − {e:.2f}²", v, porcentaje=False),
        fila("   σ = √V(X)", f"√{v:.4f}", s, porcentaje=False),
    ]
    return [bloque_distribucion("Distribución de X", t, marcas),
            bloque_tabla("Tabla de cálculo de E(X) y V(X)", m),
            bloque_resolucion(filas, notas=["En b) las desigualdades son estrictas: no se incluyen x = 1 ni x = 4."])]
