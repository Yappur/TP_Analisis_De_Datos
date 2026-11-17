from distribuciones import bloque_distribucion, bloque_resolucion, binomial, fila, prob

TITULO = "Ejercicio 10 – Binomial (tiros libres)"
ENUNCIADO = ("Un basquetbolista encesta el 70% de los tiros libres. Si lanza 14 tiros, probabilidad de que: "
             "a) enceste cuando menos 7; b) falle entre 3 y 6 inclusive; c) falle todos; d) enceste todos.")
N, PROB = 14, 0.7


def resolver():
    t = binomial(N, PROB)  # X = cantidad de encestes
    x = t["x"]
    fallas = N - x          # Y = 14 − X = cantidad de fallas ~ B(14; 0,3)
    marcas = {"a) X ≥ 7": x >= 7, "b) 3 ≤ Y ≤ 6": (fallas >= 3) & (fallas <= 6),
              "c) Y = 14": fallas == 14, "d) X = 14": x == 14}
    tabla = t.copy()
    filas = [
        fila("a) P(X ≥ 7) = Σ x=7..14 C(14,x)·0,7^x·0,3^(14−x)", "1 − P(X ≤ 6)", prob(t, marcas["a) X ≥ 7"])),
        fila("b) P(3 ≤ Y ≤ 6) = P(8 ≤ X ≤ 11)", "Y = 14 − X ~ B(14; 0,3)", prob(t, marcas["b) 3 ≤ Y ≤ 6"])),
        fila("c) P(Y = 14) = P(X = 0) = 0,3¹⁴", "C(14,0)·0,7⁰·0,3¹⁴", prob(t, marcas["c) Y = 14"])),
        fila("d) P(X = 14) = 0,7¹⁴", "C(14,14)·0,7¹⁴·0,3⁰", prob(t, marcas["d) X = 14"])),
    ]
    bl = bloque_distribucion("X ~ B(n = 14, p = 0,7): número de encestes  (Y = 14 − X: fallas)", tabla, marcas)
    bl["columnas"].insert(1, "Fallas Y")
    for f, y in zip(bl["filas"], fallas):
        f.insert(1, int(y))
    return [bl, bloque_resolucion(filas, notas=[
        "«Cuando menos 7» = X ≥ 7. «Entre 3 y 6 inclusive» incluye ambos extremos.",
        "c) es prácticamente imposible: 0,3¹⁴ ≈ 4,8 · 10⁻⁸."])]
