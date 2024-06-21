'''
    Tetris in 115 lines https://github.com/nickwritessomecode/tetris_in_115_lines
    Adapted from Nick Wirites Some Code
    
    Developed for the "Recriating Arcade Classics with Circuitpython and Neopixels" 
    Workshop At SESC São Paulo (24 de Maio) - Between May 10 and July 4, 2024
    
    Depends:
    displayio, asyncio, simpleio, adafruit_imageload, adafruit_rtttl
    adafruit_ht16k33, adafruit_pixelbuf, neopixel and custom tilegrid and tilebuf
    (only if using 8x32 panels)
    
    Tested in Seeed Xiao RP2040
    
    Thanks to Ronaldo Gonçalves Alves for the pacience, support and ideas at workshop
'''
import board, time, random, os, gc

class Tetris:

    def __init__(self, hardware):
        self.hardware = hardware
        # Algo ainda não está bem no código, mas funciona nessa rotacao
        self.hardware.screen.rotation = 2
        self.hardware.play_rtttl ('korobyeyniki:d=4,o=5,b=320:e6,8b,8c6,8d6,16e6,16d6,8c6,8b,a,8a,8c6,e6,8d6,8c6,b,8b,8c6,d6,e6,c6,a,2a,8p,d6,8f6,a6,8g6,8f6,e6,8e6,8c6,e6,8d6,8c6,b,8b,8c6,d6,e6,c6,a,a')
        print(hardware)
        
        self.game_width = self.hardware.screen.width
        self.game_height = self.hardware.screen.height
        
        print('Game Width = ', self.game_width)
        print('Game Height = ', self.game_height)
        
        # Creating colors
        self.colors = [
            0x000000,  # Black
            0xFF0000,  # Red
            0xFF7F00,  # Orange
            0xFFFF00,  # Yellow
            0x00FF00,  # Green
            0x0000FF,  # Blue
            0x4B0082,  # Indigo
            0x8B00FF   # Violet
        ]
        
        self.gamePieces = [
            [(0, 0), (0, 1), (1, 0), (1, 1)],  # O Square
            [(0, 0), (0, 1), (1, 1), (2, 1)],  # L
            [(0, 1), (1, 1), (2, 1), (2, 0)],  # J
            [(0, 1), (1, 0), (1, 1), (2, 0)],  # Z
            [(0, 1), (1, 0), (1, 1), (2, 1)],  # T
            [(0, 0), (1, 0), (1, 1), (2, 1)],  # S
            [(0, 1), (1, 1), (2, 1), (3, 1)],  # I
        ]
          
        self.hardware.screen.fill(0)
        
        self.gameField = [[0 for c in range(self.game_width)] for r in range(self.game_height)]
        self.score = 0
        self.level = 0
        
        self.total_lines_eliminated = 0
        self.lineScores = (0, 40, 80, 120, 600)
        self.pieceScore = 5  # Add 5 points when a piece is fixed
                
        self.game_over = False
        self.reset_piece()
        
        self.scoreFormat = '{0:04}'.format(self.score)
        self.hardware.display.print(self.scoreFormat)
    
    def lineSound(self):
        self.hardware.play_rtttl('Coin:d=4,o=6,b=440:c6,8d6,8e6,8f6')
    
    def pieceSound(self):
        self.hardware.play_rtttl('menuleft:d=4,o=4,b=600:a4,f4')

    def reset_piece(self):
        self.piece = random.choice(self.gamePieces)[:]
        self.piece_color = random.randint(1, len(self.colors) - 1)
        self.piece_offset = [0, self.game_width // 2]  # Start from the top middle
        self.game_over = any(not self.is_cell_free(r, c) for (r, c) in self.get_piece_coords())
    
    def get_piece_coords(self):
        return [(r + self.piece_offset[0], c + self.piece_offset[1]) for (r, c) in self.piece]

    def apply_piece(self):
        for (r, c) in self.get_piece_coords():
            self.gameField[r][c] = self.piece_color

        new_field = [row for row in self.gameField if any(tile == 0 for tile in row)]
        
        lines_eliminated = len(self.gameField) - len(new_field)
        
        self.total_lines_eliminated += lines_eliminated
        
        self.gameField = [[0] * self.game_width for _ in range(lines_eliminated)] + new_field
        
        self.score += self.lineScores[lines_eliminated] * (self.level + 1)
        self.score += self.pieceScore  # Add 5 points when a piece is fixed
        self.pieceSound()
        
        if self.lineScores[lines_eliminated] > 0:
            self.lineSound()
        
        self.level = self.total_lines_eliminated // 10
        self.reset_piece()

    def get_color(self, r, c):
        return self.piece_color if (r, c) in self.get_piece_coords() else self.gameField[r][c]
    
    def is_cell_free(self, r, c):
        return 0 <= r < self.game_height and 0 <= c < self.game_width and (r < 0 or self.gameField[r][c] == 0)
    
    def move(self, dr, dc):
        gc.collect()
        if self.game_over:
            return
        
        # Check if cell is free
        if all(self.is_cell_free(r + dr, c + dc) for (r, c) in self.get_piece_coords()):
            self.piece_offset = [self.piece_offset[0] + dr, self.piece_offset[1] + dc]
            
        elif dr == 1 and dc == 0:
            # If there is no cell free anymore...
            self.game_over = any(r < 0 for (r, c) in self.get_piece_coords())
            if not self.game_over:
                self.apply_piece()

    def rotate(self):
        if self.game_over:
            self.__init__(self.hardware)
            return

        ys = [r for (r, c) in self.piece]
        xs = [c for (r, c) in self.piece]
        
        size = max(max(ys) - min(ys), max(xs) - min(xs))
        rotated_piece = [(c, size - r) for (r, c) in self.piece]
        
        gameField_limit = self.piece_offset[:]
        
        piece_coord = [(r + gameField_limit[0], c + gameField_limit[1]) for (r, c) in rotated_piece]
        
        min_x = min(c for r, c in piece_coord)
        max_x = max(c for r, c in piece_coord)
        max_y = max(r for r, c in piece_coord)
        
        gameField_limit[1] -= min(0, min_x)
        gameField_limit[1] += min(0, self.game_width - (1 + max_x))
        gameField_limit[0] += min(0, self.game_height - (1 + max_y))

        piece_coord = [(r + gameField_limit[0], c + gameField_limit[1]) for (r, c) in rotated_piece]
        
        if all(self.is_cell_free(r, c) for (r, c) in piece_coord):
            self.piece, self.piece_offset = rotated_piece, gameField_limit
            
    def draw(self):
        gc.collect()
        self.hardware.screen.fill(0)
        
        self.scoreFormat = '{0:04}'.format(self.score)
        self.hardware.display.print(self.scoreFormat)
        
        for r in range(self.game_height):
            for c in range(self.game_width):
                color_num = self.get_color(r, c)
                if color_num != 0:
                    self.hardware.screen.pixel(c, r, self.colors[color_num])
        
        self.hardware.screen.display()
        
    def play(self):
        # Main Loop
        last_move_time = time.monotonic()
        while True:
            current_time = time.monotonic()
            if current_time - last_move_time > 1.0 - (self.level * 0.1):
                self.move(1, 0)  # Move piece down
                last_move_time = current_time
            
            # Get Joystick Move
            dx, dy = self.hardware.get_direction()

            if dx >= 1:
                self.move(3, 0)  # Accelerate downward movement
            if dy <= -1:
                self.move(0, 1)  # Move left
            if dy >= 1:
                self.move(0, -1)  # Move right
            if dx <= - 1 or not self.hardware.trigger.value:
                self.rotate()

            self.draw()
            
            time.sleep(0.02)
