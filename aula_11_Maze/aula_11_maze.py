"""
    Original code from Orestis Zekai
    in https://github.com/OrWestSide/python-scripts/blob/master/maze.py
    From Medium Article in: https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e
    Adapted by Djair Guilherme (Nicolau dos Brinquedos)
    For the "Recriating Arcade Games in Circuitpython, Neopixel and Seeed Xiao RP2040"
    SESC Workshop - São Paulo - Brazil - May 2024
    Requirements: custom tilegrid, tile_framebuf, my_framebuf libraries
    Available at: https://github.com/djairjr/oficina_CircuitPython/tree/main/aula_6_Neopixel/libraries
"""

import time
import board, random
import neopixel_spi as neopixel
import displayio
import adafruit_imageload
from rainbowio import colorwheel

# My custom version
from tile_framebuf import TileFramebuffer
spi = board.SPI()

pixel_pin = board.D10
pixel_width = 32
pixel_height = 8
num_tiles = 2
num_pixels = pixel_width * pixel_height * num_tiles

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


class Maze():
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
        self.generate()
        self.draw()
    
    def redraw(self):
        self.maze = []
        self.generate()
        self.draw()
        
    def draw(self):
        self.screen.fill(0x00000)
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (self.maze[i][j] == self.__unvisited):
                    self.screen.pixel (i,j, 0x00ff00)
                    
                elif (self.maze[i][j] == self.__cell):
                    self.screen.pixel (i,j, 0x000000)
                    
                elif (self.maze[i][j] == self.__exit):
                    self.screen.pixel (i,j, 0xffffff)
                    
                elif (self.maze[i][j] == self.__entry):
                    self.screen.pixel (i,j, 0xff0000)
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

maze = Maze(screen)
