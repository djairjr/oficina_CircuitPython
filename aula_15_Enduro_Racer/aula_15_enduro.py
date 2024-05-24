"""
    Enduro Racer
    Adapted by Djair Guilherme (Nicolau dos Brinquedos) with a help from ChatGPT
    For the "Recriating Arcade Games in Circuitpython, Neopixel and Seeed Xiao RP2040"
    SESC Workshop - São Paulo - Brazil - May 2024
    Requirements: custom tilegrid, tile_framebuf, my_framebuf libraries
    Available at: https://github.com/djairjr/oficina_CircuitPython/tree/main/aula_6_Neopixel/libraries
"""

import board, time, random

# Reading and treating Analog Input
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
import neopixel_spi as neopixel

# Sound Ringtone
import adafruit_rtttl

# My custom version
from tile_framebuf import TileFramebuffer

spi = board.SPI()  # Neopixel SPI Hack

pixel_pin = board.D10  # MOSI on Seeed Xiao RP2040
pixel_width = 32  # Width of each panel
pixel_height = 8  # Height of each panel
num_tiles = 2  # Two Tiles to create a Screen 16x32

# ThumbStick Coordinates
joystick_x = AnalogIn(board.A0)
joystick_y = AnalogIn(board.A1)

# Integrated Thumbstick Button
trigger = DigitalInOut(board.D2)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

# Neopixel Panel Connection
pixels = neopixel.NeoPixel_SPI(
    spi,
    pixel_width * pixel_height * num_tiles,  # num_tiles
    brightness=0.1, # Keep brightness low when using USB
    auto_write=False,
)

# My screen with custom TileFramebuffer Library
screen = TileFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation=1 # This setting is very important
)

# My Buzzer Sound
buzzer = board.D3


# Game Variables
car_width = 2 # Car width
car_height = 4 # Car height
player_x = (pixel_height * num_tiles) // 2 - (car_width // 2)  # Position player car
player_y = pixel_width - car_height 
player_speed = 1 # in pixels

# Enemy Cars
opponent_cars = []
opponent_speed = 1
opponent_spawn_rate = 15  # When cars will appear

# Life and Score
score = 0
lives = 5

# Colors
player_color = 0x007fff
background_color = 0x000000

# Enemy car colors
rainbow_colors = [
    0xFF0000,  # Red
    0xFF7F00,  # Orange
    0xFFFF00,  # Yellow
    0x00FF00,  # Green
    0x0000FF,  # Blue
    0x4B0082,  # Indigo
    0x8B00FF   # Violet
]

def create_opponent_car():
    # Create cars. Take care of lateral position
    car_x = random.randint(1, pixel_height * num_tiles - car_width - 1) 
    car_y = 0
    car_direction = random.choice([-1, 1])
    # Choose random color
    car_color = random.choice(rainbow_colors) 
    new_car = [car_x, car_y, car_direction, car_color]

    opponent_cars.append(new_car)

def draw():
    # Draw everyone
    screen.fill(background_color)  # Clear Screen
    draw_player()
    draw_opponents()
    screen.display()  # Show Framebuffer

def draw_player():
    # Draw player car. Just a rectangle
    screen.fill_rect(player_x, player_y, car_width, car_height, player_color)

def draw_opponents():
    for car in opponent_cars:
        car_x, car_y, _, car_color = car
        screen.fill_rect(car_x, car_y, car_width, car_height, car_color)

def update():
    global player_x, score, lives

    # Move player car with joystick
    move_player()

    # Update enemy cars
    for car in opponent_cars:
        car[1] += opponent_speed  # Down
        car[0] += car[2]  # Side to side
        if car[0] <= 0 or car[0] >= (pixel_height * num_tiles - car_width):
            car[2] *= -1  # If car bump, reverse movement

    # Check colision between cars
    for i, car1 in enumerate(opponent_cars):
        for j, car2 in enumerate(opponent_cars):
            if i != j and check_collision(car1[0], car1[1], car2[0], car2[1]):
                if car1[0] < car2[0]:
                    car1[0] -= 1
                    car2[0] += 1
                else:
                    car1[0] += 1
                    car2[0] -= 1

    # Check collision between player car and enemy car
    for car in opponent_cars:
        if check_collision(player_x, player_y, car[0], car[1]):
            lives -= 1
            print('Lives:', lives)
            if lives <= 0:
                print('Game Over')
                return
            opponent_cars.remove(car)
        elif car[1] > player_y:  # If enemy car is out, increase score
            score += 5
            print('Score:', score)

    # Remove cars outside the screen
    opponent_cars[:] = [car for car in opponent_cars if car[1] < pixel_width]
    

    # Add new car if less than three
    if len(opponent_cars) < 3 and random.randint(0, opponent_spawn_rate) == 0:
        create_opponent_car()

def move_player():
    # Another way to threat joystick
    global player_x

    # Move left
    if joystick_y.value < 2000:
        player_x = max(player_x - player_speed, 0)
    # move right
    elif joystick_y.value > 60000:
        player_x = min(player_x + player_speed, (pixel_height * num_tiles - car_width))

def check_collision(x1, y1, x2, y2):
    # Based on cars coordinates, not color
    return not (x1 > x2 + car_width or x1 + car_width < x2 or y1 > y2 + car_height or y1 + car_height < y2)

def reset_game():
    global score, lives, player_x, opponent_cars
    score = 0
    lives = 5
    player_x = (pixel_height * num_tiles) // 2 - (car_width // 2)  # Center player car
    opponent_cars = []

# Game start
reset_game()
while lives > 0:
    update()
    draw()
    time.sleep(0.01)
