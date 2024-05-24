'''
    Common Header and Auxiliary Functions for all Games
    Wroted by Djair Guilherme (Nicolau dos Brinquedos)
    For the "Recriating Arcade Games in Circuitpython, Neopixel and Seeed Xiao RP2040"
    SESC Workshop - São Paulo - Brazil - May 2024
    Requirements: custom tilegrid, tile_framebuf, my_framebuf libraries
    Available at: https://github.com/djairjr/oficina_CircuitPython/tree/main/aula_6_Neopixel/libraries
'''

# GC is a memory manager - Sometimes framebuffer get full
import gc
import board, random, time
import neopixel_spi as neopixel

# Treating Joystick
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range

# My custom version of Library
from tile_framebuf import TileFramebuffer
spi = board.SPI()

# Setting up the Neopixel Panel
pixel_pin = board.D10
pixel_width = 32
pixel_height = 8
num_tiles = 2
num_pixels = pixel_width * pixel_height * num_tiles

# Prepare Joystick in Analog Pins
joystick_x = AnalogIn(board.A0)
joystick_y = AnalogIn(board.A1)

# Prepare Trigger Switch 
trigger = DigitalInOut (board.D2)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

# Setup Buzzer. Can be any digital Pin
buzzer = board.D3

pixels = neopixel.NeoPixel_SPI(
    spi,
    pixel_width * pixel_height * num_tiles, # dont forget to multiply for num_tiles
    brightness=0.2,
    auto_write=False,
)

# Prepare PixelFramebuffer Screen
screen = TileFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation = 1 # 0 Default. 
)

def get_joystick():
    # Returns -1 0 or 1 depending on joystick position
    x_coord = int (map_range (joystick_x.value, 200, 65535, - 2 , 2))
    y_coord = int (map_range (joystick_y.value, 200, 65535, - 2 , 2))
    return x_coord, y_coord

def get_pixel_color(x, y):
    # Get Pixel color. Deal with screen rotation, because width and height changes...
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
    # Then check color
    color = get_pixel_color(x, y)
    return color != wall_color

def check_color(x, y, colorcheck):
    # Only check a color
    color = get_pixel_color(x, y)
    return color == colorcheck

class Countdown ():
    """ Countdown Class """
    
    def __init__ (self, time_sec):
        self.time_sec = time_sec
        self.update()
        
    def update(self):
        current = 0
        while self.time_sec:
            now = time.monotonic()       
            mins, secs = divmod(self.time_sec, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end='\r')
            # Para atualizar o display HT16K33 substituir
            # display.print (timeformat)
            if now >= current + 1:
                self.time_sec -= 1
                current = now
                time.sleep(0.1)
        
        print ("KABOOM")
        time.sleep(0.1)
        
        print ("STOP")
