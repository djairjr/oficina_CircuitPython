import board
import time
import random
import gc
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer

# Configurações do display NeoPixel
pixel_pin = board.A0
pixel_width = 16
pixel_height = 16

# Inicialização dos pixels NeoPixel
pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height, 
    brightness=0.1,
    auto_write=False,
)

# Inicialização do framebuffer para a tela
screen = PixelFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    rotation=0,
)

screen.fill(0)

# Configurações do joystick
joystick_x = AnalogIn(board.A1)
joystick_y = AnalogIn(board.A2)

# Configuração do botão
trigger = DigitalInOut(board.D6)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

# Cores do jogo
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

# Constantes do jogo
FIELD_HEIGHT = pixel_height
FIELD_WIDTH = pixel_width
SCORE_PER_ELIMINATED_LINES = (0, 40, 80, 120, 600)
SCORE_PER_FIXED_PIECE = 5

# Formatos dos tetrominos, que são as peças do jogo.
# O jogo se chama TETRIS, porque as peças são formadas
# por quatro quadrados dispostos de forma diferente
TETROMINOS = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],  # O Square
    [(0, 0), (0, 1), (1, 1), (2, 1)],  # L
    [(0, 1), (1, 1), (2, 1), (2, 0)],  # J ou L espelhado
    [(0, 1), (1, 0), (1, 1), (2, 0)],  # Z
    [(0, 1), (1, 0), (1, 1), (2, 1)],  # T
    [(0, 0), (1, 0), (1, 1), (2, 1)],  # S
    [(0, 1), (1, 1), (2, 1), (3, 1)],  # I
]

# Variáveis globais do jogo
field = [] # Campo do jogo
score = 0
last_printed_score = -1  # Inicializa com valor diferente do score inicial
level = 0
total_lines_eliminated = 0
game_over = False
tetromino = []
tetromino_color = 0
tetromino_offset = [0, 0]

def get_joystick():
    # Retorna -1, 0 ou 1 dependendo da posição do joystick
    x_coord = int(map_range(joystick_x.value, 200, 65535, -2, 2))
    y_coord = int(map_range(joystick_y.value, 200, 65535, -2, 2))
    return x_coord, y_coord

