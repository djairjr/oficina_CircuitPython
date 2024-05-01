# Neopixels e Matrizes de Led RGB

À medida que os seus projetos vão se tornando mais e mais complexos, os pinos da sua controladora vão escasseando.
E uma das alternativas mais bacanas que eu encontrei para fazer indicação de status, decoração, e comunicação
simples foram as fitas de led Neopixel.

O melhor guia que eu conheço para começar a mexer com essas fitas é o "The Magic of Neopixels" - https://learn.adafruit.com/adafruit-neopixel-uberguide

Lá você vai ter todos os cuidados e observações relevantes. 

Vale dizer que as fitas consomem bastante corrente e você vai perceber que em todos os códigos o brilho está definido para 10% apenas.

Isso é porque a gente está usando a corrente da USB do nosso computador, sem fonte externa. Se você alimentar as fitas led com uma 
fonte externa, lembre-se de ao menos interligar o pino GND entre a fonte externa e a alimentação via USB da controladora. Você também pode alimentar a sua Raspberry Pi Pico na mesma fonte conectando diretamente os pinos 5V e GND à saída da fonte.

Os códigos que eu estou compartilhando nesta aula vão ser a matéria inicial da próxima oficina, que vai acontecer no Sesc 24 de maio, a partir do dia 9/05.

O desafio da próxima oficina vai ser recriar alguns clássicos dos Arcades usando matrizes de fita led como display. As bibliotecas disponíveis para usar as fitas led como display ainda não dispõem de algumas funcionalidades, então eu estou fazendo as customizações necessárias para a gente poder utilizar como display de jogo.

Serão três "consoles" com alguns jogos: Snake, Minefield e Tetris, inicialmente. Utilizaremos dois painéis de 8x32 Leds, formando um painel de 16x32 para cada um dos jogos. Além disso, vamos trabalhar com o Seeed Xiao RP2040, porque o tamanho reduzido vai fazer diferença na hora de embarcar o projeto. Buzzer, Módulo de Joystick e Display de Sete Segmentos com 4 dígitos finalizam o projeto.

Os arquivos tilegrid.py e tile_framebuf.py são as minhas adaptações de duas bibliotecas da Adafruit. Além disso, estou tentando trabalhar numa versão da biblioteca BMPReader, porque preciso transformar alguns sprites BMP em pixels Neopixel. Estou deixando o código default compartilhado, mas vai ser atualizado à medida que eu for avançando na idéia.

