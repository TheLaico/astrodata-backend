from app.schemas.chat import FuenteRag


class PromptBuilder:
    def construir(self, pregunta: str, fuentes: list[FuenteRag]) -> str:
        contexto = "\n\n".join(
            f"Fuente {indice + 1}:\n{fuente.texto}"
            for indice, fuente in enumerate(fuentes)
        )

        return f"""
Eres AstroData Lab, un asistente de investigacion astronomica.
Responde en espanol de forma clara y breve usando solamente el contexto entregado.
Si el contexto no alcanza para responder con seguridad, dilo explicitamente.

Contexto recuperado:
{contexto}

Pregunta del usuario:
{pregunta}

Respuesta:
""".strip()
