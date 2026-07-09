from __future__ import annotations
import streamlit as st
from modelo_ia import HardwareRecommender

st.set_page_config(
    page_title="Identificador de Gargalos de Hardware",
    page_icon="🖥️",
    layout="wide",
)

@st.cache_resource
def carregar_modelo() -> HardwareRecommender:
    return HardwareRecommender()


def formatar_opcao(valor: str) -> str:
    return valor.replace("_", " ").capitalize()


def renderizar_formulario(modelo: HardwareRecommender) -> tuple[bool, dict[str, int | str], int]:
    with st.form("form_analise"):
        c1, c2, c3 = st.columns(3)
        with c1:
            tipo_maquina = st.selectbox("Tipo de máquina", modelo.CATEGORIAS["tipo_maquina"])
            cpu_geracao = st.selectbox("Geração da CPU", list(modelo.MAPA_CPU))
            nucleos_cpu = st.slider("Núcleos da CPU", min_value=2, max_value=16, value=4, step=2)
            ram_gb = st.slider("Memória RAM (GB)", min_value=4, max_value=64, value=8, step=4)
        with c2:
            tipo_armazenamento = st.selectbox("Armazenamento", list(modelo.MAPA_ARMAZENAMENTO))
            gpu = st.selectbox("GPU", list(modelo.MAPA_GPU))
            perfil_uso = st.selectbox("Perfil de uso", modelo.CATEGORIAS["perfil_uso"], format_func=formatar_opcao)
            sintoma_principal = st.selectbox(
                "Sintoma principal",
                modelo.CATEGORIAS["sintoma_principal"],
                format_func=formatar_opcao,
            )
        with c3:
            uso_cpu_pct = st.slider("Uso de CPU (%)", min_value=0, max_value=100, value=50)
            uso_ram_pct = st.slider("Uso de RAM (%)", min_value=0, max_value=100, value=70)
            uso_disco_pct = st.slider("Uso de disco (%)", min_value=0, max_value=100, value=60)
            k = st.slider("Quantidade de casos semelhantes (k)", min_value=1, max_value=7, value=3, step=2)

        enviado = st.form_submit_button("Analisar gargalo")

    caso = {
        "tipo_maquina": tipo_maquina,
        "cpu_geracao": cpu_geracao,
        "nucleos_cpu": nucleos_cpu,
        "ram_gb": ram_gb,
        "tipo_armazenamento": tipo_armazenamento,
        "gpu": gpu,
        "perfil_uso": perfil_uso,
        "sintoma_principal": sintoma_principal,
        "uso_cpu_pct": uso_cpu_pct,
        "uso_ram_pct": uso_ram_pct,
        "uso_disco_pct": uso_disco_pct,
    }
    return enviado, caso, k


def mostrar_resultado(modelo: HardwareRecommender, caso: dict[str, int | str], k: int) -> None:
    resultado = modelo.recomendar_upgrade(caso, k=k)
    r1, r2 = st.columns(2)
    r1.success(f"Gargalo mais provável: **{resultado.gargalo.upper()}**")
    r2.info(f"Upgrade recomendado: **{resultado.solucao}**")

    st.subheader("Casos semelhantes que sustentam a recomendação")
    colunas = [
        "id_caso",
        "tipo_maquina",
        "sintoma_principal",
        "gargalo",
        "solucao_recomendada",
        "distancia",
    ]
    st.dataframe(
        resultado.semelhantes[colunas].reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
    )


def main() -> None:
    modelo = carregar_modelo()
    metricas = modelo.metricas_resumo()

    st.title("Identificador de Gargalos e Recomendador de Upgrades")
    st.caption(
        "Interface Streamlit baseada no notebook do projeto para analisar sintomas, "
        "identificar o gargalo mais provável e sugerir upgrades."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Casos na base", metricas["total_casos"])
    col2.metric("Atributos vetorizados", metricas["total_atributos"])
    col3.metric("Acurácia no conjunto atual", f'{metricas["acuracia_treino"]:.1%}')

    aba_analise, aba_base = st.tabs(["Nova análise", "Explorar base histórica"])

    with aba_analise:
        st.subheader("Descreva o computador e os sintomas")
        enviado, caso, k = renderizar_formulario(modelo)
        if enviado:
            mostrar_resultado(modelo, caso, k)

    with aba_base:
        st.subheader("Visão geral da base de casos")
        g1, g2 = st.columns(2)
        with g1:
            st.markdown("**Distribuição de gargalos**")
            st.bar_chart(modelo.distribuicao_gargalos())
        with g2:
            st.markdown("**Sintomas mais frequentes**")
            st.bar_chart(modelo.distribuicao_sintomas())

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


if __name__ == "__main__":
    main()
