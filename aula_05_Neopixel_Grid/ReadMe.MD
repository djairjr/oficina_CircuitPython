# Recriando os Clássicos

## Diagrama de Montagem para o Console
Vou padronizar a montagem do nosso sistema para que nós sigamos a pinagem da [Led Driver Board da Seeed Studio](https://wiki.seeedstudio.com/led_driver_board/).
Essa placa possui drivers de corrente que permitem que a nossa matriz de Leds funcione em brilho máximo.

Para essa placa, as conexões vão ser as seguintes:

**Tela Neopixel**

Matriz = board.A0 (Energizada com 5V)

Os módulos abaixo, serão energizados com 3.3V:

**Joystick**

Eixo X = board.A1

Eixo Y = board.A2

Botão  = board.D6

**Som**

Buzzer = board.D7


## Criando uma função para leitura do Joystick
Os eixos X e Y do nosso Joystick analógico são dados pelas leituras de dois potenciômetros.
Nós precisamos converter os valores na faixa de 0 a 65535 para incrementos ou decrementos nas
coordenadas da tela. Para isso, vamos criar uma função chamada get_joystick.

Primeiro, vamos obter os valores mínimo e máximo dos dois potenciômetros:

```
import board, time
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn

botao = DigitalInOut (board.D6)

eixo_x = AnalogIn (board.A1)
eixo_y = AnalogIn (board.A2)

while True:
    print (eixo_x.value, eixo_y.value)
    time.sleep(0.2)
```

Movendo o Joystick para cima e para baixo, e para a esquerda e direita, devemos ter valores na faixa
de 0 a 65535. Mas como há limitações mecânicas no curso dos dois eixos, pode ser que os valores máximo
e mínimo estejam um pouco fora disso. Nos meus testes anteriores, o valor mínimo estava na faixa de 200.

A função get_joystick retorna os valores de incremento ou decremento das coordenadas x e y, em função dos valores obtidos pelos potenciômetros.

Por enquanto, nós não vamos usar essa função. Mas vamos incluí-la logo mais...

```
# Essa função retorna as coordenadas x e y do joystick
def get_joystick():
    # Returns -1 0 or 1 depending on joystick position
	# o formato de map_range (valor lido, min_lido, max_lido, min_desejado, max_desejado)
    x_coord = int (map_range (joystick_x.value, 0, 65535, - 2 , 2))
    y_coord = int (map_range (joystick_y.value, 0, 65535, - 2 , 2))
    return x_coord, y_coord
```

Nossa função vai mover os objetos numa velocidade máxima de 2 pixels em cada direção. 

## Transformando uma fita de led de 256 pixels, numa tela de 16x16 pixels.
Vamos fazer um teste para descobrir como a biblioteca Neopixel vai endereçar os Leds da nossa Matriz.
Primeiro, um pouco de matemática: nós temos um quadrado, com 16 leds de largura e 16 leds de altura.
A área preenchida por Leds vai ser igual a 16x16 = 256. Esse é o número de pixels que temos.

```
import board
import time
import neopixel

pixel_pin = board.A0
pixel_width = 16
pixel_height = 16
num_tiles = 1
num_pixels = pixel_width * pixel_height * num_tiles

print (num_pixels)

pixels = neopixel.NeoPixel(
    pixel_pin,
    num_pixels, 
    brightness=0.1,
    auto_write=False,
)

pixels.fill((0,0,0))
pixels.show()

while True:
    for idx in range(num_pixels):
        pixels[idx] = (255,0,0)
        pixels.show()
        time.sleep(0.2)
        pixels.fill((0,0,0))
        pixels.show()
        time.sleep(0.05)
```
Como você deve ter observado, o programa acima acende cada um dos Leds da nossa matriz, na cor vermelha. E vai percorrendo
a próxima posição, até chegar na última. A distribuição dos leds é em zig-zag. 
No entanto, quando vamos lidar com uma Tela, nós costumamos desenhar usando as referências de posição horizontal e vertical.
A biblioteca adafruit_pixelbuf cria esse sistema de coordenadas e também um local que armazena o próximo quadro da nossa Tela
útil para animações e mudanças rápidas.

```
import board
import time
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer

pixel_pin = board.A0
pixel_width = 16
pixel_height = 16
num_tiles = 1
num_pixels = pixel_width * pixel_height * num_tiles

pixels = neopixel.NeoPixel(
    pixel_pin,
    num_pixels, 
    brightness=0.1, # Deixe o brilho baixo para que a fonte aguente
    auto_write=False,
)

# Cada painel de Leds tem uma inicialização diferente. 
# É importante que você teste alguns parâmetros para ver se tudo está ok.

screen = PixelFramebuffer(
    pixels, # Qual objeto Neopixel vai ser a nossa tela?
    pixel_width, # A largura, em pixels
    pixel_height, # Qual a altura, em pixels...
    num_tiles, # Quantas matrizes você vai usar?
    rotation = 0, #Vai de 0 a 3, aumentando em 90 graus para cada
    reverse_x=True,# Use isso se o texto parecer espelhado no eixo horizontal

# Preenche a tela com a cor especificada.
# Para essa biblioteca, a cor não é passada como uma tupla RGB e sim como uma sequência
# de números hexadecimais (base 16). Cada cor vai variar de 0x00 a 0xFF (0x indica que o número é Hexa).
# Nesse caso, o formato é 0xRRGGBB
# Se quisermos preencher com vermelho, a cor Hexa seria 0xFF0000 
screen.fill(0) # ou screen.fill(0x000000)

# E ai temos vários métodos que servem para desenhar nessa tela
print (dir (screen))

screen.text ("HI", 1, 1, 0xFF0000) # escreve Hi, na posição 1,1
screen.rect (2,2, 5,5, 0xFF0000) # Na posição 2,2 desenha o contorno de um retangulo 5,5, na cor vermelha
screen.fill_rect(2, 2, 8, 12, 0xFF0000) # aqui, desenhamos um retângulo preenchido pela cor
screen.pixel (7,7,0x00FF00) # acende o led na posição 7,7
screen.line (0,0, 5,7, 0x0000FF) # traça uma linha da posição 0,0 até a posição 5,7 na cor azul
screen.hline(2, 3, 5, 0xFF0000) # traça uma linha horizontal de 5 pixels a partir da posição 2,3
screen.vline(2, 3, 5, 0xFF0000)# traça uma linha vertical de 5 pixels a partir da posição 2,3
screen.display()
```
## Juntando Lé com Cré
Agora, vamos usar o que aprendemos. Vamos adicionar nossa rotina get_joystick e ir movimentando
um retângulo na tela.

```
import board, time
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range

import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer

# Essa biblioteca faz umas animações com as cores muito bacanas!
from rainbowio import colorwheel

# Em alguns casos nós vamos usar a LED Driver Board da Xiao
pixel_pin = board.D0

# pixel_pin = board.D7 
pixel_width = 16
pixel_height = 16
num_tiles = 1

# Adicionando os eixos X e Y do Joystick - Lembra que são potenciômetros?
joystick_x = AnalogIn(board.A1)
joystick_y = AnalogIn(board.A2)

# Eu encontrei esses valores num teste.
minVal = 200
maxVal = 65535

trigger = DigitalInOut (board.D6)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

# Essa função retorna as coordenadas x e y do joystick
def get_joystick():
    # Returns -1 0 or 1 depending on joystick position
    x_coord = int (map_range (joystick_x.value, minVal, maxVal, - 2 , 2))
    y_coord = int (map_range (joystick_y.value, minVal, maxVal, - 2 , 2))
    return x_coord, y_coord

# Primeiro eu adiciono o objeto neopixel com num_pixels igual à largura da tela, vezes a altura vezes o número de telas
num_pixels = pixel_width * pixel_height * num_tiles

pixels = neopixel.NeoPixel(
    pixel_pin,
    num_pixels, 
    brightness=0.1,
    auto_write=False,
)

# Cria um Grid a partir da Neopixel e um Framebuffer também
screen = PixelFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation = 0, #3
    reverse_x=True,
)

# O quadrado inicia no centro da tela
old_x = pixel_width //2
old_y = pixel_height * num_tiles // 2

while True:
    # Quando apertar o botão do Joystick, apaga a tela
    if (not trigger.value):
        screen.fill (0x000000)
    else:
        # Do contrário, pega a posição x e y do joystick
        get_x, get_y = get_joystick ()
        x_pos = old_x + int (get_x)
        y_pos = old_y + int (get_y)
		
        # pinta o retangulo da tela
        screen.fill_rect (y_pos, x_pos, 2, 2, colorwheel((time.monotonic()*50)%255))
        screen.display()
        
        # Apaga o retângulo que estava desenhado na posição anterior
        if ((x_pos != old_x) or (y_pos != old_y)):
            screen.fill (0x000000)

        # Atualiza a posição
        old_x = x_pos
        old_y = y_pos
        
        # Impede que o retângulo seja desenhado para além dos limites da tela
        if (old_x < 3):
            old_x = 3
        if (old_x > pixel_width - 3):
            old_x = pixel_width - 3
        if (old_y < 3):
            old_y = 3
        if (old_y > pixel_height * num_tiles - 3):
            old_y = pixel_height * num_tiles - 3
        
```
## Desenhando na tela - Lousa Mágica
E agora, podemos fazer a nossa lousa mágica. 
Vamos usar a nossa função get_joystick para atualizar a posição do pixel de desenho
na tela e ao pressionar o botão, apagamos o desenho.

```
import board, time
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range
import neopixel
from rainbowio import colorwheel

import adafruit_rtttl
from adafruit_pixel_framebuf import PixelFramebuffer

pixel_pin = board.A0
pixel_width = 16
pixel_height = 16
num_tiles = 1

joystick_x = AnalogIn(board.A1)
joystick_y = AnalogIn(board.A2)

trigger = DigitalInOut (board.D6)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

buzzer = board.D7

pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height * num_tiles, # dont forget to multiply for num_tiles
    brightness=0.1,
    auto_write=False,
)

screen = PixelFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation = 0,
	reverse_x=True,
)

def moveSound():
    adafruit_rtttl.play (buzzer, "move:d=4,o=5,b=880:8c6")

def deleteSound():
    adafruit_rtttl.play (buzzer, "delete:d=4,o=5,b=330:8c6,8d6")

def get_joystick():
    # Returns -1 0 or 1 depending on joystick position
    x_coord = int (map_range (joystick_x.value, 200, 65535, - 2 , 2))
    y_coord = int (map_range (joystick_y.value, 200, 65535, - 2 , 2))
    return x_coord, y_coord

# Center Screen
old_x = pixel_width //2
old_y = pixel_height * num_tiles // 2
x_pos, y_pos = old_x, old_y

while True:
    if (not trigger.value):
        screen.fill (0x000000)
        deleteSound()
    else:
        x,y = get_joystick()
        x_pos = old_x + x
        y_pos = old_y + y
        if x_pos != old_x or y_pos != old_y:
            moveSound()
        screen.line (old_y, old_x, y_pos, x_pos, colorwheel((time.monotonic()*50)%255))
        screen.display()
        time.sleep(0.1)
        old_x = x_pos
        old_y = y_pos
        
        """ Tratando os limites da tela """
        if (old_x < 0):
            old_x = 0
        if (old_x > pixel_width - 1):
            old_x = pixel_width - 1
        if (old_y < 0):
            old_y = 0
        if (old_y > pixel_height * num_tiles - 1):
            old_y = pixel_height * num_tiles - 1
```
## Snake Game
Por fim, vamos fazer o jogo de Snake.

O jogo Snake é um clássico e com ele, nós vamos aprender uma das maneiras de realizar a detecção de colisões, rotina muito importante em qualquer jogo.
Nossa cobrinha é basicamente uma lista, com a cabeça sendo a primeira posição e referência para todos os movimentos. A cada vez que a serpente colide com a comida,
aumenta o comprimento, adicionando mais um elemento à lista.

Nós podemos implementar a detecção de colisão de várias maneiras. Uma delas é detectar se dois objetos estão ocupando as mesmas coordenadas na tela.

Outro modo, é detectar a cor do pixel acessado pela coordenada. Por exemplo, temos um muro de cor azul e um personagem de cor verde. O personagem se move, mas se 
na coordenada em que ele está indo houver um pixel azul, ele não avança.

Em Snake, nós vamos lidar com os dois modos. Primeiro detectar as coordenadas da comida e segundo, detectar se a serpente está batendo a cabeça no próprio corpo.

```
import board, time
import random # Para eventos aleatórios

from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range

import neopixel
from rainbowio import colorwheel

from adafruit_pixel_framebuf import PixelFramebuffer

joystick_x = AnalogIn(board.A1)
joystick_y = AnalogIn(board.A2)

trigger = DigitalInOut(board.D6)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

pixel_pin = board.A0
pixel_width = 16  
pixel_height = 16
num_tiles = 1
num_pixels = pixel_width * pixel_height * num_tiles

pixels = neopixel.NeoPixel(
    pixel_pin,
    num_pixels, 
    brightness=0.2,
    auto_write=False,
)

screen = PixelFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    rotation = 0,
    reverse_x=True
)

# A função get_direction é uma variação da get_joystick, mais útil para o jogo Snake.
# Ela compara os valores absolutos de x e y para determinar a direção do movimento.
# Sem essa implementação, a serpente colide muitas vezes com o próprio corpo.

def get_direction():
    x = int(map_range(joystick_x.value, 0, 65535, -1.5, 1.5))
    y = int(map_range(joystick_y.value, 0, 65535,  -1.5, 1.5))
    if abs(x) > abs(y):
        return (0, x)  # Horizontal Move
    else:
        return (y, 0)  # Vertical Move

# A função get_joystick foi mantida apenas para comparação das diferenças
def get_joystick():
    # Returns -1 0 or 1 depending on joystick position
    x_coord = int (map_range (joystick_x.value, 200, 65535, - 2 , 2))
    y_coord = int (map_range (joystick_y.value, 200, 65535, - 2 , 2))
    return x_coord, y_coord

def get_pixel_color(x, y):
    # Primeiro checa se as coordenadas x e y estão nos limites da tela
    if (0 <= x < screen.width) and (0 <= y < screen.height):
        # Recebe o valor da cor, na posição do pixel
        rgbint = screen.pixel(x, y)
        return (rgbint >> 16 & 0xFF, rgbint >> 8 & 0xFF, rgbint & 0xFF)

    # Return preto (0, 0, 0) se estiver fora dos limites
    return (0, 0, 0)

def check_wall(x, y, wall_color):
    # checa primeiro os limites da tela
    if x < 0 or x >= screen._width or y < 0 or y >= screen._height * screen._tile_num:
        return False
    # depois, checa as cores
    color = get_pixel_color(x, y)
    return color != wall_color

def check_color(x, y, colorcheck):
    colorcheck_rgb = ((colorcheck >> 16) & 0xFF, (colorcheck >> 8) & 0xFF, colorcheck & 0xFF)
    color = get_pixel_color(x, y)
    return color == colorcheck_rgb

# Monta o corpo da serpente no centro da tela como uma lista, com três elementos inicialmente.
# O primeiro elemento é a cabeça. E os outros dois, o corpo.
snake_body = [
    [pixel_height // 2, pixel_width // 2],
    [pixel_height // 2, pixel_width // 2 - 1],
    [pixel_height // 2, pixel_width // 2 - 2]
]

# Coloca a comida numa posição aleatória da Tela
food = [random.randint(0, pixel_height - 1), random.randint(0, pixel_width - 1)]

# Inicia sempre com a serpente se movendo da esquerda para a direita
direction = (0, 1)

def generate_food():
    global food
    while True:
        food = [random.randint(0, pixel_height - 1), random.randint(0, pixel_width - 1)]
        
        # Vê se a comida não foi gerada dentro do corpo da serpente
		# como é aleatório, pode ser que isso aconteça...
        if food not in snake_body:
		    # Se não foi gerada dentro do corpo, interrompe o loop
            break

# loop principal do jogo
while True:
    # Lê o valor da direção a partir do joystick.
    new_direction = get_direction()
    if new_direction != (0, 0) and (new_direction[0] != -direction[0] or new_direction[1] != -direction[1]):
        direction = new_direction

    # Reposiciona a cabeça segundo as novas coordenadas
    new_head = [snake_body[0][0] + direction[0], snake_body[0][1] + direction[1]]

    # Checa se o jogo acabou. A serpente chegou nos limites da tela? Ou a cabeça está em colisão com o corpo?
    if (
        new_head[0] < 0 or new_head[0] >= pixel_height  or
        new_head[1] < 0 or new_head[1] >= pixel_width or
        new_head in snake_body
    ):
		# Se isso acontece, volta para a condição inicial.
		# Que é a serpente com 3 pixels de comprimento no meio da tela
        snake_body = [
            [pixel_height // 2, pixel_width // 2],
            [pixel_height // 2, pixel_width // 2 - 1],
            [pixel_height // 2, pixel_width // 2 - 2]
        ]
    else:
	    # Senão, desenha a nova cabeça na primeira posição do corpo
		# lembrando que snake_body[0] é a cabeça atual
        snake_body.insert(0, new_head) # insere na posição 0 do corpo a nova cabeça

        # Se a serpente comeu a comida, gera nova comida
        if snake_body[0] == food: #snake_body[0] é a cabeça
            generate_food()
        else:
            snake_body.pop()

        # Sempre limpa a tela antes de desenhar o novo quadro
        screen.fill(0)
        
        # Desenha a cabeça da serpente e o corpo
        for segment in snake_body:
            screen.pixel(segment[1], segment[0], 0x00FF00)  # Snake
        
        # Desenha a comida
        screen.pixel(food[1], food[0], 0xFF0000)
        
        # Show everything
        screen.display()
        time.sleep(0.1)
```






