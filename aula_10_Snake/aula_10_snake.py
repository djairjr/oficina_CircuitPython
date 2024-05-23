import board
import time
import random
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range
import neopixel_spi as neopixel
from rainbowio import colorwheel
import framebufferio

# My custom version
from tile_framebuf import TileFramebuffer

spi = board.SPI() # Cheque sintaxe para Raspberry Pi Pico

pixel_pin = board.D10 # MOSI
pixel_width = 32
pixel_height = 8
num_tiles = 2

# Os dois eixos do Joystick na realidade são potenciômetros
joystick_x = AnalogIn(board.A0)
joystick_y = AnalogIn(board.A1)

# O Thumbstick possui um botão integrado que é o que estou usando
trigger = DigitalInOut(board.D2)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

pixels = neopixel.NeoPixel_SPI(
    spi,
    pixel_width * pixel_height * num_tiles, # don't forget to multiply for num_tiles
    brightness=0.1,
    auto_write=False,
)

screen = TileFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation=0 # Keep it simple
)

# get Joystick direction
def get_direction():
    x = int(map_range(joystick_x.value, 0, 65535, -1.5, 1.5))
    y = int(map_range(joystick_y.value, 0, 65535, -1.5, 1.5))
    if abs(x) > abs(y):
        return (0, x)  # Horizontal Move
    else:
        return (y, 0)  # Vertical Move

# Get body and head position
snake_body = [
    [pixel_height // 2, pixel_width // 2],
    [pixel_height // 2, pixel_width // 2 - 1],
    [pixel_height // 2, pixel_width // 2 - 2]
]

# Get food position
food = [random.randint(0, pixel_height * num_tiles - 1), random.randint(0, pixel_width - 1)]

direction = (0, 1)  # Move to right

def generate_food():
    global food
    while True:
        food = [random.randint(0, pixel_height * num_tiles - 1), random.randint(0, pixel_width - 1)]
        if food not in snake_body:
            break

while True:
    new_direction = get_direction()
    if new_direction != (0, 0) and (new_direction[0] != -direction[0] or new_direction[1] != -direction[1]):
        direction = new_direction

    # Calcula a nova posição da cabeça da cobra
    new_head = [snake_body[0][0] + direction[0], snake_body[0][1] + direction[1]]

    # Checa condições de game over
    if (
        new_head[0] < 0 or new_head[0] >= pixel_height * num_tiles or
        new_head[1] < 0 or new_head[1] >= pixel_width or
        new_head in snake_body
    ):
        snake_body = [
            [pixel_height // 2, pixel_width // 2],
            [pixel_height // 2, pixel_width // 2 - 1],
            [pixel_height // 2, pixel_width // 2 - 2]
        ]
    else:
        snake_body.insert(0, new_head)

        # Checa se a cobra comeu a comida
        if snake_body[0] == food:
            generate_food()
        else:
            snake_body.pop()

        # Limpa a tela e desenha a cobra e a comida
        screen.fill(0x000000)
        for segment in snake_body:
            screen.pixel(segment[1], segment[0], 0x00FF00)  # Desenha a cobra
        screen.pixel(food[1], food[0], 0xFF0000)  # Desenha a comida
        screen.display()
        time.sleep(0.1)
