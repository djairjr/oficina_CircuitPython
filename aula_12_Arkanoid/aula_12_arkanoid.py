import board
import time
import random
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
import neopixel_spi as neopixel
import adafruit_rtttl

# My custom version
from tile_framebuf import TileFramebuffer

spi = board.SPI()  

pixel_pin = board.D10 
pixel_width = 32  # Width of each panel
pixel_height = 8  # Height of each panel
num_tiles = 2  # two panels creating 32x16 screen

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
    pixel_width * pixel_height * num_tiles,  
    brightness=0.1,
    auto_write=False,
)

start_song = 'Arkanoid:d=4,o=5,b=140:8g6,16p,16g.6,2a#6,32p,8a6,8g6,8f6,8a6,2g6'

screen = TileFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation=1
)

# Game Variables
paddle_width = 6
paddle_height = 1
paddle_x = (pixel_height * num_tiles) // 2 - (paddle_width // 2)  # Center Paddle horizontally
paddle_y = pixel_width - 1  # Paddle in last screen line
paddle_speed = 1

ball_x = paddle_x + (paddle_width // 2)
ball_y = paddle_y - 1
ball_x_speed = 1
ball_y_speed = -1

bar_width = 3
bar_height = 2
bars_spacing = 1
bars_list = []
bars_offset = 4

rainbow_colors = [
    0xFF0000,  # Red
    0xFF7F00,  # Orange
    0xFFFF00,  # Yellow
    0x00FF00,  # Green
    0x0000FF,  # Blue
    0x4B0082,  # Indigo
    0x8B00FF   # Violet
]

# Score and Lives
score = 0
lives = 5

def create_bars():
    global bars_list
    bars_list = []
    color_index = 0  # Initial index
    for y in range((pixel_width // (bar_height + bars_spacing))-bars_offset):
        for x in range((pixel_height * num_tiles) // (bar_width + bars_spacing)):
            bar_x = x * (bar_width + bars_spacing)
            bar_y = y * (bar_height + bars_spacing)
            color = rainbow_colors[color_index % len(rainbow_colors)]
            bars_list.append((bar_x, bar_y, color))
            color_index += 1  # Incrementa o índice da cor

def draw():
    screen.fill(0x000000)  # Clear screen
    # Draw each game element
    draw_paddle()
    draw_ball()
    draw_bars()
    # Show everything
    screen.display()  

def draw_paddle():
    # Just a rect
    screen.fill_rect(paddle_x, paddle_y, paddle_width, paddle_height, 0x007fff)

def draw_ball():
    # Just a pixel
    screen.pixel(ball_x, ball_y, 0xff0000)

def draw_bars():
    # Just a bunch of rectangles
    for bar_x, bar_y, row in bars_list:
        color = rainbow_colors[row % len(rainbow_colors)]
        screen.fill_rect(bar_x, bar_y, bar_width, bar_height, color)

def update():
    global paddle_x, ball_x, ball_y, ball_x_speed, ball_y_speed, score, lives, paddle_width

    # Move paddle with joystick
    move_paddle()

    # Update ball position
    ball_x += ball_x_speed
    ball_y += ball_y_speed

    # Check ball position
    if ball_y >= pixel_width:
        lives -= 1
        print('Lives ', lives)
        if lives <= 0:
            print('Game Over')
            return
        else:
            reset_ball()

    # Check wall (screen limits) colision 
    if ball_x <= 0 or ball_x >= (pixel_height * num_tiles - 1):
        ball_x_speed *= -1
    if ball_y <= 0:
        ball_y_speed *= -1

    # Check paddle collision (using coordinates, not color)
    if ball_y == paddle_y and (paddle_x <= ball_x <= (paddle_x + paddle_width)):
        ball_y_speed *= -1

    # Check block collision and delete block
    for bar in bars_list:
        bar_x, bar_y, _ = bar
        if (bar_x <= ball_x <= (bar_x + bar_width)) and (bar_y <= ball_y <= (bar_y + bar_height)):
            bars_list.remove(bar)
            ball_y_speed *= -1
            score += 50
            print(score)

    # Check if all blocks are destroyed.
    if not bars_list:
        if paddle_width > 2:
            # When Level changes, paddle size get smaller
            paddle_width -= 1
        create_bars()
        reset_ball()

def move_paddle():
    global paddle_x

    # A different approach for joystick detection
    # Move to left
    if joystick_y.value < 2000:
        paddle_x = max(paddle_x - paddle_speed, 0)
    # Move to right
    elif joystick_y.value > 60000:
        paddle_x = min(paddle_x + paddle_speed, (pixel_height * num_tiles - paddle_width))

def reset_ball():
    global ball_x, ball_y, ball_x_speed, ball_y_speed
    ball_x = paddle_x + (paddle_width // 2)
    ball_y = paddle_y - 1
    ball_x_speed = 1
    ball_y_speed = -1

def reset_game():
    adafruit_rtttl.play (buzzer, start_song)
    global score, lives, paddle_width
    score = 0
    lives = 5
    paddle_width = 6  # Reset paddle size
    create_bars()
    reset_ball()

# Game start
reset_game()
while lives > 0:
    update()
    draw()
    time.sleep(0.01)
