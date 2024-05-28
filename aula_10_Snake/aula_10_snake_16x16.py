"""
Snake Game
    For the "Recriating Arcade Games in Circuitpython, Neopixel and Seeed Xiao RP2040"
    SESC Workshop - São Paulo - Brazil - May 2024
    Requirements: custom tilegrid, tile_framebuf, my_framebuf libraries
    Available at: https://github.com/djairjr/oficina_CircuitPython/tree/main/aula_6_Neopixel/libraries
"""
import board
import time
import random
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range
import neopixel_spi as neopixel
from rainbowio import colorwheel
import framebufferio

# Using HT16K33 as Score and Message Display
from adafruit_ht16k33 import segments

# This is the original version of library when using 16x16 Panels
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

# Prepare Joystick in Analog Pins
joystick_x = AnalogIn(board.A0)
joystick_y = AnalogIn(board.A1)

# Prepare Trigger Switch 
trigger = DigitalInOut(board.D2)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

spi = board.SPI() 

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

# When 16x16 Using original Adafruit_Pixel_Framebuf Library
screen = PixelFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    rotation = 0,
    reverse_x=True,
    orientation=VERTICAL,
)

def get_direction():
    # This function is a little bit different than usual joystick function
    x = int(map_range(joystick_x.value, 0, 65535, 1.5, -1.5))
    y = int(map_range(joystick_y.value, 0, 65535, -1.5, 1.5))
    if abs(x) > abs(y):
        return (0, x)  # Horizontal Move
    else:
        return (y, 0)  # Vertical Move

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

# Get body and head position
snake_body = [
    [pixel_height // 2, pixel_width // 2],
    [pixel_height // 2, pixel_width // 2 - 1],
    [pixel_height // 2, pixel_width // 2 - 2]
]

# Get food position
food = [random.randint(0, pixel_height - 1), random.randint(0, pixel_width - 1)]

direction = (0, 1)  # Move to right

def generate_food():
    global food
    while True:
        food = [random.randint(0, pixel_height - 1), random.randint(0, pixel_width - 1)]
        
        # Check if food is in snake body. Because is random, and can occur...
        if food not in snake_body:
            break

while True:
    new_direction = get_direction()
    if new_direction != (0, 0) and (new_direction[0] != -direction[0] or new_direction[1] != -direction[1]):
        direction = new_direction

    # Calculate snake head position x, y coordinates
    new_head = [snake_body[0][0] + direction[0], snake_body[0][1] + direction[1]]

    # Check game over condition. Snake beyond screen or snake head in snake body
    if (
        new_head[0] < 0 or new_head[0] >= pixel_height  or
        new_head[1] < 0 or new_head[1] >= pixel_width or
        new_head in snake_body
    ):
        # Count lives remaining, show lives message
        snake_body = [
            [pixel_height // 2, pixel_width // 2],
            [pixel_height // 2, pixel_width // 2 - 1],
            [pixel_height // 2, pixel_width // 2 - 2]
        ]
    else:
        # Increase and show score points
        snake_body.insert(0, new_head)

        # Checa se a cobra comeu a comida
        if snake_body[0] == food:
            generate_food()
        else:
            snake_body.pop()

        # Clear screen and draw
        screen.fill(0)
        
        # Draw snake head and body
        for segment in snake_body:
            screen.pixel(segment[1], segment[0], 0x00FF00)  # Snake
        
        # Draw Food
        screen.pixel(food[1], food[0], 0xFF0000)
        
        # Show everything
        screen.display()
        time.sleep(0.1)
