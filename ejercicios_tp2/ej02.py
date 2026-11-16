import pandas as pd
from estadistica import bloque
from probabilidad import conjunto

TITULO = "Ejercicio 2 – Sucesos y operaciones"
ENUNCIADO = ("Se lanza una moneda y un dado. A: «cara en la moneda»; B: «número impar en el dado». "
             "Enumerar: a) A  b) A ∩ B  c) B'  d) (A ∩ B)'  e) A' ∩ B  f) A − B.")


def resolver():
    S = pd.DataFrame([(m, d) for m in ["C", "X"] for d in range(1, 7)], columns=["moneda", "dado"])
    S["elemento"] = S["moneda"] + S["dado"].astype(str)
    A = S["moneda"] == "C"
    B = S["dado"] % 2 == 1

    def fila(inciso, definicion, mascara):
        elementos = S.loc[mascara, "elemento"]
        return [inciso, definicion, conjunto(elementos), len(elementos)]

    filas = [
        fila("a) A", "cara", A),
        fila("b) A ∩ B", "cara e impar", A & B),
        fila("c) B'", "no impar (par)", ~B),
        fila("d) (A ∩ B)'", "todo S menos A ∩ B", ~(A & B)),
        fila("e) A' ∩ B", "ceca e impar", ~A & B),
        fila("f) A − B", "cara y no impar = A ∩ B'", A & ~B),
    ]
    return [bloque(f"S = {conjunto(S['elemento'])}  (#S = {len(S)})",
                   ["Suceso", "Significado", "Elementos", "Cantidad"], filas,
                   notas=["C = cara, X = ceca. Los sucesos se obtienen filtrando S con pandas."])]
