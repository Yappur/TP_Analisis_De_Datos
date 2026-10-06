from estadistica import resolver_simple

TITULO = "Ejercicio 2"
ENUNCIADO = "Cantidad de me gusta de 30 videos de programación en sus primeras 100 visualizaciones. Calcular el decil 40 (P40)."
DATOS = [8, 7, 3, 1, 2, 1, 4, 7, 6, 1, 3, 2, 5, 5, 3, 8, 1, 4, 2, 0, 3, 1, 2, 3, 1, 2, 4, 0, 2, 1]


def resolver():
    return resolver_simple(DATOS, poblacion=True, percentiles=(40,), continuo=False)
