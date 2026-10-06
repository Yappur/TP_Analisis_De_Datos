import pandas as pd
from estadistica import resolver_agrupado

TITULO = "Ejercicio 7"
ENUNCIADO = ("Minutos de espera del autobús en 30 días laborales. "
             "Distribución de frecuencias con h = 4, Pearson y Bowley.")
DATOS = [10, 0, 13, 3, 9, 8, 11, 10, 9, 8, 6, 12, 1, 13, 10,
         7, 17, 16, 5, 10, 2, 10, 3, 8, 6, 17, 2, 10, 12, 11]
H = 4


def resolver():
    s = pd.Series(DATOS)
    inicios = [0, 4, 8, 12, 16]  # clases [0,4), [4,8), [8,12), [12,16), [16,20)
    tabla = pd.DataFrame({"li": inicios})
    tabla["etiqueta"] = [f"[{a},{a + H})" for a in inicios]
    tabla["f"] = [((s >= a) & (s < a + H)).sum() for a in inicios]
    tabla["marca"] = tabla["li"] + H / 2
    return resolver_agrupado(tabla, h=H, poblacion=False)  # 30 días: muestra
