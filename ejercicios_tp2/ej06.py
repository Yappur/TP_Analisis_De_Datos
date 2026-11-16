from estadistica import bloque
from probabilidad import bloque_resolucion, conjunto, dado, fila, laplace

TITULO = "Ejercicio 6 – Probabilidad condicional en un dado"
ENUNCIADO = ("Se tira un dado. A: «número menor que 4»; B: «número menor o igual que 2»; "
             "C: «número mayor que 3». a) P(A/B)  b) P(B/A)  c) P(A/C)  d) P(B/C)  "
             "e) ¿Son A y B independientes? Justificar.")


def condicional(evento, dado_que):
    """P(E/F) = P(E ∩ F) / P(F)"""
    return laplace(evento & dado_que) / laplace(dado_que)


def resolver():
    S = dado()["x"]
    A, B, C = S < 4, S <= 2, S > 3
    pA, pB, pAB = laplace(A), laplace(B), laplace(A & B)

    datos = [
        ["S", "Espacio muestral", conjunto(S), "1"],
        ["A", "x < 4", conjunto(S[A]), str(pA)],
        ["B", "x ≤ 2", conjunto(S[B]), str(pB)],
        ["C", "x > 3", conjunto(S[C]), str(laplace(C))],
    ]
    filas = [
        fila("a) P(A/B) = P(A ∩ B) / P(B)", f"({laplace(A & B)}) / ({pB})", condicional(A, B)),
        fila("b) P(B/A) = P(A ∩ B) / P(A)", f"({pAB}) / ({pA})", condicional(B, A)),
        fila("c) P(A/C) = P(A ∩ C) / P(C)", f"A ∩ C = ∅ → 0 / ({laplace(C)})", condicional(A, C)),
        fila("d) P(B/C) = P(B ∩ C) / P(C)", f"B ∩ C = ∅ → 0 / ({laplace(C)})", condicional(B, C)),
        fila("e) P(A) · P(B)", f"({pA}) · ({pB})", pA * pB),
        fila("   P(A ∩ B)", f"A ∩ B = {conjunto(S[A & B])}", pAB),
    ]
    return [
        bloque("Sucesos", ["Suceso", "Condición", "Elementos", "P"], datos),
        bloque_resolucion(filas, notas=[
            f"e) P(A ∩ B) = {pAB} ≠ P(A)·P(B) = {pA * pB} → A y B NO son independientes "
            f"(además P(A/B) = 1 ≠ P(A) = {pA}). B ⊂ A: si ocurre B, ocurre A seguro."]),
    ]
