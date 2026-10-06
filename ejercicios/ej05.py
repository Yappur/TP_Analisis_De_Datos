from estadistica import resolver_simple

TITULO = "Ejercicio 5"
ENUNCIADO = "Cantidad de libros leídos por 50 personas en la feria del libro. Pearson, Bowley, centil 80 (P80) y cuartil 1 (P25)."
DATOS = [2, 4, 1, 3, 8, 9, 8, 1, 5, 7, 2, 6, 2, 3, 2, 7, 4, 5, 2, 3, 9, 4, 2, 3, 5, 1, 2, 4, 0, 3, 2, 1, 6, 3, 4, 2, 1, 5, 3, 2, 4, 1, 6, 3, 2, 6, 1, 4, 5, 3]


def resolver():
    return resolver_simple(DATOS, poblacion=True, percentiles=(80, 25), continuo=False)
