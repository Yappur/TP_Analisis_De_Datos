import pandas as pd
from estadistica import bloque
from probabilidad import baraja

TITULO = "Ejercicio 1 – Espacio muestral"
ENUNCIADO = ("Determinar un espacio muestral para cada experimento: a) extraer una carta de una baraja de 52; "
             "b) contar los artículos defectuosos en un lote de 500; c) lanzar 2 veces una moneda; "
             "d) lanzar una moneda y un dado; e) medir el tiempo entre dos llegadas sucesivas a una cola.")


def resolver():
    cartas = baraja()
    moneda = ["C", "X"]  # C = cara, X = ceca
    dos_monedas = pd.MultiIndex.from_product([moneda, moneda]).map("".join)
    moneda_dado = pd.MultiIndex.from_product([moneda, range(1, 7)]).map(lambda t: f"{t[0]}{t[1]}")
    defectuosos = pd.RangeIndex(0, 501)

    filas = [
        ["a) Una carta", "S = {(v, p) / v ∈ {A, 2, …, 10, J, Q, K}, p ∈ {♠, ♥, ♦, ♣}}",
         "Finito", len(cartas)],
        ["b) Defectuosos en 500", "S = {0, 1, 2, …, 500}", "Finito (discreto)", len(defectuosos)],
        ["c) Dos monedas", "S = {" + ", ".join(dos_monedas) + "}", "Finito", len(dos_monedas)],
        ["d) Moneda y dado", "S = {" + ", ".join(moneda_dado) + "}", "Finito", len(moneda_dado)],
        ["e) Tiempo entre llegadas", "S = {t ∈ ℝ / t ≥ 0} = [0, +∞)", "Infinito no numerable (continuo)", "∞"],
    ]
    return [bloque("Espacios muestrales", ["Experimento", "Espacio muestral S", "Tipo", "#S"], filas,
                   notas=["C = cara, X = ceca.",
                          "a) #S = 13 valores × 4 palos = 52 (se generan con pandas).",
                          "e) El tiempo es una variable continua: S no se puede enumerar."])]
