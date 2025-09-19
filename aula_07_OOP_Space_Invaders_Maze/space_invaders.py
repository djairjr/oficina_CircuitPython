import board, time, random, gc
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range
import adafruit_rtttl

import neopixel
from adafruit_pixel_framebuf import PixelFramebuf, VERTICAL

from rainbowio import colorwheel
import framebufferio

pixel_pin = board.A0
pixel_width = 16
pixel_height = 16
num_tiles = 2

joystick_x = AnalogIn(board.A1)
joystick_y = AnalogIn(board.A2)

trigger = DigitalInOut(board.D6)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

buzzer = board.D7

pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height * num_tiles, # dont forget to multiply for num_tiles
    brightness=0.1,
    auto_write=False,
)

screen = PixelFramebuf(
    pixels,
    pixel_width * num_tiles,
    pixel_height,
    orientation = VERTICAL,
    rotation = 0
)

# Creating colors
COLORS = [
    0x000000,  # Black
    0xFF0000,  # Red
    0xFF7F00,  # Orange
    0xFFFF00,  # Yellow
    0x00FF00,  # Green
    0x0000FF,  # Blue
    0x4B0082,  # Indigo
    0x8B00FF   # Violet
]

def get_joystick():
    x_coord = int(map_range(joystick_x.value, 200, 65535, -2, 2))
    y_coord = int(map_range(joystick_y.value, 200, 65535, -2, 2))
    return x_coord, y_coord

# Sounds
def shoot_sound():
    adafruit_rtttl.play(buzzer, "shoot:d=4,o=5,b=880:8c6")
    
def xevious_sound():
    adafruit_rtttl.play(buzzer, "Xevious:d=4,o=5,b=160:16c,16c6,16b,16c6,16e6,16c6,16b,16c6,16c,16c6,16a#,16c6,16e6,16c6,16a#,16c6,16c,16c6,16a,16c6,16e6,16c6,16a,16c6,16c,16c6,16g#,16c6,16e6,16c6,16g#,16c6")

def galaga_sound():
    adafruit_rtttl.play(buzzer, "Galaga:d=4,o=5,b=125:8g4,32c,32p,8d,32f,32p,8e,32c,32p,8d,32a,32p,8g,32c,32p,8d,32f,32p,8e,32c,32p,8g,32b,32p,8c6,32a#,32p,8g#,32g,32p,8f,32d#,32p,8d,32a#4,32p,8a#,32c6,32p,8a#,32g,32p,16a,16f,16d,16g,16e,16d")

class Invader:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 2
        self.height = 2
        self.color = random.choice(COLORS[1:])

    def draw(self):
        for i in range(self.width):
            for j in range(self.height):
                screen.pixel(self.x + i, self.y + j, self.color)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        if self.x < 0 or self.x >= screen.width - 1:
            self.x = -1

    def shoot(self):
        return Projectile(self.x + 1, self.y + 2, COLORS[1])

class PlayerShip:
    def __init__(self):
        # Posição X: centro da tela (metade da largura menos metade da largura da nave)
        self.x = (screen.width - 3) // 2
        # Posição Y: base da tela (altura da tela menos altura da nave)
        self.y = screen.height - 2  # A nave tem 2 pixels de altura
        self.lives = 3
        self.exploding = False
        self.explode_timer = 0

    def draw(self):
        if self.exploding:
            self.draw_explosion()
        else:
            # Desenha a nave do jogador (formato de triângulo)
            screen.pixel(self.x, self.y, COLORS[5])        # Ponto esquerdo inferior
            screen.pixel(self.x + 1, self.y, COLORS[5])    # Ponto central inferior
            screen.pixel(self.x + 1, self.y - 1, COLORS[5]) # Ponto central superior
            screen.pixel(self.x + 2, self.y, COLORS[5])    # Ponto direito inferior

    def draw_explosion(self):
        screen.pixel(self.x, self.y, COLORS[1])
        screen.pixel(self.x + 1, self.y, COLORS[1])
        screen.pixel(self.x + 1, self.y - 1, COLORS[1])
        screen.pixel(self.x + 2, self.y, COLORS[1])

    def draw_lives(self):
        total_width = self.lives * 2 + (self.lives - 1) * 1
        start_x = (screen.width - total_width) // 2
        for i in range(self.lives):
            x_offset = start_x + i * 3
            for dx in range(2):
                for dy in range(2):
                    # Usando screen.height - 2 para ficar na parte inferior da tela
                    screen.pixel(x_offset + dx, screen.height - 2 + dy, COLORS[5])

    def move(self, dx):
        self.x += dx
        # Limita o movimento dentro dos limites da tela
        if self.x < 0:
            self.x = 0
        if self.x >= screen.width - 3:  # 3 é a largura da nave
            self.x = screen.width - 4

    def explode(self):
        self.exploding = True
        self.explode_timer = time.monotonic()

class Projectile:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        screen.pixel(self.x, self.y, self.color)

    def move(self, dy):
        self.y += dy
        if self.y < 0 or self.y >= screen.height:
            self.y = -1

