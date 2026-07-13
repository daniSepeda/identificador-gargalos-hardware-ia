import streamlit as st
from components.custom_style import aplicar_estilo_visual
from components.layout_graficos import grafico_pizza_distribuicao, grafico_barra_empilhado
from modelo_ia import HardwareRecommender

@st.cache_resource
def carregar_modelo() -> HardwareRecommender:
    return HardwareRecommender()

modelo = carregar_modelo()
metricas = modelo.metricas_resumo()
aplicar_estilo_visual()

st.title("Visão geral da base de casos")

col1, col2, col3 = st.columns(3)

col1.metric("Casos na base", metricas["total_casos"], border=True)
col2.metric("Atributos vetorizados", metricas["total_atributos"], border=True)
col3.metric("Acurácia no conjunto atual", f'{metricas["acuracia_treino"]:.1%}', border=True)


fig = grafico_barra_empilhado(modelo.distribuicao_gargalos_maquina(), x="tipo_maquina", y="quantidade", group="gargalo")
with st.container(border=True): 
    st.markdown("<div class='chart-title'>Distribuição de gargalos por tipo de máquina <div>", unsafe_allow_html=True)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

g1, g2 = st.columns(2)
with g1:
    gargalos = modelo.distribuicao_gargalos()

    with st.container(border=True):
        st.markdown("<div class='chart-title'>Distribuição de gargalos<div>", unsafe_allow_html=True)
        st.plotly_chart(
            grafico_pizza_distribuicao(gargalos, "gargalo"),
            width="stretch",
            config={"displayModeBar": False}
        )
with g2:
    sintomas = modelo.distribuicao_sintomas()

    with st.container(border=True):
        st.markdown("<div class='chart-title'>Sintomas mais frequentes<div>", unsafe_allow_html=True)
        st.plotly_chart(
            grafico_pizza_distribuicao(sintomas, "sintoma_principal"),
            width="stretch",
            config={"displayModeBar": False}
        )

st.subheader("Tabela completa da base")
filtro_gargalo = st.multiselect("Filtrar por gargalo", metricas["gargalos"])
base = modelo.casos.copy()
if filtro_gargalo:
    base = base[base["gargalo"].isin(filtro_gargalo)]

st.dataframe(base, use_container_width=True, hide_index=True)
st.download_button(
    "Baixar base filtrada em CSV",
    data=base.to_csv(index=False).encode("utf-8"),
    file_name="base_casos_filtrada.csv",
    mime="text/csv",
)
