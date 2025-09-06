import board, time
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range

import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer

from rainbowio import colorwheel

# Em alguns casos nós vamos usar a LED Driver Board da Xiao
pixel_pin = board.D0

# pixel_pin = board.D7 
pixel_width = 16
pixel_height = 16
num_tiles = 1

joystick_x = AnalogIn(board.A1)
joystick_y = AnalogIn(board.A2)

# Convém encontrar esses valores usando o programa da Aula 4
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
        
