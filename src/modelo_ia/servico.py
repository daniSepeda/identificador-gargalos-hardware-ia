from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

@dataclass(frozen=True)
class RecomendacaoResultado:
    gargalo: str
    solucao: str
    semelhantes: pd.DataFrame
    confianca: float = 0.0


@dataclass(frozen=True)
class RevisaoResultado:
    """Saida da etapa Revise: o diagnostico final apos confirmacao/correcao do especialista."""

    gargalo_final: str
    solucao_final: str
    gargalo_sugerido: str
    solucao_sugerida: str
    revisado: bool
    confianca: float


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
        # Vetorizacao ancorada nos dominios fechados do PRD (nao nos valores presentes na base):
        # assim as colunas one-hot ficam estaveis mesmo depois que o Retain injeta novos casos.
        self._categorias_modelo = {
            coluna: list(self.CATEGORIAS[coluna]) for coluna in self.COLUNAS_CATEGORICAS
        }
        self._acuracia_loo: float | None = None
        self._reajustar()

    def _reajustar(self) -> None:
        """(Re)treina o modelo a partir de self.casos. Chamado no init e apos cada Retain."""
        self._x_bruto = self._vetorizar(self.casos)
        self.normalizador = MinMaxScaler().fit(self._x_bruto)
        self.x = self.normalizador.transform(self._x_bruto)
        self.modelo_knn = NearestNeighbors(n_neighbors=self.k, metric="euclidean").fit(self.x)
        self._acuracia_loo = None

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
        # Similaridade legivel para o usuario: 1/(1+distancia) -> 1.0 (identico) a 0.0 (distante).
        semelhantes["similaridade"] = 1.0 / (1.0 + distancias[0])
        return semelhantes

    def recomendar_upgrade(self, caso_novo: dict[str, Any], k: int | None = None) -> RecomendacaoResultado:
        """Ciclo Retrieve + Reuse: recupera os vizinhos e adapta a solucao por votacao majoritaria."""
        semelhantes = self.recuperar_casos(caso_novo, k=k)
        gargalo = semelhantes["gargalo"].mode()[0]
        solucao = semelhantes[semelhantes["gargalo"] == gargalo].iloc[0]["solucao_recomendada"]
        # Confianca = fracao dos vizinhos que concordam com o gargalo escolhido (0 a 1).
        confianca = float((semelhantes["gargalo"] == gargalo).mean())
        return RecomendacaoResultado(
            gargalo=gargalo, solucao=solucao, semelhantes=semelhantes, confianca=confianca
        )

    def revisar(
        self,
        resultado: RecomendacaoResultado,
        gargalo_correto: str | None = None,
        solucao_correta: str | None = None,
    ) -> RevisaoResultado:
        """Etapa Revise: um especialista confirma ou corrige a sugestao do ciclo Retrieve+Reuse.

        Sem feedback (`gargalo_correto=None`), a sugestao e aceita como esta. Com feedback que
        diverge da sugestao, o diagnostico e corrigido e a solucao adaptada — a informada pelo
        especialista ou, na ausencia, a mais frequente da base para o gargalo corrigido.
        """
        sugerido, solucao_sugerida = resultado.gargalo, resultado.solucao
        if gargalo_correto is None or gargalo_correto == sugerido:
            return RevisaoResultado(
                gargalo_final=sugerido,
                solucao_final=solucao_correta or solucao_sugerida,
                gargalo_sugerido=sugerido,
                solucao_sugerida=solucao_sugerida,
                revisado=False,
                confianca=resultado.confianca,
            )
        if solucao_correta is None:
            candidatos = self.casos.loc[self.casos["gargalo"] == gargalo_correto, "solucao_recomendada"]
            solucao_correta = candidatos.mode()[0] if not candidatos.empty else solucao_sugerida
        return RevisaoResultado(
            gargalo_final=gargalo_correto,
            solucao_final=solucao_correta,
            gargalo_sugerido=sugerido,
            solucao_sugerida=solucao_sugerida,
            revisado=True,
            confianca=resultado.confianca,
        )

    def reter_caso(
        self,
        caso_novo: dict[str, Any],
        gargalo: str,
        solucao: str,
        persistir: bool = False,
    ) -> int:
        """Etapa Retain: incorpora um caso ja resolvido/confirmado a base e reajusta o modelo.

        Devolve o `id_caso` atribuido. Com `persistir=True`, grava a base atualizada em disco
        (a proxima execucao ja nasce com o caso aprendido).
        """
        registro = dict(caso_novo)
        if "perfil_carga" not in registro and "perfil_uso" in registro:
            registro["perfil_carga"] = registro.pop("perfil_uso")
        novo_id = int(self.casos["id_caso"].max()) + 1 if len(self.casos) else 1
        registro.update({"id_caso": novo_id, "gargalo": gargalo, "solucao_recomendada": solucao})
        linha = {coluna: registro.get(coluna) for coluna in self.casos.columns}
        self.casos = pd.concat([self.casos, pd.DataFrame([linha])], ignore_index=True)
        self._reajustar()
        if persistir:
            self.casos.to_csv(self.data_path, index=False)
        return novo_id

    def distribuicao_gargalos(self) -> pd.DataFrame:
        return self.casos["gargalo"].value_counts().rename_axis("gargalo").reset_index(name="quantidade")

    def distribuicao_sintomas(self) -> pd.DataFrame:
        return (
            self.casos["sintoma_principal"]
            .value_counts()
            .rename_axis("sintoma_principal")
            .reset_index(name="quantidade")
        )
    
    def distribuicao_gargalos_maquina(self) ->pd.DataFrame:
        return self.casos.groupby(["tipo_maquina", "gargalo"]).size().reset_index(name="quantidade")

    def acuracia_leave_one_out(self) -> float:
        """Acuracia honesta por validacao leave-one-out.

        Cada caso e retirado da base e classificado pelos demais. O MinMaxScaler entra num
        Pipeline para reajustar dentro de cada dobra, evitando o vazamento de dados que ocorre
        ao normalizar a base inteira antes da validacao.
        """
        if self._acuracia_loo is None:
            pipeline = Pipeline(
                [
                    ("normalizador", MinMaxScaler()),
                    ("knn", KNeighborsClassifier(n_neighbors=self.k, metric="euclidean")),
                ]
            )
            previsoes = cross_val_predict(
                pipeline, self._x_bruto, self.casos["gargalo"], cv=LeaveOneOut()
            )
            self._acuracia_loo = float(accuracy_score(self.casos["gargalo"], previsoes))
        return self._acuracia_loo

    def metricas_resumo(self) -> dict[str, Any]:
        return {
            "total_casos": len(self.casos),
            "total_atributos": self.x.shape[1],
            "acuracia_loo": self.acuracia_leave_one_out(),
            "gargalos": sorted(self.casos["gargalo"].unique().tolist()),
        }
