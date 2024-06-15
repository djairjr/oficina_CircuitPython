import time, gc, asyncio
import board, random
import neopixel_spi as neopixel
import displayio
import adafruit_imageload
import adafruit_rtttl

# Using HT16K33 as Score and Message Display
from adafruit_ht16k33 import segments

# Treating Joystick
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range

# Neopixel as Screen
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

class Hardware():
    ''' A class to init all hardware on my Console '''
    
    def __init__(self):
        # Prepare Joystick in Analog Pins
        self.joystick_x = AnalogIn(board.A0)
        self.joystick_y = AnalogIn(board.A1)

        # Prepare Trigger Switch 
        self.trigger = DigitalInOut(board.D2)
        self.trigger.direction = Direction.INPUT
        self.trigger.pull = Pull.UP

        # Setup Buzzer. Can be any digital Pin
        self.buzzer = board.D3
        
        # This is HT16K33 Four Digits 14 Segment Display
        self.display = segments.Seg14x4(board.I2C())
        
        # Init SPI Bus to used it with Neopixels
        self.spi = board.SPI()
        
        self.pixel_width = 16
        self.pixel_height = 32
        self.num_pixels = self.pixel_width * self.pixel_height

        self.pixels = neopixel.NeoPixel_SPI(
            self.spi,
            self.pixel_width * self.pixel_height, 
            brightness=0.2,
            auto_write=False,
        )

        self.screen = PixelFramebuffer(
            self.pixels,
            self.pixel_width,
            self.pixel_height,
            rotation=3, # Default to all games. Get a pattern...
            #reverse_x=True,
            #orientation=VERTICAL,
        )
    
    def play_rttl (self, song):
        adafruit_rtttl.play (self.buzzer, song)
        
    def get_joystick(self):
        # Returns -1, 0, or 1 depending on joystick position
        x_coord = int(map_range(self.joystick_x.value, 200, 65535, -2, 2))
        y_coord = int(map_range(self.joystick_y.value, 200, 65535, -2, 2))
        return x_coord, y_coord

    def get_direction(self):
        # This function is a little bit different than usual joystick function
        x = int(map_range(self.joystick_x.value, 200, 65535, -1.5, 1.5)) # X up down
        y = int(map_range(self.joystick_y.value, 200, 65535,  -1.5, 1.5)) # Y Left Right
        if abs(x) > abs(y):
            return (x, 0)  # Horizontal Move
        else:
            return (0, y)  # Vertical Move
    
    def get_pixel_color(self, x, y):
        # Check if coordinates are within valid limits
        if (0 <= x < self.screen.height) and (0 <= y < self.screen.width):
            # Get pixel color
            rgbint = self.screen.pixel(x, y)
            return (rgbint >> 16 & 0xFF, rgbint >> 8 & 0xFF, rgbint & 0xFF)

        # Return black (0, 0, 0) if out of bounds
        return (0, 0, 0)
    
    def check_wall(self,x, y, wall_color):
        # Check Screen Limits First
        if x < 0 or x >= self.screen._height or y < 0 or y >= self.screen._width:
            return False
        # Then check color
        color = self.get_pixel_color(x, y)
        return color != wall_color

    def check_color(self, x, y, colorcheck):
           # Convert colorcheck to RGB tuple if it's an integer
        if isinstance(colorcheck, int):      
            colorcheck = ((colorcheck >> 16) & 0xFF, (colorcheck >> 8) & 0xFF, colorcheck & 0xFF)
        color = self.get_pixel_color(x, y)
        return color == colorcheck

    def display_bitmap(self,tile_width, tile_height, bitmap, frame_index=0):
        bitmap_width = bitmap.width
        bitmap_height = bitmap.height
        tiles_per_row = bitmap_width // tile_width
        tiles_per_column = bitmap_height // tile_height
        
        if tiles_per_row * tiles_per_column > 1:
            total_tiles = tiles_per_row * tiles_per_column
            if frame_index >= total_tiles:
                raise ValueError("Tile index out of range")
            tile_x = (frame_index % tiles_per_row) * tile_width
            tile_y = (frame_index // tiles_per_row) * tile_height
        else:
            tile_x = 0
            tile_y = 0
        
        for x in range(tile_width):
            for y in range(tile_height):
                pixel_color = bitmap[tile_x + x, tile_y + y]
                # Extrair os componentes RGB (vermelho, verde, azul) de 16 bits
                r = (pixel_color >> 11) & 0x1F  # Componente vermelho
                g = (pixel_color >> 5) & 0x3F   # Componente verde
                b = pixel_color & 0x1F          # Componente azul
                # Converter os componentes de 16 bits em 8 bits (0-255)
                r = (r * 255) // 31
                g = (g * 255) // 63
                b = (b * 255) // 31
                # Ajustar as coordenadas para a tela de 32x16 de acordo com a rotação
                if self.screen.rotation == 0:
                    self.screen.pixel(x, 31 - y, (r, g, b))
                elif self.screen.rotation == 1:
                    self.screen.pixel(31 - y, 15 - x, (r, g, b))
                elif self.screen.rotation == 2:
                    self.screen.pixel(15 - x, y, (r, g, b))
                elif self.screen.rotation == 3:
                    self.screen.pixel(y, x, (r, g, b))


class Menu():
    
    def __init__ (self, hardware):
        self.game_list = ['Snake', 'Maze', 'Arkanoid', 'Tetris', 'Space Invaders', 'Enduro']
        self.hardware = hardware
        self.frame_index = 0  
        self.joystick_delay = 0.1  
        self.last_joystick_time = time.monotonic()
        
        # Load the sprite sheet (bitmap) with all games
        self.sprite_sheet, self.palette = adafruit_imageload.load(
            # Image with 96 pixels width and 32 pixels height. Contains 6 frames 16x32
            "images/allGames.bmp",
            bitmap=displayio.Bitmap,
            palette=displayio.Palette,
        )

        self.start_game, self.palette_start = adafruit_imageload.load(
            "images/StartGame.bmp",
            bitmap=displayio.Bitmap,
            palette=displayio.Palette,
        )
        
        self.hardware.screen.fill(0)
        self.hardware.display_bitmap(16, 32, self.start_game)
        self.hardware.screen.display()
        self.hardware.display.marquee ('Select Game    ', loop = False)
        self.update()

    def coinSound(self):
        self.hardware.play_rttl ('Coin:d=4,o=6,b=440:c6,8d6,8e6,8f6')

    def menuLeft(self):
        self.hardware.play_rttl ('menuleft:d=4,o=4,b=600:a4,f4')
        
    def menuRight(self):
        self.hardware.play_rttl ('menuright:d=4,o=4,b=600:f4,a4')

    def update(self):
        while True:
            # Limpar a tela
            self.hardware.screen.fill(0)
            
            # Exibir o tile atual na tela Neopixel   
            self.hardware.display_bitmap(16, 32, self.sprite_sheet, self.frame_index)
            self.hardware.screen.display()
            self.hardware.display.print (self.game_list[self.frame_index][:4])
            
            # Verificar a posição do joystick
            current_time = time.monotonic()
            if current_time - self.last_joystick_time >= self.joystick_delay:

                x_coord, y_coord = self.hardware.get_joystick()

                if y_coord == -1:  # Joystick para a direita
                    self.menuRight()
                    self.frame_index = (self.frame_index + 1) % 6
                    if self.frame_index > 5:
                        self.frame_index = 0
                    self.last_joystick_time = current_time
                elif y_coord == 1:  # Joystick para a esquerda
                    self.menuLeft()
                    if self.frame_index < 0:
                        self.frame_index = 5
                    self.frame_index = (self.frame_index - 1) % 6
                    self.last_joystick_time = current_time
                                      
                # Verificar se o botão trigger foi pressionado
                if not self.hardware.trigger.value:  # Botão pressionado (trigger é ativo-baixo)
                    print(self.game_list[self.frame_index])
                    self.coinSound()
                    self.hardware.screen.fill(0)
                    self.hardware.screen.display()
                    time.sleep(0.5)  # Debounce delay
                    
                    if self.game_list[self.frame_index] == 'Snake':
                        from snake_as_class import Snake
                        snakegame = Snake(self.hardware)
                        snakegame.play()
                    elif self.game_list[self.frame_index] == 'Maze':
                        gc.collect()
                        from maze_as_class import MazeGame
                        mazegame = MazeGame(self.hardware)
                        mazegame.play()
                    elif self.game_list[self.frame_index] == 'Arkanoid':
                        gc.collect()
                        from arkanoid_as_class import Arkanoid
                        arkanoid = Arkanoid(self.hardware)
                        arkanoid.play()
                    else:
                        break
        
hardware = Hardware()
menu = Menu (hardware)