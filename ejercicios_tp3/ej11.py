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
        fila("P(X ≥ 3), hipergeométrica exacta",
             "Σ[k=3..5] C(200,k)·C(300,5−k) / C(500,5)", hiper),
        fila("Aprox. binomial: P(X ≥ 3)",
             "10·0,4³·0,6² + 5·0,4⁴·0,6 + 0,4⁵", p),
    ]
    return [bloque_distribucion("Aproximación binomial: X ~ B(n = 5, p = 0,4)", t, marcas),
            bloque_resolucion(filas, notas=[
                "La muestra es sin reposición: el resultado principal es hipergeométrico exacto.",
                f"La aproximación binomial da {p:.6f}; la hipergeométrica exacta, {hiper:.6f}."])]
