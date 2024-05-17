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

def playTetrisSongMain():
    adafruit_rtttl.play (buzzer, "MainTitle:d=4,o=5,b=200:e6,8b,8c6,8d6,16e6,16d6,8c6,8b,a,8a,8c6,e6,8d6,8c6,b,8b,8c6,d6,e6,c6,a,2a,8p,d6,8f6,a6,8g6,8f6,e6,8e6,8c6,e6,8d6,8c6,b,8b,8c6,d6,e6,c6,a,a")

def playTetrisSongOne():
    adafruit_rtttl.play (buzzer, "Tetris:d=4,o=5,b=220:d6,32p,c.6,32p,8a,8c6,8a#,16a,16g,f,c,8a,8c6,8g,8a,f,c,d,8d,8e,8g,8f,8e,8d,c,c,c")

def gameOverSong():
    adafruit_rtttl.play (buzzer, "GameOver:d=4,o=5,b=120:d#6,b,c#6,a#,16b,16g#,16a#,16b,16b,16g#,16a#,16b,c#6,g,d#6,16p,16g#,16a#,16b,c#6,16p,16b,16a#,g#,g,g#,16f,16g,16g#,16a#,8d#.6,32d#6,32p,32d#6,32p,32d#6,32p,16d6,16d#6,8f.6,16d6,8a#,8p,8f#6,8d#6,8f#,8g#,a#.,16p,16a#,8d#.6,16f6,16f#6,16f6,16d#6,16a#,8g#.,16b,8d#6,16f6,16d#6,8a#.,16b,16a#,16g#,16f,16f#,d#")

def moveSound():
    adafruit_rtttl.play (buzzer, "move:d=4,o=5,b=880:8c6")

def deleteSound():
    adafruit_rtttl.play (buzzer, "delete:d=4,o=5,b=330:8c6,8d6")

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
x_pos, y_pos = old_x, old_y

while True:
    if (not trigger.value):
        pixel_framebuf.fill (0x000000)
        deleteSound()
    else:
        x_pos = old_x + int (get_x (joystick_x, pixel_width //4))
        y_pos = old_y + int (get_y (joystick_y, pixel_height // 2))
        if x_pos != old_x or y_pos != old_y:
            moveSound()
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
    
