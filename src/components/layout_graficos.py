import plotly.express as px
from utils.formatar_opcao import formatar_opcao

CORES_GRAFICO = [
    "#38bdf8",
    "#34d399",
    "#f59e0b",
    "#f87171",
    "#a78bfa",
    "#22d3ee",
]

# Cor fixa por gargalo, reutilizada em todos os graficos e no card de resultado.
CORES_BARRAS = {
    "armazenamento": "#38bdf8",
    "ram": "#34d399",
    "gpu": "#f87171",
    "cpu": "#f59e0b",
}


def grafico_barra_empilhado(dados, *, x, y, group):
    dados_grafico = dados.copy()
    dados_grafico["x_formatado"] = dados_grafico[x].map(formatar_opcao)

    figura = px.bar(dados_grafico, x="x_formatado", y=y, color=group, color_discrete_map=CORES_BARRAS)

    figura.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0f172a"),
        xaxis_title=None,
        margin=dict(r=120),
        bargap=0.5,
        legend=dict(
            orientation="v",
            xanchor="left",
            yanchor="middle",
            x=1.02,
            y=0.5,
            title=None))

    return figura

def grafico_pizza_distribuicao(dados, coluna_categoria: str, mapa_cores: dict | None = None):
    dados_grafico = dados.copy()
    dados_grafico["rotulo"] = dados_grafico[coluna_categoria].map(formatar_opcao)
    if mapa_cores:
        cores = {formatar_opcao(chave): valor for chave, valor in mapa_cores.items()}
        argumentos_cor = dict(color="rotulo", color_discrete_map=cores)
    else:
        argumentos_cor = dict(color_discrete_sequence=CORES_GRAFICO)
    figura = px.pie(
        dados_grafico,
        names="rotulo",
        values="quantidade",
        **argumentos_cor,
    )
    figura.update_traces(
        textinfo="percent+label",
        textposition="inside",
        textfont=dict(size=16, color="#f8fafc"),
        marker=dict(line=dict(color="#FFFFFF", width=2)),
        hovertemplate="%{label}<br>Casos: %{value}<br>%{percent}<extra></extra>",
    )
    figura.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=15, color="#0f172a"),
        hoverlabel=dict(bgcolor="#0f172a", font_size=15, font_color="#f8fafc"),
        margin=dict(t=34, b=34, l=24, r=24),
        legend_title_text="",
        legend=dict(font=dict(size=15), orientation="h", y=-0.08, x=0.5, xanchor="center"),
        uniformtext_minsize=14,
        uniformtext_mode="hide",
    )
    return figura