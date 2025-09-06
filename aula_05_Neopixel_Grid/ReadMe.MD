# Recriando os Clássicos

## Diagrama de Montagem para o Console
Vou padronizar a montagem do nosso sistema para que nós sigamos a pinagem da [Led Driver Board da Seeed Studio](https://wiki.seeedstudio.com/led_driver_board/).
Essa placa possui drivers de corrente que permitem que a nossa matriz de Leds funcione em brilho máximo.

Para essa placa, as conexões vão ser as seguintes:
Tela Neopixel
Matriz = board.A0 (Energizada com 5V)

Os módulos abaixo, serão energizados com 3.3V:
Joystick
Eixo X = board.A1
Eixo Y = board.A2
Botão  = board.D6

Som
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

# Limpa a tela 
screen.fill(0)
# E ai temos vários métodos que servem para desenhar nessa tela
print (dir (screen))
# Copiar o Arquivo font5x8.bin para a raiz
# Ou tem esse erro: OSError: [Errno 2] Este arquivo/diretório não existe: font5x8.bin
screen.text ("HI", 1, 1, 0xFF0000)
#screen.rect (2,2, 5,5, 0xFF0000) # A cor é passada em Hexadecimal 0xRRGGBB
screen.display()
```

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

joystick_x = AnalogIn(board.A1)
joystick_y = AnalogIn(board.A2)

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

pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height * num_tiles, # dont forget to multiply for num_tiles
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

Finalmente, podemos fazer a nossa lousa mágica. Para desenhar na tela, movemos o joystick.
Para apagar, pressione o botão.

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
    rotation = 0
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

   





