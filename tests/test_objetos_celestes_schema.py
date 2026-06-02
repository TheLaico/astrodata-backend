import pytest
from pydantic import ValidationError

from app.schemas.objetos_celestes import CrearObjetoCeleste


def test_crear_objeto_celeste_valida_datos_astronomicos() -> None:
    objeto = CrearObjetoCeleste(
        nombre="Kepler-186f",
        tipo_objeto="exoplaneta",
        descripcion="Exoplaneta ubicado en la zona habitable de su sistema estelar.",
        coordenadas={
            "ascension_recta": 298.213,
            "declinacion": 43.955,
        },
        propiedades_fisicas={
            "distancia_anios_luz": 492,
            "radio_tierra": 1.17,
            "indice_habitabilidad": 0.72,
        },
        etiquetas=["zona_habitable", "exoplaneta"],
    )

    assert objeto.nombre == "Kepler-186f"
    assert objeto.tipo_objeto == "exoplaneta"
    assert objeto.coordenadas.ascension_recta == 298.213


def test_crear_objeto_celeste_rechaza_coordenadas_invalidas() -> None:
    with pytest.raises(ValidationError):
        CrearObjetoCeleste(
            nombre="Objeto invalido",
            tipo_objeto="planeta",
            descripcion="Objeto con coordenadas fuera de rango para validar reglas.",
            coordenadas={
                "ascension_recta": 361,
                "declinacion": -91,
            },
        )
