from fractions import Fraction
from itertools import permutations

import pandas as pd
from estadistica import bloque
from probabilidad import bloque_resolucion, fila, laplace

TITULO = "Ejercicio 17 – Independencia (clasificación de cafés)"
ENUNCIADO = ("Un juez clasifica al azar tres marcas de café X, Y, Z. A: prefiere X a Y; B: X es la mejor; "
             "C: X es la segunda; D: X es la tercera. ¿El evento A es independiente de B, C y D?")


def resolver():
    S = pd.DataFrame(permutations("XYZ"), columns=["1°", "2°", "3°"])
    posicion = S.apply(lambda f: {marca: i for i, marca in enumerate(f, start=1)}, axis=1)
    pos_x, pos_y = posicion.map(lambda p: p["X"]), posicion.map(lambda p: p["Y"])

    A = pos_x < pos_y
    eventos = {"B": pos_x == 1, "C": pos_x == 2, "D": pos_x == 3}

    espacio = [[" > ".join(f), "✓" if a else "", *("✓" if e[i] else "" for e in eventos.values())]
               for i, (f, a) in enumerate(zip(S.values, A))]

    pA = laplace(A)
    filas = [fila("P(A)", "3 / 6", pA)]
    conclusiones = []
    for nombre, E in eventos.items():
        pE, pAE = laplace(E), laplace(A & E)
        filas += [fila(f"P({nombre})", f"{int(E.sum())} / 6", pE),
                  fila(f"P(A ∩ {nombre}) vs P(A)·P({nombre})", f"{pAE}  vs  {pA}·{pE} = {pA * pE}", pAE)]
        conclusiones.append(f"A y {nombre}: {'independientes' if pAE == pA * pE else 'NO independientes'} "
                            f"({pAE} {'=' if pAE == pA * pE else '≠'} {pA * pE}).")
    assert Fraction(1, 2) == pA
    return [bloque("Espacio muestral: 3! = 6 clasificaciones equiprobables",
                   ["Clasificación", "A", "B", "C", "D"], espacio),
            bloque_resolucion(filas, notas=conclusiones + [
                "Conclusión: A es independiente de C, pero no de B ni de D."])]
