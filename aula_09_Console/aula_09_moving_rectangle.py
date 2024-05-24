'''
    Moving rectangle Example. Testing Joystick and Draw functions
    Wroted by Djair Guilherme (Nicolau dos Brinquedos)
    For the "Recriating Arcade Games in Circuitpython, Neopixel and Seeed Xiao RP2040"
    SESC Workshop - São Paulo - Brazil - May 2024
    Requirements: custom tilegrid, tile_framebuf, my_framebuf libraries
    Available at: https://github.com/djairjr/oficina_CircuitPython/tree/main/aula_6_Neopixel/libraries
'''

import board, time, os
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range

import neopixel_spi as neopixel

# This is the original version of library, not used..
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

from rainbowio import colorwheel
import framebufferio

# My custom version
from tile_framebuf import TileFramebuffer

spi = board.SPI()

pixel_pin = board.D10 # Not used - using SPI
pixel_width = 32
pixel_height = 8
num_tiles = 2

joystick_x = AnalogIn(board.A0)
joystick_y = AnalogIn(board.A1)

trigger = DigitalInOut (board.D2)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

pixels = neopixel.NeoPixel_SPI(
    spi,
    pixel_width * pixel_height * num_tiles, # dont forget to multiply for num_tiles
    brightness=0.1,
    auto_write=False,
)


screen = TileFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation = 3
)

def get_joystick():
    # Returns -1 0 or 1 depending on joystick position
    x_coord = int (map_range (joystick_x.value, 200, 65535, - 2 , 2))
    y_coord = int (map_range (joystick_y.value, 200, 65535, - 2 , 2))
    return x_coord, y_coord


old_x = pixel_width //2
old_y = pixel_height * num_tiles // 2

while True:
    if (not trigger.value):
        screen.fill (0x000000)
    else:
        new_x, new_y = get_joystick()
        x_pos = old_x + new_x
        y_pos = old_y + new_y
        
        # Draw rect
        screen.fill_rect (y_pos, x_pos, 2, 2, colorwheel((time.monotonic()*50)%255))
        screen.display()
        
        if ((x_pos != old_x) or (y_pos != old_y)):
            # If moves, clear screen first
            screen.fill (0x000000)

        old_x = x_pos
        old_y = y_pos
               
        """ Tratando os limites da tela """
        if (old_x < 3):
            old_x = 3
        if (old_x > pixel_width - 3):
            old_x = pixel_width - 3
        if (old_y < 3):
            old_y = 3
        if (old_y > pixel_height * num_tiles - 3):
            old_y = pixel_height * num_tiles - 3
        
