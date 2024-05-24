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

# My custom version
from tile_framebuf import TileFramebuffer

spi = board.SPI() 

pixel_pin = board.D10 # MOSI
pixel_width = 32
pixel_height = 8
num_tiles = 2

# Prepare Joystick in Analog Pins
joystick_x = AnalogIn(board.A0)
joystick_y = AnalogIn(board.A1)

# Prepare Trigger Switch 
trigger = DigitalInOut(board.D2)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

pixels = neopixel.NeoPixel_SPI(
    spi,
    pixel_width * pixel_height * num_tiles, # don't forget to multiply for num_tiles
    brightness=0.1,
    auto_write=False,
)

screen = TileFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation=0 # Keep it simple
)

def get_direction():
    # This function is a little bit different than usual joystick function
    x = int(map_range(joystick_x.value, 0, 65535, -1.5, 1.5))
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

# Get body and head position
snake_body = [
    [pixel_height // 2, pixel_width // 2],
    [pixel_height // 2, pixel_width // 2 - 1],
    [pixel_height // 2, pixel_width // 2 - 2]
]

# Get food position
food = [random.randint(0, pixel_height * num_tiles - 1), random.randint(0, pixel_width - 1)]

direction = (0, 1)  # Move to right

def generate_food():
    global food
    while True:
        food = [random.randint(0, pixel_height * num_tiles - 1), random.randint(0, pixel_width - 1)]
        
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
        new_head[0] < 0 or new_head[0] >= pixel_height * num_tiles or
        new_head[1] < 0 or new_head[1] >= pixel_width or
        new_head in snake_body
    ):
        snake_body = [
            [pixel_height // 2, pixel_width // 2],
            [pixel_height // 2, pixel_width // 2 - 1],
            [pixel_height // 2, pixel_width // 2 - 2]
        ]
    else:
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
