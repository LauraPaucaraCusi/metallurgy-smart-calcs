from src.metallurgy.domain.calculations import cobre_hidrometalurgia, cobre_pirometalurgia


def test_hidro_basico() -> None:
    r = cobre_hidrometalurgia(1.0, 1000.0, 80.0, 20000.0)
    assert round(r.cobre_contenido_t, 2) == 10.0
    assert round(r.cobre_recuperado_t, 2) == 8.0
    assert round(r.consumo_acido_kg_t, 2) == 20.0


def test_piro_basico() -> None:
    r = cobre_pirometalurgia(1.0, 25.0, 1000.0, 85.0)
    assert round(r.cobre_contenido_t, 2) == 10.0
    assert round(r.cobre_recuperado_t, 2) == 8.5
