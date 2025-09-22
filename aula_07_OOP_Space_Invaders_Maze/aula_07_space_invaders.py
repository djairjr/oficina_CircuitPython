import board, time, random, gc
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range
import adafruit_rtttl

import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

from rainbowio import colorwheel
import framebufferio

# DisplayIO para trabalhar com fontes bitmap
from displayio import Bitmap
from adafruit_display_text.bitmap_label import Label
from adafruit_bitmap_font import bitmap_font
import terminalio

pixel_pin = board.A0
pixel_width = 16
pixel_height = 16
num_tiles = 1

joystick_x = AnalogIn(board.A1)
joystick_y = AnalogIn(board.A2)

trigger = DigitalInOut(board.D6)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

buzzer = board.D7

pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height * num_tiles,
    brightness=0.1,
    auto_write=False,
)

screen = PixelFramebuffer(
    pixels,
    pixel_width * num_tiles,
    pixel_height,
    orientation=VERTICAL,
    rotation=0
)

font = bitmap_font.load_font("/fonts/tom-thumb.pcf", Bitmap)
msg_game = Label(text="GAME", font=font)
msg_over = Label(text="OVER", font=font)
msg_level = Label(text="LVL", font=font)
    
game_bitmap = msg_game.bitmap
over_bitmap = msg_over.bitmap
level_bitmap = msg_level.bitmap


# Creating colors
COLORS = [
    0x000000,  # Black
    0xFF0000,  # Red
    0xFF7F00,  # Orange
    0xFFFF00,  # Yellow
    0x00FF00,  # Green
    0x0000FF,  # Blue
    0x4B0082,  # Indigo
    0x8B00FF,   # Violet
    0xFFFFFF   # White
]

def get_joystick():
    x_coord = int(map_range(joystick_x.value, 200, 65535, 2, -2))
    y_coord = int(map_range(joystick_y.value, 200, 65535, -2, 2))
    return x_coord, y_coord

# Sounds
def shoot_sound():
    adafruit_rtttl.play(buzzer, "shoot:d=4,o=5,b=880:8c6")

def explosion_sound():
    adafruit_rtttl.play(buzzer, "Explosion:d=4,o=3,b=100:32c2,32c1")

def level_up_sound():
    adafruit_rtttl.play(buzzer, "LevelUp:d=4,o=5,b=200:16e5,16g5")

def game_over_sound():
    adafruit_rtttl.play(buzzer, "GameOver:d=4,o=3,b=80:32c3,32c2,32c1,32c2,32c3")

def xevious_sound():
    adafruit_rtttl.play(buzzer, "Xevious:d=4,o=5,b=160:16c,16c6,16b,16c6,16e6,16c6,16b,16c6,16c,16c6,16a#,16c6,16e6,16c6,16a#,16c6,16c,16c6,16a,16c6,16e6,16c6,16a,16c6,16c,16c6,16g#,16c6,16e6,16c6,16g#,16c6")

def galaga_sound():
    adafruit_rtttl.play(buzzer, "Galaga:d=4,o=5,b=125:8g4,32c,32p,8d,32f,32p,8e,32c,32p,8d,32a,32p,8g,32c,32p,8d,32f,32p,8e,32c,32p,8g,32b,32p,8c6,32a#,32p,8g#,32g,32p,8f,32d#,32p,8d,32a#4,32p,8a#,32c6,32p,8a#,32g,32p,16a,16f,16d,16g,16e,16d")

# Função para desenhar texto usando a fonte bitmap
def draw_bitmap_text(bitmap, x, y, color):
    for dy in range(bitmap.height):
        for dx in range(bitmap.width):
            if bitmap[dx, dy]:
                screen.pixel(x + dx, y + dy, color)

