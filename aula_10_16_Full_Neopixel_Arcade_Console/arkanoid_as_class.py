'''
    ARKANOID GAME on Neopixels - 21/06/2024
    Developed for the "Recriating Arcade Classics with Circuitpython and Neopixels" 
    Workshop At SESC São Paulo (24 de Maio) - Between May 10 and July 4, 2024
    
    Depends:
    displayio, asyncio, simpleio, adafruit_imageload, adafruit_rtttl
    adafruit_ht16k33, adafruit_pixelbuf, neopixel and custom tilegrid and tilebuf
    (only if using 8x32 panels)
    
    Tested in Seeed Xiao RP2040
    
    Thanks to Ronaldo Gonçalves Alves for the pacience, support and ideas at workshop
'''

import time, gc
gc.enable()

class Arkanoid:
    def __init__(self, hardware):
        self.hardware = hardware

        self.screen_width = hardware.screen.height
        self.screen_height = hardware.screen.width
        self.hardware.screen.rotation = 1 # Easier than change all the code... again

        self.paddle_width = 5
        self.paddle_height = 1
        self.paddle_x = (self.screen_width - self.paddle_width) // 2  # Center Paddle
        self.paddle_y = self.screen_height - 1  # Last line of Screen
        self.paddle_speed = 1

        self.ball_x = self.paddle_x + (self.paddle_width // 2)
        self.ball_y = self.paddle_y - 1
        self.ball_x_speed = 1
        self.ball_y_speed = -1

        self.bar_width = 3
        self.bar_height = 2
        self.bars_spacing = 1
        self.bars_list = []

        self.start_song = 'Arkanoid:d=4,o=5,b=140:8g6,16p,16g.6,2a#6,32p,8a6,8g6,8f6,8a6,2g6'

        self.rainbow_colors = [
            0xFF0000,  # Vermelho
            0xFF7F00,  # Laranja
            0xFFFF00,  # Amarelo
            0x00FF00,  # Verde
            0x0000FF,  # Azul
            0x4B0082,  # Índigo
            0x8B00FF   # Violeta
        ]

        # Level, Score and Lives
        self.score = 0
        self.lives = 3
        self.level = 1

        self.reset_game()

    def create_bars(self):
        self.bars_list = []
        color_index = 0

        num_bars_x = 4
        num_bars_y = 7

        for x in range(num_bars_x):
            for y in range(num_bars_y):
                bar_x = x * (self.bar_width + self.bars_spacing)
                bar_y = y * (self.bar_height + self.bars_spacing)
                color = self.rainbow_colors[color_index % len(self.rainbow_colors)]
                self.bars_list.append((bar_y, bar_x, color))
                color_index += 1

    def draw(self):
        self.hardware.screen.fill(0x000000)
        self.draw_bars()
        self.draw_paddle()
        self.draw_ball()
        self.hardware.screen.display()

    def draw_paddle(self):
        self.hardware.screen.fill_rect(self.paddle_x, self.paddle_y, self.paddle_width, self.paddle_height, 0x007fff)

    def draw_bars(self):
        for bar_y, bar_x, color in self.bars_list:
            self.hardware.screen.fill_rect(bar_x, bar_y, self.bar_width, self.bar_height, color)
            
    def draw_ball(self):
        self.hardware.screen.pixel(self.ball_x, self.ball_y, 0xff0000)

    def update(self):
        self.move_paddle()

        self.ball_x += self.ball_x_speed
        self.ball_y += self.ball_y_speed

        if self.ball_y >= self.screen_height:
            self.lives -= 1
            liveStr = 'Lives ' + str(self.lives) + '    '
            self.hardware.display.marquee(liveStr, loop=False)
            if self.lives <= 0:
                self.hardware.display.marquee('Game Over', loop=False)
                    
                self.reset_game()
            else:
                self.reset_ball()

        if self.ball_x <= 0 or self.ball_x >= (self.screen_width - 1):
            self.ball_x_speed *= -1
        if self.ball_y <= 0:
            self.ball_y_speed *= -1

        if (
            self.ball_y == self.paddle_y - 1
            and self.paddle_x <= self.ball_x < self.paddle_x + self.paddle_width
        ):
            self.ball_y_speed *= -1

            # Aplica a velocidade angular dependendo da posição da bola no paddle e movimento do paddle
            paddle_center = self.paddle_x + self.paddle_width // 2
            if self.ball_x < paddle_center - self.paddle_width // 3:
                self.ball_x_speed = -1
                self.ball_y_speed = -2
            elif self.ball_x > paddle_center + self.paddle_width // 3:
                self.ball_x_speed = 1
                self.ball_y_speed = -2
            else:
                self.ball_x_speed = 0
                self.ball_y_speed = -2

            # Ajusta a velocidade horizontal baseado no movimento do paddle
            if self.paddle_x < self.last_paddle_x:
                self.ball_x_speed -= 1
            elif self.paddle_x > self.last_paddle_x:
                self.ball_x_speed += 1

            # Atualiza a última posição do paddle
            self.last_paddle_x = self.paddle_x

        for bar in self.bars_list:
            bar_y, bar_x, _ = bar
            if (
                bar_x <= self.ball_x <= bar_x + self.bar_width
                and bar_y <= self.ball_y <= bar_y + self.bar_height
            ):
                self.bars_list.remove(bar)
                self.ball_y_speed *= -1
                self.score += 50
                self.scoreFormat = '{0:04}'.format (self.score)
                self.hardware.display.print(self.scoreFormat)

        if not self.bars_list:
            self.paddle_width -= 1
            self.create_bars()
            self.reset_ball()
            self.level += 1
            levelStr = 'Level ' + str(self.level) + '    '
            self.hardware.display.marquee(levelStr, loop=False)
            self.reset_game()

    def move_paddle(self):
        x, y = self.hardware.get_direction()
        if y == 1:
            self.paddle_x = min(self.paddle_x + self.paddle_speed, self.screen_width - self.paddle_width - 1)
        elif y == -1:
            self.paddle_x = max(self.paddle_x - self.paddle_speed, 0)

    def reset_ball(self):
        self.ball_x = self.paddle_x + (self.paddle_width // 2)
        self.ball_y = self.paddle_y - 1
        self.ball_x_speed = 1
        self.ball_y_speed = -1

    def reset_game(self):
        self.score = 0
        self.lives = 3
        self.paddle_width = 5
        self.create_bars()
        self.reset_ball()
        gc.collect()
        self.draw()

    def play(self):
        self.reset_game()
        self.last_paddle_x = self.paddle_x  # Inicializa a última posição do paddle
        while self.lives > 0:
            self.update()
            self.draw()
            time.sleep(0.01)


'''
Para jogar sem o uso do sistema de menus:

from hardware import Hardware
hw = Hardware () # se o painel for 16x16
ou
hw = Hardware (panel_16x16=False) # se for 32x8
arka = Arkanoid (hw)
arka.play()

'''