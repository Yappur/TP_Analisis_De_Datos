from estadistica import resolver_simple

TITULO = "Ejercicio 1"
ENUNCIADO = "Cantidad de veces que ingresaron a Instagram en un día (20 alumnos). Calcular P10 y P90."
DATOS = [2, 1, 0, 3, 1, 2, 4, 0, 1, 2, 3, 1, 0, 2, 1, 3, 2, 0, 1, 2]


def resolver():
    return resolver_simple(DATOS, poblacion=True, percentiles=(10, 90), continuo=False)
