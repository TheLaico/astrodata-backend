from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


TipoObjetoCeleste = Literal[
    "galaxia",
    "sistema_estelar",
    "estrella",
    "planeta",
    "luna",
    "nebulosa",
    "asteroide",
    "cometa",
    "exoplaneta",
]


class CoordenadasEcuatoriales(BaseModel):
    ascension_recta: float = Field(
        ge=0,
        lt=360,
        description="Ascension recta en grados. Equivale a RA.",
    )
    declinacion: float = Field(
        ge=-90,
        le=90,
        description="Declinacion en grados. Equivale a Dec.",
    )


class PropiedadesFisicas(BaseModel):
    distancia_anios_luz: float | None = Field(default=None, ge=0)
    masa_tierra: float | None = Field(default=None, ge=0)
    radio_tierra: float | None = Field(default=None, ge=0)
    temperatura_kelvin: float | None = Field(default=None, ge=0)
    periodo_orbital_dias: float | None = Field(default=None, ge=0)
    indice_habitabilidad: float | None = Field(default=None, ge=0, le=1)


class ObjetoCelesteBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    tipo_objeto: TipoObjetoCeleste
    descripcion: str = Field(min_length=10, max_length=2000)
    coordenadas: CoordenadasEcuatoriales
    propiedades_fisicas: PropiedadesFisicas = Field(default_factory=PropiedadesFisicas)
    objeto_padre_id: str | None = Field(default=None)
    etiquetas: list[str] = Field(default_factory=list)
    metadatos: dict[str, Any] = Field(default_factory=dict)


class CrearObjetoCeleste(ObjetoCelesteBase):
    pass


class ActualizarObjetoCeleste(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=120)
    tipo_objeto: TipoObjetoCeleste | None = None
    descripcion: str | None = Field(default=None, min_length=10, max_length=2000)
    coordenadas: CoordenadasEcuatoriales | None = None
    propiedades_fisicas: PropiedadesFisicas | None = None
    objeto_padre_id: str | None = None
    etiquetas: list[str] | None = None
    metadatos: dict[str, Any] | None = None


class ObjetoCelesteRespuesta(ObjetoCelesteBase):
    id: str
    creado_en: datetime
    actualizado_en: datetime

    model_config = ConfigDict(from_attributes=True)


def fecha_actual_utc() -> datetime:
    return datetime.now(timezone.utc)
