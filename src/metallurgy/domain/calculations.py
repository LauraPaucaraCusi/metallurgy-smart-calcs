from __future__ import annotations

from .models import ResultadoHidro, ResultadoPiro, ResultadoSimple
from .validators import validar_no_negativo, validar_positivo


def cobre_hidrometalurgia(
    ley_cabeza_pct: float,
    toneladas_t: float,
    recuperacion_pct: float,
    acido_kg: float,
) -> ResultadoHidro:
    validar_positivo("toneladas_t", toneladas_t)
    validar_no_negativo("ley_cabeza_pct", ley_cabeza_pct)
    validar_no_negativo("recuperacion_pct", recuperacion_pct)
    validar_no_negativo("acido_kg", acido_kg)

    contenido = toneladas_t * (ley_cabeza_pct / 100.0)
    recuperado = contenido * (recuperacion_pct / 100.0)
    consumo = acido_kg / toneladas_t
    return ResultadoHidro(contenido, recuperado, consumo)


def cobre_pirometalurgia(
    ley_cabeza_pct: float,
    ley_concentrado_pct: float,
    toneladas_t: float,
    recuperacion_pct: float,
) -> ResultadoPiro:
    validar_positivo("toneladas_t", toneladas_t)
    validar_no_negativo("ley_cabeza_pct", ley_cabeza_pct)
    validar_no_negativo("ley_concentrado_pct", ley_concentrado_pct)
    validar_no_negativo("recuperacion_pct", recuperacion_pct)

    contenido = toneladas_t * (ley_cabeza_pct / 100.0)
    recuperado = contenido * (recuperacion_pct / 100.0)
    return ResultadoPiro(contenido, recuperado, ley_concentrado_pct)


def produccion_caliza(toneladas_t: float) -> ResultadoSimple:
    validar_no_negativo("toneladas_t", toneladas_t)
    return ResultadoSimple(toneladas_t, "Producción caliza")


def produccion_sal(toneladas_t: float) -> ResultadoSimple:
    validar_no_negativo("toneladas_t", toneladas_t)
    return ResultadoSimple(toneladas_t, "Producción sal")


def porcentaje_a_ppm(valor_pct: float) -> float:
    return valor_pct * 10000.0


def ppm_a_porcentaje(valor_ppm: float) -> float:
    return valor_ppm / 10000.0
