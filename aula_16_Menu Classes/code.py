'''
    Console Menu System
    Choose the game and play
'''

import time, gc, adafruit_imageload, displayio
from hardware import Hardware

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
# If 32x8 panel        
hardware = Hardware(panel_16x16 = False)
# If 16x16 panel
# hardware = Hardware()
menu = Menu (hardware)