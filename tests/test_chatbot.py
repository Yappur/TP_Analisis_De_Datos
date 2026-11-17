"""Tests del chatbot por palabras clave.  Ejecutar:  python -m unittest tests.test_chatbot"""
import unittest

from fastapi.testclient import TestClient

from chatbot import search
from chatbot.indexer import _dividir_en_secciones, normalizar, preparar

MD_DE_PRUEBA = """# TP9 — Prueba
Introducción que no se indexa.

## Conceptos
Palabras clave: promedio, centro

La media es la suma dividida por n.

## Código

```python
## esto es un comentario, NO un título
print("hola")
```

### Detalle
#### Sub-detalle
Texto del detalle.
"""


class IndexadorTests(unittest.TestCase):
    def setUp(self):
        self.secciones = _dividir_en_secciones(MD_DE_PRUEBA, "tp9.md")

    def test_normaliza_tildes_mayusculas_y_signos(self):
        self.assertEqual(normalizar("¿Qué es la Desviación Estándar?"), "que es la desviacion estandar")
        self.assertEqual(preparar("¿Qué es la media?"), "media")

    def test_corta_por_titulos_y_deduce_el_tp(self):
        titulos = [s.titulo for s in self.secciones]
        self.assertEqual(titulos, ["Conceptos", "Código", "Detalle"])
        self.assertTrue(all(s.tp == "TP9" for s in self.secciones))
        self.assertEqual(self.secciones[2].padre, "Código")

    def test_lee_palabras_clave_y_las_quita_del_contenido(self):
        conceptos = self.secciones[0]
        self.assertEqual(conceptos.palabras_clave, ["promedio", "centro"])
        self.assertNotIn("Palabras clave", conceptos.contenido)

    def test_respeta_bloques_de_codigo_y_subtitulos(self):
        codigo, detalle = self.secciones[1], self.secciones[2]
        self.assertIn("## esto es un comentario", codigo.contenido)
        self.assertIn("```python", codigo.contenido)
        self.assertIn("#### Sub-detalle", detalle.contenido)


class BuscadorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.buscador = search.cargar()   # usa los .md reales de chatbot/knowledge

    def test_devuelve_texto_literal_del_markdown(self):
        r = self.buscador.buscar("ejercicio 4 del tp 2")
        self.assertTrue(r.encontrado)
        self.assertEqual(r.tp, "TP2")
        seccion = next(s for s in self.buscador.secciones if s.etiqueta == f"{r.tp} · {r.titulo}")
        self.assertEqual(r.respuesta_md, seccion.contenido)

    def test_filtra_por_tp(self):
        r = self.buscador.buscar("ejercicio 5 tp1")
        self.assertEqual(r.tp, "TP1")

    def test_tolera_errores_de_tipeo(self):
        r = self.buscador.buscar("probabilida condicinal")
        self.assertTrue(r.encontrado)
        self.assertIn("condicional", r.consulta)

    def test_fuera_de_tema_no_responde(self):
        for pregunta in ("¿Cuál es la capital de Francia?", "receta de pizza", "hola"):
            r = self.buscador.buscar(pregunta)
            self.assertFalse(r.encontrado, pregunta)
            self.assertEqual(r.respuesta_md, search.MENSAJE_SIN_RESULTADO)

    def test_etiqueta_exacta_devuelve_esa_seccion(self):
        seccion = self.buscador.secciones[10]
        r = self.buscador.buscar(seccion.etiqueta)
        self.assertEqual((r.tp, r.titulo), (seccion.tp, seccion.titulo))
        self.assertLessEqual(len(r.sugerencias), search.MAX_SUGERENCIAS)


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from main import app
        cls.cliente = TestClient(app)
        cls.cliente.__enter__()   # dispara el lifespan (carga del índice)

    @classmethod
    def tearDownClass(cls):
        cls.cliente.__exit__(None, None, None)

    def test_chat_responde_con_el_formato_acordado(self):
        r = self.cliente.post("/api/chat", json={"pregunta": "glosario"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(set(r.json()), {"encontrado", "titulo", "tp", "archivo", "respuesta_md", "sugerencias"})

    def test_rechaza_preguntas_de_mas_de_300_caracteres(self):
        r = self.cliente.post("/api/chat", json={"pregunta": "a" * 301})
        self.assertEqual(r.status_code, 422)

    def test_temas_agrupados_por_tp(self):
        temas = self.cliente.get("/api/chat/temas").json()
        self.assertTrue({"TP1", "TP2", "TP3"} <= set(temas))
        self.assertTrue(all(isinstance(t, str) for t in temas["TP1"]))


if __name__ == "__main__":
    unittest.main()
