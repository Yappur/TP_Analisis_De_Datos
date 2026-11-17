from distribuciones import bloque_distribucion, bloque_resolucion, binomial, fila, prob

TITULO = "Ejercicio 13 – Binomial (filtro de spam)"
ENUNCIADO = ("Un filtro bayesiano detecta correos basura con precisión del 80%. Entran 10 correos que son "
             "efectivamente spam. Probabilidad de que el script filtre menos de 7 correos no deseados.")
N, PROB = 10, 0.8


def resolver():
    t = binomial(N, PROB)
    x = t["x"]
    marcas = {"< 7": x < 7}
    filas = [fila("P(X < 7) = P(X ≤ 6) = 1 − [P(7) + P(8) + P(9) + P(10)]",
                  "Σ x=0..6 C(10,x)·0,8^x·0,2^(10−x)", prob(t, marcas["< 7"]))]
    return [bloque_distribucion("X ~ B(n = 10, p = 0,8): correos spam filtrados", t, marcas),
            bloque_resolucion(filas, notas=["«Menos de 7» no incluye el 7: x = 0, …, 6."])]
