"""Rutas HTTP del chatbot.

    POST /api/chat         -> busca la mejor sección para una pregunta
    GET  /api/chat/temas   -> títulos agrupados por TP (menú inicial del widget)

Las funciones son `def` (no `async def`): FastAPI las ejecuta en un hilo aparte,
así una búsqueda no bloquea al resto de la aplicación.
"""
from fastapi import APIRouter
from pydantic import BaseModel, Field

from chatbot import search

router = APIRouter(prefix="/api/chat", tags=["chatbot"])


class Pregunta(BaseModel):
    # Pydantic rechaza automáticamente (error 422) textos vacíos o de más de 300 caracteres.
    pregunta: str = Field(..., min_length=1, max_length=300)


class Respuesta(BaseModel):
    encontrado: bool
    titulo: str
    tp: str
    archivo: str
    respuesta_md: str
    sugerencias: list[str]


@router.post("", response_model=Respuesta)
def chat(body: Pregunta):
    resultado = search.buscar(body.pregunta.strip())
    return resultado.a_dict()


@router.get("/temas")
def listar_temas() -> dict[str, list[str]]:
    """Ejemplo: {"TP1": ["Alcance y criterio de lectura", ...], "TP2": [...], ...}"""
    return search.temas()