# Variáveis globais do jogo
invaders = []
player_ship = PlayerShip()
projectiles = []
enemy_projectiles = []
score = 0
level = 1
invader_move_direction = 1
invader_speed = 0.1
game_over = False
reverse = False
last_update_time = time.monotonic()
last_shot_time = 0

def resetinvaders():
    global invaders
    invaders = []
    # Posiciona os invasores na parte superior da tela
    for i in range(4):
        for j in range(4):
            # Centraliza os invasores horizontalmente
            start_x = (screen.width - 16) // 2  # 16 = 4 invasores * 4 pixels de espaçamento
            invaders.append(Invader(start_x + i * 4, j * 2))

def draw_game():
    gc.collect()
    screen.fill(0)
    
    for invader in invaders:
        invader.draw()
        
    player_ship.draw()
    player_ship.draw_lives()
    
    for projectile in projectiles:
        projectile.draw()
        
    for projectile in enemy_projectiles:
        projectile.draw()
        
    if game_over:
        screen.fill(0)
        print('Game Over')
        xevious_sound()
        
    screen.display()

def update_game(dt):
    global invaders, projectiles, enemy_projectiles, score, game_over, reverse
    global invader_move_direction, last_shot_time
    
    gc.collect()
    dx, dy = get_joystick()
    player_ship.move(dy)
    
    # Disparar com botão
    current_time = time.monotonic()
    if not trigger.value and current_time - last_shot_time > 0.2:
        # Dispara do centro da nave (x + 1)
        projectiles.append(Projectile(player_ship.x + 1, player_ship.y - 1, COLORS[7]))
        last_shot_time = current_time
        shoot_sound()

    # Move player projectiles
    for projectile in projectiles[:]:
        projectile.move(-1)
        if projectile.y == -1:
            projectiles.remove(projectile)

        # Check for collision with invaders
        for invader in invaders[:]:
            if invader.x <= projectile.x < invader.x + 2 and invader.y <= projectile.y < invader.y + 2:
                invaders.remove(invader)
                shoot_sound()
                if projectile in projectiles:
                    projectiles.remove(projectile)
                score += 10
                print('{0:04}'.format(score))
                if score % 1000 == 0:
                    player_ship.lives += 1
                break

        # Check for collision with enemy projectiles
        for enemy_projectile in enemy_projectiles[:]:
            if projectile.x == enemy_projectile.x and projectile.y == enemy_projectile.y:
                enemy_projectiles.remove(enemy_projectile)
                if projectile in projectiles:
                    projectiles.remove(projectile)
                break

    # Move enemy projectiles
    for projectile in enemy_projectiles[:]:
        projectile.move(1)
        if projectile.y == -1:
            enemy_projectiles.remove(projectile)

        # Check for collision with player ship
        if player_ship.x <= projectile.x < player_ship.x + 3 and player_ship.y <= projectile.y < player_ship.y + 3:
            player_ship.lives -= 1
            player_ship.explode()
            enemy_projectiles.remove(projectile)
            if player_ship.lives <= 0:
                game_over = True

    # Move invaders
    for invader in invaders[:]:
        invader.move(invader_move_direction, 0)

        # Check collision between invaders and player ship
        if invader.x <= player_ship.x < invader.x + invader.width and invader.y <= player_ship.y < invader.y + invader.height:
            player_ship.lives -= 1
            invaders.remove(invader)
            if player_ship.lives <= 0:
                game_over = True

    # Check for invader edge collision
    if any(invader.x >= screen.width - 2 or invader.x <= 0 for invader in invaders):
        invader_move_direction *= -1
        for invader in invaders:
            if not reverse:
                invader.move(0, 1)
            else:
                invader.move(0, -1)

    # Check if invader is near player ship
    if any(invader.y >= player_ship.y - 1 for invader in invaders):
        reverse = True
    if any(invader.y <= 0 for invader in invaders):
        reverse = False

    # Enemy shooting
    if len(invaders) <= 3 and random.random() < 0.03:
        shooter = random.choice(invaders)
        enemy_projectiles.append(shooter.shoot())

    if not invaders:
        screen.fill(0)
        screen.display()
        projectiles[:] = []
        enemy_projectiles[:] = []
        resetinvaders()
        xevious_sound()

def reset_game():
    global invaders, player_ship, projectiles, enemy_projectiles
    global score, level, invader_move_direction, game_over, reverse
    
    screen.fill(0)
    screen.display()
    
    invaders = []
    player_ship = PlayerShip()
    projectiles = []
    enemy_projectiles = []
    score = 0
    level = 1
    invader_move_direction = 1
    game_over = False
    reverse = False
    
    resetinvaders()
    draw_game()
    galaga_sound()

# Inicializar o jogo
reset_game()

# Loop principal do jogo
while True:
    if not game_over:
        current_time = time.monotonic()
        dt = current_time - last_update_time
        last_update_time = current_time
        update_game(dt)
        draw_game()
        time.sleep(0.02)
    else:
        # Aguardar reinício do jogo (pode adicionar lógica para reiniciar com um botão)
        time.sleep(1)
        # Para reiniciar automaticamente, descomente a linha abaixo:
        # reset_game()