import pandas as pd
from probabilidad import bloque_resolucion, bloque_tabla, con_totales, fila

TITULO = "Ejercicio 9 – Tabla de probabilidades conjuntas"
ENUNCIADO = ("Clientes de un almacén clasificados por sexo y residencia (proporciones). Se elige un adulto: "
             "a) que resida en los suburbios; b) que sea mujer y viva en la ciudad; c) que sea hombre.")

TABLA = pd.DataFrame({"Masculino": [0.17, 0.04], "Femenino": [0.67, 0.12]},
                     index=["Suburbios", "Ciudad"])


def resolver():
    t = con_totales(TABLA)
    filas = [
        fila("a) P(Suburbios) = P(Sub ∩ M) + P(Sub ∩ F)", "0.17 + 0.67", t.loc["Suburbios", "Total"]),
        fila("b) P(F ∩ Ciudad)", "Celda Ciudad – Femenino", t.loc["Ciudad", "Femenino"]),
        fila("c) P(M) = P(M ∩ Sub) + P(M ∩ Ciudad)", "0.17 + 0.04", t.loc["Total", "Masculino"]),
    ]
    return [bloque_tabla("Tabla con totales marginales", t, "Residencia", 2,
                         notas=["La suma de todas las celdas es 1 (es una distribución de probabilidad)."]),
            bloque_resolucion(filas)]
