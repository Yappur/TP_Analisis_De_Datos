"""API del TP 1.  Ejecutar:  uvicorn main:app --reload
Frontend en http://localhost:8000  |  Documentación automática en http://localhost:8000/docs
"""
import importlib
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="TP 1 - Probabilidad y Estadística")
NUMEROS = range(1, 11)
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


def cargar(n):
    if n not in NUMEROS:
        raise HTTPException(status_code=404, detail="Ejercicio inexistente")
    return importlib.import_module(f"ejercicios.ej{n:02d}")


@app.get("/api/ejercicios")
def listar():
    return [{"numero": n, "titulo": cargar(n).TITULO} for n in NUMEROS]


@app.get("/api/ejercicios/{n}")
def ver(n: int):
    ej = cargar(n)
    return {"numero": n, "titulo": ej.TITULO, "enunciado": ej.ENUNCIADO,
            "excel_url": LINKS_EXCEL[n], "bloques": ej.resolver()}


# El frontend (carpeta static) se sirve en "/"; va al final para no pisar la API
app.mount("/", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="static")
