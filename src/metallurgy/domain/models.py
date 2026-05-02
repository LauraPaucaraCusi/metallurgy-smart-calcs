from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Elemento(str, Enum):
    COBRE = "Cu"
    CALIZA = "Ca"
    SAL = "Na"


class Proceso(str, Enum):
    HIDRO = "hidro"
    PIRO = "piro"
    CALCINACION = "cal"
    EVAPORACION = "eva"


@dataclass(frozen=True)
class ResultadoHidro:
    cobre_contenido_t: float
    cobre_recuperado_t: float
    consumo_acido_kg_t: float


@dataclass(frozen=True)
class ResultadoPiro:
    cobre_contenido_t: float
    cobre_recuperado_t: float
    ley_concentrado_pct: float


@dataclass(frozen=True)
class ResultadoSimple:
    produccion_t: float
    etiqueta: str
