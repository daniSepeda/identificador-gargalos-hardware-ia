import streamlit as st
from modelo_ia import HardwareRecommender

@st.cache_resource
def carregar_modelo() -> HardwareRecommender:
    """Carrega o recomendador uma unica vez e compartilha o cache entre as paginas."""
    return HardwareRecommender()
