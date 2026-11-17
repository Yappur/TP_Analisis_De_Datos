"""Prueba el buscador por consola, sin levantar el servidor.

Uso (desde la carpeta tp1_app):
    python -m chatbot.probar                      -> corre las 10 preguntas de ejemplo
    python -m chatbot.probar "que es la mediana"  -> prueba tus propias preguntas

Sirve para ajustar UMBRAL en search.py: mirá el puntaje de las preguntas que
DEBERÍAN responderse y el de las que NO (las de fuera de tema). El umbral tiene
que quedar entre ambos grupos.
"""
import sys

from chatbot import search

PREGUNTAS_EJEMPLO = [
    "¿Qué es la desviación estándar?",
    "promedio del tp1",
    "ejercicio 4 del tp 2",
    "teorema de bayes",
    "como se calcula la varianca de una binomal",   # con errores de tipeo a propósito
    "distribución de Poisson",
    "glosario",
    "¿Cómo se genera el Excel?",
    "qué hace main.py",
    "¿Cuál es la capital de Francia?",              # fuera de tema: no debe responder
]


def main(preguntas: list[str]) -> None:
    buscador = search.cargar()
    print(f"Secciones indexadas: {len(buscador.secciones)} | UMBRAL = {search.UMBRAL}\n")

    for pregunta in preguntas:
        r = buscador.buscar(pregunta)
        marca = "OK " if r.encontrado else "-- "
        print(f"{marca}[{r.puntaje:5.3f}] {pregunta}")
        print(f"      consulta procesada: {r.consulta!r}")
        if r.encontrado:
            print(f"      → {r.tp} · {r.titulo}  ({r.archivo})")
            for s in r.sugerencias or []:
                print(f"        sugerencia: {s}")
        else:
            print("      → sin respuesta")
        print()


if __name__ == "__main__":
    main(sys.argv[1:] or PREGUNTAS_EJEMPLO)
