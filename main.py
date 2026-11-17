"""API de los TP 1, TP 2 y TP 3.  Ejecutar:  uvicorn main:app --reload
Frontend en http://localhost:8000 (TP 1), /tp2 (TP 2) y /tp3 (TP 3)
Documentación automática en http://localhost:8000/docs
"""
import importlib
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from chatbot import search as chatbot_search
from chatbot.router import router as chatbot_router
from exportar_excel import CARPETA_SALIDA_TP2, CARPETA_SALIDA_TP3, exportar_tp2, exportar_tp3

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Al arrancar: el chatbot lee los .md de chatbot/knowledge y arma su índice en memoria.
    # Si editás un .md, reiniciá el servidor para que tome los cambios.
    chatbot_search.cargar()
    yield


app = FastAPI(title="TP 1, TP 2 y TP 3 - Probabilidad y Estadística", lifespan=lifespan)
BASE = Path(__file__).parent
NUMEROS = range(1, 11)
NUMEROS_TP2 = range(1, 18)
NUMEROS_TP3 = range(1, 26)
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
# TP 2 y TP 3: misma estructura de respuesta que el TP 1.
# Cada TP registra /api/tpN/ejercicios, /api/tpN/ejercicios/{n}, /api/tpN/excel/{n} y la página /tpN
# ------------------------------------------------------------
def registrar_tp(tp, paquete, numeros, carpeta_excel, exportador):
    def cargar_tp(n):
        return cargar(n, paquete, numeros)

    @app.get(f"/api/tp{tp}/ejercicios", name=f"listar_tp{tp}")
    def listar_tp():
        return [{"numero": n, "titulo": cargar_tp(n).TITULO} for n in numeros]

    @app.get(f"/api/tp{tp}/ejercicios/{{n}}", name=f"ver_tp{tp}")
    def ver_tp(n: int):
        ej = cargar_tp(n)
        return {"numero": n, "titulo": ej.TITULO, "enunciado": ej.ENUNCIADO,
                "excel_url": f"/api/tp{tp}/excel/{n}", "bloques": ej.resolver()}

    @app.get(f"/api/tp{tp}/excel/{{n}}", name=f"excel_tp{tp}")
    def excel_tp(n: int):
        """Descarga excel/tpN/ejercicio_NN.xlsx (si todavía no existe, se genera con OpenPyXL)."""
        ruta = carpeta_excel / f"ejercicio_{n:02d}.xlsx"
        if not ruta.exists():
            ruta = exportador(cargar_tp(n))
        return FileResponse(ruta, filename=f"TP{tp}_{ruta.name}",
                            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    @app.get(f"/tp{tp}", include_in_schema=False, name=f"pagina_tp{tp}")
    def pagina_tp():
        return FileResponse(BASE / "static" / f"tp{tp}.html")


registrar_tp(2, "ejercicios_tp2", NUMEROS_TP2, CARPETA_SALIDA_TP2, exportar_tp2)
registrar_tp(3, "ejercicios_tp3", NUMEROS_TP3, CARPETA_SALIDA_TP3, exportar_tp3)

# Se registra antes de montar static para que el catch-all no intercepte la API.
app.include_router(chatbot_router)


# El frontend (carpeta static) se sirve en "/"; va al final para no pisar la API
app.mount("/", StaticFiles(directory=BASE / "static", html=True), name="static")
