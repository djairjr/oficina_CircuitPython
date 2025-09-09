# Neopixel Grid - Usando Neopixel como Tela

## Diagrama de Montagem para o Console
Vou padronizar a montagem do nosso sistema para que nós sigamos a pinagem da [Led Driver Board da Seeed Studio](https://wiki.seeedstudio.com/led_driver_board/).
Essa placa possui drivers de corrente que permitem que a nossa matriz de Leds funcione em brilho máximo.

Para essa placa, as conexões vão ser as seguintes:

| Módulo       | Função      | Pino        | Tensão  |
|--------------|-------------|-------------|---------|
| Tela Neopixel| Matriz      | board.A0    | 5V      |
| Joystick     | Eixo X      | board.A1    | 3.3V    |
| Joystick     | Eixo Y      | board.A2    | 3.3V    |
| Joystick     | Botão       | board.D6    | 3.3V    |
| Som          | Buzzer      | board.D7    | 3.3V    |


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
de **0 a 65535**. Mas como há limitações mecânicas no curso dos dois eixos, pode ser que os valores máximo
e mínimo estejam um pouco fora disso. Nos meus testes anteriores, o valor mínimo estava na faixa de 200.

A função get_joystick retorna os valores de incremento ou decremento das coordenadas x e y, em função dos valores obtidos pelos potenciômetros.

Por enquanto, nós não vamos usar essa função. Mas vamos incluí-la logo mais...

```
# Essa função retorna as coordenadas x e y do joystick
def get_joystick():
    # Returns -2, -1, 0, 1 or 2 depending on joystick position
	# o formato de map_range (valor lido, min_lido, max_lido, min_desejado, max_desejado)
    x_coord = int (map_range (joystick_x.value, 0, 65535, - 2 , 2))
    y_coord = int (map_range (joystick_y.value, 0, 65535, - 2 , 2))
    return x_coord, y_coord
```

Nossa função vai mover os objetos numa velocidade máxima de 2 pixels em cada direção. 

## Entendendo a matriz de Leds
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
## Transformando a matriz de Leds em Tela
Como você deve ter observado, o programa anterior acende cada um dos Leds da nossa matriz, na cor vermelha. E vai percorrendo
a próxima posição, até chegar na última. A distribuição dos leds é em zig-zag. 
No entanto, quando vamos lidar com uma Tela, nós costumamos desenhar usando as referências de posição horizontal e vertical.
A biblioteca adafruit_pixelbuf cria esse sistema de coordenadas e também um local que armazena o próximo quadro da nossa Tela
útil para animações e mudanças rápidas.

```
import board
import time
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

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
    rotation = 0, #Vai de 0 a 3, aumentando em 90 graus para cada
	orientation = VERTICAL, # como elas estão dispostas
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
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

# Essa biblioteca faz umas animações com as cores muito bacanas!
from rainbowio import colorwheel

# Em alguns casos nós vamos usar a LED Driver Board da Xiao
pixel_pin = board.D0
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
    orientation=VERTICAL,
    rotation = 0, 
)

# O quadrado inicia no centro da tela
old_x = screen.width //2
old_y = screen.height * num_tiles // 2

while True:
    # Quando apertar o botão do Joystick, apaga a tela
    if (not trigger.value):
        screen.fill (0x000000)
    else:
        # Do contrário, pega a posição x e y do joystick
        get_x, get_y = get_joystick ()
        x_pos = old_x + int (get_x) # A coordenada x vai ser o valor anterior somado ao que obtemos do joystick
        y_pos = old_y + int (get_y) # O mesmo para a coordenada y
		
        # pinta o retangulo da tela
        screen.fill_rect (x_pos, y_pos, 2, 2, colorwheel((time.monotonic()*50)%255)) # desenho o retângulo colorido
        screen.display() # Mostro o retângulo
        
        # Apaga o retângulo que estava desenhado na posição anterior
        if ((x_pos != old_x) or (y_pos != old_y)):
            screen.fill (0x000000)

        # Atualiza a posição
        old_x = x_pos # atualizo a posição antiga, com os valores da nova
        old_y = y_pos
        
        # Impede que o retângulo seja desenhado para além dos limites da tela
        if (old_x < 3):
            old_x = 3
        if (old_x > screen.width - 3):
            old_x = screen.width - 3
        if (old_y < 3):
            old_y = 3
        if (old_y > screen.height * num_tiles - 3):
            old_y = screen.height * num_tiles - 3

        
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
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

pixel_pin = board.A0
pixel_width = 16
pixel_height = 16
num_tiles = 2

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
    pixel_width * num_tiles,
    pixel_height,
    orientation = VERTICAL,
    rotation = 0
)


def moveSound():
    adafruit_rtttl.play (buzzer, "move:d=4,o=5,b=880:8c6")

def deleteSound():
    adafruit_rtttl.play (buzzer, "delete:d=4,o=5,b=330:8c6,8d6")

def get_joystick():
    # Returns -1 0 or 1 depending on joystick position
    x_coord = int (map_range (joystick_x.value, 200, 65535, 2 , -2))
    y_coord = int (map_range (joystick_y.value, 200, 65535, 2 , -2))
    return x_coord, y_coord

# Center Screen
old_x = screen.width //2
old_y = screen.height // 2
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
        screen.line (old_x, old_y, x_pos, y_pos, colorwheel((time.monotonic()*50)%255))
        screen.display()
        time.sleep(0.1)
        old_x = x_pos
        old_y = y_pos
        
        """ Tratando os limites da tela """
        if (old_x < 0):
            old_x = 0
        if (old_x > screen.width - 1):
            old_x = screen.width - 1
        if (old_y < 0):
            old_y = 0
        if (old_y > screen.height - 1):
            old_y = screen.height - 1    
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

from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

joystick_x = AnalogIn(board.A1)
joystick_y = AnalogIn(board.A2)

trigger = DigitalInOut(board.D6)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

pixel_pin = board.A0
pixel_width = 16  
pixel_height = 16
num_tiles = 2
num_pixels = pixel_width * pixel_height * num_tiles

pixels = neopixel.NeoPixel(
    pixel_pin,
    num_pixels, 
    brightness=0.2,
    auto_write=False,
)

screen = PixelFramebuffer(
    pixels,
    pixel_width * num_tiles,
    pixel_height,
    orientation = VERTICAL,
    rotation = 0
)

# A função get_direction é uma variação da get_joystick, mais útil para o jogo Snake.
# Ela compara os valores absolutos de x e y para determinar a direção do movimento.
# Sem essa implementação, a serpente colide muitas vezes com o próprio corpo.

def get_direction():
    x = int(map_range(joystick_x.value, 0, 65535, 1.5, -1.5))
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
    if x < 0 or x >= screen.width  or y < 0 or y >= screen.height :
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
    [screen.height // 2, screen.width // 2],
    [screen.height // 2, screen.width // 2 - 1],
    [screen.height // 2, screen.width // 2 - 2]
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
        new_head[0] < 0 or new_head[0] >= screen.height  or
        new_head[1] < 0 or new_head[1] >= screen.width or
        new_head in snake_body
    ):
		# Se isso acontece, volta para a condição inicial.
        snake_body = [
            [screen.height // 2, screen.width // 2],
            [screen.height // 2, screen.width // 2 - 1],
            [screen.height // 2, screen.width // 2 - 2]
        ]
    else:
        snake_body.insert(0, new_head)

        # Se a serpente comeu a comida, gera nova comida
        if snake_body[0] == food: #snake_body[0] é a cabeça
            generate_food()
        else:
            snake_body.pop()

        # Clear screen and draw
        screen.fill(0)
        
        # Draw snake head and body
        for segment in snake_body:
            screen.pixel(segment[1], segment[0], 0x00FF00)  # Snake
        
        # Draw Food
        screen.pixel(food[1], food[0], 0xFF0000)
        
        # Show everything
        screen.display()
        time.sleep(0.1)

```

## Usando algumas facilidades da DisplayIO
O pessoal da Adafruit criou uma biblioteca fenomenal para lidar com qualquer tipo de display, a DisplayIO.
Com ela, podemos iniciar qualquer display, em qualquer barramento e depois usar os mesmos métodos para 
escrever na tela.
Infelizmente, usar Neopixels como display não é totalmente viável, por limitações de hardware mesmo.
Então a biblioteca pixel_framebuf faz o possível num hardware tão limitado.
Apesar de não termos todas as comodidades de usar DisplayIO para as Neopixels, podemos usar algumas
das suas facilidades, como desenhar bitmaps, fontes, e etc...

O exemplo abaixo escreve um texto na tela e o desloca para a esquerda, enquanto muda as cores dele. Veja 
com que facilidade se pode fazer isso...

```
import time
import board
import neopixel_spi as neopixel
from rainbowio import colorwheel
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

#Essas bibliotecas trabalham em interface com a DisplayIO
from displayio import Bitmap
from adafruit_display_text.bitmap_label import Label
from adafruit_bitmap_font import bitmap_font
import terminalio

pixel_pin = board.A0
pixel_width = 16
pixel_height = 16
num_tiles = 1
num_pixels = pixel_width * pixel_height * num_tiles

# Y offset, from the top of the display
offset = 4
# whether to mirror horizontally (test both values)
upside_down = True

pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height * num_tiles, 
    brightness=0.2,
    auto_write=False,
)

screen = PixelFramebuffer(
    pixels,
    pixel_width * num_tiles,
    pixel_height,
    orientation = VERTICAL,
    rotation = 0,
	reverse_x = True # Se o texto sair espelhado
)

# Como estamos usando DisplayIO, podemos usar fontes Bitmap
font = bitmap_font.load_font("/fonts/tom-thumb.pcf", Bitmap)
# Crio um Label, com texto customizado, usando a fonte e uma escala para ela
label = Label(text="Sesc Av. Paulista     ", font=font, scale=2)
# Leio o bitmap que está em Label, no caso, o texto na fonte especificada montado como Bitmap
bitmap = label.bitmap

colors = [0, 0]
hue = 0
while True:
    # Para cada pixel na largura do bitmap
    for x in range(bitmap.width):
        # Uso uma cor do arco-iris para cada coluna do bitmap
        hue = hue + 7
        if hue >= 256:
            hue = hue - 256
        colors[1] = colorwheel(hue)

        # Desloco o texto antigo para a esquerda
        for a in range(screen.width - 1):
            # Para cada linha
            for y in range(screen.height):
                screen.pixel(a, y, screen.pixel(a + 1, y))  # Desloco os pixels na horizontal

        # Desenho a próxima linha
        for y in range(screen.height):
            # Pego o pixel dentro do bitmap
            bm_y = y - offset
            # Vejo se é preto ou colorido
            if 0 <= bm_y < bitmap.height:
                color_index = bitmap[x, bm_y] # colorido
            else:
                color_index = 0 # preto
            screen.pixel(screen.width - 1, y, colors[color_index])  # Gravo o valor

        # Mostro o display
        screen.display()
        #time.sleep(0.04)

```
## Dá pra exibir Imagens?
Dá sim! Mas nós temos que ter alguns cuidados.
Como estamos lidando com um microcontrolador com recursos muito limitados, o ideal é que
nós usemos um tipo de imagem sem nenhuma compressão. Isso porque as operações de descompressão
consomem muitos recursos. Então, não vale usar JPEG, PNG ou GIF, se você quiser trabalhar rápido.

Nesse caso, temos que trabalhar com imagens BMP, com 24 bits (8 bits para cada cor RGB). Você
pode gerar esse tipo de imagem usando GIMP e é claro que você pode converter uma imagem JPG
para esse formato.

Uma imagem BMP é simplesmente uma lista com todos as cores dos pixels da imagem, no formato RGB,
sem nenhum tipo de compressão.

![Mario BMP](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_05_Neopixel_Grid/ExemploMario.png)

```
mario_bmp = [
    [(43, 128, 178), (52, 150, 198), (54, 149, 197), (58, 155, 203), (50, 146, 190), (27, 18, 16), (28, 21, 20), (28, 21, 19), (28, 19, 16), (31, 21, 19), (28, 21, 20), (48, 140, 186), (52, 147, 195), (58, 159, 204), (52, 149, 199), (55, 151, 199)],
    [(54, 149, 194), (55, 155, 201), (62, 162, 207), (23, 18, 16), (28, 20, 17), (200, 30, 28), (199, 29, 26), (202, 31, 27), (200, 30, 27), (206, 31, 29), (29, 19, 19), (24, 19, 20), (62, 164, 207), (43, 132, 179), (56, 158, 204), (51, 150, 198)],
    [(57, 154, 201), (53, 155, 201), (22, 20, 21), (198, 27, 26), (199, 28, 26), (248, 233, 217), (249, 229, 214), (205, 31, 27), (250, 228, 211), (201, 28, 27), (188, 23, 23), (199, 27, 25), (25, 19, 17), (20, 17, 17), (60, 160, 209), (47, 140, 187)],
    [(59, 159, 208), (58, 157, 203), (26, 18, 19), (205, 29, 29), (201, 29, 27), (250, 238, 222), (198, 30, 25), (204, 32, 29), (254, 241, 227), (202, 31, 30), (192, 27, 27), (201, 30, 27), (199, 27, 28), (24, 19, 18), (61, 163, 210), (50, 143, 191)],
    [(44, 133, 181), (21, 19, 20), (203, 30, 29), (197, 28, 25), (197, 26, 24), (203, 32, 30), (254, 242, 230), (253, 240, 224), (202, 30, 26), (204, 30, 29), (207, 32, 28), (208, 33, 31), (203, 30, 29), (200, 28, 26), (22, 21, 21), (62, 166, 213)],
    [(62, 164, 210), (17, 17, 20), (29, 19, 16), (30, 21, 19), (31, 19, 22), (28, 20, 19), (28, 19, 17), (32, 20, 19), (25, 17, 15), (205, 31, 31), (207, 31, 27), (199, 29, 26), (194, 28, 25), (192, 27, 26), (26, 16, 16), (56, 149, 193)],
    [(62, 166, 211), (55, 156, 203), (23, 22, 23), (207, 125, 70), (250, 233, 218), (45, 130, 178), (228, 173, 119), (206, 125, 66), (251, 225, 208), (227, 173, 117), (32, 20, 16), (32, 18, 15), (151, 20, 19), (147, 21, 18), (150, 21, 22), (20, 19, 21)],
    [(49, 139, 186), (55, 156, 203), (23, 24, 23), (234, 180, 123), (246, 227, 209), (24, 22, 26), (225, 171, 115), (46, 138, 185), (23, 22, 23), (247, 226, 209), (224, 167, 110), (35, 24, 19), (29, 18, 15), (26, 18, 16), (151, 23, 19), (22, 22, 23)],
    [(45, 138, 185), (57, 159, 205), (21, 23, 24), (235, 182, 124), (59, 159, 205), (23, 21, 23), (223, 168, 113), (77, 186, 232), (24, 24, 23), (253, 240, 220), (216, 138, 74), (69, 33, 19), (35, 21, 20), (224, 170, 113), (32, 21, 18), (47, 145, 190)],
    [(53, 147, 192), (56, 148, 192), (237, 190, 128), (226, 179, 119), (223, 172, 115), (230, 181, 121), (222, 163, 100), (48, 152, 201), (51, 139, 183), (254, 239, 222), (58, 31, 21), (73, 34, 21), (72, 34, 21), (207, 125, 67), (221, 169, 110), (22, 25, 26)],
    [(58, 158, 204), (20, 23, 23), (201, 122, 66), (228, 173, 115), (242, 192, 132), (228, 175, 118), (26, 25, 26), (27, 26, 25), (30, 24, 21), (39, 25, 22), (242, 191, 128), (229, 174, 116), (216, 132, 69), (211, 127, 65), (23, 21, 20), (49, 140, 186)],
    [(46, 135, 186), (48, 140, 184), (22, 23, 22), (214, 133, 70), (221, 143, 79), (203, 124, 68), (24, 25, 27), (24, 22, 23), (31, 24, 20), (197, 114, 65), (230, 174, 114), (225, 149, 79), (213, 129, 67), (212, 129, 67), (52, 148, 193), (57, 153, 202)],
    [(45, 134, 180), (57, 160, 207), (20, 22, 24), (24, 25, 25), (21, 23, 23), (21, 21, 24), (25, 24, 24), (27, 25, 28), (198, 116, 61), (228, 179, 122), (229, 148, 79), (204, 120, 62), (30, 21, 19), (25, 19, 18), (62, 168, 211), (47, 134, 182)],
    [(56, 160, 204), (57, 161, 208), (67, 174, 218), (22, 21, 24), (194, 114, 65), (37, 25, 22), (69, 34, 20), (234, 187, 128), (229, 177, 118), (230, 177, 116), (204, 123, 65), (34, 17, 16), (30, 20, 16), (58, 150, 192), (48, 147, 192), (61, 165, 211)],
    [(58, 155, 202), (47, 144, 189), (19, 22, 24), (23, 23, 26), (32, 85, 132), (21, 19, 20), (73, 35, 20), (73, 36, 22), (35, 22, 16), (32, 79, 126), (143, 16, 16), (186, 25, 23), (200, 29, 27), (187, 24, 21), (53, 149, 196), (52, 147, 195)],
    [(54, 154, 200), (44, 135, 181), (155, 22, 22), (18, 19, 19), (27, 77, 122), (148, 19, 19), (148, 19, 17), (154, 19, 18), (14, 47, 85), (27, 69, 110), (145, 19, 16), (202, 30, 27), (198, 27, 27), (190, 23, 23), (31, 18, 18), (53, 149, 196)]
    ]

```


Na pasta imgs eu deixei salvas algumas imagens já convertidas. No código abaixo, conecte duas 
matrizes 16x16 para criar uma tela 32x16 e exibir a imagem salva.

![Conhece o Mario?](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_05_Neopixel_Grid/images/Mario.bmp)

```
import time
import board
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

# A biblioteca bmp_reader é customizada
# ela lê um arquivo bitmap e faz as conversões necessárias.
from bmp_reader import BMPReader

# Lê o Bitmap como arquivo
friend_img = BMPReader ("images\Mario.bmp")

# Pega os pixels do Bitmap e grava no objeto friend
friend = friend_img.get_pixels()

pixel_pin = board.A0
pixel_width = 16
pixel_height = 16
num_tiles = 2
num_pixels = pixel_width * pixel_height * num_tiles

pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height * num_tiles, # dont forget to multiply for num_tiles
    brightness=0.2,
    auto_write=False,
)

screen = PixelFramebuffer(
    pixels,
    pixel_width * num_tiles,
    pixel_height,
    orientation = VERTICAL,
    rotation = 0,
	reverse_x = True
)

# Percorre o objeto friend (colunas e linhas)
for x in range (friend_img.width):
    for y in range (friend_img.height):
        # atribui a cor ao pixel na tela.
        screen.pixel (y,x,friend[y][x])


screen.display()
```

## BMP_Reader
É uma biblioteca que implementa uma classe e métodos para lidar com as conversões de arquivos no formato BMP
para que sejam lidos e interpretados pelo nosso sistema.

```
# The original is here: https://github.com/stuartm2/CircuitPython_BMP_Reader
# This class reads in a simple BMP image returning a multi-dimensional
# array of RGB values ideal for displaying with an array of Neopixels.

class BMPReader(object):
    def __init__(self, filename):
        self._filename = filename
        self._read_img_data()

    def get_pixels(self):
        pixel_grid = []
        pixel_data = list(self._pixel_data)  # Trabalhamos com uma cópia

        bytes_per_pixel = 3  # Assumindo 24-bit color depth (RGB)
        row_size = self.width * bytes_per_pixel

        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Cálculo do índice do pixel no vetor de dados
                idx = (y * row_size) + (x * bytes_per_pixel)
                b = pixel_data[idx]
                g = pixel_data[idx + 1]
                r = pixel_data[idx + 2]
                row.append((r, g, b))
            pixel_grid.append(row)

        return pixel_grid

    def _read_img_data(self):
        def lebytes_to_int(bytes):
            n = 0x00
            for b in reversed(bytes):
                n = (n << 8) | b
            return n

        with open(self._filename, 'rb') as f:
            img_bytes = bytearray(f.read())

        # Verificação do formato BMP
        assert img_bytes[0:2] == b'BM', "Não é um arquivo BMP válido"
        assert lebytes_to_int(img_bytes[30:34]) == 0, \
            "A compressão não é suportada"
        assert lebytes_to_int(img_bytes[28:30]) == 24, \
            "A profundidade de cor de 24 bits é a única suportada"

        # Extração das dimensões da imagem
        start_pos = lebytes_to_int(img_bytes[10:14])
        self.width = lebytes_to_int(img_bytes[18:22])
        self.height = lebytes_to_int(img_bytes[22:26])

        # Extração dos dados dos pixels
        self._pixel_data = img_bytes[start_pos:]

```
## E animação? Dá também?
Dá sim. De dois jeitos. Ou você pode salvar cada frame como um bmp separado e carregar um por um
usando BMPReader, ou você salva um grande bitmap, com os frames lado a lado, como uma tira de filme
e vai carregando cada pedaço da tira (sprite) e exibindo na tela, usando tileGrid.

Não vou detalhar muito as duas abordagens, mas vou colocar os códigos de exemplo aqui.

![Frame1](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_05_Neopixel_Grid/images/frame_1.bmp)
![Frame2](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_05_Neopixel_Grid/images/frame_2.bmp)
![Frame3](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_05_Neopixel_Grid/images/frame_3.bmp)
![Frame4](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_05_Neopixel_Grid/images/frame_4.bmp)

```
# Usando BMPReader
import time
import board
import neopixel
from bmp_reader import BMPReader
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

pixel_pin = board.A0
pixel_width = 16
pixel_height = 16
num_tiles = 2
num_pixels = pixel_width * pixel_height * num_tiles

pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height * num_tiles, 
    brightness=0.2,
    auto_write=False,
)

screen = PixelFramebuffer(
    pixels,
    pixel_width * num_tiles,
    pixel_height,
    orientation = VERTICAL,
    rotation = 0,
	reverse_x = True
)

# Cada um dos frames é um arquivo 16x32 separado
frame_file = ['frame_1.bmp', 'frame_2.bmp', 'frame_3.bmp', 'frame_4.bmp']

# Criei uma rotina para ler cada um dos frames e me retornar
# largura, altura e a matriz de cores
def getframe (framefile):
    frame_img = BMPReader ("images/" + framefile)
    frame = frame_img.get_pixels()
    return frame_img.width, frame_img.height, frame

while True:
    screen.fill(0) # limpo a tela
    # Para cada arquivo da lista de frames
    for file in frame_file:
        # Recupero os valores usando minha função getframe
        frame_width, frame_height, myframe = getframe(file)
        for x in range (frame_width):
            for y in range (frame_height):
                #Atribuo o valor de cor na coordenada correta
                screen.pixel (y,x,myframe[y][x])

        screen.display() # Mostro a imagem     
        # time.sleep (0.05)


```
E por fim, usando Adafruit_Imageload e as facilidades da biblioteca DisplayIO.

![All Frames](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_05_Neopixel_Grid/images/all_frames.bmp)

```
# Usando Display IO e ImageLoad

import time
import board
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

# Nessa abordagem vou usar os objetos Bitmap e Pallete da biblioteca
# Display IO e carregar a imagem, usando Imageload
import displayio
import adafruit_imageload

pixel_pin = board.A0
pixel_width = 16
pixel_height = 16
num_tiles = 2
num_pixels = pixel_width * pixel_height * num_tiles

pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height * num_tiles, # dont forget to multiply for num_tiles
    brightness=0.2,
    auto_write=False,
)

screen = PixelFramebuffer(
    pixels,
    pixel_width * num_tiles,
    pixel_height,
    orientation = VERTICAL,
    rotation = 0,
	reverse_x = True
)

# A imagem está organizada como uma Folha de Sprites, com 16 quadros com 16x32 pixels
# organizados lado a lado.
sprite_sheet, palette = adafruit_imageload.load(
    "images/all_frames.bmp",
    bitmap=displayio.Bitmap, # Coloco essa imagem, num objeto displayio Bitmap
    palette=displayio.Palette, # E a Paleta da imagem num objeto palette
)

# make the color at 0 index transparent.
#palette.make_transparent(0)

# Agora eu indico o tamanho do meu Sprite. Nesse caso, eu criei uma imagem em uma linha
# horizontal, com 16 sprites lado a lado.
sprite = displayio.TileGrid(
    sprite_sheet, # Meu objeto adafruit_imageload
    pixel_shader=palette, # a paleta desse objeto
    width=16, # tenho 16 sprites lado a lado
    height=1, # em uma unica linha
    tile_width=16, # cada sprite mede 16 pixels de largura
    tile_height=16, # por 16 pixels de altura
    default_tile=0, # e o tile que vai ser exibido por padrão é o primeiro
)

frame_index = 0  # índice do frame atual
frame_delay = 0.02 # Seria o FPS, mas não funciona
last_frame_time = time.monotonic()

while True:
    # Limpar a tela
    screen.fill(0)

    # Calcular o índice do tile atual dentro do bitmap
    tile_x = frame_index % sprite.width
    tile_y = frame_index // sprite.width

    # Essa rotina exibe o tile atual na neopixel
    # e faz uma conversão da cor de 16 bits por cor
    # para uma cor de 8 bits por cor.
    
    for x in range(sprite.tile_width):
        for y in range(sprite.tile_height):
            pixel_color = sprite_sheet[tile_x * sprite.tile_width + x, tile_y * sprite.tile_height + y]
            
            # Extrair os componentes RGB (vermelho, verde, azul) de 16 bits
            r = (pixel_color >> 11) & 0x1F  # Componente vermelho
            g = (pixel_color >> 5) & 0x3F    # Componente verde
            b = pixel_color & 0x1F           # Componente azul
            
            # Converter os componentes de 16 bits em 8 bits (0-255)
            r = (r * 255) // 31
            g = (g * 255) // 63
            b = (b * 255) // 31
            
            # Exibir o pixel na tela Neopixel (formato RGB de 24 bits)
            neopixel_color = (r, g, b)
            screen.pixel(x, y, neopixel_color)


    # Verifica se é hora de exibir o próximo frame
    current_time = time.monotonic()
    if current_time - last_frame_time >= frame_delay:
        # Atualizar o índice do frame para o próximo
        frame_index = (frame_index + 1) % (sprite.width * sprite.height)

        # Atualizar o tempo do último frame exibido
        last_frame_time = current_time
    
    # Atualizar a exibição
    screen.display()
```
