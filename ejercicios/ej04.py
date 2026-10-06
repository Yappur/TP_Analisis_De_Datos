from estadistica import resolver_simple

TITULO = "Ejercicio 4"
ENUNCIADO = "Cantidad de errores en la carga de datos de 40 operadores. Pearson, Bowley, decil 60 (P60) y cuartil 3 (P75)."
DATOS = [4, 3, 5, 6, 1, 5, 0, 3, 2, 4, 3, 5, 3, 2, 4, 3, 1, 2, 3, 1, 0, 3, 2, 4, 0, 4, 5, 2, 0, 2, 5, 0, 4, 2, 3, 0, 5, 4, 2, 3]


def resolver():
    return resolver_simple(DATOS, poblacion=True, percentiles=(60, 75), continuo=False)
