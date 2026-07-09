# 🖥️ Identificador de Gargalos e Recomendador de Upgrades de Hardware

Projeto final destinado à disciplina de **Inteligência Artificial**, ministrada pelo Professor **Adolfo Colares**, na **Universidade Federal do Amapá (UNIFAP)**, no semestre **2026.1**.

## 👥 Componentes do Grupo

- Daniela Marques Haber Sepeda
- Geovanni Rodrigues da Silva
- Maria Fernanda Fernandes de Souza Gonçalves
- Miguel Peres Lobo

## 🎯 Objetivo do Projeto

Criar um sistema baseado em **Raciocínio Baseado em Casos (RBC)** capaz de identificar gargalos de hardware e recomendar upgrades de componentes conforme sintomas, perfil de uso, configuração atual e histórico de soluções semelhantes.

## 🧠 Abordagem Técnica

O projeto utiliza uma base de casos históricos com exemplos de computadores, sintomas observados, componentes instalados e solução adotada. Para cada novo caso, o sistema calcula a similaridade com registros anteriores usando **K-Nearest Neighbors (KNN)** com distância euclidiana, recupera os casos mais próximos (*Retrieve*) e adapta a recomendação para a máquina analisada (*Reuse*).

## 📁 Entregas

### Entrega 1 — Proposta (28/05)

- `docs/Proposta-IA.pdf`: proposta inicial de 1 página.
- `docs/proposta.md`: versão editável da proposta.

### Entrega 2 — Checkpoint (18/06)

- `data/base_casos.csv`: primeira base de casos (40 casos com foco em uso doméstico/gamer), mantida no repositório como registro histórico.
- Primeiros experimentos com as etapas *Retrieve* e *Reuse* e validação leave-one-out (acurácia de 80% com k=3).

### Entrega 3 — Final (09/07)

- `docs/PRD_base_casos_corporativa.md`: PRD que repriorizou o escopo do projeto para **ambientes corporativos**.
- `data/base_casos_corporativa_v1.csv`: **nova base oficial** — 80 casos corporativos, balanceados em 20 casos por classe de gargalo (cpu, ram, gpu, armazenamento). Substitui a `base_casos.csv` como base usada pelo notebook.
- `notebooks/checkpoint_experimentos.ipynb`: notebook atualizado para a base corporativa, com validação de domínios (correção do bug de categoria não vista), métricas por classe e análise dos erros.
- `CHANGELOG.md`: diferenças detalhadas entre a base corporativa e a base original.
- Resultado: **acurácia leave-one-out de 80% com k=3** (mesmo baseline da Entrega 2, agora com o dobro de casos e classes perfeitamente balanceadas).

## 🗃️ De onde veio a base corporativa (fontes espelhadas)

Não existe dataset público com o rótulo "gargalo de hardware" pronto. A base foi **construída manualmente pela equipe**, com rotulagem por regras de decisão (ex.: uso de disco ≥ 95% sustentado + HDD → gargalo de armazenamento) validada por dupla checagem. Para os valores serem realistas em vez de inventados, cada aspecto da base **espelha o padrão de um dataset público** — aproveitamos a *estrutura* das fontes, não suas linhas:

