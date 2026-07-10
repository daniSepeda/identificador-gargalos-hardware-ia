# PRD — Base de Casos "Gargalos de Hardware em Ambientes Corporativos"

**Projeto:** Identificador de Gargalos e Recomendador de Upgrades de Hardware
**Disciplina:** Inteligência Artificial — Prof. Adolfo Colares — UNIFAP — 2026.1
**Equipe:** Daniela Marques Haber Sepeda · Geovanni Rodrigues da Silva · Maria Fernanda Fernandes de Souza Gonçalves · Miguel Peres Lobo
**Versão:** 1.0 — Repriorização do escopo para foco corporativo (substitui a base `base_casos.csv` da Entrega 2)

---

## 1. Objetivo

Redesenhar a base de casos do sistema RBC/KNN, migrando o foco de **uso doméstico/gamer** para **ambientes corporativos** (escritórios, estações de trabalho, servidores, virtualização), mantendo a técnica de gargalos e reaproveitando a estrutura e a metodologia validadas na Entrega 2 (40 casos, 80% de acurácia com k=3).

**Fora do escopo como *alvo*:** perfis e sintomas exclusivamente de jogos (`fps_baixo`, `carregamento_lento_jogos`).
**Dentro do escopo como *insumo de construção*:** o dataset de FPS em jogos é reaproveitado — não pelo conteúdo, mas pelo **padrão estrutural** que ele representa (config de hardware + tipo de carga de trabalho → métrica de desempenho), replicado para cargas de trabalho corporativas (renderização CAD, consulta a banco de dados, processamento em lote, virtualização).

---

## 2. Problema e motivação

A base atual modela bem cenários de consumidor final (notebook de estudante, desktop gamer), mas uma empresa toma decisões de upgrade com critérios diferentes: **criticidade do negócio, custo de aquisição, número de usuários afetados e tipo de carga de trabalho** (ofimática, banco de dados, virtualização, engenharia). Adaptar a base para esse contexto torna o projeto mais robusto tecnicamente (mais classes de uso, telemetria mais realista) e mais defensável como estudo de caso aplicado.

---

## 3. Personas / cenários corporativos cobertos

| Perfil de uso (`perfil_carga`) | Exemplos de máquina | Sintomas típicos |
|---|---|---|
| `ofimatica_administrativa` | desktop/notebook corporativo | boot lento, travamento com várias abas/planilhas |
| `desenvolvimento_software` | estação de trabalho / notebook dev | build lento, IDE travando, VM local lenta |
| `banco_de_dados` | servidor de BD | consultas lentas, timeout, fila de queries |
| `servidor_aplicacao_web` | servidor | latência alta sob carga, timeout de requisições |
| `virtualizacao_vdi` | servidor / hypervisor | contenção de VM, lentidão para múltiplos usuários |
| `engenharia_cad` | estação de trabalho gráfica | renderização/simulação lenta |
| `design_grafico_marketing` | estação de trabalho gráfica | exportação de vídeo/imagem lenta |
| `atendimento_cliente` | desktop de call center | lentidão em sistema de tickets/CRM, muitas janelas abertas |
| `ciencia_de_dados_ml` | estação de trabalho / servidor | treinamento de modelo lento, RAM estourando |
| `financeiro_erp` | desktop | lentidão ao gerar relatórios/fechamentos no ERP |

Isso substitui os antigos `escritorio`, `estudo`, `jogos`, `edicao_video` por categorias de carga de trabalho corporativa, mantendo `programacao` como `desenvolvimento_software`.

---

## 4. Fontes usadas como espelho (o que foi e o que NÃO foi aproveitado)

