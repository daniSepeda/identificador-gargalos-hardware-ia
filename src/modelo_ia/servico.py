from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.preprocessing import MinMaxScaler

@dataclass(frozen=True)
class RecomendacaoResultado:
    gargalo: str
    solucao: str
    semelhantes: pd.DataFrame


class HardwareRecommender:
    MAPA_CPU = {"antiga": 0, "intermediaria": 1, "recente": 2}
    MAPA_ARMAZENAMENTO = {"HDD": 0, "SSD_SATA": 1, "SSD_NVMe": 2}
    MAPA_GPU = {
        "integrada": 0,
        "dedicada_baixa": 1,
        "dedicada_media": 2,
        "dedicada_alta": 3,
    }
    CATEGORIAS = {
        "tipo_maquina": [
            "desktop_escritorio",
            "notebook_corporativo",
            "servidor",
            "maquina_virtual",
            "estacao_trabalho",
        ],
        "perfil_carga": [
            "ofimatica_administrativa",
            "banco_de_dados",
            "atendimento_cliente",
            "financeiro_erp",
            "design_grafico_marketing",
            "desenvolvimento_software",
            "virtualizacao_vdi",
            "ciencia_de_dados_ml",
            "servidor_aplicacao_web",
            "engenharia_cad",
        ],
        "perfil_uso": [
            "ofimatica_administrativa",
            "banco_de_dados",
            "atendimento_cliente",
            "financeiro_erp",
            "design_grafico_marketing",
            "desenvolvimento_software",
            "virtualizacao_vdi",
            "ciencia_de_dados_ml",
            "servidor_aplicacao_web",
            "engenharia_cad",
        ],
        "sintoma_principal": [
            "boot_lento",
            "lentidao_geral",
            "falta_espaco",
            "consulta_bd_lenta",
            "relatorio_erp_lento",
            "travamento_multitarefa",
            "contencao_maquina_virtual",
            "lentidao_programas_pesados",
            "treinamento_modelo_lento",
            "timeout_aplicacao_web",
            "renderizacao_cad_lenta",
            "exportacao_video_lenta",
        ],
    }
    COLUNAS_CATEGORICAS = ["tipo_maquina", "perfil_carga", "sintoma_principal"]
    ATRIBUTOS = [
        "tipo_maquina",
        "cpu_geracao",
        "nucleos_cpu",
        "ram_gb",
        "tipo_armazenamento",
        "gpu",
        "perfil_carga",
        "sintoma_principal",
        "uso_cpu_pct",
        "uso_ram_pct",
        "uso_disco_pct",
    ]

    def __init__(self, data_path: str | Path | None = None, k: int = 3) -> None:
        base_dir = Path(__file__).resolve().parents[2]
        self.data_path = Path(data_path) if data_path else base_dir / "data" / "base_casos_corporativa_v1.csv"
        self.k = k
        self.casos = pd.read_csv(self.data_path)
        self._categorias_modelo = self._extrair_categorias(self.casos)
        self.CATEGORIAS = {
            **self._categorias_modelo,
            "perfil_uso": self._categorias_modelo["perfil_carga"],
        }
        self._x_bruto = self._vetorizar(self.casos)
        self.normalizador = MinMaxScaler().fit(self._x_bruto)
        self.x = self.normalizador.transform(self._x_bruto)
        self.modelo_knn = NearestNeighbors(n_neighbors=self.k, metric="euclidean").fit(self.x)
        self.classificador = KNeighborsClassifier(n_neighbors=self.k, metric="euclidean").fit(
            self.x, self.casos["gargalo"]
        )

    def _extrair_categorias(self, df: pd.DataFrame) -> dict[str, list[Any]]:
        return {
            coluna: df[coluna].dropna().drop_duplicates().tolist()
            for coluna in self.COLUNAS_CATEGORICAS
        }

    def _normalizar_entrada(self, df: pd.DataFrame) -> pd.DataFrame:
        normalizado = df.copy()
        if "perfil_carga" not in normalizado.columns and "perfil_uso" in normalizado.columns:
            normalizado["perfil_carga"] = normalizado["perfil_uso"]
        return normalizado

    def _vetorizar(self, df: pd.DataFrame) -> pd.DataFrame:
        dados = self._normalizar_entrada(df)
        x = dados[self.ATRIBUTOS].copy()
        x["cpu_geracao"] = x["cpu_geracao"].map(self.MAPA_CPU)
        x["tipo_armazenamento"] = x["tipo_armazenamento"].map(self.MAPA_ARMAZENAMENTO)
        x["gpu"] = x["gpu"].map(self.MAPA_GPU)

        for coluna, valores in self._categorias_modelo.items():
            x[coluna] = pd.Categorical(x[coluna], categories=valores)

        return pd.get_dummies(x, columns=list(self._categorias_modelo)).astype(float)

    def _transformar_caso(self, caso_novo: dict[str, Any]):
        vetor = self._vetorizar(pd.DataFrame([caso_novo]))
        vetor = vetor.reindex(columns=self._x_bruto.columns, fill_value=0.0)
        return self.normalizador.transform(vetor)

    def recuperar_casos(self, caso_novo: dict[str, Any], k: int | None = None) -> pd.DataFrame:
        vizinhos = k or self.k
        vetor = self._transformar_caso(caso_novo)
        distancias, indices = self.modelo_knn.kneighbors(vetor, n_neighbors=vizinhos)
        semelhantes = self.casos.iloc[indices[0]].copy()
        semelhantes["distancia"] = distancias[0].round(3)
        return semelhantes

    def recomendar_upgrade(self, caso_novo: dict[str, Any], k: int | None = None) -> RecomendacaoResultado:
        semelhantes = self.recuperar_casos(caso_novo, k=k)
        gargalo = semelhantes["gargalo"].mode()[0]
        solucao = semelhantes[semelhantes["gargalo"] == gargalo].iloc[0]["solucao_recomendada"]
        return RecomendacaoResultado(gargalo=gargalo, solucao=solucao, semelhantes=semelhantes)

    def distribuicao_gargalos(self) -> pd.DataFrame:
        return self.casos["gargalo"].value_counts().rename_axis("gargalo").reset_index(name="quantidade")

    def distribuicao_sintomas(self) -> pd.DataFrame:
        return (
            self.casos["sintoma_principal"]
            .value_counts()
            .rename_axis("sintoma_principal")
            .reset_index(name="quantidade")
        )

    def metricas_resumo(self) -> dict[str, Any]:
        return {
            "total_casos": len(self.casos),
            "total_atributos": self.x.shape[1],
            "acuracia_treino": self.classificador.score(self.x, self.casos["gargalo"]),
            "gargalos": sorted(self.casos["gargalo"].unique().tolist()),
        }
