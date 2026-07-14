import streamlit as st
from utils.formatar_opcao import formatar_opcao
from utils.modelo import carregar_modelo
from modelo_ia import HardwareRecommender


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
    # Etapas Retrieve + Reuse.
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
        "similaridade",
    ]
    tabela = resultado.semelhantes[colunas].reset_index(drop=True)
    tabela["similaridade"] = tabela["similaridade"] * 100
    st.dataframe(
        tabela,
        width="stretch",
        hide_index=True,
        column_config={
            "similaridade": st.column_config.ProgressColumn(
                "Similaridade",
                help="Quão parecido é o caso histórico com a máquina analisada (1 / (1 + distância)).",
                format="%.0f%%",
                min_value=0,
                max_value=100,
            ),
        },
    )

    # Etapas Revise + Retain executadas nos bastidores (sem expor o usuario ao ciclo RBC):
    # a sugestao e confirmada e o caso e incorporado a base para uso futuro.
    revisao = modelo.revisar(resultado)
    novo_id = modelo.reter_caso(caso, gargalo=revisao.gargalo_final, solucao=revisao.solucao_final)
    st.caption(
        f"✅ Esta entrada foi adicionada à base de casos "
        f"(caso #{novo_id} — base agora com {len(modelo.casos)} casos)."
    )


modelo = carregar_modelo()

st.markdown("""
        <h1 class='title'>🖥️ Identificador de Gargalos e Recomendador de Upgrades </h1>
        <p class='subtitle'>
            Interface gráfica para entrada de novos casos,focada em identificar o gargalo mais provável e sugerir upgrades.
        </p>
        """, unsafe_allow_html=True)

st.divider()

st.subheader("Descreva o computador e os sintomas")
enviado, caso, k = renderizar_formulario(modelo)
if enviado:
    mostrar_resultado(modelo, caso, k)

