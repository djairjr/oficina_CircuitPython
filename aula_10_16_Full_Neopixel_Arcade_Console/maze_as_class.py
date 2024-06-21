"""
    Original code from Orestis Zekai
    in https://github.com/OrWestSide/python-scripts/blob/master/maze.py
    From Medium Article in: https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e
    
    Developed for the "Recriating Arcade Classics with Circuitpython and Neopixels" 
    Workshop At SESC São Paulo (24 de Maio) - Between May 10 and July 4, 2024
    
    Depends:
    displayio, asyncio, simpleio, adafruit_imageload, adafruit_rtttl
    adafruit_ht16k33, adafruit_pixelbuf, neopixel and custom tilegrid and tilebuf
    (only if using 8x32 panels)
    
    Tested in Seeed Xiao RP2040
    
    Thanks to Ronaldo Gonçalves Alves for the pacience, support and ideas at workshop
"""

import time, gc, asyncio
import board, random
import adafruit_rtttl

gc.enable()

class Maze():
    # This class create and draw a maze
    def __init__(self, hardware):
        gc.collect()
        self.hardware = hardware
        
        if self.hardware.screen.rotation == 1 or self.hardware.screen.rotation == 3:
            self.height = self.hardware.screen.height
            self.width = self.hardware.screen.width
        else:
            self.height = self.hardware.screen.width
            self.width = self.hardware.screen.height
            
        self.__unvisited = 'u'
        self.__cell = ' '
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
        gc.collect()
        self.maze = []
        self.generate()
        self.draw()
        
    def draw(self):
        gc.collect()
        self.hardware.screen.fill(0x00000)
        
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (self.maze[i][j] == self.__unvisited):
                    self.hardware.screen.pixel (i,j, 0xffffff)
                    
                elif (self.maze[i][j] == self.__cell):
                    self.hardware.screen.pixel (i,j, 0x000000)
                    
                elif (self.maze[i][j] == self.__exit):
                    self.hardware.screen.pixel (i,j, 0x00ff00)
                    self.set_exit (i,j)
                    
                elif (self.maze[i][j] == self.__entry):
                    self.hardware.screen.pixel (i,j, 0xff0000)
                    self.set_entry (i,j)
                else:
                    self.hardware.screen.pixel (i,j, 0x00ffff)
        '''
        position = 0
        for line in self.maze:
            print (position, line)
            position+=1
        '''
        self.hardware.screen.display()

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

class MazeGame:
    # Main Game Class
    def __init__(self, hardware, time_limit=60):
        gc.collect()
        self.hardware = hardware
        
        self.maze = Maze(self.hardware)
        self.level_count = 1
        self.player_x, self.player_y = self.maze.get_entry()
        self.new_x, self.new_y = self.player_x, self.player_y
        self.time_limit = time_limit
        self.score = 0
           
    def gameOver(self):
        self.hardware.display.marquee ("GAME OVER    ", loop = False)
        gc.collect()
        self.level_count = 1
        self.time_limit = 60
        self.score = 0
        self.maze = Maze(self.hardware.screen)
        self.player_x, self.player_y = self.maze.get_entry()
        self.play()
        
    async def countdown(self):
        gc.collect()
        current_time = time.monotonic()
        end_time = current_time + self.time_limit

        while current_time < end_time:
            remaining_time = end_time - current_time
            self.mins, self.secs = divmod(remaining_time, 60)
            self.mins, self.secs = int(self.mins), int(self.secs)  # Converter para inteiros
            timeformat = '{:04d}'.format(self.mins *60 + self.secs)
            self.hardware.display.print(timeformat)
            await asyncio.sleep(0.1)
            current_time = time.monotonic()
        
        self.gameOver()
           
    # Sound effects
    def moveSound(self):
        self.hardware.play_rtttl ("move:d=4,o=5,b=880:16c4,16a4")

    def endLevelSound(self):
        self.hardware.play_rtttl ("endlevel:d=4,o=5,b=330:16c6,16d6")
    
    async def run_game(self):
        gc.collect()
        # Inicia a contagem regressiva em segundo plano
        self.countdown_task = asyncio.create_task(self.countdown())
        
        while True:
            gc.collect()
            self.hardware.screen.pixel(self.player_x, self.player_y, (0, 0, 0))
            dx, dy = self.hardware.get_direction()

            if dx != 0 or dy != 0:
                
                # Increase or decrease player position
                self.new_x = self.player_x - dx
                self.new_y = self.player_y - dy
                print (self.new_x, self.new_y)
                
                if self.hardware.check_wall(self.new_x, self.new_y, (0,255,255)):
                    # No wall?
                    self.moveSound()
                    self.player_x = self.new_x
                    self.player_y = self.new_y
                    
                    
                # Check if is end of maze (Green Color)
                if self.hardware.check_color(self.player_x, self.player_y, 0x00ff00):
                    self.hardware.screen.pixel(self.player_x, self.player_y, (255, 0, 0))
                    self.hardware.screen.display()
                    self.endLevelSound()
                    self.level_count += 1
                    self.score = self.score + self.secs * 10
                    print (self.secs, self.score)
                    # Reinicia a contagem regressiva para o próximo nível
                    if self.countdown_task:
                        self.countdown_task.cancel()
                        self.countdown_task = asyncio.create_task(self.countdown())
                    # Write a Message
                    self.hardware.display.marquee (f' Score {self.score}    Level {self.level_count}    ', loop=False)
                    self.maze.redraw()
                    self.player_x, self.player_y = self.maze.get_entry()
                
                               

            self.hardware.screen.pixel(self.player_x, self.player_y, (255, 0, 0))
            
            self.hardware.screen.display()
            await asyncio.sleep(0.1)
        
    def play(self):
        gc.collect()
        self.hardware.display.marquee("Maze Game    ", loop=False)
        asyncio.run(self.run_game())
