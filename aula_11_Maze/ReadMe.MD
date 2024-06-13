# Maze Game
Encontrei um código excelente para gerar labirintos aleatórios, com entrada
e saída válidas. https://github.com/OrWestSide/python-scripts/blob/master/maze.py

O jogo utiliza um algoritmo chamado 'Algoritmo de Prim' para desenhar o labirinto.
https://www.ime.usp.br/~pf/analise_de_algoritmos/aulas/MST-prim.html

1. Imaginando o terreno como uma grande folha de papel quadriculado, iniciamos o processo com todas
as células vazias.
2. Escolhemos uma posição do quadriculado aleatoriamente, e essa vai ser a entrada do nosso labirinto.
3. Colocamos paredes em volta dessa entrada.
4. Temos uma lista de paredes que cercam o caminho atual. Escolhemos uma dessas paredes aleatoriamente.
5. Verificamos se a quadrícula do outro lado dessa parede ainda está "intacta" (não visitada). Se estiver, verificamos quantas quadrículas ao redor dessa nova quadrícula já foram convertidas em caminhos.
6. Se a nova quadrícula tiver menos de duas quadrículas vizinhas já convertidas em caminhos, quebramos a parede e transformamos essa nova quadrícula em um caminho.
7. Adicionamos as novas paredes ao redor dessa nova quadrícula à nossa lista de paredes.
8. Repetimos o processo de escolher uma parede aleatoriamente e tentar convertê-la em um caminho, seguindo as regras acima, até que todas as paredes na lista tenham sido verificadas.
9. Por fim, depois que todas as paredes foram verificadas e convertidas quando possível, transformamos todas as quadrículas ainda intactas em paredes permanentes.

Então utilizei as rotinas auxiliares para detectar as paredes do labirinto e a saída.

Uma possibilidade interessante seria criar um adversário, que persegue o jogador 
ou que tenta sair primeiro do labirinto.

A pontuação pode ser dada por pontos. Ou por contagem regressiva.

![Maze Game](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_11_Maze/Maze.png)
