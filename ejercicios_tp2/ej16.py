import pandas as pd
from probabilidad import bloque_resolucion, bloque_tabla, con_totales, fila

TITULO = "Ejercicio 16 – Tabla de probabilidad, condicional e independencia"
ENUNCIADO = ("Encuesta a 1000 adultos sobre la carga del préstamo universitario (A: muy alta, B: adecuada, "
             "C: muy baja) y si tienen un hijo en la universidad (D) o no (D'). Se elige una persona: "
             "a) P(D); b) P(A); c) P(A ∩ D); d) P(A/D); e) P(D/A); f) ¿D y A son independientes?")

TABLA = pd.DataFrame({"Muy alta (A)": [0.35, 0.25], "Adecuada (B)": [0.08, 0.20], "Muy baja (C)": [0.01, 0.11]},
                     index=["Con hijo (D)", "Sin hijo (D')"])


def resolver():
    t = con_totales(TABLA)
    pD, pA = t.loc["Con hijo (D)", "Total"], t.loc["Total", "Muy alta (A)"]
    pAD = t.loc["Con hijo (D)", "Muy alta (A)"]
    filas = [
        fila("a) P(D)", "0.35 + 0.08 + 0.01", pD),
        fila("b) P(A)", "0.35 + 0.25", pA),
        fila("c) P(A ∩ D)", "Celda D – A", pAD),
        fila("d) P(A/D) = P(A ∩ D) / P(D)", "0.35 / 0.44", pAD / pD),
        fila("e) P(D/A) = P(A ∩ D) / P(A)", "0.35 / 0.60", pAD / pA),
        fila("f) P(D) · P(A)", "0.44 · 0.60", pD * pA),
    ]
    return [bloque_tabla("Tabla de probabilidad con marginales", t, "Encuestado", 2),
            bloque_resolucion(filas, notas=[
                f"f) P(A ∩ D) = 0.35 ≠ P(A)·P(D) = {pD * pA:.3f} → D y A NO son independientes: "
                f"tener un hijo en la universidad cambia la opinión (P(A/D) ≈ {pAD / pD:.4f} ≠ P(A) = 0.60)."])]