def reset_tetromino():
    global tetromino, tetromino_color, tetromino_offset, game_over
    
    # Escolhe aleatoriamente um tetromino da lista
    tetromino = random.choice(TETROMINOS)[:]
    # Atribui uma cor aleatória a ele
    tetromino_color = random.randint(1, len(COLORS) - 1)
    # Posiciona ele fora da tela, na metade da largura
    tetromino_offset = [-2, FIELD_WIDTH // 2]
    
    # Verifica se o jogo acabou - Quando não houver nenhuma célula vazia
    # nas coordenadas do tetromino
    game_over = any(not is_cell_free(r, c) for (r, c) in get_tetromino_coords())

def get_tetromino_coords():
    return [(r + tetromino_offset[0], c + tetromino_offset[1]) for (r, c) in tetromino]

def is_cell_free(r, c):
    return r < FIELD_HEIGHT and 0 <= c < FIELD_WIDTH and (r < 0 or field[r][c] == 0)

def apply_tetromino():
    global field, score, level, total_lines_eliminated
    
    # Fixa o tetromino no campo
    for (r, c) in get_tetromino_coords():
        field[r][c] = tetromino_color

    # Remove linhas completas
    new_field = [row for row in field if any(tile == 0 for tile in row)]
    lines_eliminated = len(field) - len(new_field)
    total_lines_eliminated += lines_eliminated
    
    # Atualiza pontuação
    score += SCORE_PER_ELIMINATED_LINES[lines_eliminated] * (level + 1)
    score += SCORE_PER_FIXED_PIECE  # Adiciona 5 pontos quando uma peça é fixada
    
    # Atualiza nível
    level = total_lines_eliminated // 10
    
    # Atualiza campo
    field = [[0] * FIELD_WIDTH for _ in range(lines_eliminated)] + new_field
    
    # Reseta o tetromino
    reset_tetromino()

def move_tetromino(dr, dc):
    global tetromino_offset, game_over
    
    if game_over:
        return
    
    # Verifica se a célula está livre
    if all(is_cell_free(r + dr, c + dc) for (r, c) in get_tetromino_coords()):
        tetromino_offset = [tetromino_offset[0] + dr, tetromino_offset[1] + dc]
    elif dr == 1 and dc == 0:
        game_over = any(r < 0 for (r, c) in get_tetromino_coords())
        if not game_over:
            apply_tetromino()

def rotate_tetromino(): #90 Graus - Troca linha por coluna e coluna por linha
    global tetromino, tetromino_offset, game_over
    
    if game_over:
        init_game()
        return

    ys = [r for (r, c) in tetromino]
    xs = [c for (r, c) in tetromino]
    size = max(max(ys) - min(ys), max(xs) - min(xs))
    rotated_tetromino = [(c, size - r) for (r, c) in tetromino]
    wallkick_offset = tetromino_offset[:]
    
    tetromino_coord = [(r + wallkick_offset[0], c + wallkick_offset[1]) for (r, c) in rotated_tetromino]
    min_x = min(c for r, c in tetromino_coord)
    max_x = max(c for r, c in tetromino_coord)
    max_y = max(r for r, c in tetromino_coord)
    
    wallkick_offset[1] -= min(0, min_x)
    wallkick_offset[1] += min(0, FIELD_WIDTH - (1 + max_x))
    wallkick_offset[0] += min(0, FIELD_HEIGHT - (1 + max_y))

    tetromino_coord = [(r + wallkick_offset[0], c + wallkick_offset[1]) for (r, c) in rotated_tetromino]
    if all(is_cell_free(r, c) for (r, c) in tetromino_coord):
        tetromino, tetromino_offset = rotated_tetromino, wallkick_offset

def get_color(r, c):
    # Retorna a cor do tetromino se estiver na coordenada, caso contrário retorna a cor do campo
    return tetromino_color if (r, c) in get_tetromino_coords() else field[r][c]

def print_score_if_changed():
    global last_printed_score
    
    # Imprime o score apenas se ele mudou desde a última impressão
    if score != last_printed_score:
        print(f"Score: {score}")
        last_printed_score = score

def draw_screen():
    gc.collect()  # Coleta de lixo para evitar problemas de memória
    screen.fill(0)
    
    # Imprime o score apenas se mudou
    print_score_if_changed()
    
    # Desenha o campo na tela
    for r in range(FIELD_HEIGHT):
        for c in range(FIELD_WIDTH):
            color_num = get_color(r, c)
            if color_num != 0:
                screen.pixel(c, r, COLORS[color_num])
    
    screen.display()

def init_game():
    global field, score, level, total_lines_eliminated, game_over, last_printed_score
    
    screen.fill(0)
    field = [[0 for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]
    score = 0
    last_printed_score = -1  # Reseta para forçar a primeira impressão
    level = 0
    total_lines_eliminated = 0
    game_over = False
    reset_tetromino()
    
    # Imprime o score inicial
    print_score_if_changed()

# Inicializa o jogo
init_game()
last_move_time = time.monotonic()

# Loop principal do jogo
while True:
    current_time = time.monotonic()
    
    # Move o tetromino para baixo automaticamente
    if current_time - last_move_time > 1.0 - (level * 0.1):
        move_tetromino(1, 0)
        last_move_time = current_time
    
    # Obtem o movimento do joystick
    dx, dy = get_joystick()

    # Movimento horizontal
    if dy == -1:
        move_tetromino(0, 1)
    elif dy == 1:
        move_tetromino(0, -1)
    
    # Rotação
    if dx == -1:
        rotate_tetromino()
    
    # Movimento rápido para baixo
    if dx == 1:
        move_tetromino(3, 0)
    
    # Rotação com botão
    if not trigger.value:
        rotate_tetromino()

    # Desenha a tela
    draw_screen()
    
    time.sleep(0.02)
