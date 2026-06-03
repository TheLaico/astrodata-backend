from collections.abc import Sequence


class GeneradorEmbeddings:
    def __init__(self, nombre_modelo: str) -> None:
        self.nombre_modelo = nombre_modelo
        self._modelo = None

    def generar(self, textos: Sequence[str]) -> list[list[float]]:
        if not textos:
            return []

        modelo = self._obtener_modelo()
        embeddings = modelo.embed(list(textos))

        return [self._a_lista_float(embedding) for embedding in embeddings]

    def _obtener_modelo(self):
        if self._modelo is None:
            try:
                from fastembed import TextEmbedding
            except ImportError as exc:
                raise RuntimeError(
                    "Instala fastembed para generar embeddings: pip install -r requirements-ml.txt"
                ) from exc

            self._modelo = TextEmbedding(model_name=self.nombre_modelo)

        return self._modelo

    def _a_lista_float(self, embedding) -> list[float]:
        if hasattr(embedding, "tolist"):
            embedding = embedding.tolist()

        return [float(valor) for valor in embedding]
