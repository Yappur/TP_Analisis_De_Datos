from distribuciones import bloque_distribucion, bloque_resolucion, binomial, fila, prob

TITULO = "Ejercicio 14 – Binomial (chips defectuosos)"
ENUNCIADO = ("La probabilidad de falla de cualquier chip es 0,10. En una muestra aleatoria de 20 chips, "
             "probabilidad de que: a) a lo sumo fallen 3; b) por lo menos fallen 2; c) ningún chip venga fallado.")
N, PROB = 20, 0.1


def resolver():
    t = binomial(N, PROB)
    x = t["x"]
    marcas = {"a) ≤ 3": x <= 3, "b) ≥ 2": x >= 2, "c) = 0": x == 0}
    filas = [
        fila("a) P(X ≤ 3) = P(0) + P(1) + P(2) + P(3)", "Σ x=0..3 C(20,x)·0,1^x·0,9^(20−x)", prob(t, marcas["a) ≤ 3"])),
        fila("b) P(X ≥ 2) = 1 − [P(0) + P(1)]", "1 − (0,9²⁰ + 20·0,1·0,9¹⁹)", prob(t, marcas["b) ≥ 2"])),
        fila("c) P(X = 0) = 0,9²⁰", "C(20,0)·0,1⁰·0,9²⁰", prob(t, marcas["c) = 0"])),
    ]
    return [bloque_distribucion("X ~ B(n = 20, p = 0,1): chips que fallan", t, marcas),
            bloque_resolucion(filas, notas=["«A lo sumo 3» incluye el 3; «por lo menos 2» incluye el 2."])]
