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

O projeto utilizará uma base de casos históricos com exemplos de computadores, sintomas observados, componentes instalados e solução adotada. Para cada novo caso, o sistema calcula a similaridade com registros anteriores usando métricas matemáticas, como **K-Nearest Neighbors (KNN)**, recupera os casos mais próximos e adapta a recomendação para a máquina analisada.

## 📁 Entregas

### Entrega 1 — Proposta (28/05)

- `docs/Proposta-IA.pdf`: proposta inicial de 1 página.
- `docs/proposta.md`: versão editável da proposta.

### Entrega 2 — Checkpoint (18/06)

- `data/base_casos.csv`: base de casos históricos estruturada pela equipe (40 casos com configuração, perfil de uso, sintomas, gargalo identificado e solução adotada).
- `notebooks/checkpoint_experimentos.ipynb`: primeiros experimentos — etapas *Retrieve* (KNN com distância euclidiana) e *Reuse* (votação majoritária) do ciclo RBC, avaliação inicial por validação leave-one-out (acurácia de 80% com k=3) e dificuldades encontradas.
- `requirements.txt`: dependências do projeto.

## ▶️ Como executar

```bash
pip install -r requirements.txt
jupyter notebook notebooks/checkpoint_experimentos.ipynb
```

O notebook também pode ser aberto diretamente no **Google Colab** (fazer upload de `data/base_casos.csv` ou ajustar o caminho do CSV).
