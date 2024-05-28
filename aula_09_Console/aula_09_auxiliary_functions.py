'''
    Common Header and Auxiliary Functions for all Games
    Wroted by Djair Guilherme (Nicolau dos Brinquedos)
    For the "Recriating Arcade Games in Circuitpython, Neopixel and Seeed Xiao RP2040"
    SESC Workshop - São Paulo - Brazil - May 2024
    Requirements: custom tilegrid, tile_framebuf, my_framebuf libraries
    Available at: https://github.com/djairjr/oficina_CircuitPython/tree/main/aula_6_Neopixel/libraries
'''

# GC is a memory manager - Sometimes framebuffer get full
import board, random, time, gc
import neopixel_spi as neopixel

# Using HT16K33 as Score and Message Display
from adafruit_ht16k33 import segments

# Treating Joystick
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range

# My custom version of Library, using two 8 x 32 pannels
'''from tile_framebuf import TileFramebuffer'''

# This is the original version of library when using 16x16 Panels
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

# This is HT16K33 Four Digits 14 Segment Display
display = segments.Seg14x4(board.I2C())
display.marquee("Game Start    ", loop=False)

spi = board.SPI()
pixel_pin = board.D10 #board.MOSI

# Prepare Joystick in Analog Pins
joystick_x = AnalogIn(board.A0)
joystick_y = AnalogIn(board.A1)

# Prepare Trigger Switch 
trigger = DigitalInOut (board.D2)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

# Setup Buzzer. Can be any digital Pin
buzzer = board.D3

'''
# Setting up the Neopixel Pannel - 8 x 32 Version
pixel_width = 32
pixel_height = 8
num_tiles = 2 
num_pixels = pixel_width * pixel_height * num_tiles
'''

# Setting up the Neopixel Pannel - 16 x 16 Version
pixel_width = 32 
pixel_height = 16
num_pixels = pixel_width * pixel_height

pixels = neopixel.NeoPixel_SPI(
    spi,
    num_pixels, # dont forget to multiply for num_tiles
    brightness=0.2,
    auto_write=False,
)

'''
# Prepare PixelFramebuffer Screen 8 x 32 Version
screen = TileFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation = 1 # 0 Default. 
)
'''

# When 16x16 Using original Adafruit_Pixel_Framebuf Library
screen = PixelFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    rotation = 3,
    reverse_x=True,
    orientation=VERTICAL,
)

def get_joystick():
    # Returns -1 0 or 1 depending on joystick position
    x_coord = int (map_range (joystick_x.value, 200, 65535, - 2 , 2))
    y_coord = int (map_range (joystick_y.value, 200, 65535, - 2 , 2))
    return x_coord, y_coord

def get_pixel_color(x, y):
    # Check if coordinates are within valid limits
    if (0 <= x < screen.width) and (0 <= y < screen.height):
        # Get pixel color
        rgbint = screen.pixel(x, y)
        return (rgbint >> 16 & 0xFF, rgbint >> 8 & 0xFF, rgbint & 0xFF)

    # Return black (0, 0, 0) if out of bounds
    return (0, 0, 0)

def check_wall(x, y, wall_color):
    # Check Screen Limits First
    if x < 0 or x >= screen._width or y < 0 or y >= screen._height * screen._tile_num:
        return False
    # Then check color
    color = get_pixel_color(x, y)
    return color != wall_color

def check_color(x, y, colorcheck):
    colorcheck_rgb = ((colorcheck >> 16) & 0xFF, (colorcheck >> 8) & 0xFF, colorcheck & 0xFF)
    color = get_pixel_color(x, y)
    return color == colorcheck_rgb

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
