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

# Cores
BLACK = 0x000000
WHITE = 0xFFFFFF
RED = 0xFF0000
GREEN = 0x00FF00
CYAN = 0x00FFFF
YELLOW = 0xFFFF00

# Configuração escalável baseada no CELL_SIZE
CELL_SIZE = 1  # Tamanho de cada célula em pixels (1 para 16x16)
MAZE_CELLS = 16 // CELL_SIZE  # Número de células que cabem na tela

# Função para ler o joystick
def get_joystick():
    # Retorna -1, 0 ou 1 dependendo da posição do joystick
    x_coord = int(map_range(joystick_x.value, 200, 65535, -2, 2))
    y_coord = int(map_range(joystick_y.value, 200, 65535, -2, 2))
    return x_coord, y_coord

# Função alternativa para embaralhar lista
def shuffle_list(lst):
    """Embaralha uma lista usando algoritmo Fisher-Yates"""
    for i in range(len(lst)-1, 0, -1):
        j = random.randint(0, i)
        lst[i], lst[j] = lst[j], lst[i]
    return lst

class Maze:
    def __init__(self):
        self.cell_width = MAZE_CELLS
        self.cell_height = MAZE_CELLS
        self.maze = []
        # Entrada no canto superior esquerdo
        self.entry_pos = (1, 1)
        # Saída no canto inferior direito (no limite do caminho)
        self.exit_pos = (MAZE_CELLS - 2, MAZE_CELLS - 2)
        self.generate()
        
    def get_entry(self):
        return self.entry_pos
    
    def get_exit(self):
        return self.exit_pos

    def generate(self):
        # Inicializa o labirinto com paredes (1 = parede, 0 = caminho, 2 = saída)
        self.maze = [[1 for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        
        # Cria bordas sólidas (1 célula de espessura)
        for i in range(self.cell_width):
            self.maze[0][i] = 1  # Borda superior
            self.maze[self.cell_height-1][i] = 1  # Borda inferior
        
        for i in range(self.cell_height):
            self.maze[i][0] = 1  # Borda esquerda
            self.maze[i][self.cell_width-1] = 1  # Borda direita
        
        # Cria entrada
        entry_x, entry_y = self.entry_pos
        self.maze[entry_y][entry_x] = 0
        
        # Cria saída no canto inferior direito (ainda não conectada)
        exit_x, exit_y = self.exit_pos
        self.maze[exit_y][exit_x] = 2
        
        # Algoritmo de labirinto (recursive backtracking)
        stack = [(entry_x, entry_y)]
        self.maze[entry_y][entry_x] = 0
        
        # Direções possíveis (em células)
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        
        while stack:
            current_x, current_y = stack[-1]
            # Usa nossa função alternativa para embaralhar
            shuffled_directions = shuffle_list(directions.copy())
            found = False
            
            for dx, dy in shuffled_directions:
                nx, ny = current_x + dx, current_y + dy
                if (1 <= nx < self.cell_width-1 and 1 <= ny < self.cell_height-1 and 
                    self.maze[ny][nx] == 1):
                    # Remove a parede entre as células
                    self.maze[current_y + dy//2][current_x + dx//2] = 0
                    self.maze[ny][nx] = 0
                    stack.append((nx, ny))
                    found = True
                    break
            
            if not found:
                stack.pop()
        
        # Garante que a saída no canto inferior direito esteja conectada
        self.connect_exit_to_maze()

    def connect_exit_to_maze(self):
        """Conecta a saída no canto inferior direito ao labirinto"""
        exit_x, exit_y = self.exit_pos
        
        # Tenta conectar a saída criando um caminho a partir das células adjacentes
        # Prioriza conectar pela esquerda ou acima da saída
        connection_points = [
            (exit_x - 1, exit_y),    # Esquerda
            (exit_x, exit_y - 1),    # Acima
            (exit_x - 1, exit_y - 1) # Diagonal (caso as outras falhem)
        ]
        
        for cx, cy in connection_points:
            if (1 <= cx < self.cell_width-1 and 1 <= cy < self.cell_height-1):
                self.maze[cy][cx] = 0  # Cria caminho
                break

    def is_wall(self, cell_x, cell_y):
        """Verifica se a célula na posição dada é uma parede"""
        if 0 <= cell_x < self.cell_width and 0 <= cell_y < self.cell_height:
            return self.maze[cell_y][cell_x] == 1
        return True  # Fora dos limites é considerado parede

class Game:
    def __init__(self):
        self.level = 1
        self.maze = Maze()
        self.player_pos = self.maze.get_entry()  # Posição em células
        self.setup_display()
        
        # Histórico para suavizar o movimento do joystick
        self.move_history = []
        self.history_size = 3
        
        # Configurações do joystick
        self.joystick_deadzone = 0.2  # Zona morta para evitar movimento acidental
        self.last_joystick_pos = (0.5, 0.5)  # Posição central normalizada
        
    def setup_display(self):
        # Limpa a tela
        screen.fill(0)
        
        # Desenha o labirinto
        for cell_y in range(self.maze.cell_height):
            for cell_x in range(self.maze.cell_width):
                cell_value = self.maze.maze[cell_y][cell_x]
                
                if cell_value == 1:  # Parede
                    color = CYAN
                elif cell_value == 2:  # Saída
                    color = GREEN
                else:  # Caminho
                    color = BLACK
                
                # Desenha a célula
                screen.pixel(cell_x, cell_y, color)
        
        # Desenha o jogador
        self.draw_player()
        
        # Atualiza a tela
        screen.display()
    
    def draw_player(self):
        """Desenha o jogador na posição atual"""
        player_x, player_y = self.player_pos
        screen.pixel(player_x, player_y, RED)
    
    def clear_player(self):
        """Limpa a posição anterior do jogador"""
        player_x, player_y = self.player_pos
        cell_value = self.maze.maze[player_y][player_x]
        
        if cell_value == 2:  # Se estava na saída
            color = GREEN
        else:  # Caminho normal
            color = BLACK
            
        screen.pixel(player_x, player_y, color)
    
    def get_joystick_direction(self):
        """Lê o joystick usando a função fornecida e retorna a direção do movimento"""
        x_coord, y_coord = get_joystick()
        
        # Converte os valores -2, -1, 0, 1, 2 para -1, 0, 1
        dx = 0
        dy = 0
        
        if x_coord < 0:
            dx = -1
        elif x_coord > 0:
            dx = 1
            
        if y_coord < 0:
            dy = -1
        elif y_coord > 0:
            dy = 1
        
        return dx, dy
    
    def move_player(self):
        dx, dy = self.get_joystick_direction()
        
        if dx != 0 or dy != 0:
            new_cell_x = self.player_pos[0] + dx
            new_cell_y = self.player_pos[1] + dy
            
            # Verifica se o movimento é válido (não é parede)
            if not self.maze.is_wall(new_cell_x, new_cell_y):
                # Limpa a posição anterior do jogador
                self.clear_player()
                
                # Atualiza a posição do jogador
                self.player_pos = (new_cell_x, new_cell_y)
                
                # Desenha o jogador na nova posição
                self.draw_player()
                
                # Atualiza a tela
                screen.display()
                
                # Verifica se chegou na saída
                if self.player_pos == self.maze.get_exit():
                    self.next_level()
    
    def next_level(self):
        # Incrementa nível e gera novo labirinto
        self.level += 1
        self.maze = Maze()
        self.player_pos = self.maze.get_entry()
        self.setup_display()
        
        time.sleep(0.5)
    
    def run(self):
        last_update = time.monotonic()
        update_interval = 0.2  # Atualiza a cada 200ms
        
        while True:
            current_time = time.monotonic()
            
            if current_time - last_update >= update_interval:
                self.move_player()
                last_update = current_time
            
            time.sleep(0.05)

# Inicia o jogo
game = Game()
game.run()