"""
    Space Invaders with two 16x16
    Adapted by Djair Guilherme (Nicolau dos Brinquedos) with a help from ChatGPT
    For the "Recriating Arcade Games in Circuitpython, Neopixel and Seeed Xiao RP2040"
    SESC Workshop - São Paulo - Brazil - May 2024
    Requirements: Adafruit_Pixel_Framebuf, Simpleio, Neopixel_SPI, Adafruit_rtttl
    Available at: https://github.com/djairjr/oficina_CircuitPython/tree/main/aula_6_Neopixel/libraries
"""

import board, time, random, os, gc
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range
import adafruit_rtttl

import neopixel_spi as neopixel

# This is the original version of library using 16x16 Panels
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

from rainbowio import colorwheel
import framebufferio

spi = board.SPI()

pixel_pin = board.D10 
pixel_width = 32 # Two Panels 16 x 16
pixel_height = 16

joystick_x = AnalogIn(board.A0)
joystick_y = AnalogIn(board.A1)

trigger = DigitalInOut (board.D2)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

# Setup Buzzer. Can be any digital Pin
buzzer = board.D3

pixels = neopixel.NeoPixel_SPI(
    spi,
    pixel_width * pixel_height, 
    brightness=0.2,
    auto_write=False,
)

# Using original Adafruit_Pixel_Framebuf Library
screen = PixelFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    rotation = 3,
    reverse_x=True,
    orientation=VERTICAL,
)

# Creating colors
COLORS = [
    0x000000,  # Black
    0xFF0000,  # Red
    0xFF7F00,  # Orange
    0xFFFF00,  # Yellow
    0x00FF00,  # Green
    0x0000FF,  # Blue
    0x4B0082,  # Indigo
    0x8B00FF   # Violet
]

def get_joystick():
    # Returns -1 0 or 1 depending on joystick position
    x_coord = int (map_range (joystick_x.value, 200, 65535, - 2 , 2))
    y_coord = int (map_range (joystick_y.value, 200, 65535, - 2 , 2))
    return x_coord, y_coord

# Sounds
def shoot_sound():
    adafruit_rtttl.play (buzzer, "shoot:d=4,o=5,b=880:8c6")
    
def xevious_sound():
    adafruit_rtttl.play (buzzer, "Xevious:d=4,o=5,b=160:16c,16c6,16b,16c6,16e6,16c6,16b,16c6,16c,16c6,16a#,16c6,16e6,16c6,16a#,16c6,16c,16c6,16a,16c6,16e6,16c6,16a,16c6,16c,16c6,16g#,16c6,16e6,16c6,16g#,16c6")

def galaga_sound():
    adafruit_rtttl.play (buzzer, "Galaga:d=4,o=5,b=125:8g4,32c,32p,8d,32f,32p,8e,32c,32p,8d,32a,32p,8g,32c,32p,8d,32f,32p,8e,32c,32p,8g,32b,32p,8c6,32a#,32p,8g#,32g,32p,8f,32d#,32p,8d,32a#4,32p,8a#,32c6,32p,8a#,32g,32p,16a,16f,16d,16g,16e,16d")

class Invader:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width =2
        self.height = 2
        self.color = random.choice(COLORS[1:])  # Choose a random color from the list, excluding black

    def draw(self):
        # Draw a 2x2 invader
        for i in range(self.width):
            for j in range(self.height):
                screen.pixel(self.x + i, self.y + j, self.color)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

        # Check if invader is off the screen
        if self.x < 0 or self.x >= pixel_height - 1 :
            self.x = -1  # Mark invader as inactive


class PlayerShip:
    def __init__(self):
        self.x = 7  # Screen Height // 2 - 1
        self.y = 31  # Screen Width - 1

    def draw(self):
        # Draw the player ship using Neopixels
        screen.pixel(self.x, self.y, COLORS[5])
        screen.pixel(self.x + 1, self.y, COLORS[5])
        screen.pixel(self.x + 1, self.y - 1, COLORS[5])
        screen.pixel(self.x + 2, self.y, COLORS[5])

    def move(self, dx):
        self.x += dx

        # Check if player ship is within the screen boundaries
        if self.x < 0 or self.x >= pixel_height   - 3: # Ship is 3 pixels wide
            self.x = max(0, min(pixel_height   - 3, self.x)) # Ship is 3 pixels wide


