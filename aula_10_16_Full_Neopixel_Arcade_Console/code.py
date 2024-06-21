'''
    NEOPIXEL CONSOLE MENU SYSTEM
    
    Developed for the "Recriating Arcade Classics with Circuitpython and Neopixels" 
    Workshop At SESC São Paulo (24 de Maio) - Between May 10 and July 4, 2024
    
    Depends:
    displayio, asyncio, simpleio, adafruit_imageload, adafruit_rtttl
    adafruit_ht16k33, adafruit_pixelbuf, neopixel and custom tilegrid and tilebuf
    (only if using 8x32 panels)
    
    Tested in Seeed Xiao RP2040
    
    Thanks to Ronaldo Gonçalves Alves for the pacience, support and ideas at workshop
'''

import time
import gc
import adafruit_imageload
import displayio
from hardware import Hardware

class Menu:
    def __init__(self, hardware):
        self.game_list = ['Snake', 'Maze', 'Arkanoid', 'Tetris', 'Space Invaders']
        self.game_amount = len (self.game_list)
        self.hardware = hardware
        self.hardware.screen.fill(0)
        self.hardware.screen.display()
        print (self.hardware)
        self.frame_index = 0  
        self.joystick_delay = 0.1  
        self.last_joystick_time = time.monotonic()

        # Load the sprite sheet (bitmap) with all games
        self.sprite_sheet, self.palette = adafruit_imageload.load(
            "images/allGames.bmp",
            bitmap=displayio.Bitmap,
            palette=displayio.Palette,
        )

        self.start_game, self.palette_start = adafruit_imageload.load(
            "images/StartGame.bmp",
            bitmap=displayio.Bitmap,
            palette=displayio.Palette,
        )

        self.hardware.display_bitmap(16, 32, self.start_game)
        self.hardware.screen.display()
        self.hardware.display.marquee('OOOOoooo____', loop=False)
        self.update()

    def coinSound(self):
        self.hardware.play_rtttl('Coin:d=4,o=6,b=440:c6,8d6,8e6,8f6')

    def menuLeft(self):
        self.hardware.play_rtttl('menuleft:d=4,o=4,b=600:a4,f4')
        
    def menuRight(self):
        self.hardware.play_rtttl('menuright:d=4,o=4,b=600:f4,a4')

    def update(self):
        while True:
            self.hardware.screen.fill(0)
            self.hardware.display_bitmap(16, 32, self.sprite_sheet, self.frame_index)
            self.hardware.screen.display()
            self.hardware.display.print(self.game_list[self.frame_index][:4])
            
            current_time = time.monotonic()
            if current_time - self.last_joystick_time >= self.joystick_delay:
                x_coord, y_coord = self.hardware.get_joystick()

                if y_coord == 1:
                    self.menuRight()
                    self.frame_index = (self.frame_index + 1) % self.game_amount
                    self.last_joystick_time = current_time
                elif y_coord == -1:
                    self.menuLeft()
                    self.frame_index = (self.frame_index - 1) % self.game_amount
                    self.last_joystick_time = current_time
                                      
                if not self.hardware.trigger.value:
                    selected_game = self.game_list[self.frame_index]
                    print(selected_game)
                    self.coinSound()
                    self.hardware.screen.fill(0)
                    self.hardware.screen.display()
                    time.sleep(0.5)

                    self.cleanup()
                    gc.collect()
                    
                    if selected_game == 'Snake':
                        from snake_as_class import Snake
                        game = Snake(self.hardware)
                    elif selected_game == 'Maze':
                        from maze_as_class import MazeGame
                        game = MazeGame(self.hardware)
                    elif selected_game == 'Arkanoid':
                        from arkanoid_as_class import Arkanoid
                        game = Arkanoid(self.hardware)
                    elif selected_game == 'Tetris':
                        from tetris_as_class import Tetris
                        game = Tetris(self.hardware)
                    elif selected_game == 'Space Invaders':
                        from space_as_class import SpaceInvaders
                        game = SpaceInvaders(self.hardware)
                    else:
                        break

                    game.play()
                    break

    def cleanup(self):
        #print ("Limpando a memória ")
        #print ("Antes ", gc.mem_free())
        self.sprite_sheet = None
        self.palette = None
        self.start_game = None
        self.palette_start = None
        self.hardware.screen.fill(0)
        self.hardware.screen.display()
        gc.collect()
        #print ("Depois ", gc.mem_free())

if __name__ == "__main__":
    hardware = Hardware(panel_16x16=False)
    menu = Menu(hardware)
