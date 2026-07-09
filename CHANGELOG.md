# CHANGELOG

## base_casos_corporativa_v1.csv — 09/07/2026

Nova base oficial do projeto, substituindo `base_casos.csv` (Entrega 2) conforme o PRD
(`docs/PRD_base_casos_corporativa.md`). A base antiga permanece no repositório como registro histórico.

### Diferenças em relação a `base_casos.csv`

| Aspecto | base_casos.csv (v1, Entrega 2) | base_casos_corporativa_v1.csv |
|---|---|---|
| Foco | Doméstico/gamer | Corporativo (escritórios, servidores, virtualização) |
| Casos | 40 | 80 |
| Balanceamento por gargalo | armazenamento=14, gpu=10, ram=9, cpu=7 | 20 × 20 × 20 × 20 |
| Coluna de perfil | `perfil_uso` (escritorio, estudo, programacao, jogos, edicao_video) | `perfil_carga` (10 perfis corporativos) |
| `tipo_maquina` | notebook, desktop | desktop_escritorio, notebook_corporativo, servidor, estacao_trabalho, maquina_virtual |
| Sintomas | 8, incluindo `fps_baixo` e `carregamento_lento_jogos` | 12, todos corporativos (sem sintomas de jogos) |
| RAM | 4–32 GB | 4–128 GB (servidores e estações) |
| Núcleos | 2–8 | 2–24 |

### Colunas

- **Mantidas:** id_caso, tipo_maquina, cpu_geracao, nucleos_cpu, ram_gb, tipo_armazenamento, gpu,
  sintoma_principal, uso_cpu_pct, uso_ram_pct, uso_disco_pct, gargalo, solucao_recomendada.
- **Renomeada:** perfil_uso → **perfil_carga** (novos domínios).
- **Adiadas para a v2 (roadmap do PRD):** cpu_score, gpu_score, criticidade_negocio, custo_estimado_solucao.

### Sintomas

- **Removidos:** fps_baixo, carregamento_lento_jogos, render_lento (substituído pelos específicos abaixo).
- **Mantidos:** boot_lento, travamento_multitarefa, lentidao_programas_pesados, lentidao_geral, falta_espaco.
- **Adicionados:** consulta_bd_lenta, timeout_aplicacao_web, contencao_maquina_virtual,
  renderizacao_cad_lenta, exportacao_video_lenta, treinamento_modelo_lento, relatorio_erp_lento.

### Metodologia de construção

- Rotulagem manual por regras de decisão (ex.: uso_disco_pct ≥ 95% sustentado + HDD → armazenamento;
  uso_ram_pct ≥ 93% → ram; uso_cpu_pct ≥ 89% → cpu; GPU insuficiente para a carga com CPU/RAM folgadas → gpu).
- Valores calibrados espelhando padrões de datasets públicos (benchmarks de CPU/GPU, telemetria NAB,
  especificações de notebooks corporativos) — detalhes na seção "fontes espelhadas" do README e na seção 4 do PRD.
- Casos deliberadamente ambíguos (mesmo sintoma, gargalos diferentes) para exigir uso da telemetria pelo KNN.

### Validação (critérios de aceitação da seção 9 do PRD)

- Sem valores nulos; todas as categorias nos domínios fechados; sem duplicatas. ✅
- Combinações (perfil_carga × gargalo) mais frequentes com ≥ 4 casos (máx.: engenharia_cad × gpu = 8). ✅
- Balanceamento 20–25 casos por classe: exatamente 20 por gargalo. ✅
- Acurácia leave-one-out (mesma vetorização da Entrega 2): **k=3 = 80,0%** (critério: ≥ 75%);
  k=1 = 83,8%; k=5 = 80,0%; k=7 = 76,2%. ✅
