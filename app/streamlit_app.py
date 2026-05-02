from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.metallurgy.domain.calculations import (
    cobre_hidrometalurgia,
    cobre_pirometalurgia,
    costo_acido_usd,
    margen_operativo_bruto_usd,
    porcentaje_a_ppm,
    ppm_a_porcentaje,
    produccion_caliza,
    produccion_sal,
)
from src.metallurgy.domain.models import Elemento, Proceso
from src.metallurgy.services.market_data import (
    LB_PER_METRIC_TON,
    obtener_precio_cobre_usd_por_lb,
    valor_proyectado_usd,
)


def _grafico_sensibilidad(ton: float, ley: float) -> None:
    recuperaciones: list[int] = list(range(50, 101, 5))
    recuperado_t: list[float] = [ton * (ley / 100.0) * (r / 100.0) for r in recuperaciones]
    df = pd.DataFrame({"Recuperación (%)": recuperaciones, "Cobre recuperado (t)": recuperado_t})
    fig = px.line(df, x="Recuperación (%)", y="Cobre recuperado (t)", markers=True, title="Sensibilidad de cobre recuperado")
    st.plotly_chart(fig, use_container_width=True)


def ui_streamlit() -> None:
    st.set_page_config(page_title="Simulador Metalúrgico", page_icon="⛏️")
    st.title("⛏️ Simulador Metalúrgico")

    elemento = st.selectbox("🧪 Elemento", ["", Elemento.COBRE.value, Elemento.CALIZA.value, Elemento.SAL.value],
                            format_func=lambda x: {"": "Seleccionar", "Cu": "Cobre", "Ca": "Caliza", "Na": "Sal"}[x])

    procesos_disponibles = [""]
    if elemento == Elemento.COBRE.value:
        procesos_disponibles += [Proceso.HIDRO.value, Proceso.PIRO.value]
    elif elemento == Elemento.CALIZA.value:
        procesos_disponibles += [Proceso.CALCINACION.value]
    elif elemento == Elemento.SAL.value:
        procesos_disponibles += [Proceso.EVAPORACION.value]

    proceso = st.selectbox("⚙️ Proceso", procesos_disponibles,
                           format_func=lambda x: {
                               "": "Selecciona proceso", "hidro": "Hidrometalurgia", "piro": "Pirometalurgia",
                               "cal": "Calcinación", "eva": "Evaporación"
                           }.get(x, x))

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
                    try:
                        precio_lb: float = obtener_precio_cobre_usd_por_lb()
                        st.caption("Precio de cobre obtenido desde Yahoo Finance (HG=F).")
                    except RuntimeError:
                        precio_lb = 4.00
                        st.warning("No se pudo consultar Yahoo Finance. Se usa precio por defecto: USD 4.00/lb")

                    ingreso_bruto_usd: float = valor_proyectado_usd(r.cobre_recuperado_t, precio_lb)
                    costo_acido_total_usd: float = costo_acido_usd(acido)
                    margen_bruto_usd: float = margen_operativo_bruto_usd(ingreso_bruto_usd, costo_acido_total_usd)
                    st.markdown("🔵 **Hidrometalurgia**")
                    st.write(f"Cobre contenido: {r.cobre_contenido_t:.2f} t")
                    st.write(f"Cobre recuperado: {r.cobre_recuperado_t:.2f} t")
                    st.write(f"Cobre recuperado: {r.cobre_recuperado_kg:,.2f} kg")
                    st.write(f"Consumo específico de ácido: {r.consumo_especifico_acido_kg_cu:.4f} kg ácido/kg Cu")
                    st.write(f"Precio cobre aplicado: USD {precio_lb:.4f}/lb")
                    st.write(f"Ingreso bruto por cobre: USD {ingreso_bruto_usd:,.2f}")
                    st.write(f"Costo del ácido consumido: USD {costo_acido_total_usd:,.2f}")
                    st.write(f"Margen operativo bruto: USD {margen_bruto_usd:,.2f}")
                    st.caption(f"Conversión usada: 1 t = {LB_PER_METRIC_TON:.4f} lb")
                    _grafico_sensibilidad(ton, ley)

            elif elemento == Elemento.COBRE.value and proceso == Proceso.PIRO.value:
                ley = st.number_input("Ley cabeza (%)", min_value=0.0, step=0.1)
                ley_c = st.number_input("Ley concentrado (%)", min_value=0.0, step=0.1)
                ton = st.number_input("Toneladas (t)", min_value=0.0, step=1.0)
                rec = st.number_input("Recuperación (%)", min_value=0.0, step=0.1)
                if st.button("Calcular", key="calc_piro"):
                    r = cobre_pirometalurgia(ley, ley_c, ton, rec)
                    try:
                        precio_lb: float = obtener_precio_cobre_usd_por_lb()
                        st.caption("Precio de cobre obtenido desde Yahoo Finance (HG=F).")
                    except RuntimeError:
                        precio_lb = 4.00
                        st.warning("No se pudo consultar Yahoo Finance. Se usa precio por defecto: USD 4.00/lb")

                    ingreso_bruto_usd: float = valor_proyectado_usd(r.cobre_recuperado_t, precio_lb)
                    st.markdown("🔴 **Pirometalurgia**")
                    st.write(f"Cobre contenido: {r.cobre_contenido_t:.2f} t")
                    st.write(f"Cobre recuperado: {r.cobre_recuperado_t:.2f} t")
                    st.write(f"Ley concentrado: {r.ley_concentrado_pct:.2f} %")
                    st.write(f"Precio cobre aplicado: USD {precio_lb:.4f}/lb")
                    st.write(f"Ingreso bruto por cobre: USD {ingreso_bruto_usd:,.2f}")
                    st.caption(f"Conversión usada: 1 t = {LB_PER_METRIC_TON:.4f} lb")
                    _grafico_sensibilidad(ton, ley)

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
        except (ValueError, RuntimeError) as error:
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
