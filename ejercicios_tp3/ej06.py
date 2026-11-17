import pandas as pd
from distribuciones import P, bloque_distribucion, bloque_resolucion, fila, prob

TITULO = "Ejercicio 6 – Constante k y probabilidades (peticiones fallidas)"
ENUNCIADO = ("X: peticiones fallidas por minuto en un microservicio de autenticación, con P(X=0)=0,45; "
             "P(X=1)=0,30; P(X=2)=0,15; P(X=3)=k; P(X=4)=0,03. a) Encontrar k para que sea una FMP legítima. "
             "b) Probabilidad de que en un minuto: exactamente 2 fallidas; menos de 3; al menos 2.")


def resolver():
    t = pd.DataFrame({"x": range(5), P: [0.45, 0.30, 0.15, None, 0.03]})
    k = 1 - t[P].sum()
    t.loc[t["x"] == 3, P] = k
    t["P(X ≤ x)"] = t[P].cumsum()
    x = t["x"]
    marcas = {"= 2": x == 2, "< 3": x < 3, "≥ 2": x >= 2}

    filas = [
        fila("a) k = 1 − (0,45 + 0,30 + 0,15 + 0,03)", "1 − 0,93", k),
        fila("b1) P(X = 2) (exactamente)", "f(2)", prob(t, marcas["= 2"])),
        fila("b2) P(X < 3) = P(X ≤ 2) (menos de 3)", "0,45 + 0,30 + 0,15", prob(t, marcas["< 3"])),
        fila("b3) P(X ≥ 2) (al menos 2)", "0,15 + k + 0,03 = 0,15 + 0,07 + 0,03", prob(t, marcas["≥ 2"])),
    ]
    return [bloque_distribucion("FMP con k = 0,07", t, marcas,
                                notas=["«Menos de 3» no incluye el 3; «al menos 2» sí incluye el 2."]),
            bloque_resolucion(filas)]
