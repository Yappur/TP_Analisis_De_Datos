from estadistica import resolver_simple

TITULO = "Ejercicio 6"
ENUNCIADO = "Cantidad de materias aprobadas por 40 estudiantes de abogacía. Percentil 95, cuartil 3 y tipo de asimetría."
DATOS = [0, 5, 4, 2, 6, 3, 4, 5, 1, 3, 4, 6, 5, 3, 2, 4, 5, 6, 3, 1, 2, 5, 3, 6, 4, 5, 2, 3, 4, 6, 5, 3, 2, 4, 5, 0, 6, 4, 2, 5]


def resolver():
    return resolver_simple(DATOS, poblacion=True, percentiles=(95, 75), continuo=False)
