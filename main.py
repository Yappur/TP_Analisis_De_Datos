"""API de los TP 1 y TP 2.  Ejecutar:  uvicorn main:app --reload
Frontend en http://localhost:8000 (TP 1) y http://localhost:8000/tp2 (TP 2)
Documentación automática en http://localhost:8000/docs
"""
import importlib
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from exportar_excel import CARPETA_SALIDA_TP2, exportar_tp2

app = FastAPI(title="TP 1 y TP 2 - Probabilidad y Estadística")
BASE = Path(__file__).parent
NUMEROS = range(1, 11)
NUMEROS_TP2 = range(1, 18)
LINKS_EXCEL = {
    1: "https://docs.google.com/spreadsheets/d/1ntUDOVLjxvnwRmPu9sbs54PqR72pIvsw/edit?usp=sharing&ouid=111584918977987168067&rtpof=true&sd=true",
    2: "https://docs.google.com/spreadsheets/d/1DN83woe-1iRDSHMkTkpv6WT_IvpNJ4FB/edit?usp=sharing&ouid=111584918977987168067&rtpof=true&sd=true",
    3: "https://docs.google.com/spreadsheets/d/1izHEvUiTZq9F7d2z0SYDRE9wYzyheuhf/edit?usp=sharing&ouid=111584918977987168067&rtpof=true&sd=true",
    4: "https://docs.google.com/spreadsheets/d/1DhD36yWXd3t9Djl9CxbX-ajoHF3Uf93e/edit?usp=sharing&ouid=111584918977987168067&rtpof=true&sd=true",
    5: "https://docs.google.com/spreadsheets/d/1OYuBdQqUcjLGtK55CDi-lfXWThvGuHZM/edit?usp=sharing&ouid=111584918977987168067&rtpof=true&sd=true",
    6: "https://docs.google.com/spreadsheets/d/1tEJhh3_nRO34qJGFEnVjwn_3aEO2iM38/edit?usp=sharing&ouid=111584918977987168067&rtpof=true&sd=true",
    7: "https://docs.google.com/spreadsheets/d/1FroSH5M4O5g24cyCX3qPBjZADRKhVjyq/edit?usp=sharing&ouid=111584918977987168067&rtpof=true&sd=true",
    8: "https://docs.google.com/spreadsheets/d/1aDJer1lSb3dKdkuTsBOZuvUXfkVcrd_l/edit?usp=sharing&ouid=111584918977987168067&rtpof=true&sd=true",
    9: "https://docs.google.com/spreadsheets/d/1Yk9oe-VOMkuJzFBT8ujYZHxOmHf6SwYt/edit?usp=sharing&ouid=111584918977987168067&rtpof=true&sd=true",
    10: "https://docs.google.com/spreadsheets/d/1FNVnKKWeGC5xUKZzrmfSqQCAIynTEJnB/edit?usp=sharing&ouid=111584918977987168067&rtpof=true&sd=true",
}


def cargar(n, paquete="ejercicios", numeros=NUMEROS):
    if n not in numeros:
        raise HTTPException(status_code=404, detail="Ejercicio inexistente")
    return importlib.import_module(f"{paquete}.ej{n:02d}")


@app.get("/api/ejercicios")
def listar():
    return [{"numero": n, "titulo": cargar(n).TITULO} for n in NUMEROS]


@app.get("/api/ejercicios/{n}")
def ver(n: int):
    ej = cargar(n)
    return {"numero": n, "titulo": ej.TITULO, "enunciado": ej.ENUNCIADO,
            "excel_url": LINKS_EXCEL[n], "bloques": ej.resolver()}


# ------------------------------------------------------------
# TP 2: misma estructura de respuesta que el TP 1
# ------------------------------------------------------------
def cargar_tp2(n):
    return cargar(n, "ejercicios_tp2", NUMEROS_TP2)


@app.get("/api/tp2/ejercicios")
def listar_tp2():
    return [{"numero": n, "titulo": cargar_tp2(n).TITULO} for n in NUMEROS_TP2]


@app.get("/api/tp2/ejercicios/{n}")
def ver_tp2(n: int):
    ej = cargar_tp2(n)
    return {"numero": n, "titulo": ej.TITULO, "enunciado": ej.ENUNCIADO,
            "excel_url": f"/api/tp2/excel/{n}", "bloques": ej.resolver()}


@app.get("/api/tp2/excel/{n}")
def excel_tp2(n: int):
    """Descarga excel/tp2/ejercicio_NN.xlsx (si todavía no existe, se genera con OpenPyXL)."""
    ruta = CARPETA_SALIDA_TP2 / f"ejercicio_{n:02d}.xlsx"
    if not ruta.exists():
        ruta = exportar_tp2(cargar_tp2(n))
    return FileResponse(ruta, filename=f"TP2_{ruta.name}",
                        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@app.get("/tp2", include_in_schema=False)
def pagina_tp2():
    return FileResponse(BASE / "static" / "tp2.html")


# El frontend (carpeta static) se sirve en "/"; va al final para no pisar la API
app.mount("/", StaticFiles(directory=BASE / "static", html=True), name="static")
