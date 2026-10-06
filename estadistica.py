"""Funciones comunes del TP 1.
Cada ejercicio las usa y devuelve una lista de "bloques" (tabla + gráfico + notas)
que la API entrega como JSON y el frontend dibuja.
"""
import pandas as pd


def r(x, decimales=4):
    """Redondea y convierte a float normal (para que sea JSON)."""
    return round(float(x), decimales)


def bloque(subtitulo, columnas, filas, grafico=None, notas=()):
    return {"subtitulo": subtitulo, "columnas": columnas, "filas": filas,
            "grafico": grafico, "notas": list(notas)}


def barras(etiquetas, series):
    """series = {"nombre": [valores]} -> datos para un gráfico de barras."""
    return {"etiquetas": [str(e) for e in etiquetas],
            "series": [{"nombre": n, "valores": [float(v) for v in vs]}
                       for n, vs in series.items()]}


def percentil(datos, p):
    """Percentil con el criterio del TP: posición = p*n/100.
    Si es entera -> promedio de ese dato y el siguiente. Si no -> el dato siguiente."""
    x = pd.Series(datos).sort_values().reset_index(drop=True)
    n = len(x)
    pos = p * n // 100
    if (p * n) % 100 == 0:
        return x.iloc[pos - 1: pos + 1].mean()
    return x.iloc[pos]


def tipo_asimetria(valor):
    if valor > 0.05:
        return "positiva (cola a la derecha)"
    if valor < -0.05:
        return "negativa (cola a la izquierda)"
    return "aproximadamente simétrica"


def pearson_bowley(media, moda, mediana, desvio, q1, q2, q3):
    # Con una sola moda: (media - moda) / desvío. Sin moda única: 3*(media - mediana) / desvío
    pearson = (media - moda) / desvio if moda is not None else 3 * (media - mediana) / desvio
    bowley = (q3 + q1 - 2 * q2) / (q3 - q1) if q3 != q1 else 0
    return pearson, bowley


def interpretar(pearson, bowley):
    return [f"Pearson = {r(pearson, 3)}: asimetría {tipo_asimetria(pearson)}",
            f"Bowley = {r(bowley, 3)}: asimetría {tipo_asimetria(bowley)}"]


# ------------------------------------------------------------
# Datos sin agrupar
# ------------------------------------------------------------
def resolver_simple(datos, poblacion=True, percentiles=(), continuo=False):
    s = pd.Series(datos, dtype=float)
    ddof = 0 if poblacion else 1  # 0 = divide por N, 1 = divide por N-1

    media, mediana = s.mean(), s.median()
    desvio = s.std(ddof=ddof)
    q1, q2, q3 = percentil(s, 25), percentil(s, 50), percentil(s, 75)

    frec = s.value_counts()
    modas = sorted(frec[frec == frec.max()].index) if frec.max() > 1 else []
    pearson, bowley = pearson_bowley(media, modas[0] if len(modas) == 1 else None,
                                     mediana, desvio, q1, q2, q3)

    filas = [
        ["Media", r(media)],
        ["Mediana", r(mediana)],
        ["Moda", ", ".join(f"{m:g}" for m in modas) if modas else "No hay"],
        ["Rango", r(s.max() - s.min())],
        ["Varianza", r(desvio ** 2)],
        ["Desvío estándar", r(desvio)],
        ["Coeficiente de variación (%)", r(desvio / media * 100, 2)],
        ["Q1", r(q1)], ["Q2", r(q2)], ["Q3", r(q3)],
        ["Pearson", r(pearson, 3)], ["Bowley", r(bowley, 3)],
    ] + [[f"P{p}", r(percentil(s, p))] for p in percentiles]

    # Gráfico: barras por valor (discreta) o histograma por intervalos (continua)
    if continuo:
        conteo = pd.cut(s, bins=6).value_counts(sort=False)
        etiquetas = [f"{i.left:.2f} a {i.right:.2f}" for i in conteo.index]
    else:
        conteo = s.value_counts().sort_index()
        etiquetas = [f"{v:g}" for v in conteo.index]

    titulo = f"Medidas ({'población' if poblacion else 'muestra'}, n = {len(s)})"
    return [bloque(titulo, ["Medida", "Valor"], filas,
                   barras(etiquetas, {"Frecuencia": conteo.values}),
                   interpretar(pearson, bowley))]


# ------------------------------------------------------------
# Datos agrupados con clase
# ------------------------------------------------------------
def resolver_agrupado(tabla, h, poblacion=True):
    """tabla: DataFrame con columnas etiqueta, li (límite inferior), f y marca."""
    t = tabla.copy()
    N = int(t["f"].sum())
    t["F"] = t["f"].cumsum()  # frecuencia acumulada
    ddof = 0 if poblacion else 1

    media = (t["marca"] * t["f"]).sum() / N
    varianza = (t["f"] * (t["marca"] - media) ** 2).sum() / (N - ddof)
    desvio = varianza ** 0.5

    def cuantil(q):
        # L + (q*N - F anterior) / f de la clase * h
        pos = q * N
        i = (t["F"] >= pos).idxmax()
        return t["li"][i] + (pos - (t["F"][i] - t["f"][i])) / t["f"][i] * h

    q1, mediana, q3 = cuantil(0.25), cuantil(0.50), cuantil(0.75)

    # Moda: L + d1 / (d1 + d2) * h
    i = t["f"].idxmax()
    d1 = t["f"][i] - (t["f"][i - 1] if i > 0 else 0)
    d2 = t["f"][i] - (t["f"][i + 1] if i < len(t) - 1 else 0)
    moda = t["li"][i] + d1 / (d1 + d2) * h

    pearson, bowley = pearson_bowley(media, moda, mediana, desvio, q1, mediana, q3)

    filas_tabla = [[e, int(f), r(m, 2), int(F)]
                   for e, f, m, F in zip(t["etiqueta"], t["f"], t["marca"], t["F"])]
    filas = [["Media", r(media, 3)], ["Mediana", r(mediana, 3)], ["Moda", r(moda, 3)],
             ["Varianza", r(varianza, 3)], ["Desvío estándar", r(desvio, 3)],
             ["Coeficiente de variación (%)", r(desvio / media * 100, 2)],
             ["Q1", r(q1, 3)], ["Q3", r(q3, 3)],
             ["Pearson", r(pearson, 3)], ["Bowley", r(bowley, 3)]]

    return [
        bloque("Distribución de frecuencias", ["Clase", "f", "Marca", "F"], filas_tabla,
               barras(t["etiqueta"], {"Frecuencia": t["f"]})),
        bloque(f"Medidas ({'población' if poblacion else 'muestra'}, N = {N})",
               ["Medida", "Valor"], filas, None, interpretar(pearson, bowley)),
    ]