| Fonte | O que aproveitamos | O que descartamos |
|---|---|---|
| [Achieved FPS in Video Games (Kaggle)](https://www.kaggle.com/datasets/kritikseth/achieved-frames-per-second-fps-in-video-games) | O padrão estrutural "config de CPU+GPU + tipo de carga → desempenho", replicado para cargas corporativas (render CAD, query de BD, treino de ML) | Valores de FPS, jogos e sintomas de jogos (`fps_baixo`, `carregamento_lento_jogos`) |
| [UCI Computer Hardware (id 29)](https://archive.ics.uci.edu/dataset/29/computer+hardware) | O conceito de score de desempenho combinado por máquina (inspira o `cpu_score` da v2) | Os 209 registros originais (hardware de 1987) |
| [GPU Benchmarks Compilation](https://www.kaggle.com/datasets/alanjo/gpu-benchmarks) + CPU Specs (Kaggle) | Faixas realistas de benchmark para calibrar a escala ordinal de CPU/GPU (antiga → recente, integrada → dedicada_alta) | Importação literal linha a linha |
| [pc-part-dataset (PCPartPicker)](https://github.com/docyx/pc-part-dataset) | Faixas de preço de mercado para o futuro campo `custo_estimado_solucao` (v2) | Peças de consumidor gamer |
| Laptop Specifications & Prices (Kaggle) | Configurações plausíveis de notebooks corporativos (RAM, armazenamento, CPU) | Notebooks gamer/consumo |
| [Numenta Anomaly Benchmark — NAB](https://github.com/numenta/NAB) | O padrão de telemetria real de servidores (picos e patamares de CPU/disco) para calibrar `uso_cpu_pct`/`uso_disco_pct` dos casos de servidor | Séries temporais completas e rótulos de anomalia |
| [Lohmann, Gaspary & Melchiors — SBSeg 2005](https://sol.sbc.org.br/index.php/sbseg/article/view/21538) | A estrutura de caso do RBC e a similaridade ponderada por relevância de sintoma (roadmap v2) | Não é dataset — referência metodológica |

### O que mudou em relação à base da Entrega 2

- **Foco**: uso doméstico/gamer → **ambientes corporativos** (escritórios, servidores, virtualização, estações de trabalho);
- **`perfil_uso` → `perfil_carga`**: os 5 perfis antigos (escritório, estudo, jogos, programação, edição de vídeo) deram lugar a **10 perfis de carga corporativa** (ofimática, desenvolvimento, banco de dados, servidor web, VDI, CAD, design, atendimento, ciência de dados/ML, financeiro/ERP);
- **`tipo_maquina`**: de 2 valores (notebook, desktop) para **5** (desktop_escritorio, notebook_corporativo, servidor, estacao_trabalho, maquina_virtual);
- **Sintomas**: saem os de jogos, entram **7 sintomas corporativos** (consulta_bd_lenta, timeout_aplicacao_web, contencao_maquina_virtual, renderizacao_cad_lenta, exportacao_video_lenta, treinamento_modelo_lento, relatorio_erp_lento);
- **Tamanho e balanceamento**: 40 → **80 casos**, com as classes de gargalo corrigidas de 14×7 para **20×20×20×20**;
- **Ambiguidade proposital**: o mesmo sintoma aparece com gargalos diferentes (ex.: `consulta_bd_lenta` pode ser disco, RAM ou CPU), forçando o KNN a usar a telemetria para desambiguar, como num diagnóstico real.

O detalhamento completo está no `CHANGELOG.md` e no PRD.

## 📊 Resultados

Avaliação por **validação leave-one-out** (cada caso é retirado da base e classificado pelos 79 restantes), a mesma métrica usada na Entrega 2:

| k (vizinhos) | Acurácia |
|---|---|
| 1 | 83,8% |
| **3** | **80,0%** ✅ (critério do PRD: ≥ 75%) |
| 5 | 80,0% |
| 7 | 76,2% |

Métricas por classe de gargalo (k=3), com a base agora **perfeitamente balanceada** (20 casos por classe):

| Gargalo | Precisão | Revocação | F1 |
|---|---|---|---|
| armazenamento | 0,76 | 0,80 | 0,78 |
| cpu | 0,82 | 0,70 | 0,76 |
| gpu | 0,80 | 1,00 | 0,89 |
| ram | 0,82 | 0,70 | 0,76 |

- A migração para o contexto corporativo **manteve os 80% de acurácia** da Entrega 2, agora com o **dobro de casos** (80 vs 40) e classes balanceadas (contra 14×7 na base antiga);
- A classe **`gpu` acerta 100%** dos casos (revocação 1,00), refletindo o padrão causa-efeito espelhado do dataset de FPS (carga gráfica + GPU insuficiente → gargalo de GPU), transplantado para CAD, design e ML;
- Os **erros se concentram nos casos deliberadamente ambíguos** (ex.: `consulta_bd_lenta`, que pode ser disco, RAM ou CPU), em que sintomas idênticos só se distinguem pela telemetria — exatamente o comportamento esperado de um sistema RBC.

## ▶️ Como executar

### Google Colab (recomendado — sem instalar nada)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/daniSepeda/identificador-gargalos-hardware-ia/blob/main/notebooks/checkpoint_experimentos.ipynb)

Clique no badge acima e, no Colab, use **Ambiente de execução → Executar tudo**. O notebook baixa a base de casos corporativa automaticamente do GitHub.

### Localmente

```bash
pip install -r requirements.txt
jupyter notebook notebooks/checkpoint_experimentos.ipynb
```
