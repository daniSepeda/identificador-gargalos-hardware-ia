# Proposta de Projeto - Inteligência Artificial

**Título:** Identificador de Gargalos e Recomendador de Upgrades de Hardware

**Equipe:** Daniela Marques Haber Sepeda; Geovanni Rodrigues da Silva; Maria Fernanda Fernandes de Souza Gonçalves; Miguel Peres Lobo.

## 1. Descrição do problema

A escolha de upgrades de hardware costuma exigir análise técnica de sintomas, componentes instalados, perfil de uso e limitações da máquina. Usuários podem perceber lentidão no boot, travamentos em multitarefa, baixo desempenho em jogos, demora em programas pesados ou falta de espaço, mas nem sempre conseguem identificar se o gargalo está em armazenamento, memória RAM, processador, placa de vídeo ou outro componente. Essa incerteza pode levar a compras inadequadas, desperdício de recursos e manutenção pouco eficiente.

## 2. Fonte de dados pretendida

Será estruturado um dataset próprio com casos históricos conhecidos de máquinas e recomendações de upgrade. Cada caso deve conter sintomas observados, configuração atual, perfil de uso, componente identificado como gargalo e solução recomendada. Exemplos: notebook com boot muito lento e armazenamento limitado, com solução de instalação de SSD NVMe; computador com lentidão em multitarefa, com solução de aumento de memória RAM; máquina com baixo desempenho em jogos, com recomendação de GPU compatível. A base poderá ser complementada com especificações públicas de hardware e exemplos técnicos documentados.

## 3. Abordagem técnica

O foco da ementa será Raciocínio Baseado em Casos (RBC). O sistema representará cada computador como um caso com variáveis como tipo de armazenamento, quantidade de RAM, uso de CPU, uso de disco, tipo de aplicação e sintomas relatados. Ao receber um novo caso, o algoritmo calculará a similaridade com os casos históricos usando métricas matemáticas, como K-Nearest Neighbors (KNN). Os casos mais próximos serão recuperados e a solução será adaptada para gerar uma recomendação de upgrade coerente com a necessidade e com a configuração analisada.

## 3.1 Sobre a abordagem RBC

O RBC é uma abordagem de inteligencia artificial que busca resolver novos problemas com base em problemas anteriores, comparando-os e adaptando a resolução com base nisso, muito inspirado no raciocínio humano para solucionar problemas. Para tanto, o RBC segue as seguintes etapas, em ordem:

1. **Retrieve:** O sistema, ao detectar um novo problema, busca na memória por problemas antigos similares ou identicos.
2. **Reuse:** O sistema utiliza a solução para o problema antigo e adapta de modo a solucionar o novo. Caso o problema anterior seja identico ao atual, o sistema apenas usa da mesma resolução feita anteriormente.
3. **Revise:** O sistema, depois de aplicar a solução, monitora a máquina para analisar se ela está funcionando corretamente e se o problema foi devidamente sanado.
4. **Retain:** O sistema salva a solução aplicada para caso uma máquina tenha um problema semelhante no futuro, aprendendo e aprimorando a cada resolução.

## 3.2 Sobre o algoritmo KNN (K-Nearest Neighbors)
Para fazer a etapa de *Retrieve* (Recuperação) do RBC funcionar na prática, o projeto vai utilizar o algoritmo KNN (K-Nearest Neighbors). A ideia é usar esse modelo de aprendizado supervisionado para calcular o nível de similaridade entre os computadores. Basicamente, ele avalia um problema novo olhando para os registros que estão matematicamente mais próximos dele no nosso histórico.

O funcionamento do KNN para gerar as recomendações vai seguir esta lógica:

- **Conversão dos dados:** As características da máquina (como quantidade de memória RAM e tipo de armazenamento) e os sintomas que o usuário relatar são transformados em números para o sistema conseguir ler.
- **Cálculo da distância:** Quando entra um caso novo, o algoritmo faz um cálculo matemático (como a distância Euclidiana, por exemplo) para medir o "espaço" entre o perfil desse computador atual e os casos que já estão na base.
- **Encontrando os vizinhos (K):** Em seguida, o sistema filtra os "K" registros que tiveram a menor distância. Esse valor de "K" é simplesmente a quantidade de máquinas semelhantes que queremos analisar de uma vez (por exemplo, puxar os 3 ou 5 computadores que apresentaram o cenário mais parecido).
- **Definição do upgrade:** Olhando para esses vizinhos mais próximos, o sistema verifica qual solução se repetiu mais. Se na maioria desses casos parecidos o gargalo foi resolvido colocando um SSD NVMe, essa será a recomendação final adaptada para o usuário.

## 4. Resultado esperado

Espera-se entregar um protótipo em Google Colab capaz de receber dados de uma máquina ou cenário de uso, comparar com a base de casos históricos e retornar uma recomendação justificada de upgrade. O resultado deve indicar o provável gargalo, sugerir o componente mais adequado e explicar quais casos semelhantes sustentaram a recomendação, tornando o processo mais claro para usuários e técnicos.
