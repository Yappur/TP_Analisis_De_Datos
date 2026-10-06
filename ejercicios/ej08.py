from estadistica import resolver_simple

TITULO = "Ejercicio 8"
ENUNCIADO = "Tiempos de CPU (segundos) de 30 trabajos tomados al azar (muestra). Percentil 15, cuartil 1, coeficiente de variación y tipo de asimetría."
DATOS = [1.17, 1.23, 0.15, 0.19, 0.92, 1.61, 3.76, 2.41, 0.82, 0.75, 1.16, 1.94, 0.71, 0.47, 2.59, 1.38, 0.96, 0.02, 2.16, 3.07, 3.53, 4.75, 1.59, 2.01, 1.40, 0.55, 0.18, 3.20, 1.15, 4.58]


def resolver():
    return resolver_simple(DATOS, poblacion=False, percentiles=(15, 25), continuo=True)
