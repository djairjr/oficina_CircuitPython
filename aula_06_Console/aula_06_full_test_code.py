'''
    Test all modules of console.
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
from rainbowio import colorwheel
import framebufferio
import adafruit_rtttl

# My custom version
from tile_framebuf import TileFramebuffer
spi = board.SPI()

# Neopixel information
pixel_pin = board.D10
pixel_width = 32
pixel_height = 8
num_tiles = 2
num_pixels = pixel_width * pixel_height * num_tiles

# Joystick Axis
joystick_x = AnalogIn(board.A0)
joystick_y = AnalogIn(board.A1)

# Joystick Button
trigger = DigitalInOut (board.D2)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

# Sound
buzzer = board.D3 
adafruit_rtttl.play (buzzer, "delete:d=4,o=5,b=330:8c6,8d6")

# Create Neopixel Object
pixels = neopixel.NeoPixel_SPI(
    spi,
    pixel_width * pixel_height * num_tiles, # dont forget to multiply for num_tiles
    brightness=0.1,
    auto_write=False,
)

# Turn Neopixel into a screen framebuffer
screen = TileFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation = 0
)

# Fill Screen with black (clear screen)
screen.fill(0)

# Write a text
screen.text ('Teste', 1,4, 0xff0000)

# Show everything
screen.display()

def get_joystick():
    x_coord = int (map_range (joystick_x.value, 200, 65535, - 2 , 2) )
    y_coord = int (map_range (joystick_y.value, 200, 65535, - 2 , 2) )
    return x_coord, y_coord


while True:
    print (get_joystick()) # Getting joystick coordinates
    if not trigger.value:
        # Check sound
        print ('Trigger press')
        adafruit_rtttl.play (buzzer, "delete:d=4,o=5,b=330:8c6,8d6")
        
    # In the workshop exercise, the students will change this code
    # into move rectangle code.

    time.sleep(0.02)
    


