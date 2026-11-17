from distribuciones import bloque_resolucion, bloque_tabla, fila, momentos

TITULO = "Ejercicio 2 – Esperanza y varianza (boletos de avión)"
ENUNCIADO = ("Avión con capacidad para 8 pasajeros; se venden 10 boletos. X: número de boletos vendidos en un "
             "vuelo, con P(X=6)=0,25; P(X=7)=0,35; P(X=8)=0,25; P(X=9)=0,10; P(X=10)=0,05. "
             "a) Valor esperado del número de pasajeros que se presentan al vuelo con boleto. "
             "b) Varianza y desviación estándar.")

X = [6, 7, 8, 9, 10]
FX = [0.25, 0.35, 0.25, 0.10, 0.05]


def resolver():
    t, e, v, s = momentos(X, FX)
    filas = [
        fila("a) E(X) = Σ x·f(x)", "6·0,25 + 7·0,35 + 8·0,25 + 9·0,10 + 10·0,05", e, porcentaje=False),
        fila("   E(X²) = Σ x²·f(x)", "36·0,25 + 49·0,35 + 64·0,25 + 81·0,10 + 100·0,05",
             t["x²·f(x)"].sum(), porcentaje=False),
        fila("b) V(X) = E(X²) − [E(X)]²", f"{r6(t['x²·f(x)'].sum())} − {r6(e)}²", v, porcentaje=False),
        fila("   σ = √V(X)", f"√{r6(v)}", s, porcentaje=False),
    ]
    return [bloque_tabla("Tabla de cálculo", t),
            bloque_resolucion(filas, notas=[
                "X se toma como la cantidad de pasajeros con boleto que se presentan (es la variable de la tabla).",
                f"En promedio se presentan {r6(e)} pasajeros, con una dispersión de ±{s:.4f}."])]


def r6(x):
    return f"{round(float(x), 6):g}"
