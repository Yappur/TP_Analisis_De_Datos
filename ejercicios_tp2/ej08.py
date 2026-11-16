from fractions import Fraction as F

from estadistica import bloque
from probabilidad import fraccion

TITULO = "Ejercicio 8 – Independencia y exclusión (diagrama)"
ENUNCIADO = ("Tres eventos A, B y C según el diagrama (B y C se cortan con A, pero no entre sí). "
             "Datos: P(A) = 1/4, P(B) = 1/2, P(C) = 1/6, P(A ∩ C) = 1/12, P(A ∩ B) = 1/8. "
             "Verdadero o falso: a) A y B son mutuamente excluyentes; b) A y B son independientes; "
             "c) A, B y C son independientes; d) A es independiente de C; e) A es independiente de B.")

P = {"A": F(1, 4), "B": F(1, 2), "C": F(1, 6), "A∩C": F(1, 12), "A∩B": F(1, 8), "B∩C": F(0)}


def resolver():
    def indep(x, y):
        return P[f"{x}∩{y}"] == P[x] * P[y]

    filas = [
        ["a) A ∩ B = ∅ ?", f"P(A ∩ B) = {fraccion(P['A∩B'])} ≠ 0", "FALSO",
         "Tienen intersección, no son excluyentes"],
        ["b) P(A ∩ B) = P(A)·P(B) ?", f"{fraccion(P['A∩B'])} vs (1/4)·(1/2) = {fraccion(P['A'] * P['B'])}",
         "VERDADERO" if indep("A", "B") else "FALSO", "Se cumple la igualdad"],
        ["c) A, B, C independientes ?",
         f"P(B ∩ C) = 0 ≠ (1/2)·(1/6) = {fraccion(P['B'] * P['C'])}; "
         f"P(A ∩ C) = 1/12 ≠ {fraccion(P['A'] * P['C'])}",
         "FALSO", "Falla la independencia de a pares (y la triple: P(A∩B∩C) = 0 ≠ 1/48)"],
        ["d) P(A ∩ C) = P(A)·P(C) ?", f"1/12 vs (1/4)·(1/6) = {fraccion(P['A'] * P['C'])}",
         "VERDADERO" if indep("A", "C") else "FALSO", "1/12 ≠ 1/24"],
        ["e) P(A ∩ B) = P(A)·P(B) ?", "1/8 = (1/4)·(1/2) = 1/8",
         "VERDADERO" if indep("A", "B") else "FALSO", "Mismo análisis que b)"],
    ]
    return [bloque("Resolución", ["Afirmación", "Cálculo", "Respuesta", "Justificación"], filas,
                   notas=["Del diagrama: B y C no se superponen, entonces P(B ∩ C) = 0 y P(A ∩ B ∩ C) = 0.",
                          "Independencia: P(X ∩ Y) = P(X)·P(Y). Exclusión: P(X ∩ Y) = 0."])]
