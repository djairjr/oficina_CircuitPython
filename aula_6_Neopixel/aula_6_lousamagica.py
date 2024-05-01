"""
Neopixel tem um hack bacana, que é uma biblioteca que se beneficia da 
velocidade do barramento SPI. É a Neopixel_spi.
Aqui eu estou usando as bibliotecas que eu customizei 
"""
import board, time, os
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range
import neopixel_spi as neopixel
from rainbowio import colorwheel
import framebufferio

# My custom version
from tile_framebuf import TileFramebuffer
spi = board.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16) # Cheque sintaxe para Raspberry Pi Pico

pixel_pin = board.GP19 # MOSI
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

"""
# Slow Version 
pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height * num_tiles, # dont forget to multiply for num_tiles
    brightness=0.1,
    auto_write=False,
)
"""

pixel_framebuf = TileFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation = 3
)

def get_x(pin, number):
    return map_range (pin.value, 200, 65535, - number //2 , number // 2) 

def get_y(pin, number):
    return map_range (pin.value, 65535, 200, - number //2 , number // 2) 

old_x = pixel_width //2
old_y = pixel_height * num_tiles // 2

while True:
    if (not trigger.value):
        pixel_framebuf.fill (0x000000)
    else:
        x_pos = old_x + int (get_x (joystick_x, pixel_width //4))
        y_pos = old_y + int (get_y (joystick_y, pixel_height // 2))
        pixel_framebuf.line (old_y, old_x, y_pos, x_pos, colorwheel((time.monotonic()*50)%255))
        pixel_framebuf.display()
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
    
