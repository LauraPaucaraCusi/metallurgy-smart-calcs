from __future__ import annotations

from .models import ResultadoHidro, ResultadoPiro, ResultadoSimple
from .validators import validar_no_negativo, validar_positivo

KG_PER_TON: float = 1000.0
USD_ACIDO_POR_TON: float = 120.0


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

    cobre_contenido_t: float = toneladas_t * (ley_cabeza_pct / 100.0)
    cobre_recuperado_t: float = cobre_contenido_t * (recuperacion_pct / 100.0)
    cobre_recuperado_kg: float = cobre_recuperado_t * KG_PER_TON
    validar_positivo("cobre_recuperado_kg", cobre_recuperado_kg)

    consumo_especifico_acido_kg_cu: float = acido_kg / cobre_recuperado_kg
    return ResultadoHidro(
        cobre_contenido_t=cobre_contenido_t,
        cobre_recuperado_t=cobre_recuperado_t,
        cobre_recuperado_kg=cobre_recuperado_kg,
        consumo_especifico_acido_kg_cu=consumo_especifico_acido_kg_cu,
    )


def costo_acido_usd(acido_kg: float) -> float:
    validar_no_negativo("acido_kg", acido_kg)
    return (acido_kg / KG_PER_TON) * USD_ACIDO_POR_TON


def margen_operativo_bruto_usd(ingreso_bruto_usd: float, costo_acido_usd_total: float) -> float:
    return ingreso_bruto_usd - costo_acido_usd_total


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