| # | Fonte | O que foi espelhado | O que **não** foi usado |
|---|---|---|---|
| 1 | **Achieved FPS in Video Games** (Kaggle, kritikseth) — [link](https://www.kaggle.com/datasets/kritikseth/achieved-frames-per-second-fps-in-video-games) | O **padrão estrutural** "config de CPU+GPU + tipo de carga → métrica de desempenho contínua", reaplicado a cargas corporativas (tempo de render, tempo de query, throughput de VM) | Os valores de FPS, os jogos, e qualquer rótulo de sintoma de jogo |
| 2 | **UCI Computer Hardware** (id 29, CC BY 4.0) — [link](https://archive.ics.uci.edu/dataset/29/computer+hardware) | O conceito de representar cada máquina por um **score de desempenho combinado** (equivalente ao PRP/ERP do dataset), inspirando o campo numérico `cpu_score` além da categoria ordinal | Os 209 registros originais (hardware de 1987, obsoleto) |
| 3 | **GPU Benchmarks Compilation** (Kaggle/alanjo, PassMark + Geekbench) — [link](https://www.kaggle.com/datasets/alanjo/gpu-benchmarks) e **CPU Specifications Dataset** (Kaggle/lincolnzh) | Faixas realistas de score de benchmark (G3D Mark / CPU Mark) usadas para calibrar o campo numérico `cpu_score`/`gpu_score`, substituindo a escala puramente ordinal (antiga/intermediária/recente) | Importação literal linha a linha; usados só como referência de faixas de valores |
| 4 | **pc-part-dataset** (PCPartPicker, GitHub/docyx) — [link](https://github.com/docyx/pc-part-dataset) | Faixas de preço realistas de mercado para o novo campo `custo_estimado_solucao` (relevante para decisão de compra corporativa) | Peças voltadas a consumidor gamer (gabinetes RGB, etc.) |
| 5 | **Laptop Specifications & Prices** (Kaggle) | Configurações plausíveis de notebooks de linha corporativa (RAM, armazenamento, CPU) para ancorar os casos de `notebook_corporativo` em valores de mercado reais, em vez de inventados | Notebooks gamers/consumo geral fora do perfil corporativo |
| 6 | **Numenta Anomaly Benchmark — NAB** (AWS CloudWatch CPU/disk) — [link](https://github.com/numenta/NAB) | O **padrão de telemetria realista de servidores** (picos e patamares de uso de CPU/disco em infraestrutura real) usado para calibrar os campos `uso_cpu_pct`/`uso_disco_pct` em casos de servidor, em vez de números arbitrários | As séries temporais completas e os rótulos de anomalia (problema diferente — detecção não supervisionada) |
| 7 | **psutil** (coleta própria, biblioteca Python) | Metodologia de **coleta primária**: script para medir uso real de CPU/RAM/disco em máquinas de laboratório da equipe/UNIFAP, gerando uma fração dos casos com dados 100% originais (não só espelhados) | — (fonte primária, não é um dataset de terceiros) |
| 8 | **Lohmann, Gaspary & Melchiors — CIACE (SBSeg/SBC)** — [link](https://sol.sbc.org.br/index.php/sbseg/article/view/21538) | Estrutura de caso (partes administrativa/classificatória/descritiva) e a **fórmula de similaridade ponderada por sintoma** (relevância), usada para desenhar o esquema de colunas e o mecanismo de pesos do próximo passo | Não é dataset — é referência metodológica de esquema, listada aqui porque molda a estrutura da tabela |

---

## 5. Esquema de dados (schema) proposto

```
id_caso                 int, chave única
tipo_maquina             {desktop_escritorio, notebook_corporativo, servidor, estacao_trabalho, maquina_virtual}
perfil_carga             {ofimatica_administrativa, desenvolvimento_software, banco_de_dados,
                           servidor_aplicacao_web, virtualizacao_vdi, engenharia_cad,
                           design_grafico_marketing, atendimento_cliente, ciencia_de_dados_ml, financeiro_erp}
cpu_geracao               {antiga, intermediaria, recente}      # ordinal, mantido da v1
cpu_score                 int (0-100, normalizado)               # NOVO — espelhado das fontes 2 e 3
nucleos_cpu                int
ram_gb                     int
tipo_armazenamento         {HDD, SSD_SATA, SSD_NVMe}
gpu                        {integrada, dedicada_baixa, dedicada_media, dedicada_alta}
gpu_score                  int (0-100, normalizado)               # NOVO — espelhado da fonte 3
sintoma_principal           # lista corporativa (seção 6)
uso_cpu_pct / uso_ram_pct / uso_disco_pct   int (0-100)          # calibrados com padrão da fonte 6
criticidade_negocio         {baixa, media, alta}                  # NOVO — quantos usuários/processos dependem da máquina
gargalo                     {cpu, ram, gpu, armazenamento}
solucao_recomendada         texto livre curto
custo_estimado_solucao      faixa em R$ (opcional / v2)           # NOVO — espelhado da fonte 4
```

---

## 6. Sintomas corporativos (substituem os de jogos)

`boot_lento` · `travamento_multitarefa` · `lentidao_programas_pesados` · `lentidao_geral` · `falta_espaco` · `consulta_bd_lenta` · `timeout_aplicacao_web` · `contencao_maquina_virtual` · `renderizacao_cad_lenta` · `exportacao_video_lenta` · `treinamento_modelo_lento` · `relatorio_erp_lento`

`fps_baixo` e `carregamento_lento_jogos` **saem** da lista de rótulos-alvo (mas seu padrão de causa-efeito com GPU permanece útil para os casos de `engenharia_cad` e `ciencia_de_dados_ml`, onde GPU também é gargalo comum).

---

## 7. Pipeline de tratamento de dados

```
[1] EXTRAÇÃO           → baixar/consultar as fontes da seção 4 (CSV do Kaggle, JSON do pc-part-dataset,
                          CSV do NAB, coleta psutil em máquinas próprias)
        ↓
[2] LIMPEZA             → remover duplicatas e nulos; padronizar unidades (GHz, GB, R$);
                          normalizar nomes de CPU/GPU para permitir join com as tabelas de benchmark
        ↓
[3] TRANSFORMAÇÃO       → join com GPU Benchmarks Compilation / CPU specs para gerar cpu_score/gpu_score;
                          mapear perfis de uso doméstico → perfis corporativos equivalentes onde aplicável;
                          converter séries do NAB em estatísticas resumo (pico, patamar sustentado) por cenário
        ↓
[4] ROTULAGEM           → atribuição manual de gargalo + solução por caso, seguindo regras de decisão
                          (ex.: uso_disco_pct ≥ 90% sustentado + tipo_armazenamento=HDD → gargalo=armazenamento),
                          validada por pelo menos 2 integrantes da equipe (dupla checagem)
        ↓
[5] ANONIMIZAÇÃO        → para dados de coleta própria (psutil em máquinas reais): remover hostname, IP,
                          usuário — atender princípios da LGPD já que a base passa a representar contexto
                          corporativo, mesmo em protótipo acadêmico
        ↓
[6] BALANCEAMENTO       → amostragem estratificada por classe de gargalo, alvo de 20-25 casos por classe
                          (cpu/ram/gpu/armazenamento), corrigindo o desbalanceamento já detectado na v1
                          (armazenamento=14 vs cpu=7)
        ↓
[7] VALIDAÇÃO           → checagem de schema (tipos, domínios de categoria, faixas numéricas);
                          checagem de duplicatas; leave-one-out KNN (k=1,3,5,7) como smoke test de qualidade,
                          igual ao usado na Entrega 2
        ↓
[8] VERSIONAMENTO       → data/base_casos_corporativa_v1.csv + CHANGELOG.md descrevendo diffs em relação
                          à base_casos.csv original
```

---

## 8. Escopo para hoje (MVP) vs. próxima iteração

**MVP — hoje (09/07):**
- Colunas `cpu_geracao`, `nucleos_cpu`, `ram_gb`, `tipo_armazenamento`, `gpu`, `perfil_carga`, `sintoma_principal`, `uso_cpu_pct/ram/disco`, `gargalo`, `solucao_recomendada` — reaproveitando o pipeline de vetorização já validado (KNN + MinMaxScaler) do notebook atual.
- 60–80 casos corporativos, substituindo os de jogos, mantendo os demais.
- Passos [1]-[4] e [7] do pipeline.

**v2 — roadmap (pós-entrega):**
- `cpu_score`/`gpu_score` numéricos (join com benchmarks reais).
- `criticidade_negocio` e `custo_estimado_solucao` — adicionam a dimensão de priorização/custo-benefício que mais diferencia uma recomendação corporativa de uma doméstica.
- Coleta real via `psutil` em máquinas de laboratório.
- Passo [5] (anonimização) só se dados reais de terceiros forem incorporados.

---

## 9. Critérios de aceitação

- Nenhuma coluna com valores nulos.
- Todas as categorias pertencem ao domínio fechado definido na seção 5 (sem valores fora do dicionário, para evitar o bug de categoria não vista já identificado no notebook atual).
- Pelo menos 4 casos por combinação (`perfil_carga` × `gargalo`) mais frequente, para o KNN ter vizinhos relevantes.
- Acurácia leave-one-out ≥ 75% com k=3 (baseline: 80% obtido na base atual) — se cair muito abaixo, revisar rotulagem antes de seguir.

## 10. Riscos e limitações

- Rotulagem manual continua sendo o gargalo metodológico central (nenhuma fonte pública tem o rótulo pronto) — mitigado por dupla checagem.
- Poucos dias para atingir 60-80 casos com qualidade — priorizar `perfil_carga` mais comuns (ofimática, dev, BD) e deixar CAD/ciência de dados como classes menores, mas presentes.
- `custo_estimado_solucao` depende de preços de mercado que mudam rápido — se entrar no MVP, marcar explicitamente a data de referência dos preços.

## 11. Referências completas

1. Kaggle — Achieved Frames per Second (FPS) in Video Games: https://www.kaggle.com/datasets/kritikseth/achieved-frames-per-second-fps-in-video-games
2. UCI ML Repository — Computer Hardware (id 29): https://archive.ics.uci.edu/dataset/29/computer+hardware
3. Kaggle — GPU Benchmarks Compilation: https://www.kaggle.com/datasets/alanjo/gpu-benchmarks
4. GitHub docyx/pc-part-dataset: https://github.com/docyx/pc-part-dataset
5. GitHub numenta/NAB: https://github.com/numenta/NAB
6. Lohmann, S.; Gaspary, L. P.; Melchiors, C. "Avaliação do Emprego de Raciocínio Baseado em Casos para Identificar Cenários de Intrusão em Logs de Firewalls". V SBSeg, 2005, pp. 298–310. https://sol.sbc.org.br/index.php/sbseg/article/view/21538
