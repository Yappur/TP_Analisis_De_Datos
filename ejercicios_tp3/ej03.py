from fractions import Fraction as Fr

from distribuciones import bloque_resolucion, bloque_tabla, fila, momentos

TITULO = "Ejercicio 3 – Esperanza de una función g(X)"
ENUNCIADO = ("X: autos que pasan por un lavadero entre las 16 y las 17 h de un viernes soleado: "
             "f(4)=1/12, f(5)=1/12, f(6)=1/4, f(7)=1/4, f(8)=1/6, f(9)=1/6. g(X) = 2X − 1 es lo que el "
             "administrador paga al operador (en dólares). Calcular la ganancia esperada del operador.")

X = [4, 5, 6, 7, 8, 9]
FX = [Fr(1, 12), Fr(1, 12), Fr(1, 4), Fr(1, 4), Fr(1, 6), Fr(1, 6)]


def resolver():
    t, e, _, _ = momentos(X, FX)
    t = t[["x", "f(x)", "x·f(x)"]].copy()
    t["g(x) = 2x − 1"] = 2 * t["x"] - 1
    t["g(x)·f(x)"] = t["g(x) = 2x − 1"] * t["f(x)"]
    eg = t["g(x)·f(x)"].sum()
    assert eg == 2 * e - 1

    filas = [
        fila("Σ f(x) = 1 (FMP válida)", "1/12 + 1/12 + 1/4 + 1/4 + 1/6 + 1/6", t["f(x)"].sum(), porcentaje=False),
        fila("E(X) = Σ x·f(x)", f"= {e}", e, porcentaje=False),
        fila("E[g(X)] = Σ (2x − 1)·f(x)", f"= {eg}", eg, porcentaje=False),
        fila("Verificación: E(2X − 1) = 2·E(X) − 1", f"2·({e}) − 1 = {eg}", eg, porcentaje=False),
    ]
    tabla = t.copy()
    tabla["g(x) = 2x − 1"] = tabla["g(x) = 2x − 1"].astype(object)
    bl = bloque_tabla("Tabla de cálculo", tabla)
    bl["filas"][-1][3] = "—"  # Σ g(x) no tiene sentido
    return [bl, bloque_resolucion(filas, notas=[f"Ganancia esperada del operador: ${float(eg):.2f} "
                                                f"(exactamente {eg} dólares)."])]
