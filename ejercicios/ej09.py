import pandas as pd
from estadistica import resolver_agrupado

TITULO = "Ejercicio 9"
ENUNCIADO = ("Niños atendidos en un hospital infantil, por edad (el PDF no indica qué calcular; "
             "se asumen las mismas medidas que en el ejercicio 7). La clase '12 y más' tiene "
             "115 personas cuya suma de edades es 1725, por lo que su marca es 1725/115 = 15.")

INTERPRETACION_INTERVALOS = (
    "[0, 3) = de 0 a menos de 3 años; "
    "[3, 6) = de 3 a menos de 6 años; "
    "[6, 9) = de 6 a menos de 9 años; "
    "[9, 12) = de 9 a menos de 12 años; "
    "12 y más = 12 años o más."
)

NOTA_CLASE_ABIERTA = (
    "En la clase abierta existen 115 personas cuya suma de las edades es 1725, "
    "con un promedio de 15 años por persona."
)


def resolver():
    tabla = pd.DataFrame({
        "etiqueta": ["[0,3)", "[3,6)", "[6,9)", "[9,12)", "12 y más"],
        "li": [0, 3, 6, 9, 12],
        "f": [5080, 4551, 3000, 955, 115],
        "marca": [1.5, 4.5, 7.5, 10.5, 1725 / 115],
    })
    bloques = resolver_agrupado(tabla, h=3, poblacion=True)
    bloques[0]["notas"].extend([INTERPRETACION_INTERVALOS, NOTA_CLASE_ABIERTA])
    return bloques
