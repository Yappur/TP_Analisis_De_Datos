from itertools import product

import pandas as pd
from probabilidad import bloque_resolucion, fila, laplace, texto_laplace

TITULO = "Ejercicio 7 – Dos dados y condicional"
ENUNCIADO = ("Un jugador tira dos dados, uno rojo y otro negro. a) Probabilidad de que la suma sea siete. "
             "b) Probabilidad de que la suma haya sido siete dado que en el dado rojo salió un dos.")


def resolver():
    S = pd.DataFrame(product(range(1, 7), repeat=2), columns=["rojo", "negro"])
    siete = S["rojo"] + S["negro"] == 7
    rojo2 = S["rojo"] == 2
    p_cond = laplace(siete & rojo2) / laplace(rojo2)

    filas = [
        fila("a) P(suma = 7) = casos favorables / 36", f"{texto_laplace(siete)}  "
             "{(1,6), (2,5), (3,4), (4,3), (5,2), (6,1)}", laplace(siete)),
        fila("b) P(7 / R=2) = P(7 ∩ R=2) / P(R=2)", f"(1/36) / (6/36)  → solo (2,5)", p_cond),
    ]
    return [bloque_resolucion(filas, notas=[
        "#S = 6 · 6 = 36 pares (rojo, negro) equiprobables.",
        "Como P(7 / R=2) = P(7) = 1/6, los sucesos «suma 7» y «rojo = 2» son independientes."])]
