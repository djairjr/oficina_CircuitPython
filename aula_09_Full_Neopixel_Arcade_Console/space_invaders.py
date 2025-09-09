"""
    Space Invaders with two 16x16
    Adapted by Djair Guilherme (Nicolau dos Brinquedos) with a help from ChatGPT
    For the "Recriating Arcade Games in Circuitpython, Neopixel and Seeed Xiao RP2040"
    SESC Workshop - São Paulo - Brazil - May 2024
    Available at: https://github.com/djairjr/oficina_CircuitPython/
"""

import board, time, random, os, gc
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range
import adafruit_rtttl

import neopixel_spi as neopixel

# Using HT16K33 as Score and Message Display
from adafruit_ht16k33 import segments

# This is the original version of library using 16x16 Panels
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

from rainbowio import colorwheel
import framebufferio

spi = board.SPI()
display = segments.Seg14x4(board.I2C())

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
        self.width = 2
        self.height = 2
        self.color = random.choice(COLORS[1:])

    def draw(self):
        for i in range(self.width):
            for j in range(self.height):
                screen.pixel(self.x + i, self.y + j, self.color)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        if self.x < 0 or self.x >= pixel_height - 1:
            self.x = -1

    def shoot(self):
        return Projectile(self.x + 1, self.y + 2, COLORS[1])

class PlayerShip:
    def __init__(self):
        self.x = 7
        self.y = 27
        self.lives = 3
        self.exploding = False
        self.explode_timer = 0

    def draw(self):
        if self.exploding:
            self.draw_explosion()
        else:
            screen.pixel(self.x, self.y, COLORS[5])
            screen.pixel(self.x + 1, self.y, COLORS[5])
            screen.pixel(self.x + 1, self.y - 1, COLORS[5])
            screen.pixel(self.x + 2, self.y, COLORS[5])

    def draw_explosion(self):
        screen.pixel(self.x, self.y, COLORS[1])
        screen.pixel(self.x + 1, self.y, COLORS[1])
        screen.pixel(self.x + 1, self.y - 1, COLORS[1])
        screen.pixel(self.x + 2, self.y, COLORS[1])

    def draw_lives(self):
        total_width = self.lives * 2 + (self.lives - 1) * 1
        start_x = (pixel_height - total_width) // 2
        for i in range(self.lives):
            x_offset = start_x + i * 3
            for dx in range(2):
                for dy in range(2):
                    screen.pixel(x_offset + dx, 29 + dy, COLORS[5])

    def move(self, dx):
        self.x += dx
        if self.x < 0 or self.x >= pixel_height - 3:
            self.x = max(0, min(pixel_height - 3, self.x))

    def explode(self):
        self.exploding = True
        self.explode_timer = time.monotonic()

class Projectile:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        screen.pixel(self.x, self.y, self.color)

    def move(self, dy):
        self.y += dy
        if self.y < 0 or self.y >= pixel_width:
            self.y = -1

class Game:
    def __init__(self):
        screen.fill(0)
        screen.display()
        self.invaders = []
        self.player_ship = PlayerShip()
        self.projectiles = []
        self.enemy_projectiles = []
        self.score = 0
        display.print('{0:04}'.format(self.score))
        self.level = 1
        self.invader_move_direction = 1
        self.invader_speed = 0.1
        self.game_over = False
        self.reverse = False
        self.resetinvaders()
        self.draw()
        galaga_sound()

    def resetinvaders(self):
        self.invaders = []
        for i in range(4):
            for j in range(4):
                self.invaders.append(Invader(i * 4, j * 4))

    def draw(self):
        gc.collect()
        screen.fill(0)
        
        for invader in self.invaders:
            invader.draw()
            
        self.player_ship.draw()
        self.player_ship.draw_lives()
        
        for projectile in self.projectiles:
            projectile.draw()
            
        for projectile in self.enemy_projectiles:
            projectile.draw()
            
        if self.game_over:
            screen.fill(0)
            display.marquee('Game Over   ', loop=False)
            xevious_sound()
            
        screen.display()

    def update(self, dt):
        gc.collect()
        dx, dy = get_joystick()
        self.player_ship.move(dy)
        if not trigger.value:
            self.projectiles.append(Projectile(self.player_ship.x + 1, self.player_ship.y - 1, COLORS[7]))
            time.sleep(0.2)

        # Move player projectiles
        for projectile in self.projectiles[:]:
            projectile.move(-1)
            if projectile.y == -1:
                self.projectiles.remove(projectile)

            # Check for collision with invaders
            for invader in self.invaders[:]:
                if invader.x <= projectile.x < invader.x + 2 and invader.y <= projectile.y < invader.y + 2:
                    self.invaders.remove(invader)
                    shoot_sound()
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    self.score += 10
                    display.print('{0:04}'.format(self.score))
                    if self.score % 1000 == 0:
                        self.player_ship.lives += 1
                    break

            # Check for collision with enemy projectiles
            for enemy_projectile in self.enemy_projectiles[:]:
                if projectile.x == enemy_projectile.x and projectile.y == enemy_projectile.y:
                    self.enemy_projectiles.remove(enemy_projectile)
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    break

        # Move enemy projectiles
        for projectile in self.enemy_projectiles[:]:
            projectile.move(1)
            if projectile.y == -1:
                self.enemy_projectiles.remove(projectile)

            # Check for collision with player ship
            if self.player_ship.x <= projectile.x < self.player_ship.x + 3 and self.player_ship.y <= projectile.y < self.player_ship.y + 3:
                self.player_ship.lives -= 1
                self.player_ship.explode()
                self.enemy_projectiles.remove(projectile)
                if self.player_ship.lives <= 0:
                    self.game_over = True

        # Move invaders
        for invader in self.invaders[:]:
            invader.move(self.invader_move_direction, 0)

            # Check collision between invaders and player ship
            if invader.x <= self.player_ship.x < invader.x + invader.width and invader.y <= self.player_ship.y < invader.y + invader.height:
                self.player_ship.lives -= 1
                self.invaders.remove(invader)
                if self.player_ship.lives <= 0:
                    self.game_over = True

        # Check for invader edge collision
        if any(invader.x >= (pixel_height - 1 // 2) - 2 or invader.x <= 0 for invader in self.invaders):
            self.invader_move_direction *= -1
            for invader in self.invaders:
                if not self.reverse:
                    invader.move(0, 1)
                else:
                    invader.move(0, -1)

        # Check if invader is near player ship
        if any(invader.y >= self.player_ship.y - 1 for invader in self.invaders):
            self.reverse = True
        if any(invader.y <= 0 for invader in self.invaders):
            self.reverse = False

        # Enemy shooting
        if len(self.invaders) <= 3 and random.random() < 0.03:
            shooter = random.choice(self.invaders)
            self.enemy_projectiles.append(shooter.shoot())

        if not self.invaders:
            screen.fill(0)
            screen.display()
            self.projectiles[:] = []
            self.enemy_projectiles[:] = []
            self.resetinvaders()
            xevious_sound()


    def play(self):
        self.last_update_time = time.monotonic()
        while not self.game_over:
            current_time = time.monotonic()
            dt = current_time - self.last_update_time
            self.last_update_time = current_time
            self.update(dt)
            self.draw()
            time.sleep(0.02)

game = Game()
game.play()
