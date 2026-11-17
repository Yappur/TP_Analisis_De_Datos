"""Funciones comunes del TP 3 (variable aleatoria discreta, binomial, Poisson y geométrica).
Igual que en los TP anteriores, cada ejercicio devuelve una lista de "bloques" (ver estadistica.bloque).
Las probabilidades se calculan con la precisión completa de Python y se redondean solo al mostrarlas.
"""
from fractions import Fraction
from math import comb, exp, factorial, sqrt

import pandas as pd

from estadistica import barras, bloque, r
from probabilidad import fraccion

DECIMALES = 6
COLUMNAS = ["Inciso / fórmula", "Cálculo", "Resultado", "Porcentaje"]
P, F = "P(X = x)", "P(X ≤ x)"


def num(v):
    """Redondeo para mostrar: 6 decimales, o 4 cifras significativas si el valor es muy chico."""
    v = float(v)
    if 0 < abs(v) < 0.001:
        return float(f"{v:.4g}")
    return r(v, DECIMALES)


def en_porcentaje(v):
    v = float(v) * 100
    return f"{v:.4g} %" if 0 < abs(v) < 0.01 else f"{v:.2f} %"


def texto(v):
    """Fracciones como fracción (1/12); el resto redondeado a 6 decimales."""
    if isinstance(v, Fraction):
        return fraccion(v)
    return f"{num(v):g}"


def coma(x):
    """0.005 -> '0,005' (notación de la consigna)."""
    return f"{x:g}".replace(".", ",")


def fila(planteo, calculo, valor, porcentaje=True):
    """Fila de resolución. porcentaje=False para esperanzas, varianzas, costos, etc."""
    return [planteo, calculo, num(valor), en_porcentaje(valor) if porcentaje else "—"]


def bloque_resolucion(filas, notas=(), subtitulo="Resolución"):
    return bloque(subtitulo, COLUMNAS, filas, notas=notas)


# ------------------------------------------------------------
# Distribuciones
# ------------------------------------------------------------
def binomial(n, p, x_max=None):
    """B(n, p): P(X = x) = C(n, x) · p^x · q^(n−x),  x = 0, …, n  (o hasta x_max).
    Para n chico se usa la fórmula directa; para n grande (8000, 10000) C(n, x) no entra en un float,
    así que se usa la recurrencia equivalente P(x + 1) = P(x) · (n − x)/(x + 1) · p/q."""
    x_max = n if x_max is None else min(n, x_max)
    q = 1 - p
    if n <= 1000:
        valores = [comb(n, x) * p ** x * q ** (n - x) for x in range(x_max + 1)]
    else:
        valores = [q ** n]
        for x in range(x_max):
            valores.append(valores[-1] * (n - x) / (x + 1) * p / q)
    t = pd.DataFrame({"x": range(x_max + 1), P: valores})
    t[F] = t[P].cumsum()
    return t


def poisson(lam, x_max):
    """P(λ): P(X = x) = e^(−λ) · λ^x / x!,  se tabula x = 0, …, x_max"""
    t = pd.DataFrame({"x": range(x_max + 1)})
    t[P] = [exp(-lam) * lam ** x / factorial(x) for x in t["x"]]
    t[F] = t[P].cumsum()
    return t


def geometrica(p, x_max):
    """G(p): X = n.º de ensayos hasta el primer éxito. P(X = x) = q^(x−1) · p,  x = 1, 2, …"""
    t = pd.DataFrame({"x": range(1, x_max + 1)})
    t[P] = [(1 - p) ** (x - 1) * p for x in t["x"]]
    t[F] = t[P].cumsum()
    return t


def prob(tabla, mascara):
    """Suma de P(X = x) para los x que cumplen la condición."""
    return tabla.loc[mascara, P].sum()


def bloque_distribucion(subtitulo, tabla, marcas=None, notas=()):
    """Tabla x | P(X = x) | P(X ≤ x) | columnas ✓ por inciso, con gráfico de barras."""
    marcas = marcas or {}
    columnas = ["x", P, F] + list(marcas)
    filas = [[int(x), num(p), num(f)] + ["✓" if m.iloc[i] else "" for m in marcas.values()]
             for i, (x, p, f) in enumerate(zip(tabla["x"], tabla[P], tabla[F]))]
    grafico = barras(tabla["x"], {P: [num(p) for p in tabla[P]]})
    grafico["eje"] = "Probabilidad"
    notas = list(notas) + (["✓ = valores de x que se suman en ese inciso."] if marcas else [])
    return bloque(subtitulo, columnas, filas, grafico, notas)


def bloque_comparacion(filas, n, p, notas=()):
    """Binomial exacta vs. aproximación de Poisson con λ = n·p."""
    return bloque(f"Binomial exacta vs. aproximación de Poisson (λ = n·p = {coma(r(n * p, 4))})",
                  ["Inciso / fórmula", "Cálculo", "Binomial exacta", "Poisson (λ = n·p)"], filas,
                  notas=list(notas) + [f"n = {n} ≥ 20 y p = {coma(p)} ≤ 0,05: la aproximación de Poisson es válida "
                                       "y difiere de la binomial exacta en milésimas."])


# ------------------------------------------------------------
# Esperanza y varianza de una variable aleatoria discreta
# ------------------------------------------------------------
def momentos(x, f):
    """E(X) = Σ x·f(x),  V(X) = E(X²) − [E(X)]²,  σ = √V(X). Devuelve (tabla, E, V, σ)."""
    t = pd.DataFrame({"x": x, "f(x)": f})
    t["x·f(x)"] = t["x"] * t["f(x)"]
    t["x²·f(x)"] = t["x"] ** 2 * t["f(x)"]
    e, e2 = t["x·f(x)"].sum(), t["x²·f(x)"].sum()
    v = e2 - e ** 2
    return t, e, v, sqrt(v)


def bloque_tabla(subtitulo, tabla, totales=True, notas=()):
    """DataFrame -> bloque con fila Σ (las columnas de x no se suman)."""
    filas = [[texto(v) if not isinstance(v, str) else v for v in f] for f in tabla.values]
    if totales:
        filas.append(["Σ"] + [texto(tabla[c].sum()) for c in tabla.columns[1:]])
    return bloque(subtitulo, list(tabla.columns), filas, notas=notas)
