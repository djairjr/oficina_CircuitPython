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
        snake_body = [
            [pixel_height // 2, pixel_width // 2],
            [pixel_height // 2, pixel_width // 2 - 1],
            [pixel_height // 2, pixel_width // 2 - 2]
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