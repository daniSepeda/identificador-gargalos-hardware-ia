import streamlit as st
from components.custom_style import aplicar_estilo_visual

st.set_page_config(
    page_title="Identificador de Gargalos de Hardware",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded",
)

aplicar_estilo_visual()

pagina_analise = st.Page(
    "pages/analise.py",
    title="Nova análise",
    icon="🏠",
    default=True,
)

pagina_indicadores = st.Page(
    "pages/dashboard.py",
    title="Indicadores",
    icon="📊",
    url_path="indicadores",
)

pages = [pagina_analise, pagina_indicadores]

pagina_atual = st.navigation({"Navegação": pages}, position="sidebar")

with st.sidebar:
    st.markdown("#### 👥 Equipe")
    st.markdown("""
        <div style='color: rgba(15, 23, 42, 0.65);'>
            Daniela Sepeda<br>
            Geovanni Silva<br>
            Maria Fernanda Gonçalves
            <br>Miguel Lobo
        </div>""", unsafe_allow_html=True)

pagina_atual.run()
