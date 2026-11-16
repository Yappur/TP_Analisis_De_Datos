"""Funciones comunes del TP 2 (probabilidad).
Igual que en el TP 1, cada ejercicio devuelve una lista de "bloques" (ver estadistica.bloque).
Las probabilidades se calculan con Fraction para obtener resultados exactos (1/6, 15/32, ...).
"""
from fractions import Fraction
from itertools import product

import pandas as pd

from estadistica import bloque, r

# Columnas de los bloques de resolución: inciso + fórmula | cálculo | fracción | decimal
COLUMNAS = ["Inciso / fórmula", "Cálculo", "Resultado", "Decimal"]

VALORES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
PALOS = ["Picas", "Corazones", "Diamantes", "Tréboles"]
FIGURAS = ["J", "Q", "K"]


def es_decimal_exacto(x):
    """True si la fracción se escribe mejor como decimal (denominador 10, 100, 125, 1000, ...)."""
    d = x.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return d == 1 and (x.denominator % 10 == 0 or x.denominator >= 100)


def fraccion(x):
    """Fraction -> texto '1/6' (o '0.23' si viene de datos decimales). Floats -> '0.35'."""
    if isinstance(x, Fraction):
        return f"{float(x):.10g}" if es_decimal_exacto(x) else str(x)
    return f"{r(x):g}"


def fila(planteo, calculo, valor):
    return [planteo, calculo, fraccion(valor), r(valor)]


def laplace(casos):
    """Regla de Laplace sobre una columna booleana de pandas: favorables / posibles."""
    return Fraction(int(casos.sum()), len(casos))


def texto_laplace(casos):
    return f"{int(casos.sum())} / {len(casos)}"


def conjunto(elementos):
    return "{" + ", ".join(str(e) for e in elementos) + "}" if len(elementos) else "∅"


def baraja():
    """Baraja francesa de 52 cartas como DataFrame (valor, palo)."""
    return pd.DataFrame(list(product(VALORES, PALOS)), columns=["valor", "palo"])


def dado():
    return pd.DataFrame({"x": range(1, 7)})


def con_totales(tabla):
    """Agrega fila y columna 'Total' (probabilidades marginales) a una tabla de contingencia."""
    t = tabla.copy()
    t["Total"] = t.sum(axis=1)
    t.loc["Total"] = t.sum()
    return t


def bloque_tabla(subtitulo, tabla, nombre_indice, decimales=4, notas=()):
    """DataFrame -> bloque (la primera columna es el índice)."""
    filas = [[str(i)] + [int(v) if decimales == 0 else r(v, decimales) for v in fila_]
             for i, fila_ in zip(tabla.index, tabla.values)]
    return bloque(subtitulo, [nombre_indice] + [str(c) for c in tabla.columns], filas, notas=notas)


def bloque_resolucion(filas, notas=(), subtitulo="Resolución"):
    return bloque(subtitulo, COLUMNAS, filas, notas=notas)


def total(probabilidades, condicionales):
    """Teorema de la probabilidad total: P(E) = Σ P(Hi)·P(E/Hi). Devuelve (tabla, P(E))."""
    t = pd.DataFrame({"P(Hi)": probabilidades, "P(E/Hi)": condicionales})
    t["P(Hi)·P(E/Hi)"] = t["P(Hi)"] * t["P(E/Hi)"]
    return t, t["P(Hi)·P(E/Hi)"].sum()


def bloque_bayes(tabla, nombre_hipotesis, decimal=False, bayes=True):
    """Tabla del teorema de Bayes: P(Hi/E) = P(Hi)·P(E/Hi) / P(E).
    decimal=True muestra los datos como decimales (cuando la consigna los da así).
    bayes=False deja solo la probabilidad total (sin la columna P(Hi/E))."""
    t = tabla.copy()
    pe = t["P(Hi)·P(E/Hi)"].sum()
    if bayes:
        t["P(Hi/E)"] = t["P(Hi)·P(E/Hi)"] / pe
    t.loc["Total"] = t.sum()
    t.loc["Total", "P(E/Hi)"] = None
    def texto(v, columna):
        if v is None or pd.isna(v):
            return "—"
        if not decimal or v == int(v):
            return fraccion(v)
        if columna == "P(Hi/E)":
            return f"{v} ≈ {r(v)}"
        return f"{float(v):.10g}"

    filas = [[str(i)] + [texto(v, c) for v, c in zip(fila_, t.columns)] for i, fila_ in zip(t.index, t.values)]
    titulo = "Tabla de probabilidad total y Bayes" if bayes else "Tabla de probabilidad total"
    return bloque(titulo, [nombre_hipotesis] + list(t.columns), filas)
