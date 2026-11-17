# Chatbot del proyecto (buscador local, sin IA)

El bot **no genera texto**: busca en `chatbot/knowledge/*.md` la sección que mejor
coincide con la pregunta y la devuelve tal cual. No usa APIs, API keys, LLMs,
embeddings ni bases vectoriales. Solo `scikit-learn` (TF-IDF) y `rapidfuzz` (errores de tipeo).

```powershell
pip install -r requirements.txt
uvicorn main:app --reload
python -m chatbot.probar                       # 10 preguntas de ejemplo con su puntaje
python -m chatbot.probar "que es la mediana"   # tus propias preguntas
```

Para sumarlo a otra página: `<script src="/chatbot/chatbot.js" defer></script>` antes de `</body>`.
Después de editar un `.md`, **reiniciá el servidor** (el índice se arma al arrancar).

## Cómo escribir los `.md` para que el bot responda mejor

**1. Una sección por tema.** El bot corta cada archivo en los títulos `##` y `###` y
devuelve **una** sección completa. Si una sección mezcla tres temas, la respuesta
trae los tres; si un tema está repartido en dos secciones, devuelve solo una mitad.
Los `####` quedan adentro de su `###`.

**2. Títulos claros, con forma de concepto o de pregunta.** El título es lo que más pesa.

| Mejor                                      | Peor              |
|--------------------------------------------|-------------------|
| `### Desvío estándar`                      | `### Punto 3`     |
| `### ¿Cómo se generan los Excel?`          | `### Otros`       |
| `### Ejercicio 4 — Laplace con reposición` | `### Ej. 4`       |

**3. Línea opcional `Palabras clave:` debajo del título.** Sirve para las formas en
que alguien preguntaría algo que no está escrito en la sección. No se muestra en la respuesta.

```markdown
### Desvío estándar
Palabras clave: desviación típica, dispersión, sigma, qué tan separados están los datos

El desvío estándar es la raíz cuadrada de la varianza...
```

**4. El nombre del archivo define el TP.** `tp1.md` → TP1, `tp2.md` → TP2. Si la
pregunta dice "tp2", solo se busca en `tp2.md`. Los demás archivos usan su nombre
("Programación", "Arquitectura"; se agregan en `NOMBRES_ARCHIVO` de `indexer.py`).

**5. Sin texto suelto antes del primer `##`.** Lo que está entre el `#` y el primer
`##` no se indexa.

## Ajustes

- `chatbot/sinonimos.py`: equivalencias ("promedio" → "media", "tp 1" → "tp1").
- `chatbot/search.py`: `UMBRAL` (por defecto 0.15) y los pesos de cada bonus.
  Usá `python -m chatbot.probar` para ver los puntajes: las preguntas válidas tienen
  que quedar por encima del umbral y las de fuera de tema, por debajo.
- `chatbot/indexer.py`: `STOPWORDS`, las palabras que se ignoran al comparar.
