from estadistica import resolver_simple

TITULO = "Ejercicio 3"
ENUNCIADO = "Cantidad de errores cada 10 horas de programación de 30 estudiantes. Calcular cuartil 2, decil 50 y percentil 50 (los tres coinciden con la mediana)."
DATOS = [22, 20, 23, 21, 24, 22, 21, 26, 28, 27, 20, 21, 24, 28, 23, 21, 26, 25, 23, 20, 25, 24, 21, 23, 25, 21, 24, 23, 26, 20]


def resolver():
    return resolver_simple(DATOS, poblacion=True, percentiles=(50,), continuo=False)
