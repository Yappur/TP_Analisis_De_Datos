import pandas as pd
from estadistica import barras, bloque, r
from distribuciones import bloque_resolucion, fila

TITULO = "Ejercicio 1 – FMP válida (loot boxes)"
ENUNCIADO = ("Sistema de recompensas de un RPG: ID 101 Común (0,60), ID 202 Raro (0,25), ID 303 Épico (0,12) "
             "e ID 404 Legendario. a) Determinar la probabilidad del ítem Legendario para que la función "
             "sea una FMP válida.")

ITEMS = pd.DataFrame({
    "ID": [101, 202, 303, 404],
    "Rareza": ["Común", "Raro", "Épico", "Legendario"],
    "Ítem": ["Cortaplumas viejo", "Espada de acero", "Grimorio antiguo", "Reliquia de dragón"],
    "P(X = x)": [0.60, 0.25, 0.12, None],
})


def resolver():
    t = ITEMS.copy()
    conocidas = t["P(X = x)"].sum()
    legendario = 1 - conocidas
    t.loc[t["ID"] == 404, "P(X = x)"] = legendario

    filas = [[int(i), rz, it, r(p, 6)] for i, rz, it, p in t.values]
    filas.append(["Σ", "", "", r(t["P(X = x)"].sum(), 6)])
    grafico = barras(t["Rareza"], {"P(X = x)": [r(p, 6) for p in t["P(X = x)"]]})
    grafico["eje"] = "Probabilidad"
    return [
        bloque("FMP de los ítems", ["ID (x)", "Rareza", "Ítem", "P(X = x)"], filas, grafico),
        bloque_resolucion([
            fila("Condición: Σ P(X = x) = 1", "0,60 + 0,25 + 0,12 + P(404) = 1", 1),
            fila("a) P(X = 404) = 1 − (0,60 + 0,25 + 0,12)", f"1 − {r(conocidas, 6):g}", legendario),
        ], notas=["Además todas las probabilidades son ≥ 0, entonces la FMP es válida con P(Legendario) = 0,03."]),
    ]
