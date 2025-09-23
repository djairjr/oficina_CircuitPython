'''
O código abaixo foi gerado com ajuda de IA e deve ainda ser testado e validado.
Ele implementa o jogo Batalha Naval em duas placas LED DRIVER BOARD para XIAO,
que se comunicam via I2C. O código é o mesmo para as duas placas, que devem estar
conectadas ao joystick e buzzer. A tela é de 32x16 (duas matrizes 16x16).
'''
import board
import time
import random
import gc
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer
import busio

# Configurações do I2C para comunicação entre as placas
i2c = busio.I2C(board.SCL, board.SDA)

# Configurações do display NeoPixel
pixel_pin = board.A0
pixel_width = 16
pixel_height = 16
num_tiles = 2  # Dois painéis 16x16 lado a lado

# Inicialização dos pixels NeoPixel
pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height * num_tiles, 
    brightness=0.1,
    auto_write=False,
)

# Inicialização do framebuffer para a tela
screen = PixelFramebuffer(
    pixels,
    pixel_width * num_tiles,  # 32 pixels de largura
    pixel_height,             # 16 pixels de altura
    rotation=0,
)

screen.fill(0)
screen.display()

# Configurações do joystick
joystick_x = AnalogIn(board.A1)
joystick_y = AnalogIn(board.A2)

# Configuração do botão
trigger = DigitalInOut(board.D6)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

# Configuração do buzzer checa se há um buzzer conectado
try:
    import pwmio
    buzzer = pwmio.PWMOut(board.D5, frequency=440, duty_cycle=0)
except:
    buzzer = None

# Cores do jogo
COLOR_BLACK = 0x000000
COLOR_RED = 0xFF0000
COLOR_GREEN = 0x00FF00
COLOR_BLUE = 0x0000FF
COLOR_YELLOW = 0xFFFF00
COLOR_WHITE = 0xFFFFFF
COLOR_GRAY = 0x808080
COLOR_CYAN = 0x00FFFF
COLOR_ORANGE = 0xFFA500
COLOR_PURPLE = 0x800080

# Estados do jogo
STATE_SETUP = 0
STATE_WAITING = 1
STATE_ATTACK = 2
STATE_DEFEND = 3
STATE_GAME_OVER = 4

# Definição das embarcações (nome, tamanho, cor)
SHIPS = [
    {"name": "Fragata", "size": 2, "color": COLOR_CYAN, "count": 1},
    {"name": "Destroyer", "size": 3, "color": COLOR_ORANGE, "count": 1},
    {"name": "Submarino", "size": 3, "color": COLOR_GREEN, "count": 1},
    {"name": "Cruzador", "size": 4, "color": COLOR_PURPLE, "count": 1},
    {"name": "Porta-Aviões", "size": 5, "color": COLOR_YELLOW, "count": 1}
]

