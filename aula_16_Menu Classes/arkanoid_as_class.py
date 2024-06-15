import time

class Arkanoid:
    def __init__(self, hardware):
        self.hardware = hardware
        self.paddle_width = 6
        self.paddle_height = 1
        self.paddle_x = (self.hardware.pixel_width - self.paddle_width) // 2  # Centraliza o paddle horizontalmente
        self.paddle_y = self.hardware.pixel_height - 1  # Paddle na última linha da tela
        self.paddle_speed = 1

        self.ball_x = self.paddle_x + (self.paddle_width // 2)
        self.ball_y = self.paddle_y - 1
        self.ball_x_speed = 1
        self.ball_y_speed = -1

        self.bar_width = 3
        self.bar_height = 2
        self.bars_spacing = 1
        self.bars_list = []
        self.bars_offset = 4
        
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

        # Pontuação e Vidas
        self.score = 0
        self.lives = 3
        self.level = 1
        print ('Init concluído')
        self.reset_game()

    def create_bars(self):
        print('Criando blocos')
        self.bars_list = []
        color_index = 0
        
        # Usando pixel_width e pixel_height corretamente
        '''
        num_bars_x = (self.hardware.pixel_height // self.bar_height + self.bars_spacing)  - self.bars_offset
        num_bars_y = self.hardware.pixel_width // self.bar_width + self.bars_spacing
        '''
        
        num_bars_x = 4
        num_bars_y = 4        
        
        print ("Largura da Tela ",self.hardware.pixel_height )
        print ("Largura da Tela ",self.hardware.pixel_width )
        print("Número de barras ao longo do eixo x:", num_bars_x)
        print("Número de barras ao longo do eixo y:", num_bars_y)
        
        for y in range(num_bars_y):
            for x in range(num_bars_x):
                bar_x = x * (self.bar_width + self.bars_spacing)
                bar_y = y * (self.bar_height + self.bars_spacing)
                print (bar_x, bar_y)
                color = self.rainbow_colors[color_index % len(self.rainbow_colors)]
                # Trocando bar_x por bar_y e bar_y por bar_x
                self.bars_list.append((bar_y, bar_x, color))
                color_index += 1

    def draw(self):
        print ('Desenhando elementos')
        self.hardware.screen.fill(0x000000)
        self.draw_bars()
        self.draw_paddle()
        self.draw_ball()      
        self.hardware.screen.display()  

    def draw_paddle(self):
        print ('Paddle ')
        # Trocando paddle_x por paddle_y e paddle_y por paddle_x
        self.hardware.screen.fill_rect(self.paddle_y, self.paddle_x, self.paddle_height, self.paddle_width, 0x007fff)

    def draw_bars(self):
        print ('Bars')
        for bar_x, bar_y, row in self.bars_list:
            color = self.rainbow_colors[row % len(self.rainbow_colors)]
            # Trocando bar_x por bar_y e bar_y por bar_x
            self.hardware.screen.fill_rect(bar_y, bar_x, self.bar_height, self.bar_width, color)
            
    def draw_ball(self):
        print ('Ball')
        # Trocando ball_x por ball_y e ball_y por ball_x
        self.hardware.screen.pixel(self.ball_y, self.ball_x, 0xff0000)

    def update(self):
        # Move o paddle com o joystick
        self.move_paddle()

        # Atualiza a posição da bola
        self.ball_x += self.ball_x_speed
        self.ball_y += self.ball_y_speed

        # Verifica a posição da bola
        if self.ball_y >= self.hardware.pixel_height:
            self.lives -= 1
            liveStr = 'Lives ' + str(self.lives) + '    '
            self.hardware.display.marquee(liveStr, loop=False)
            if self.lives <= 0:
                self.hardware.display.marquee('Game Over', loop=False)
                self.reset_game()
            else:
                self.reset_ball()

        # Verifica colisão com as paredes (limites da tela)
        if self.ball_x <= 0 or self.ball_x >= (self.hardware.pixel_width - 1):
            self.ball_x_speed *= -1
        if self.ball_y <= 0:
            self.ball_y_speed *= -1

        # Verifica colisão com o paddle
        if (
            self.ball_y == self.paddle_y - 1
            and self.paddle_x <= self.ball_x < self.paddle_x + self.paddle_width
        ):
            self.ball_y_speed *= -1

        # Verifica colisão com os blocos e remove o bloco
        for bar in self.bars_list:
            bar_x, bar_y, _ = bar
            if (
                bar_x <= self.ball_x <= bar_x + self.bar_width
                and bar_y <= self.ball_y <= bar_y + self.bar_height
            ):
                self.bars_list.remove(bar)
                self.ball_y_speed *= -1
                self.score += 50
                self.hardware.display.print("{0:04}".format(self.score))

        # Verifica se todos os blocos foram destruídos
        if not self.bars_list:
            print ('No bars')
            self.hardware.screen.fill(0)
            self.hardware.screen.display()
            if self.paddle_width > 2:
                self.paddle_width -= 1
            self.create_bars()
            self.reset_ball()
            levelStr = "Level " + str(self.level) + "    "
            print (levelStr)
            self.hardware.display.marquee(levelStr, loop=False)
            self.level += 1
            print ('Resetando Jogo')
            time.sleep(3)  # Espera 3 segundos antes de iniciar o próximo nível
            self.reset_game()

    def move_paddle(self):
        x,y = self.hardware.get_direction()
        # Move para a esquerda
        if y == 1:
            self.paddle_x = max(self.paddle_x - self.paddle_speed, 0)
        # Move para a direita
        elif y == -1 :
            self.paddle_x = min(self.paddle_x + self.paddle_speed, self.hardware.pixel_height - self.paddle_width)

    def reset_ball(self):
        print ('Reset Ball')
        self.ball_x = self.paddle_x + (self.paddle_width // 2)
        self.ball_y = self.paddle_y - 1
        self.ball_x_speed = 1
        self.ball_y_speed = -1

    def reset_game(self):
        # self.hardware.display.marquee("Arkanoid    ", loop=False)
        print ('Reset Game')
        self.score = 0
        self.lives = 3
        self.paddle_width = 6
        self.create_bars()
        self.reset_ball()
        self.draw()

    def play(self):
        print ('Play Game')
        self.reset_game()
        while self.lives > 0:
            self.update()
            self.draw()
            time.sleep(0.01)

