from distribuciones import bloque_distribucion, bloque_resolucion, binomial, fila, prob

TITULO = "Ejercicio 9 – Binomial (campaña telefónica)"
ENUNCIADO = ("Una de cada 20 personas que reciben la llamada se une al club. Si en un día 25 personas reciben la "
             "llamada, ¿cuál es la probabilidad de que por lo menos dos de ellas se inscriban?")
N, PROB = 25, 1 / 20


def resolver():
    t = binomial(N, PROB)
    x = t["x"]
    marcas = {"≥ 2": x >= 2}
    p0, p1 = prob(t, x == 0), prob(t, x == 1)
    filas = [
        fila("P(X = 0) = 0,95²⁵", "C(25,0)·0,05⁰·0,95²⁵", p0),
        fila("P(X = 1) = C(25,1)·0,05·0,95²⁴", "25 · 0,05 · 0,95²⁴", p1),
        fila("P(X ≥ 2) = 1 − [P(0) + P(1)]", f"1 − ({p0:.6f} + {p1:.6f})", prob(t, marcas["≥ 2"])),
    ]
    return [bloque_distribucion("X ~ B(n = 25, p = 0,05): personas que se inscriben", t, marcas),
            bloque_resolucion(filas, notas=["«Por lo menos dos» = X ≥ 2; se usa el complemento."])]
