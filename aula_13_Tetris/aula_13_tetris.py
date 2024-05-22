import board, time, random
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range
import neopixel_spi as neopixel
from tile_framebuf import TileFramebuffer

# Neopixel using SPI Hack
spi = board.SPI()
pixel_pin = board.D10
pixel_width = 32
pixel_height = 8
num_tiles = 2

# Joystick Pins
joystick_x = AnalogIn(board.A0)
joystick_y = AnalogIn(board.A1)

# Joystick Button Pin
trigger = DigitalInOut(board.D2)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

# Define Neopixel Stripe
pixels = neopixel.NeoPixel_SPI(
    spi,
    pixel_width * pixel_height * num_tiles,  # Multiplicando por num_tiles
    brightness=0.1,
    auto_write=False,
)

# Create a Screen with Neopixel using two panels 8x32
screen = TileFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation=1  # Needed Screen 16 pixels wide and 32 pixels height
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

# Check color routine. Can check collision?
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

# Routine to treat Joystick values
def get_joystick(x_pin, y_pin):
    return int(map_range(y_pin.value, 200, 65535, -2, 2)), int(map_range(x_pin.value, 200, 65535, -2, 2))

class Tetris():
    FIELD_HEIGHT = 32
    FIELD_WIDTH = 16
    
    SCORE_PER_ELIMINATED_LINES = (0, 40, 100, 300, 1200)
    TETROMINOS = [
        [(0, 0), (0, 1), (1, 0), (1, 1)],  # O
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
        self.level = self.total_lines_eliminated // 10
        self.reset_tetromino()

    def get_color(self, r, c):
        return self.tetromino_color if (r, c) in self.get_tetromino_coords() else self.field[r][c]
    
    def is_cell_free(self, r, c):
        return r < Tetris.FIELD_HEIGHT and 0 <= c < Tetris.FIELD_WIDTH and (r < 0 or self.field[r][c] == 0)
    
    def move(self, dr, dc):
        if self.game_over:
            return

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
    def __init__(self):
        self.tetris = Tetris(screen)
    
    def play(self):
        last_move_time = time.monotonic()
        while True:
            current_time = time.monotonic()
            if current_time - last_move_time > 1.0 - (self.tetris.level * 0.1):
                self.tetris.move(1, 0)
                last_move_time = current_time

            dx, dy = get_joystick(joystick_x, joystick_y)

            if dx == -1:
                self.tetris.move(0, -1)
            elif dx == 1:
                self.tetris.move(0, 1)
            if dy == 1:
                self.tetris.rotate()
            if dy == -1:
                self.tetris.move(3, 0)
            if not trigger.value:
                self.tetris.rotate()

            self.draw()
            time.sleep(0.1)

    def draw(self):
        screen.fill(0)
        for r in range(Tetris.FIELD_HEIGHT):
            for c in range(Tetris.FIELD_WIDTH):
                color_num = self.tetris.get_color(r, c)
                if color_num != 0:
                    screen.pixel(c, r, COLORS[color_num])
        screen.display()

game = Game()
game.play()