import re


def dividir_texto_por_oraciones(texto: str, max_caracteres: int = 700) -> list[str]:
    texto_limpio = " ".join(texto.split())
    if not texto_limpio:
        return []

    oraciones = re.split(r"(?<=[.!?])\s+", texto_limpio)
    chunks: list[str] = []
    actual = ""

    for oracion in oraciones:
        if not actual:
            actual = oracion
            continue

        if len(actual) + 1 + len(oracion) <= max_caracteres:
            actual = f"{actual} {oracion}"
        else:
            chunks.append(actual)
            actual = oracion

    if actual:
        chunks.append(actual)

    return chunks
