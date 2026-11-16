from estadistica import bloque
from probabilidad import conjunto, dado

TITULO = "Ejercicio 3 – Complementarios y mutuamente excluyentes"
ENUNCIADO = ("Indicar si son verdaderas o falsas y justificar: a) si dos sucesos son complementarios, "
             "entonces son mutuamente excluyentes; b) si dos sucesos son mutuamente excluyentes, "
             "entonces son complementarios.")


def resolver():
    S = dado()["x"]
    A, B = S == 1, S == 2  # contraejemplo para b)
    par = S % 2 == 0
    filas = [
        ["a) VERDADERA",
         "A y A' cumplen A ∩ A' = ∅ (y además A ∪ A' = S)",
         f"Ej. dado: A = par = {conjunto(S[par])}, A' = {conjunto(S[~par])}, A ∩ A' = {conjunto(S[par & ~par])}",
         "Todo par complementario es excluyente"],
        ["b) FALSA",
         "Excluyentes solo exige A ∩ B = ∅; complementarios exige además A ∪ B = S",
         f"Contraejemplo dado: A = {conjunto(S[A])}, B = {conjunto(S[B])}: A ∩ B = {conjunto(S[A & B])} "
         f"pero A ∪ B = {conjunto(S[A | B])} ≠ S",
         "Excluyentes no implica complementarios"],
    ]
    return [bloque("Resolución", ["Proposición", "Justificación", "Ejemplo", "Conclusión"], filas)]
