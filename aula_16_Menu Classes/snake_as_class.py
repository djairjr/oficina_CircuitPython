import time
import random

class Snake:
    def __init__(self, hardware):
        self.hardware = hardware
        self.hardware.screen.rotation = 2
        self.score = 0
        self.pixel_width = hardware.pixel_width
        self.pixel_height = hardware.pixel_height
        self.snake_body = [
            [self.pixel_height // 2, self.pixel_width // 2],
            [self.pixel_height // 2, self.pixel_width // 2 - 1],
            [self.pixel_height // 2, self.pixel_width // 2 - 2]
        ]
        self.food = [random.randint(0, self.pixel_height - 1), random.randint(0, self.pixel_width - 1)]
        self.direction = (0, 1)  # Move to right

    def generate_food(self):
        while True:
            self.food = [random.randint(0, self.pixel_height - 1), random.randint(0, self.pixel_width - 1)]
            # Check if food is in snake body. Because it is random, it can occur...
            if self.food not in self.snake_body:
                break

    def play(self):
        while True:
            self.hardware.display.print('{0:04}'.format (self.score))
            new_direction = self.hardware.get_direction()
            if new_direction != (0, 0) and (new_direction[0] != -self.direction[0] or new_direction[1] != -self.direction[1]):
                self.direction = new_direction

            # Calculate snake head position x, y coordinates
            new_head = [self.snake_body[0][0] + self.direction[0], self.snake_body[0][1] + self.direction[1]]

            # Check game over condition. Snake beyond screen or snake head in snake body
            if (
                new_head[0] < 0 or new_head[0] >= self.pixel_height or
                new_head[1] < 0 or new_head[1] >= self.pixel_width or
                new_head in self.snake_body
            ):
                # Count lives remaining, show lives message
                self.snake_body = [
                    [self.pixel_height // 2, self.pixel_width // 2],
                    [self.pixel_height // 2, self.pixel_width // 2 - 1],
                    [self.pixel_height // 2, self.pixel_width // 2 - 2]
                ]
                self.score = 0
                
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
                    self.hardware.screen.pixel(segment[1], segment[0], 0x00FF00)  # Snake
                
                # Draw Food
                self.hardware.screen.pixel(self.food[1], self.food[0], 0xFF0000)
                
                # Show everything
                self.hardware.screen.display()
                time.sleep(0.1)