class BattleshipGame:
    def __init__(self):
        self.state = STATE_SETUP
        self.player_id = None
        self.opponent_id = None
        self.current_ship_type = 0
        self.ship_orientation = 0  # 0: horizontal, 1: vertical
        self.cursor_x = 0
        self.cursor_y = 0
        self.board_size = 16
        self.my_board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.opponent_board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.my_ships = []
        self.ships_placed = {i: 0 for i in range(len(SHIPS))}  # Controle de quantas de cada tipo foram colocadas
        self.opponent_ships_remaining = sum(ship["size"] * ship["count"] for ship in SHIPS)
        self.my_ships_remaining = sum(ship["size"] * ship["count"] for ship in SHIPS)
        self.last_communication = time.monotonic()
        self.setup_complete = False
        self.opponent_setup_complete = False
        self.selected_ship_index = 0  # Índice do tipo de navio selecionado
        
        # Determinar ID do jogador via I2C
        self.determine_player_id()
    
    def determine_player_id(self):
        """Determina qual placa é jogador 1 e qual é jogador 2 via I2C"""
        time.sleep(1)  # Espera para estabilização
        
        # Tenta se tornar líder do I2C
        try:
            i2c.try_lock()
            i2c.unlock()
            self.player_id = 1
            print("Sou o jogador 1")
        except:
            self.player_id = 2
            print("Sou o jogador 2")
        
        self.opponent_id = 1 if self.player_id == 2 else 2
    
    def beep(self, frequency=440, duration=0.1):
        """Faz um som no buzzer"""
        if buzzer:
            try:
                buzzer.frequency = frequency
                buzzer.duty_cycle = 32768
                time.sleep(duration)
                buzzer.duty_cycle = 0
            except:
                pass
    
    def get_direction(self):
        x = int(map_range(joystick_x.value, 0, 65535, 1.5, -1.5))
        y = int(map_range(joystick_y.value, 0, 65535,  -1.5, 1.5))
        if abs(x) > abs(y):
            return (0, x)  # Horizontal Move
        else:
            return (y, 0)  # Vertical Move

    # A função get_joystick foi mantida apenas para comparação das diferenças
    def get_joystick(self):
        # Returns -1 0 or 1 depending on joystick position
        x_coord = int (map_range (joystick_x.value, 200, 65535, - 2 , 2))
        y_coord = int (map_range (joystick_y.value, 200, 65535, - 2 , 2))
        return x_coord, y_coord
    
    def send_message(self, message_type, data=0):
        """Envia mensagem via I2C"""
        try:
            i2c.try_lock()
            address = 0x40 + self.opponent_id
            message = bytes([self.player_id, message_type, data & 0xFF, (data >> 8) & 0xFF])
            i2c.writeto(address, message)
            i2c.unlock()
            return True
        except:
            i2c.unlock()
            return False
    
    def receive_message(self):
        """Recebe mensagem via I2C"""
        try:
            i2c.try_lock()
            address = 0x40 + self.player_id
            result = bytearray(4)
            i2c.readfrom_into(address, result)
            i2c.unlock()
            return result
        except:
            i2c.unlock()
            return None
    
    def check_collision(self, x, y, size, orientation):
        """Verifica se há colisão com navios existentes"""
        if orientation == 0:  # Horizontal
            if x + size > self.board_size:
                return True
            for i in range(size):
                if self.my_board[y][x + i] != 0:
                    return True
        else:  # Vertical
            if y + size > self.board_size:
                return True
            for i in range(size):
                if self.my_board[y + i][x] != 0:
                    return True
        return False
    
    def place_ship(self, x, y, ship_index, orientation):
        """Coloca um navio no tabuleiro"""
        ship = SHIPS[ship_index]
        size = ship["size"]
        ship_cells = []
        
        if orientation == 0:  # Horizontal
            for i in range(size):
                self.my_board[y][x + i] = ship_index + 1  # +1 para diferenciar tipos
                ship_cells.append((x + i, y))
        else:  # Vertical
            for i in range(size):
                self.my_board[y + i][x] = ship_index + 1
                ship_cells.append((x, y + i))
        
        self.ships_placed[ship_index] += 1
        return ship_cells
    
    def draw_board(self):
        """Desenha o tabuleiro na tela (32x16)"""
        screen.fill(0)
        
        # Desenha tabuleiro do jogador (lado esquerdo: 0-15)
        for y in range(self.board_size):
            for x in range(self.board_size):
                color = COLOR_BLUE
                cell_value = self.my_board[y][x]
                
                if cell_value > 0:  # Navio
                    ship_index = cell_value - 1
                    color = SHIPS[ship_index]["color"]
                elif cell_value == -1:  # Tiro certeiro
                    color = COLOR_RED
                elif cell_value == -2:  # Tiro na água
                    color = COLOR_WHITE
                
                screen.pixel(x, y, color)
        
        # Desenha tabuleiro do oponente (lado direito: 16-31)
        for y in range(self.board_size):
            for x in range(self.board_size):
                color = COLOR_BLUE
                cell_value = self.opponent_board[y][x]
                
                if cell_value == -1:  # Tiro certeiro
                    color = COLOR_RED
                elif cell_value == -2:  # Tiro na água
                    color = COLOR_WHITE
                # Não mostra navios do oponente
                
                screen.pixel(x + 16, y, color)
        
        # Desenha cursor e informações
        if self.state == STATE_SETUP:
            # Cursor para posicionamento
            ship = SHIPS[self.selected_ship_index]
            size = ship["size"]
            cursor_color = ship["color"]
            
            if self.ship_orientation == 0:  # Horizontal
                for i in range(size):
                    if self.cursor_x + i < self.board_size:
                        screen.pixel(self.cursor_x + i, self.cursor_y, cursor_color)
            else:  # Vertical
                for i in range(size):
                    if self.cursor_y + i < self.board_size:
                        screen.pixel(self.cursor_x, self.cursor_y + i, cursor_color)
            
            # Mostra quantos navios de cada tipo faltam
            for i, ship in enumerate(SHIPS):
                remaining = ship["count"] - self.ships_placed[i]
                if remaining > 0:
                    color = ship["color"]
                    # Indicador simples na borda
                    screen.pixel(31, i, color)
                    
        elif self.state == STATE_ATTACK:
            # Cursor para ataque (no tabuleiro do oponente)
            screen.pixel(self.cursor_x + 16, self.cursor_y, COLOR_YELLOW)
        
        # Linha divisória entre os tabuleiros
        for y in range(16):
            screen.pixel(15, y, COLOR_WHITE)
        
        screen.display()
    
    def all_ships_placed(self):
        """Verifica se todos os navios foram posicionados"""
        for i, ship in enumerate(SHIPS):
            if self.ships_placed[i] < ship["count"]:
                return False
        return True
    
    def process_setup(self):
        """Processa a fase de posicionamento dos navios"""
        x_dir, y_dir = self.get_joystick()
        
        # Move cursor
        if abs(x_dir) > 0.5:
            self.cursor_x = max(0, min(self.board_size - 1, self.cursor_x + int(x_dir)))
            time.sleep(0.15)
        if abs(y_dir) > 0.5:
            self.cursor_y = max(0, min(self.board_size - 1, self.cursor_y + int(y_dir)))
            time.sleep(0.15)
        
        # Botão para rotacionar navio
        if not trigger.value and time.monotonic() - self.last_communication > 0.3:
            self.ship_orientation = 1 - self.ship_orientation
            self.beep(300, 0.1)
            time.sleep(0.2)
        
        # Seleção de tipo de navio (usando movimento vertical rápido)
        if abs(y_dir) > 1.5 and time.monotonic() - self.last_communication > 0.5:
            self.selected_ship_index = (self.selected_ship_index + int(y_dir)) % len(SHIPS)
            # Pula para próximo tipo de navio que ainda não foi totalmente colocado
            for _ in range(len(SHIPS)):
                ship = SHIPS[self.selected_ship_index]
                if self.ships_placed[self.selected_ship_index] < ship["count"]:
                    break
                self.selected_ship_index = (self.selected_ship_index + 1) % len(SHIPS)
            self.beep(400, 0.1)
            self.last_communication = time.monotonic()
        
        # Botão para colocar navio
        if not trigger.value and time.monotonic() - self.last_communication > 0.5:
            ship = SHIPS[self.selected_ship_index]
            if self.ships_placed[self.selected_ship_index] < ship["count"]:
                size = ship["size"]
                if not self.check_collision(self.cursor_x, self.cursor_y, size, self.ship_orientation):
                    ship_cells = self.place_ship(self.cursor_x, self.cursor_y, self.selected_ship_index, self.ship_orientation)
                    self.my_ships.append(ship_cells)
                    self.beep(600, 0.1)
                    
                    if self.all_ships_placed():
                        self.setup_complete = True
                        self.send_message(1)  # Mensagem de setup completo
                        self.state = STATE_WAITING
                        self.beep(800, 0.2)
                        self.beep(1000, 0.2)
                    
                    self.last_communication = time.monotonic()
    
    def process_attack(self):
        """Processa a fase de ataque"""
        x_dir, y_dir = self.get_joystick()
        
        # Move cursor no tabuleiro do oponente
        if abs(x_dir) > 0.5:
            self.cursor_x = max(0, min(self.board_size - 1, self.cursor_x + int(x_dir)))
            time.sleep(0.15)
        if abs(y_dir) > 0.5:
            self.cursor_y = max(0, min(self.board_size - 1, self.cursor_y + int(y_dir)))
            time.sleep(0.15)
        
        # Botão para atacar
        if not trigger.value and time.monotonic() - self.last_communication > 0.5:
            # Verifica se já atacou esta posição
            if self.opponent_board[self.cursor_y][self.cursor_x] == 0:
                # Envia coordenada do ataque (16 bits: YYYYXXXX)
                coord_data = (self.cursor_y << 8) | self.cursor_x
                if self.send_message(2, coord_data):
                    self.state = STATE_WAITING
                    self.last_communication = time.monotonic()
                    self.beep(800, 0.1)
    
    def process_defend(self):
        """Processa a fase de defesa (aguardando ataque do oponente)"""
        message = self.receive_message()
        if message and message[0] == self.opponent_id:
            if message[1] == 2:  # Ataque
                coord_data = (message[3] << 8) | message[2]
                attack_y = (coord_data >> 8) & 0xFF
                attack_x = coord_data & 0xFF
                
                hit = False
                ship_hit = None
                
                # Verifica se acertou algum navio
                for ship_cells in self.my_ships:
                    for cell in ship_cells:
                        if cell[0] == attack_x and cell[1] == attack_y:
                            hit = True
                            self.my_board[attack_y][attack_x] = -1  # Marcador de acerto
                            self.my_ships_remaining -= 1
                            # Remove a célula atingida
                            ship_cells.remove((attack_x, attack_y))
                            if len(ship_cells) == 0:
                                # Navio afundado!
                                self.beep(200, 0.5)  # Som longo para navio afundado
                            break
                    if hit:
                        break
                
                if not hit:
                    self.my_board[attack_y][attack_x] = -2  # Marcador de água
                    self.beep(200, 0.1)
                else:
                    self.beep(1000, 0.2)
                
                # Envia resultado do ataque
                self.send_message(3, 1 if hit else 0)
                
                if self.my_ships_remaining <= 0:
                    self.state = STATE_GAME_OVER
                    self.send_message(4)  # Mensagem de vitória do oponente
                else:
                    self.state = STATE_ATTACK if not hit else STATE_DEFEND
            
            elif message[1] == 3:  # Resultado do ataque
                hit = message[2] == 1
                if hit:
                    self.opponent_board[self.cursor_y][self.cursor_x] = -1
                    self.opponent_ships_remaining -= 1
                    if self.opponent_ships_remaining <= 0:
                        self.state = STATE_GAME_OVER
                        self.beep(1000, 1.0)  # Vitória!
                    else:
                        self.state = STATE_ATTACK
                        self.beep(800, 0.3)
                else:
                    self.opponent_board[self.cursor_y][self.cursor_x] = -2
                    self.state = STATE_DEFEND
                    self.beep(300, 0.2)
            
            elif message[1] == 4:  # Game Over
                self.state = STATE_GAME_OVER
    
    def check_communication(self):
        """Verifica mensagens de comunicação"""
        if self.state == STATE_WAITING:
            message = self.receive_message()
            if message and message[0] == self.opponent_id:
                if message[1] == 1:  # Setup completo
                    self.opponent_setup_complete = True
                    if self.setup_complete:
                        # Decide quem começa atacando (jogador 1 começa)
                        if self.player_id == 1:
                            self.state = STATE_ATTACK
                            self.beep(600, 0.2)
                            self.beep(800, 0.2)
                        else:
                            self.state = STATE_DEFEND
                            self.beep(400, 0.2)
                            self.beep(600, 0.2)
                
                elif message[1] == 2:  # Ataque recebido
                    self.state = STATE_DEFEND
    
    def show_game_over(self):
        """Mostra animação de game over"""
        # Pisca as telas com cores diferentes
        colors = [COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW]
        for _ in range(10):
            for color in colors:
                screen.fill(color)
                screen.display()
                time.sleep(0.2)
        
        # Mostra resultado final
        if self.my_ships_remaining <= 0:
            # Derrota
            for i in range(3):
                screen.fill(COLOR_RED)
                screen.display()
                time.sleep(0.5)
                screen.fill(COLOR_BLACK)
                screen.display()
                time.sleep(0.5)
        else:
            # Vitória!
            for i in range(3):
                screen.fill(COLOR_GREEN)
                screen.display()
                time.sleep(0.5)
                screen.fill(COLOR_BLACK)
                screen.display()
                time.sleep(0.5)
    
    def run(self):
        """Loop principal do jogo"""
        while True:
            self.check_communication()
            
            if self.state == STATE_SETUP:
                self.process_setup()
            elif self.state == STATE_ATTACK:
                self.process_attack()
            elif self.state == STATE_DEFEND:
                self.process_defend()
            elif self.state == STATE_GAME_OVER:
                self.show_game_over()
                break
            
            self.draw_board()
            time.sleep(0.05)

# Inicializa e executa o jogo
game = BattleshipGame()
game.run()