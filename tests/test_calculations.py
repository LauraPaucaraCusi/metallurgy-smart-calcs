from src.metallurgy.domain.calculations import (
    cobre_hidrometalurgia,
    cobre_pirometalurgia,
    costo_acido_usd,
    margen_operativo_bruto_usd,
)


def test_hidro_basico() -> None:
    r = cobre_hidrometalurgia(1.0, 1000.0, 80.0, 20000.0)
    assert round(r.cobre_contenido_t, 2) == 10.0
    assert round(r.cobre_recuperado_t, 2) == 8.0
    assert round(r.cobre_recuperado_kg, 2) == 8000.0
    assert round(r.consumo_especifico_acido_kg_cu, 4) == 2.5


def test_piro_basico() -> None:
    r = cobre_pirometalurgia(1.0, 25.0, 1000.0, 85.0)
    assert round(r.cobre_contenido_t, 2) == 10.0
    assert round(r.cobre_recuperado_t, 2) == 8.5


def test_margen_operativo_bruto() -> None:
    costo = costo_acido_usd(20000.0)
    assert round(costo, 2) == 2400.0
    margen = margen_operativo_bruto_usd(100000.0, costo)
    assert round(margen, 2) == 97600.0
