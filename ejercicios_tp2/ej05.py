import pandas as pd
from probabilidad import FIGURAS, baraja, bloque_resolucion, fila, laplace, texto_laplace

TITULO = "Ejercicio 5 – Dos cartas sucesivas"
ENUNCIADO = ("Se extraen 2 cartas sucesivamente de una baraja de 52. Expresar el espacio muestral, su cantidad "
             "de elementos y hallar la probabilidad de que: a) la primera no sea un diez de trébol o un as; "
             "b) la primera sea un as, pero la segunda no; c) al menos una sea diamante; "
             "d) no sean del mismo palo; e) la segunda no sea una figura.")


def resolver():
    cartas = baraja()
    # Espacio muestral: pares ordenados (1ª, 2ª) de cartas distintas (sin reposición) -> 52 · 51
    S = cartas.merge(cartas, how="cross", suffixes=("1", "2"))
    S = S[(S["valor1"] != S["valor2"]) | (S["palo1"] != S["palo2"])].reset_index(drop=True)

    a = ~((S["valor1"] == "A") | ((S["valor1"] == "10") & (S["palo1"] == "Tréboles")))
    b = (S["valor1"] == "A") & (S["valor2"] != "A")
    c = (S["palo1"] == "Diamantes") | (S["palo2"] == "Diamantes")
    d = S["palo1"] != S["palo2"]
    e = ~S["valor2"].isin(FIGURAS)

    filas = [
        ["#S = 52 · 51", "Pares ordenados de cartas distintas", str(len(S)), len(S)],
        fila("a) P[(10♣ ∪ As)'] = 1 − 5/52", f"1 − (1 + 4)/52 = {texto_laplace(a)}", laplace(a)),
        fila("b) P(As₁ ∩ No As₂) = (4/52)·(48/51)", texto_laplace(b), laplace(b)),
        fila("c) P(al menos un ♦) = 1 − (39/52)·(38/51)", texto_laplace(c), laplace(c)),
        fila("d) P(distinto palo) = 1 − 12/51", texto_laplace(d), laplace(d)),
        fila("e) P(2ª no figura) = 40/52", texto_laplace(e), laplace(e)),
    ]
    return [bloque_resolucion(filas, notas=[
        "S = {(c₁, c₂) / c₁, c₂ ∈ baraja, c₁ ≠ c₂}: se interpreta «sucesivamente» como sin reposición.",
        "Figuras: J, Q y K (12 cartas). El as no se considera figura.",
        "Cada probabilidad se obtiene contando con pandas los casos favorables sobre los 2652 posibles."])]
