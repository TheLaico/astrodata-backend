from collections.abc import Sequence
from typing import Protocol


class ModeloEmbeddings(Protocol):
    def encode(
        self,
        sentences: Sequence[str],
        *,
        normalize_embeddings: bool,
    ):
        pass


class GeneradorEmbeddings:
    def __init__(self, nombre_modelo: str) -> None:
        self.nombre_modelo = nombre_modelo
        self._modelo: ModeloEmbeddings | None = None

    def generar(self, textos: Sequence[str]) -> list[list[float]]:
        if not textos:
            return []

        modelo = self._obtener_modelo()
        embeddings = modelo.encode(textos, normalize_embeddings=True)

        return [self._a_lista_float(embedding) for embedding in embeddings]

    def _obtener_modelo(self) -> ModeloEmbeddings:
        if self._modelo is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as exc:
                raise RuntimeError(
                    "Instala sentence-transformers para generar embeddings."
                ) from exc

            self._modelo = SentenceTransformer(self.nombre_modelo)

        return self._modelo

    def _a_lista_float(self, embedding) -> list[float]:
        if hasattr(embedding, "tolist"):
            embedding = embedding.tolist()

        return [float(valor) for valor in embedding]
