"""
    Original code from Orestis Zekai
    in https://github.com/OrWestSide/python-scripts/blob/master/maze.py
    From Medium Article in: https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e
    Adapted by Djair Guilherme (Nicolau dos Brinquedos) with a help from ChatGPT
    For the "Recriating Arcade Games in Circuitpython, Neopixel and Seeed Xiao RP2040"
    SESC Workshop - São Paulo - Brazil - May 2024
    Requirements: custom tilegrid, tile_framebuf, my_framebuf libraries
    Available at: https://github.com/djairjr/oficina_CircuitPython/tree/main/aula_6_Neopixel/libraries
"""

import time, gc
import board, random
import neopixel_spi as neopixel

# To display Level Change Message in Rainbow Marquee
from adafruit_display_text.bitmap_label import Label
from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap
from rainbowio import colorwheel
import terminalio

# Treating Joystick
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range

# Adding simple RTTTL Sound
import adafruit_rtttl

# My custom version of Library
from tile_framebuf import TileFramebuffer
spi = board.SPI()

pixel_pin = board.D10
pixel_width = 32
pixel_height = 8
num_tiles = 2
num_pixels = pixel_width * pixel_height * num_tiles

joystick_x = AnalogIn(board.A0)
joystick_y = AnalogIn(board.A1)

trigger = DigitalInOut (board.D2)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

buzzer = board.D3

pixels = neopixel.NeoPixel_SPI(
    spi,
    pixel_width * pixel_height * num_tiles, # dont forget to multiply for num_tiles
    brightness=0.2,
    auto_write=False,
)

screen = TileFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation = 0
)

# Load Bitmap Font
font = bitmap_font.load_font("/fonts/tom-thumb.pcf", Bitmap)

def get_x(pin):
    return map_range (pin.value, 200, 65535, - 2 , 2) 

def get_y(pin):
    return map_range (pin.value, 200, 65535, - 2 , 2)

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

# Set pixel color
def set_pixel_color(x, y, color):
    screen.pixel(x, y, color)

# Check if is valid movement
def is_valid_move(x, y):
    if x < 0 or x >= screen._width or y < 0 or y >= screen._height * screen._tile_num:
        return False
    color = get_pixel_color(x, y)
    return color != (0, 255, 255)  # Wall color is 0x00ffff

# Check end of maze
def is_end(x, y):
    color = get_pixel_color(x, y)
    # print(f"Check if ({x}, {y}) is end maze: {color}")
    return color == (0, 255, 0)  # End Color is 0x00ff00