class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        screen.pixel(self.x, self.y, COLORS[7])

    def move(self, dy):
        self.y += dy

        # Check if projectile goes off the screen
        if self.y < 0:
            self.y = -1  # Mark projectile as inactive


class Game:
    def __init__(self):
        self.invaders = []
        self.player_ship = PlayerShip()
        self.projectiles = []
        self.score = 0
        self.level = 1
        self.invader_move_direction = 1 # Down is positive. 
        self.invader_speed = 0.1
        self.game_over = False
        # Create this to reverse Enemy Ship
        self.reverse = False

        # Create initial invaders
        for i in range(4):  # Adjust for the number of invaders in the width of the screen
            for j in range(4):
                self.invaders.append(Invader(i * 4, j * 4))  # Adjust for spacing and alignment
        
        galaga_sound()
    
    def resetinvaders(self):      
        self.invaders = []
        # Create initial invaders
        for i in range(4):  # Adjust for the number of invaders in the width of the screen
            for j in range(4):
                self.invaders.append(Invader(i * 4, j * 4))  # Adjust for spacing and alignment
        
        
    def draw(self):
        gc.collect()
        # Clear the screen
        screen.fill(0)

        # Draw invaders
        for invader in self.invaders:
            invader.draw()

        # Draw player ship
        self.player_ship.draw()

        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw()

        # Display game over message if necessary
        if self.game_over:
            screen.fill(0)
            print('Game Over')
            xevious_sound()

        screen.display()

    def update(self, dt):
        gc.collect()
        # Player ship movement
        dx, dy = get_joystick()
        self.player_ship.move(dy) # only y is needed.

        # Fire projectile
        if not trigger.value:
            self.projectiles.append(Projectile(self.player_ship.x + 1, self.player_ship.y - 1))
            time.sleep(0.2)  # Delay to prevent multiple shots on single press

        # Move projectiles
        for projectile in self.projectiles:
            projectile.move(-1)

            # Check for collision with invaders
            for invader in self.invaders:
                if invader.x <= projectile.x < invader.x + 2 and invader.y <= projectile.y < invader.y + 2:
                    self.invaders.remove(invader)
                    shoot_sound()
                    self.projectiles.remove(projectile)
                    self.score += 10
                    break  # Stop checking this projectile if it hit an invader

       
# Move invaders
        for invader in self.invaders:
            invader.move(self.invader_move_direction, 0)

        # Check for invader edge collision
        # My screen is rotated - check this variables position pixel_height pixel_width
        if any(invader.x >= (pixel_height // 2) - 2 or invader.x <= 0 for invader in self.invaders):
            self.invader_move_direction *= -1
            for invader in self.invaders:
                if not self.reverse:
                    invader.move(0, 1)  # Move down when changing direction
                else:
                    invader.move(0,-1)

        # Check if invader is near player ship
        if any(invader.y >= pixel_width - 4 for invader in self.invaders):
            # Reverse movement of invaders here
            self.reverse = True
        
        if any(invader.y <= 0 for invader in self.invaders):
            # Reverse movement of invaders here
            self.reverse = False
        
        if not self.invaders:
            # Just Reseting. Need Improovment
            screen.fill(0)
            self.resetinvaders()
            xevious_sound()

    def play(self):
        self.last_update_time = time.monotonic()  # Initialize the variable here
        while not self.game_over:
            current_time = time.monotonic()
            dt = current_time - self.last_update_time
            self.last_update_time = current_time

            self.update(dt) # erro aqui
            self.draw()

            time.sleep(0.02)

# Initialize the game
game = Game()

# Play the game
game.play()
