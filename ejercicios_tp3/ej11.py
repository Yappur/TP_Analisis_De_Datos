from math import comb

from distribuciones import bloque_distribucion, bloque_resolucion, binomial, fila, prob

TITULO = "Ejercicio 11 – Binomial (billetes de lotería)"
ENUNCIADO = ("De 500 billetes de lotería, 200 le dan al comprador al menos el costo del billete. Si usted compra "
             "5 billetes, calcule la probabilidad de ganar al menos el costo de 3 billetes.")
N, GANADORES, TOTAL = 5, 200, 500
PROB = GANADORES / TOTAL


def resolver():
    t = binomial(N, PROB)
    x = t["x"]
    marcas = {"≥ 3": x >= 3}
    p = prob(t, marcas["≥ 3"])
    hiper = sum(comb(GANADORES, k) * comb(TOTAL - GANADORES, N - k) for k in range(3, 6)) / comb(TOTAL, N)
    filas = [
        fila("p = 200 / 500", "probabilidad de que un billete gane", PROB),
        fila("P(X ≥ 3) = P(3) + P(4) + P(5)", "10·0,4³·0,6² + 5·0,4⁴·0,6 + 0,4⁵", p),
    ]
    return [bloque_distribucion("X ~ B(n = 5, p = 0,4): billetes que ganan al menos su costo", t, marcas),
            bloque_resolucion(filas, notas=[
                "Se usa la binomial porque se compran 5 de 500 billetes (5/500 = 1% < 5%): extraer sin reposición "
                "casi no cambia p.",
                f"Control con la hipergeométrica exacta: {hiper:.6f} (diferencia {abs(hiper - p):.4f})."])]
