from app.rag.prompt_builder import PromptBuilder
from app.schemas.chat import FuenteRag


def test_prompt_builder_incluye_pregunta_y_contexto() -> None:
    prompt = PromptBuilder().construir(
        "Que condiciones favorecen la habitabilidad?",
        [
            FuenteRag(
                chunk_id="chunk-1",
                documento_id="doc-1",
                texto="La presencia de agua liquida es relevante para habitabilidad.",
                score=0.91,
            )
        ],
    )

    assert "Que condiciones favorecen la habitabilidad?" in prompt
    assert "agua liquida" in prompt
    assert "solamente el contexto" in prompt
