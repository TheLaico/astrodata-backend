from app.repositories.chunks_documentos_repository import ChunksDocumentosRepository


def test_coseno_calcula_similitud() -> None:
    repository = ChunksDocumentosRepository.__new__(ChunksDocumentosRepository)

    assert repository._coseno([1.0, 0.0], [1.0, 0.0]) == 1.0
    assert repository._coseno([1.0, 0.0], [0.0, 1.0]) == 0.0


def test_coseno_retorna_cero_con_vectores_invalidos() -> None:
    repository = ChunksDocumentosRepository.__new__(ChunksDocumentosRepository)

    assert repository._coseno([], [1.0]) == 0.0
    assert repository._coseno([1.0], [1.0, 2.0]) == 0.0
