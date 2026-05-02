"""Calculadora metalúrgica en Python con lógica pura y UI en Streamlit.

Este módulo traduce la lógica de ``script.js`` a funciones puras tipadas,
separando el dominio de cálculo de la capa de presentación.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import streamlit as st


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


def cobre_hidrometalurgia(
    ley_cabeza_pct: float,
    toneladas_t: float,
    recuperacion_pct: float,
    acido_kg: float,
) -> ResultadoHidro:
    """Calcula métricas de hidrometalurgia para cobre."""
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
    """Calcula métricas de pirometalurgia para cobre."""
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


def validar_positivo(nombre: str, valor: float) -> None:
    if valor <= 0:
        raise ValueError(f"{nombre} debe ser mayor que 0")


def validar_no_negativo(nombre: str, valor: float) -> None:
    if valor < 0:
        raise ValueError(f"{nombre} no puede ser negativo")


def ui_streamlit() -> None:
    st.set_page_config(page_title="Simulador Metalúrgico", page_icon="⛏️")
    st.title("⛏️ Simulador Metalúrgico")

    elemento = st.selectbox(
        "🧪 Elemento",
        options=["", Elemento.COBRE.value, Elemento.CALIZA.value, Elemento.SAL.value],
        format_func=lambda x: {
            "": "Seleccionar",
            Elemento.COBRE.value: "Cobre",
            Elemento.CALIZA.value: "Caliza",
            Elemento.SAL.value: "Sal",
        }[x],
    )

    procesos_disponibles: list[str] = [""]
    if elemento == Elemento.COBRE.value:
        procesos_disponibles += [Proceso.HIDRO.value, Proceso.PIRO.value]
    elif elemento == Elemento.CALIZA.value:
        procesos_disponibles += [Proceso.CALCINACION.value]
    elif elemento == Elemento.SAL.value:
        procesos_disponibles += [Proceso.EVAPORACION.value]

    proceso = st.selectbox(
        "⚙️ Proceso",
        options=procesos_disponibles,
        format_func=lambda x: {
            "": "Selecciona proceso",
            Proceso.HIDRO.value: "Hidrometalurgia",
            Proceso.PIRO.value: "Pirometalurgia",
            Proceso.CALCINACION.value: "Calcinación",
            Proceso.EVAPORACION.value: "Evaporación",
        }.get(x, x),
    )

    st.subheader("Resultados")
    if elemento and proceso:
        try:
            if elemento == Elemento.COBRE.value and proceso == Proceso.HIDRO.value:
                ley = st.number_input("Ley cabeza (%)", min_value=0.0, step=0.1)
                ton = st.number_input("Toneladas (t)", min_value=0.0, step=1.0)
                rec = st.number_input("Recuperación (%)", min_value=0.0, step=0.1)
                acido = st.number_input("Ácido (kg)", min_value=0.0, step=1.0)
                if st.button("Calcular", key="calc_hidro"):
                    r = cobre_hidrometalurgia(ley, ton, rec, acido)
                    st.markdown("🔵 **Hidrometalurgia**")
                    st.write(f"Cobre contenido: {r.cobre_contenido_t:.2f} t")
                    st.write(f"Cobre recuperado: {r.cobre_recuperado_t:.2f} t")
                    st.write(f"Consumo ácido: {r.consumo_acido_kg_t:.2f} kg/t")

            elif elemento == Elemento.COBRE.value and proceso == Proceso.PIRO.value:
                ley = st.number_input("Ley cabeza (%)", min_value=0.0, step=0.1)
                ley_c = st.number_input("Ley concentrado (%)", min_value=0.0, step=0.1)
                ton = st.number_input("Toneladas (t)", min_value=0.0, step=1.0)
                rec = st.number_input("Recuperación (%)", min_value=0.0, step=0.1)
                if st.button("Calcular", key="calc_piro"):
                    r = cobre_pirometalurgia(ley, ley_c, ton, rec)
                    st.markdown("🔴 **Pirometalurgia**")
                    st.write(f"Cobre contenido: {r.cobre_contenido_t:.2f} t")
                    st.write(f"Cobre recuperado: {r.cobre_recuperado_t:.2f} t")
                    st.write(f"Ley concentrado: {r.ley_concentrado_pct:.2f} %")

            elif elemento == Elemento.CALIZA.value:
                ton = st.number_input("Toneladas", min_value=0.0, step=1.0)
                if st.button("Calcular", key="calc_ca"):
                    r = produccion_caliza(ton)
                    st.write(f"{r.etiqueta}: {r.produccion_t:.2f} t")

            elif elemento == Elemento.SAL.value:
                ton = st.number_input("Producción sal", min_value=0.0, step=1.0)
                if st.button("Calcular", key="calc_na"):
                    r = produccion_sal(ton)
                    st.write(f"{r.etiqueta}: {r.produccion_t:.2f} t")
        except ValueError as error:
            st.error(str(error))

    st.markdown("---")
    st.subheader("🔄 Conversor")
    valor = st.number_input("Valor", step=0.1)
    unidad = st.selectbox("Unidad", options=["porcentaje", "ppm"])

    if st.button("Convertir"):
        if unidad == "porcentaje":
            st.write(f"{valor}% = {porcentaje_a_ppm(valor):.2f} ppm")
        else:
            st.write(f"{valor} ppm = {ppm_a_porcentaje(valor):.4f}%")


if __name__ == "__main__":
    ui_streamlit()
