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
num_pixels = pixel_width * pixel_height * num_tiles

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

screen.fill(0)
screen.text ('Teste', 1,4, 0xff0000)
screen.display()
adafruit_rtttl.play (buzzer, "delete:d=4,o=5,b=330:8c6,8d6")

def get_joystick():
    x_coord = int (map_range (joystick_x.value, 200, 65535, - 2 , 2) )
    y_coord = int (map_range (joystick_y.value, 200, 65535, - 2 , 2) )
    return x_coord, y_coord


while True:
    print (get_joystick())
    if not trigger.value:
        print ('Trigger press')
        adafruit_rtttl.play (buzzer, "delete:d=4,o=5,b=330:8c6,8d6")

    time.sleep(0.02)
    