def show_game_over():
    screen.fill(0)
    draw_bitmap_text(game_bitmap, (screen.width - game_bitmap.width) // 2, 2, COLORS[1])
    draw_bitmap_text(over_bitmap, (screen.width - over_bitmap.width) // 2, 8, COLORS[1])
    screen.display()

def show_level(level_num):
    screen.fill(0)
    draw_bitmap_text(level_bitmap, (screen.width - level_bitmap.width) // 2, 1, COLORS[5])
    level_num_text = Label(text=str(level_num), font=font)
    num_bitmap = level_num_text.bitmap
    draw_bitmap_text(num_bitmap, (screen.width - num_bitmap.width) // 2, 7, COLORS[5])
    screen.display()
    level_up_sound()
    time.sleep(1.5)

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
        # Verificar limites horizontais
        if self.x < 0 or self.x >= screen.width - 1:
            self.x = -1
        # Verificar limites verticais (modo reverso)
        if reverse and self.y < 0:
            self.y = 0  # Impede que suba além do topo
        # Verificar limites verticais (modo normal)
        if not reverse and self.y >= screen.height - 1:
            self.y = screen.height - 2  # Impede que desça além da base

    def shoot(self):
        return Projectile(self.x + 1, self.y + 2, COLORS[1])

class PlayerShip:
    def __init__(self):
        self.x = (screen.width - 3) // 2
        self.y = screen.height - 2
        self.lives = 3
        self.exploding = False
        self.explode_timer = 0
        self.explode_duration = 0.5

    def draw(self):
        current_time = time.monotonic()
        if self.exploding and current_time - self.explode_timer < self.explode_duration:
            self.draw_explosion()
        else:
            self.exploding = False
            screen.pixel(self.x, self.y, COLORS[5])
            screen.pixel(self.x + 1, self.y, COLORS[5])
            screen.pixel(self.x + 1, self.y - 1, COLORS[5])
            screen.pixel(self.x + 2, self.y, COLORS[5])

    def draw_explosion(self):
        screen.pixel(self.x, self.y, COLORS[1])
        screen.pixel(self.x + 1, self.y, COLORS[1])
        screen.pixel(self.x + 1, self.y - 1, COLORS[1])
        screen.pixel(self.x + 2, self.y, COLORS[1])

    def draw_lives(self):
        total_width = self.lives * 1 + (self.lives - 1) * 1
        start_x = (screen.width - total_width) // 2
        for i in range(self.lives):
            x_offset = start_x + i * 2
            screen.pixel(x_offset, screen.height - 1, COLORS[8])

    def move(self, dx):
        self.x += dx
        if self.x < 0:
            self.x = 0
        if self.x >= screen.width - 3:
            self.x = screen.width - 4

    def explode(self):
        self.exploding = True
        self.explode_timer = time.monotonic()
        explosion_sound()  # Som de explosão

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
invader_descent_amount = 0
last_update_time = time.monotonic()
last_shot_time = 0
reverse = False

def resetinvaders():
    global invaders
    invaders = []
    # Posiciona 3 linhas de invasores
    for i in range(4):  # 4 colunas
        for j in range(2):  # 2 linhas
            start_x = (screen.width - (4 * 3)) // 2
            invaders.append(Invader(start_x + i * 3, j * 3))

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
        
    screen.display()

def update_game(dt):
    global invaders, projectiles, enemy_projectiles, score, game_over, invader_move_direction, invader_descent_amount
    global last_shot_time, level, reverse
    
    gc.collect()
    dx, dy = get_joystick()
    player_ship.move(dx)
    
    # Disparar com botão
    current_time = time.monotonic()
    if not trigger.value and current_time - last_shot_time > 0.2:
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
                print('Score: {0:04}'.format(score))
                if score % 100 == 0:
                    player_ship.lives += 1
                break

    # Move enemy projectiles
    for projectile in enemy_projectiles[:]:
        projectile.move(1)
        if projectile.y == -1:
            enemy_projectiles.remove(projectile)

        # Check for collision with player ship
        if player_ship.x <= projectile.x < player_ship.x + 3 and player_ship.y <= projectile.y < player_ship.y + 2:
            player_ship.lives -= 1
            player_ship.explode()
            enemy_projectiles.remove(projectile)
            if player_ship.lives <= 0:
                game_over = True
                game_over_sound()
            # Log para debug
            print(f"Player hit by enemy projectile! Lives remaining: {player_ship.lives}")

    # Variável para controlar se houve colisão com invasor
    player_hit_by_invader = False
    
    # Move invaders and check collision with player ship
    for invader in invaders[:]:
        invader.move(invader_move_direction, 0)

        # Check collision between invaders and player ship
        if (invader.x <= player_ship.x < invader.x + invader.width and 
            invader.y <= player_ship.y < invader.y + invader.height):
            player_hit_by_invader = True
            invaders.remove(invader)
            # Não processar game over aqui ainda

    # Processar colisão com invasor APÓS remover todos os invasores colididos
    if player_hit_by_invader:
        player_ship.lives -= 1
        player_ship.explode()
        reverse = True
        if player_ship.lives <= 0:
            game_over = True
            game_over_sound()
        # Log para debug
        print(f"Player collided with invader! Lives remaining: {player_ship.lives}")

    # Check for invader edge collision (horizontal)
    if any(invader.x >= screen.width - 2 or invader.x <= 0 for invader in invaders):
        invader_move_direction *= -1
        
        # Adicionar descento para todos os inimigos
        for invader in invaders:
            if not reverse:
                invader.move(0, 1)  # Mover para baixo
            else:
                invader.move(0, -1)  # Mover para cima
    
    # Nova verificação: colisão com o topo no modo reverso
    if reverse and any(invader.y <= 0 for invader in invaders):
        # Inverte a direção vertical quando atinge o topo
        for invader in invaders:
            invader.move(0, 1)  # Começa a descer
        reverse = False  # Desativa o modo reverso

    # Enemy shooting
    if len(invaders) > 0 and len(invaders) <= 3 and random.random() < 0.03:
        shooter = random.choice(invaders)
        enemy_projectiles.append(shooter.shoot())

    # VERIFICAÇÃO DE LEVEL UP DEVE VIR POR ÚLTIMO
    if not invaders and not game_over:  # Só avança de nível se o jogo não acabou
        # Level up!
        level += 1
        show_level(level)
        screen.fill(0)
        screen.display()
        projectiles[:] = []
        enemy_projectiles[:] = []
        resetinvaders()
        xevious_sound()

def reset_game():
    global invaders, player_ship, projectiles, enemy_projectiles
    global score, level, invader_move_direction, game_over, invader_descent_amount, reverse
    
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
    invader_descent_amount = 0
    reverse = False
    
    resetinvaders()
    draw_game()
    galaga_sound()

# Inicializar o jogo
reset_game()
last_button_press = time.monotonic()

# Loop principal do jogo
while True:
    current_time = time.monotonic()
    
    # Verifica se o botão foi pressionado para resetar o jogo
    if not trigger.value and current_time - last_button_press > 0.5:
        if game_over:
            reset_game()
        last_button_press = current_time
    
    if not game_over:
        dt = current_time - last_update_time
        last_update_time = current_time
        update_game(dt)
        draw_game()
        time.sleep(0.02)
    else:
        # Mostra tela de Game Over
        show_game_over()
        time.sleep(0.1)
