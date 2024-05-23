'''
Rotinas auxiliares
'''

import time, gc
import board, random
import neopixel_spi as neopixel

# Treating Joystick
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range

# My custom version of Library
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
    brightness=0.2,
    auto_write=False,
)

screen = TileFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation = 0
)

def get_joystick():
    x_coord = int (map_range (joystick_x.value, 200, 65535, - 2 , 2))
    y_coord = int (map_range (joystick_y.value, 200, 65535, - 2 , 2))
    return x_coord, y_coord

def get_pixel_color(x, y):
    # Adjusting coordinates based on rotation
    if screen.rotation == 1:
        x, y = y, x
        x = screen._width - x - 1
    elif screen.rotation == 2:
        x = screen._width - x - 1
        y = screen._height * screen._tile_num - y - 1
    elif screen.rotation == 3:
        x, y = y, x
        y = screen._height * screen._tile_num - y - 1

    # Check if coordinates are in valid limits
    if (0 <= x < screen._width) and (0 <= y < screen._height * screen._tile_num):
        # Get pixel adjusting screen position
        rgbint = screen.format.get_pixel(screen, x, y)
        return (rgbint // 256 // 256 % 256, rgbint // 256 % 256, rgbint % 256)

    # Black (0, 0, 0) if out bounds
    return (0, 0, 0)

def check_wall(x, y, wall_color):
    # Check Screen Limits First
    if x < 0 or x >= screen._width or y < 0 or y >= screen._height * screen._tile_num:
        return False
    color = get_pixel_color(x, y)
    return color != wall_color

def check_color(x, y, colorcheck):
    color = get_pixel_color(x, y)
    return color == colorcheck  