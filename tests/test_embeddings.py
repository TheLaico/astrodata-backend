from app.rag.embeddings import GeneradorEmbeddings


class ModeloFalso:
    def embed(self, sentences):
        return [[float(indice), 0.5] for indice, _ in enumerate(sentences)]


def test_generador_embeddings_convierte_resultado_a_lista_float() -> None:
    generador = GeneradorEmbeddings("modelo-falso")
    generador._modelo = ModeloFalso()

    embeddings = generador.generar(["texto uno", "texto dos"])

    assert embeddings == [[0.0, 0.5], [1.0, 0.5]]


def test_generador_embeddings_responde_lista_vacia_sin_cargar_modelo() -> None:
    generador = GeneradorEmbeddings("modelo-falso")

    assert generador.generar([]) == []
