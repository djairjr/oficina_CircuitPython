# SPDX-FileCopyrightText: 2020 Melissa LeBlanc-Williams, written for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
This example runs on an Seeed Xiao RP2040
"""
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

pixel_pin = board.D10
pixel_width = 32
pixel_height = 8
num_tiles = 2

joystick_x = AnalogIn(board.A0)
joystick_y = AnalogIn(board.A1)

trigger = DigitalInOut (board.D2)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

buzzer = board.D3

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
    
