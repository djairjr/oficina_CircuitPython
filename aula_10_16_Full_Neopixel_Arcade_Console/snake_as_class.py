'''
    Snake (Nibbles)
    
    Developed for the "Recriating Arcade Classics with Circuitpython and Neopixels" 
    Workshop At SESC São Paulo (24 de Maio) - Between May 10 and July 4, 2024
    
    Depends:
    displayio, asyncio, simpleio, adafruit_imageload, adafruit_rtttl
    adafruit_ht16k33, adafruit_pixelbuf, neopixel and custom tilegrid and tilebuf
    (only if using 8x32 panels)
    
    Tested in Seeed Xiao RP2040
    
    Thanks to Ronaldo Gonçalves Alves for the pacience, support and ideas at workshop    

'''

import time, random

class Snake:
    def __init__(self, hardware):
        self.hardware = hardware
        self.hardware.screen.rotation = 1
        self.snake_body = []
        self.score = 0
        
        # A biblioteca não ajusta altura e largura automaticamente
        # Sempre pressupoe que a rotação é 0. Temos que fazer isso
        # em todos os jogos
        
        self.screen_width = self.hardware.screen.height # trocando largura e altura
        self.screen_height = self.hardware.screen.width
        
        self.snake_x = self.screen_width // 2
        self.snake_y = self.screen_height // 2
        
        self.direction_x = 0 # Horizontal
        self.direction_y = 1 # Vertical
        
        self.generate_food()
        self.resetsnake()

    def generate_food(self):
        while True:
            self.food = [random.randint(0, self.screen_width - 1), random.randint(0, self.screen_height - 1)]
            # Check if food is in snake body. Because it is random, it can occur...
            if self.food not in self.snake_body:
                break
    
    def resetsnake(self):
        self.snake_x = self.screen_width // 2
        self.snake_y = self.screen_height // 2
        
        self.snake_body = [
            [self.snake_x, self.snake_y], # Head
            [self.snake_x, self.snake_y - 1],
            [self.snake_x, self.snake_y - 2]
        ]
    
    
    def gameover(self):
        self.hardware.display.marquee("Ouch", loop=False)
        self.score = 0
        self.generate_food()
        self.resetsnake()
        
    def play(self):

        while True:
            self.hardware.display.print('{0:04}'.format (self.score))
            # Check correct axis
            new_direction_y, new_direction_x = self.hardware.get_direction()

            if new_direction_x != 0 or new_direction_y !=0:
                if (new_direction_x != -self.direction_x or new_direction_y != -self.direction_y):
                    self.direction_x = new_direction_x
                    self.direction_y = new_direction_y

            # Calculate snake head position x, y coordinates
            new_head = [self.snake_body[0][0] + self.direction_x, self.snake_body[0][1] + self.direction_y]

            # Check game over condition. Snake beyond screen or snake head in snake body
            if (
                new_head[0] < 0 or new_head[0] >= self.screen_width or
                new_head[1] < 0 or new_head[1] >= self.screen_height or
                new_head in self.snake_body
            ):
                
                self.gameover()
                
            else:
                # Increase and show score points
                self.snake_body.insert(0, new_head)


                # Check if the snake ate the food
                if self.snake_body[0] == self.food:
                    self.score += 10
                    self.generate_food()
                else:
                    self.snake_body.pop()

                # Clear screen and draw
                self.hardware.screen.fill(0)
                
                # Draw snake head and body
                for segment in self.snake_body:
                    self.hardware.screen.pixel(segment[0], segment[1], 0x00FF00)  # Snake
                
                # Draw Food
                self.hardware.screen.pixel(self.food[0], self.food[1], 0xFF0000)
                
                # Show everything
                self.hardware.screen.display()
                time.sleep(0.1)
