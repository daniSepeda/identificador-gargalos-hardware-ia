import streamlit as st

def aplicar_estilo_visual():
    st.markdown("""
    <style>
                
    [data-testid='stHeaderActionElements'] {
        display: none;
    }
                
    .stSidebar * {
        font-size: 1rem !important;
    }
                
    [data-testid="stMetricLabel"] p {
        font-size: 1rem !important;
    }
                
    .chart-title {
        font-size: 1.3rem !important;
        font-weight: 600;
        text-align: center;
    }
                
    .title {
        font-size: 3.75rem;
        padding: 0;
        margin: 0;
    }
    
    .subtitle {
        color: #8892a8;
        font-size: 1.2rem !important;
        padding: 0 20px 0 0;
    }

    .brand {
        font-size: 1.4rem;
        font-weight: 700;
        letter-spacing: .02em;
    }
    </style>
""", unsafe_allow_html=True)