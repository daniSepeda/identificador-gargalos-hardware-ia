# Proposta de Projeto - Inteligência Artificial

**Título:** Identificador de Gargalos e Recomendador de Upgrades de Hardware

**Equipe:** Daniela Marques Haber Sepeda; Geovanni Rodrigues da Silva; Maria Fernanda Fernandes de Souza Gonçalves; Miguel Peres Lobo.

## Descrição do problema

A escolha de upgrades de hardware costuma exigir análise técnica de sintomas, componentes instalados, perfil de uso e limitações da máquina. Usuários podem perceber lentidão no boot, travamentos em multitarefa, baixo desempenho em jogos, demora em programas pesados ou falta de espaço, mas nem sempre conseguem identificar se o gargalo está em armazenamento, memória RAM, processador, placa de vídeo ou outro componente. Essa incerteza pode levar a compras inadequadas, desperdício de recursos e manutenção pouco eficiente.

## Fonte de dados pretendida

Será estruturado um dataset próprio com casos históricos conhecidos de máquinas e recomendações de upgrade. Cada caso deve conter sintomas observados, configuração atual, perfil de uso, componente identificado como gargalo e solução recomendada. Exemplos: notebook com boot muito lento e armazenamento limitado, com solução de instalação de SSD NVMe; computador com lentidão em multitarefa, com solução de aumento de memória RAM; máquina com baixo desempenho em jogos, com recomendação de GPU compatível. A base poderá ser complementada com especificações públicas de hardware e exemplos técnicos documentados.

## Abordagem técnica

O foco da ementa será Raciocínio Baseado em Casos (RBC). O sistema representará cada computador como um caso com variáveis como tipo de armazenamento, quantidade de RAM, uso de CPU, uso de disco, tipo de aplicação e sintomas relatados. Ao receber um novo caso, o algoritmo calculará a similaridade com os casos históricos usando métricas matemáticas, como K-Nearest Neighbors (KNN). Os casos mais próximos serão recuperados e a solução será adaptada para gerar uma recomendação de upgrade coerente com a necessidade e com a configuração analisada.

## Resultado esperado

Espera-se entregar um protótipo em Google Colab capaz de receber dados de uma máquina ou cenário de uso, comparar com a base de casos históricos e retornar uma recomendação justificada de upgrade. O resultado deve indicar o provável gargalo, sugerir o componente mais adequado e explicar quais casos semelhantes sustentaram a recomendação, tornando o processo mais claro para usuários e técnicos.
