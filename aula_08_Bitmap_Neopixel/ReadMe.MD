# Recriando os Clássicos

# Esquema de montagem para o nosso Console Arcade
![Esquema de Montagem](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_08_Bitmap_Neopixel/images/Xiao_Neopixel_bb.png?raw=true)

Eu comecei a programar computadores em 1984, quando eu tinha 10 anos. 
Naquela época apareciam os primeiros microcomputadores domésticos e nas livrarias e bancas de jornal, começaram a pipocar livros e revistas
sobre o assunto.

Eu tinha todos os livros dessa coleção aqui: https://usborne.com/gb/books/computer-and-coding-books

E essa coleção aqui completa: https://datassette.org/revistas/input-0

E essa revista, eu comprava quase todo mês: https://datassette.org/revistas/micro-sistemas

Para conseguir jogar alguma coisa no computador, você precisava digitar várias linhas de comando em Basic.
Isso me ensinou muito sobre lógica e sobre como os computadores se organizam.

A Kari é uma garota inglesa que adora Retrocomputação. Nos vídeos dela, é possível ver como é que a gente
programava na época:
https://www.youtube.com/watch?v=3kdM9wyglnw&t=735s&ab_channel=Kari

Tem até um exemplo, com os códigos dos livros da Usborne:
https://www.youtube.com/watch?v=Oo47qPvs3HQ&t=0s&ab_channel=Kari

E se você quiser dar uma conferida nesses livros, o link é esse aqui:
https://github.com/djairjr/oficina_CircuitPython/tree/main/old_osbourne_games

Meu melhor computador na época, o MSX Hotbit HB8000 https://pt.wikipedia.org/wiki/HotBit_HB-8000, 
possuia um processador Z80 que funcionava em 3,58Mhz, memória RAM de 64Kb, Video Ram de 16KB 
e seu sistema operacional ficava numa memória ROM de 32Kb compartilhado com um interpretador BASIC. 
A resolução de vídeo era de 256x192 (modo gráfico), mas muitos jogos rodavam em 64x48 (modo caractere).

As nossas Seeed Xiao ou Raspberry Pi Pico rodam num dual core Arm Cortex M0+, com 133Mhz, 
com 264kB de sRam e 2Mb de memória flash (onde fica nosso Circuitpython e o USB disk).

Já estão rolando experiências com ela, rodando vídeo em DVI e alguns jogos.
https://learn.adafruit.com/picodvi-arduino-library-video-out-for-rp2040-boards/overview

Já existem várias soluções de jogos, utilizando telas TFT SPI, como as que utilizamos lá no Sesc Santana.
https://blog.adafruit.com/2021/11/03/new-product-pimoroni-picosystem-rp2040-handheld-gaming-system-pim559/

O desafio dessa oficina é portar alguns clássicos dos Arcades para essa plaquinha, usando uma tela de 32x16 pixels
feita com Fitas de Led, numa configuração um pouco diferente da habitual.
![Painel com duas matrizes 8x32 em 16x32](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_06_Neopixel/images/Arranjo%20Necessario.png)

Será que vai dar certo?

Todos os exemplos nesta pasta vão utilizar as minhas bibliotecas customizadas, contidas nesta pasta:
https://github.com/djairjr/oficina_CircuitPython/tree/main/aula_08_Bitmap_Neopixel/libraries 

As imagens da experiência Bitmap Animado estão aqui:
https://github.com/djairjr/oficina_CircuitPython/tree/main/aula_08_Bitmap_Neopixel/images

E as fontes Bitmap aqui:
https://github.com/djairjr/oficina_CircuitPython/tree/main/aula_08_Bitmap_Neopixel/fonts