class Maze():
    # This class create and draw a maze
    def __init__(self, screen):
        self.screen = screen
        self.height = self.screen.height * self.screen._tile_num
        self.width = self.screen.width // 2
        self.__unvisited = 'u'
        self.__cell = 'c'
        self.__walls = 'w'
        self.__entry = 'e'
        self.__exit = 'x'
        self.maze = []
        self.entry_x = 0
        self.entry_y = 0
        self.exit_x = 0
        self.exit_y = 0
        self.generate()
        self.draw()
  
    def get_entry(self):
        return self.entry_x, self.entry_y
    
    def get_exit(self):
        return self.exit_x, self.exit_y

    def set_entry(self,x,y):
        self.entry_x = x
        self.entry_y = y
    
    def set_exit(self,x,y):
        self.exit_x = x
        self.exit_y = y
    
    def redraw(self):
        self.maze = []
        self.generate()
        self.draw()
        
    def draw(self):
        self.screen.fill(0x00000)
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (self.maze[i][j] == self.__unvisited):
                    self.screen.pixel (i,j, 0xffffff)
                    
                elif (self.maze[i][j] == self.__cell):
                    self.screen.pixel (i,j, 0x000000)
                    
                elif (self.maze[i][j] == self.__exit):
                    self.screen.pixel (i,j, 0x00ff00)
                    self.set_exit (i,j)
                    
                elif (self.maze[i][j] == self.__entry):
                    self.screen.pixel (i,j, 0xff0000)
                    self.set_entry (i,j)
                else:
                    self.screen.pixel (i,j, 0x00ffff)
        screen.display()

    # Find number of surrounding cells
    def surroundingCells(self, rand_wall):
        s_cells = 0
        if (self.maze[rand_wall[0]-1][rand_wall[1]] == self.__cell):
            s_cells += 1
        if (self.maze[rand_wall[0]+1][rand_wall[1]] == self.__cell):
            s_cells += 1
        if (self.maze[rand_wall[0]][rand_wall[1]-1] == self.__cell):
            s_cells +=1
        if (self.maze[rand_wall[0]][rand_wall[1]+1] == self.__cell):
            s_cells += 1

        return s_cells
    
    def generate(self):
     # Denote all cells as unvisited
        for i in range(0, self.height):
            line = []
            for j in range(0, self.width):
                line.append(self.__unvisited)
            self.maze.append(line)
            
        # Randomize starting point and set it a cell
        starting_height = int(random.random()*self.height)
        starting_width = int(random.random()*self.width)
        if (starting_height == 0):
            starting_height += 1
        if (starting_height == self.height-1):
            starting_height -= 1
        if (starting_width == 0):
            starting_width += 1
        if (starting_width == self.width-1):
            starting_width -= 1

        # Mark it as cell and add surrounding walls to the list
        self.maze[starting_height][starting_width] = self.__cell
        walls = []
        walls.append([starting_height - 1, starting_width])
        walls.append([starting_height, starting_width - 1])
        walls.append([starting_height, starting_width + 1])
        walls.append([starting_height + 1, starting_width])

        # Denote walls in maze
        self.maze[starting_height-1][starting_width] = self.__walls
        self.maze[starting_height][starting_width - 1] = self.__walls
        self.maze[starting_height][starting_width + 1] = self.__walls
        self.maze[starting_height + 1][starting_width] = self.__walls

        while (walls):
            # Pick a random wall
            rand_wall = walls[int(random.random()*len(walls))-1]

            # Check if it is a left wall
            if (rand_wall[1] != 0):
                if (self.maze[rand_wall[0]][rand_wall[1]-1] == self.__unvisited and self.maze[rand_wall[0]][rand_wall[1]+1] == self.__cell):
                    # Find the number of surrounding cells
                    s_cells = self.surroundingCells(rand_wall)

                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.__cell

                        # Mark the new walls
                        # Upper cell
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != self.__cell):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = self.__walls
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])

                        # Bottom cell
                        if (rand_wall[0] != self.height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != self.__cell):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = self.__walls
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])

                        # Leftmost cell
                        if (rand_wall[1] != 0):	
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != self.__cell):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = self.__walls
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])

                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)

                    continue

            # Check if it is an upper wall
            if (rand_wall[0] != 0):
                if (self.maze[rand_wall[0]-1][rand_wall[1]] == self.__unvisited and self.maze[rand_wall[0]+1][rand_wall[1]] == self.__cell):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.__cell

                        # Mark the new walls
                        # Upper cell
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != self.__cell):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = self.__walls
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])

                        # Leftmost cell
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != self.__cell):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = self.__walls
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])

                        # Rightmost cell
                        if (rand_wall[1] != self.width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != self.__cell):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = self.__walls
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])

                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)

                    continue

            # Check the bottom wall
            if (rand_wall[0] != self.height-1):
                if (self.maze[rand_wall[0]+1][rand_wall[1]] == self.__unvisited and self.maze[rand_wall[0]-1][rand_wall[1]] == self.__cell):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.__cell

                        # Mark the new walls
                        if (rand_wall[0] != self.height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != self.__cell):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = self.__walls
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != self.__cell):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = self.__walls
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])
                        if (rand_wall[1] != self.width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != self.__cell):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = self.__walls
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])

                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)

                    continue

            # Check the right wall
            if (rand_wall[1] != self.width-1):
                if (self.maze[rand_wall[0]][rand_wall[1]+1] == self.__unvisited and self.maze[rand_wall[0]][rand_wall[1]-1] == self.__cell):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.__cell

                        # Mark the new walls
                        if (rand_wall[1] != self.width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != self.__cell):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = self.__walls
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])
                        if (rand_wall[0] != self.height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != self.__cell):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = self.__walls
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != self.__cell):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = self.__walls
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])

                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)

                    continue

            # Delete the wall from the list anyway
            for wall in walls:
                if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                    walls.remove(wall)

        # Mark the remaining unvisited cells as walls
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (self.maze[i][j] == self.__unvisited):
                    self.maze[i][j] = self.__walls

        # Set entrance and exit
        for i in range(0, self.width):
            if (self.maze[1][i] == self.__cell):
                self.maze[0][i] = self.__entry
                break

        for i in range(self.width-1, 0, -1):
            if (self.maze[self.height-2][i] == self.__cell):
                self.maze[self.height-1][i] = self.__exit
                break

class Game:
    # Main Game Class
    def __init__(self):
        self.maze = Maze(screen)
        self.level_count = 1
        self.player_x, self.player_y = self.maze.get_entry()
    
    # Sound effects
    def moveSound(self):
        adafruit_rtttl.play (buzzer, "move:d=4,o=5,b=880:8c6")

    def endLevelSound(self):
        adafruit_rtttl.play (buzzer, "endlevel:d=4,o=5,b=330:8c6,8d6")
    
    def display_message(self, message, color):
        # Marquee Message
        label = Label(text=message, font=font, scale=2)
        bitmap = label.bitmap
        colors = [0, 0]
        hue = 0
        start_time = time.time()
        while time.time() - start_time < 2:  # Display for 2 seconds
            for x in range(bitmap.width):
                hue = hue + 7
                if hue >= 256:
                    hue = hue - 256
                colors[1] = colorwheel(hue)

                for a in range(screen.width - 1):
                    for y in range(screen.height):
                        screen.pixel(a, y, screen.pixel(a + 1, y))

                for y in range(screen.height):
                    bm_y = y - 6 #offset
                    if 0 <= bm_y < bitmap.height:
                        color_index = bitmap[x, bm_y]
                    else:
                        color_index = 0
                    screen.pixel(screen.width - 1, y, colors[color_index])

                screen.display()
                gc.collect()
                time.sleep(0.02)

    def play(self):
        while True:
            screen.pixel(self.player_x, self.player_y, (0, 0, 0))
            dx = int(get_x(joystick_x))
            dy = int(get_y(joystick_y))
            if dx != 0 or dy != 0:
                self.moveSound()
                new_x = self.player_x + dx
                new_y = self.player_y + dy
                if is_valid_move(new_x, new_y):
                    self.player_x = new_x
                    self.player_y = new_y
                    if is_end(self.player_x, self.player_y):
                        screen.pixel(self.player_x, self.player_y, (255, 0, 0))
                        screen.display()
                        self.endLevelSound()
                        self.level_count += 1
                        # Write a Message
                        self.display_message(f' Level {self.level_count} ', 0xff0000)
                        self.maze.redraw()
                        self.player_x, self.player_y = self.maze.get_entry()

            screen.pixel(self.player_x, self.player_y, (255, 0, 0))
            screen.display()
            time.sleep(0.1)

game = Game()
game.play()
