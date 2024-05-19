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

from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range

# My custom version
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

def get_x(pin):
    return map_range (pin.value, 200, 65535, - 2 , 2) 

def get_y(pin):
    return map_range (pin.value, 200, 65535, - 2 , 2)

def get_pixel_color(x, y):
    # Ajusta as coordenadas com base na rotação da tela
    if screen.rotation == 1:
        x, y = y, x
        x = screen._width - x - 1
    elif screen.rotation == 2:
        x = screen._width - x - 1
        y = screen._height * screen._tile_num - y - 1
    elif screen.rotation == 3:
        x, y = y, x
        y = screen._height * screen._tile_num - y - 1

    # Verifica se as coordenadas ajustadas estão dentro dos limites válidos
    if (0 <= x < screen._width) and (0 <= y < screen._height * screen._tile_num):
        # Obtém o pixel ajustado da tela
        rgbint = screen.format.get_pixel(screen, x, y)
        return (rgbint // 256 // 256 % 256, rgbint // 256 % 256, rgbint % 256)

    # Retorna preto (0, 0, 0) se estiver fora dos limites
    return (0, 0, 0)

# Função para definir a cor de um pixel específico
def set_pixel_color(x, y, color):
    screen.pixel(x, y, color)

# Função para verificar se a nova posição é válida
def is_valid_move(x, y):
    if x < 0 or x >= screen._width or y < 0 or y >= screen._height * screen._tile_num:
        return False
    color = get_pixel_color(x, y)
    return color != (0, 255, 255)  # A cor das paredes é 0x00ffff

# Função para verificar se o jogador alcançou o final
def is_end(x, y):
    color = get_pixel_color(x, y)
    print(f"Verificando se ({x}, {y}) é o final: {color}")
    return color == (0, 255, 0)  # A cor do final é 0x00ff00

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

maze = Maze(screen)

player_x, player_y = maze.get_entry()
set_pixel_color(player_x, player_y, (255, 0, 0))


while True:
    time.sleep(0.1)  

    # Obtém a direção do joystick
    move_x = int (get_x(joystick_x))
    move_y = int (get_y(joystick_y))

    # Calcula a nova posição potencial do jogador
    new_x = player_x + move_x
    new_y = player_y + move_y
    
    # Verifica se a nova posição é válida
    if is_valid_move(new_x, new_y):
        if is_end(new_x, new_y):
            print("Você alcançou o final do labirinto!")
            set_pixel_color(player_x, player_y, (0, 0, 0))

            # Atualiza a posição do jogador
            player_x, player_y = new_x, new_y

            # Define a nova cor da posição do jogador
            set_pixel_color(player_x, player_y, (255, 0, 0))
       
            screen.display()
            time.sleep(2)
            break
        else:
            print ('Movendo para ', new_x, new_y)
            # Apaga a cor da posição antiga do jogador
            set_pixel_color(player_x, player_y, (0, 0, 0))

            # Atualiza a posição do jogador
            player_x, player_y = new_x, new_y

            # Define a nova cor da posição do jogador
            set_pixel_color(player_x, player_y, (255, 0, 0))
       
            screen.display()
