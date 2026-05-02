from __future__ import annotations

import yfinance as yf

LB_PER_METRIC_TON = 2204.62262185


def obtener_precio_cobre_usd_por_lb(ticker: str = "HG=F") -> float:
    """Obtiene precio actual del cobre en USD/lb desde Yahoo Finance."""
    try:
        info = yf.Ticker(ticker).fast_info
        precio = info.get("lastPrice") if isinstance(info, dict) else getattr(info, "lastPrice", None)
        if precio is None:
            historial = yf.Ticker(ticker).history(period="1d")
            if historial.empty:
                raise ValueError("No hay datos históricos del ticker")
            precio = float(historial["Close"].iloc[-1])
        return float(precio)
    except Exception as exc:
        raise RuntimeError(f"No se pudo obtener precio del cobre para {ticker}: {exc}") from exc


def valor_proyectado_usd(cobre_recuperado_t: float, precio_usd_lb: float) -> float:
    """Convierte t métricas a lb y calcula valor económico bruto en USD."""
    return cobre_recuperado_t * LB_PER_METRIC_TON * precio_usd_lb
