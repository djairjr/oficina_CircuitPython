'''
    Moving rectangle Example. Testing Joystick and Draw functions
    Wroted by Djair Guilherme (Nicolau dos Brinquedos)
    For the "Recriating Arcade Games in Circuitpython, Neopixel and Seeed Xiao RP2040"
    SESC Workshop - São Paulo - Brazil - May 2024
    Requirements: Adafruit_Pixel_Framebuf, Simpleio
    Available at: https://github.com/djairjr/oficina_CircuitPython/tree/main/aula_6_Neopixel/libraries
'''

import board, time, random, os, gc
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range

import neopixel_spi as neopixel

# This is the original version of library
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

from rainbowio import colorwheel
import framebufferio

# Using HT16K33 as Score and Message Display
from adafruit_ht16k33 import segments

spi = board.SPI()

pixel_pin = board.D10 
pixel_width = 32
pixel_height = 16

joystick_x = AnalogIn(board.A0)
joystick_y = AnalogIn(board.A1)

trigger = DigitalInOut (board.D2)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

pixels = neopixel.NeoPixel_SPI(
    spi,
    pixel_width * pixel_height, 
    brightness=0.2,
    auto_write=False,
)

screen = PixelFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    rotation = 3,
    reverse_x=True,
    orientation=VERTICAL,
)

screen.fill(0)

# This is HT16K33 Four Digits 14 Segment Display
display = segments.Seg14x4(board.I2C())
display.marquee("Tetris    ", loop=False)

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

class Tetris():

    FIELD_HEIGHT = 32 # screen._width
    FIELD_WIDTH = 16 # screen._height
    
    SCORE_PER_ELIMINATED_LINES = (0, 40, 80, 120, 600)
    SCORE_PER_FIXED_PIECE = 5  # Add 5 points when a piece is fixed
    
    TETROMINOS = [
        [(0, 0), (0, 1), (1, 0), (1, 1)],  # O Square
        [(0, 0), (0, 1), (1, 1), (2, 1)],  # L
        [(0, 1), (1, 1), (2, 1), (2, 0)],  # J
        [(0, 1), (1, 0), (1, 1), (2, 0)],  # Z
        [(0, 1), (1, 0), (1, 1), (2, 1)],  # T
        [(0, 0), (1, 0), (1, 1), (2, 1)],  # S
        [(0, 1), (1, 1), (2, 1), (3, 1)],  # I
    ]
    
    def __init__(self, screen):
        self.screen = screen
        self.screen.fill(0)
        self.field = [[0 for c in range(Tetris.FIELD_WIDTH)] for r in range(Tetris.FIELD_HEIGHT)]
        self.score = 0
        self.level = 0
        self.total_lines_eliminated = 0
        self.game_over = False
        self.reset_tetromino()

    def reset_tetromino(self):
        self.tetromino = random.choice(Tetris.TETROMINOS)[:]
        self.tetromino_color = random.randint(1, len(COLORS) - 1)
        self.tetromino_offset = [-2, Tetris.FIELD_WIDTH // 2]
        self.game_over = any(not self.is_cell_free(r, c) for (r, c) in self.get_tetromino_coords())
    
    def get_tetromino_coords(self):
        return [(r + self.tetromino_offset[0], c + self.tetromino_offset[1]) for (r, c) in self.tetromino]

    def apply_tetromino(self):
        for (r, c) in self.get_tetromino_coords():
            self.field[r][c] = self.tetromino_color

        new_field = [row for row in self.field if any(tile == 0 for tile in row)]
        lines_eliminated = len(self.field) - len(new_field)
        self.total_lines_eliminated += lines_eliminated
        self.field = [[0] * Tetris.FIELD_WIDTH for x in range(lines_eliminated)] + new_field
        self.score += Tetris.SCORE_PER_ELIMINATED_LINES[lines_eliminated] * (self.level + 1)
        self.score += Tetris.SCORE_PER_FIXED_PIECE  # Add 5 points when a piece is fixed
        
        self.level = self.total_lines_eliminated // 10
        self.reset_tetromino()

    def get_color(self, r, c):
        # Same color detection routine....
        return self.tetromino_color if (r, c) in self.get_tetromino_coords() else self.field[r][c]
    
    def is_cell_free(self, r, c):
        return r < Tetris.FIELD_HEIGHT and 0 <= c < Tetris.FIELD_WIDTH and (r < 0 or self.field[r][c] == 0)
    
    def move(self, dr, dc):
        gc.collect()
        if self.game_over:
            # If wasn't game over
            return
        # Check cell is free
        
        if all(self.is_cell_free(r + dr, c + dc) for (r, c) in self.get_tetromino_coords()):
            self.tetromino_offset = [self.tetromino_offset[0] + dr, self.tetromino_offset[1] + dc]
        elif dr == 1 and dc == 0:
            self.game_over = any(r < 0 for (r, c) in self.get_tetromino_coords())
            if not self.game_over:
                self.apply_tetromino()

    def rotate(self):
        if self.game_over:
            self.__init__(self.screen)
            return

        ys = [r for (r, c) in self.tetromino]
        xs = [c for (r, c) in self.tetromino]
        size = max(max(ys) - min(ys), max(xs) - min(xs))
        rotated_tetromino = [(c, size - r) for (r, c) in self.tetromino]
        wallkick_offset = self.tetromino_offset[:]
        tetromino_coord = [(r + wallkick_offset[0], c + wallkick_offset[1]) for (r, c) in rotated_tetromino]
        min_x = min(c for r, c in tetromino_coord)
        max_x = max(c for r, c in tetromino_coord)
        max_y = max(r for r, c in tetromino_coord)
        wallkick_offset[1] -= min(0, min_x)
        wallkick_offset[1] += min(0, Tetris.FIELD_WIDTH - (1 + max_x))
        wallkick_offset[0] += min(0, Tetris.FIELD_HEIGHT - (1 + max_y))

        tetromino_coord = [(r + wallkick_offset[0], c + wallkick_offset[1]) for (r, c) in rotated_tetromino]
        if all(self.is_cell_free(r, c) for (r, c) in tetromino_coord):
            self.tetromino, self.tetromino_offset = rotated_tetromino, wallkick_offset

class Game:
    # This class was adapted to work with Neopixel Screen
    def __init__(self):
        self.tetris = Tetris(screen)
        self.scoreFormat = '{0:04}'.format (self.tetris.score)
        display.print (self.scoreFormat)
    
    def play(self):
        last_move_time = time.monotonic()
        while True:
            current_time = time.monotonic()
            if current_time - last_move_time > 1.0 - (self.tetris.level * 0.1):
                self.tetris.move(1, 0)
                last_move_time = current_time
            
            # Get Joystick Move
            dx, dy = get_joystick()

            if dy == -1:
                self.tetris.move(0, 1)
            elif dy == 1:
                self.tetris.move(0, -1)
            if dx == 1:
                self.tetris.rotate()
            if dx == -1:
                # Fast Move Down
                self.tetris.move(3, 0)
            if not trigger.value:
                self.tetris.rotate()

            self.draw()
            
            time.sleep(0.02)

    def draw(self):
        gc.collect() # Or else, get memory issues
        screen.fill(0)
        self.scoreFormat = '{0:04}'.format (self.tetris.score)
        display.print (self.scoreFormat)
        for r in range(Tetris.FIELD_HEIGHT):
            for c in range(Tetris.FIELD_WIDTH):
                color_num = self.tetris.get_color(r, c)
                if color_num != 0:
                    screen.pixel(c, r, COLORS[color_num])
        screen.display()

game = Game()
game.play()