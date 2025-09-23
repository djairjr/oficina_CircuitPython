# Revisão Final do Curso e Comentário sobre o Space Invaders
Bem, chegamos a nossa última aula do curso. Achei por bem fazer uma revisão do conteúdo,  ao mesmo tempo em que comento passo a passo o código do jogo Space Invaders.
Como bônus, vou deixar também meu código para o jogo Maze, que gera o labirinto de cada fase de forma procedural, quer dizer, o labirinto é gerado aleatóriamente por algoritmo ao invés de ser carregado via arquivo externo.

## Entradas e Saídas Digitais
Em primeiro lugar, precisamos importar o módulo **board**, que vai fazer a interface com os nomes dos pinos da plaquinha.
Lembre-se que esse módulo apenas faz a tradução dos nomes dos pinos do microcontrolador para o nome dos pinos de acordo com o fabricante da placa.
Por isso, em todo código que usamos no curso, sempre fizemos o **import board** no inicio do código.

Nosso Joystick analógico é um arranjo mecânico de dois potenciômetros (entradas analógicas) e um botão (entrada digital). Nós precisamos usar os módulos específicos para lidar com cada um desses tipos de entrada.

Nem sempre nós precisamos importar todas as funcionalidades de um módulo, ou porque temos limitações de memória ou porque gostaríamos de acessar essas funcionalidades de maneira mais direta.
Nesses casos, podemos usar o comando **from módulo import funcionalidade1, funcionalidade2 as f1, f2**, por exemplo.
O que isso faz? Ele vai pegar apenas as funcionalidades 1 e 2 do módulo e nós podemos chamar essas funcionalidades no código usando **f1 e f2**.

Por isso, quando usamos os módulos **analogio e digitalio** fazemos o seguinte:
```
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull 
```

São essas as funcionalidades que precisamos de cada um deles.
Para **analogio**, só usaremos a **AnalogIn**, que processa as **entradas analógicas**.
Já para **digitalio**, importamos **DigitalInOut**, que lida com as **entradas e saídas digitais**, **Direction** que lida com as definições de **Entrada e Saída** e finalmente **Pull** que estabelece qual vai ser o nível da **Entrada Digital** quando não tiver nenhuma conexão feita.
Como as entradas digitais possuem níveis bastante restritos(**LOW ou HIGH**), temos que garantir que quando a entrada estiver inativa, ela esteja num nível específico que nós podemos determinar por código ou por hardware.

## Mapeando Valores, ou Regra de Três
As nossas **entradas analógicas** registram variações numa faixa de valores bem grande, que vai de 0 a 65535.
Mas nós estamos usando essas entradas para realizar movimentos numa tela bastante restrita (16x16). Por isso, precisamos mapear os valores dessa faixa tão grande, para valores que nos sejam úteis.
Então nós usamos uma regra de três para fazer essa conversão de valores. Como esse tipo de aplicação é bastante comum, a Adafruit criou uma biblioteca com várias ferramentas úteis, chamada **Adafruit_SimpleIO**.
Nos nossos jogos, só vamos usar a função **map_range (valor a calcular, valor minimo principal, valor maximo principal, novo minimo, novo maximo)**. 
Então fazemos o seguinte:

```
from simpleio import map_range
# e até poderíamos fazer algo assim:
# from simpleio import map_range as regra_de_tres
```

No nosso código, faremos com que a função map_range receba os valores dos pinos analógicos **Board.A1 e Board.A2** na faixa de 200 a 65535 e converta para valores de -2 pixels a +2 pixels, que são as direções de movimento.
Isso é feito nas funções **get_joystick** ou **get_direction**.

## Fazendo uma tela simples usando fitas de Led Neopixel
Usar as fitas de led como tela nos permite ter consciência total de como as imagens são geradas. As telas de altíssima resolução nos impedem de perceber a técnica com que as imagens são geradas.
Circuitpython nos permite acessar telas de todo o tipo, e gerar imagens, formas geométricas, escrever texto com fontes diversas, etc... Mas usando as telas dessa maneira, não teríamos a experiência de entender como é que as imagens são feitas.
Por isso fizemos a opção no curso de usar as rudimentares fitas de led (usadas para decoração natalina) como uma tela com baixíssima resolução.

Numa fita Led, cada um dos leds pode ser acessado individualmente e ter sua cor definida de maneira independente dos demais. O endereçamento é puramente linear, com valores que vão variar de 0 ao último Led da fita, menos um.

Para transformar uma fita de Led em tela, nós precisamos cortá-la em pedaços iguais e montar o arranjo de várias linhas. Felizmente já existem no mercado as matrizes de Led, que nada mais são do que arranjos de fitas Led formando um quadriculado.

Ainda assim, não conseguimos acessar os pontos dessa matriz usando um sistema de coordenadas do tipo linha, coluna. Precisamos criar isso através de software, usando bibliotecas específicas que fazem toda a matemática necessária.

As fitas leds são interfaceadas pela biblioteca **Adafruit_Neopixel**, que assim como a SimpleIO não vem instalada por padrão. Nós precisamos adicioná-la usando o comando **circup install adafruit_neopixel**, no prompt de comando do nosso sistema operacional.
(Se você não entendeu nada do que eu falei, dê uma revisada nas duas primeiras aulas).
```
import neopixel
pixel_pin = board.A0 # Pino em que a Matriz está ligada
pixel_width = 16 # Largura da Matriz
pixel_height = 16 # Altura da Matriz
num_tiles = 1 # Quantas matrizes
pixels = neopixel.NeoPixel(
    pixel_pin, # Pino onde esta ligada a fita Led
    pixel_width * pixel_height * num_tiles, # Isso vai dar o número total de Leds no arranjo
    brightness=0.1, # Brilho bem baixo, pra usar direto na USB. O máximo é 1.
    auto_write=False, # Não escreve automaticamente o valor da cor no pixel. Vai precisar usar pixel.show() para atualizar.
)
pixels = (0,0,0) # Apaga a fita de led - cor preta (0,0,0) - as cores  são dadas por uma tupla (Red, Green, Blue) com os valores Red, Green, Blue variando entre 0 e 255.
pixels.show() # mostra a alteração
# Para acender um pixel específico:
pixels[0] = (255,0,0)
pixels[1] = (0,255,0)
pixels[2] = (0,0,255)
pixels.show()
```

## Usando algumas ferramentas para NeoPixel
A Adafruit criou algumas bibliotecas para incrementar as funcionalidades das fitas led. Animações com cores e mesmo o uso das Neopixel como tela são possíveis.
Para isso, nós usamos duas bibliotecas, **rainbowio** e **adafruit_pixelbuf**. Ainda que nós não estejamos utilizando telas padrão, nós podemos usar algumas facilidades da biblioteca de interfaceamento para display, a **displayio** como a capacidade de transformar fontes em imagens.
Ou ainda, de carregar um Bitmap salvo e exibir na tela.

```
import neopixel
from adafruit_pixel_framebuf import PixelFramebuf, VERTICAL

from rainbowio import colorwheel

pixel_pin = board.A0 # Pino em que a Matriz está ligada
pixel_width = 16 # Largura da Matriz
pixel_height = 16 # Altura da Matriz
num_tiles = 1 # Quantas matrizes

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

screen.pixel (0,0, (255,0,0)) # acende o pixel na coordenada 0,0 na cor vermelha
screen.display() # mostra a alteração

```
## Usando o Buzzer para o som do jogo.
Se você adicionar hardware específico, pode fazer com que a sua plaquinha RP2040 toque inclusive arquivos do tipo WAV, MP3 e OGG.
Mas de maneira direta, nós conseguimos gerar audio através de tons PWM, simplesmente adicionando um buzzer piezoelétrico.
Nós falamos pouquíssimo sobre som no nosso curso, mas você pode fazer alguns experimentos simples, usando a biblioteca pwmio.

```
import time, board, simpleio # mas uma função do SimpleIO
while True:
    for f in (262, 294, 330, 349, 392, 440, 494, 523): # frequencias das notas em Hz
        simpleio.tone(board.D7, f, 0.25) # Toque a nota f, com duração 0.25s no pino board.D7
    time.sleep(1)
```

De forma simples, também é possível tocar arquivos WAV (que não são comprimidos).
```
import time, board
import audiocore, audiopwmio #audiocore lida com tudo o que é arquivo de audio. audiopwmio transforma saída pwm em saída de audio.
audio = audiopwmio.PWMAudioOut(board.D7)
wave = audiocore.WaveFile("laser2.wav") # toca o arquivo laser2.wav que deve estar na pasta principal
audio.play(wave)
while True:
  pass 
```

Mas na abordagem atual, eu estou usando a biblioteca Adafruit_RTTTL, que toca audio no formato Ring Tone.

```
import board
import time
import adafruit_rtttl
fileHandle = open('rtttlsongs.txt') # Esse arquivo tem uma música por linha no formato RTTTL

songs = []
for line in fileHandle: # Lê cada linha do arquivo
    songs.append(line) # Adiciona cada linha como um elemento da lista songs

fileHandle.close()

for song in songs: # Para cada elemento da lista song
    adafruit_rtttl.play(board.D7, song) # toque o elemento
    time.sleep(1) # aguarde 1s antes de tocar o próximo
```

## Inicializando todo o Hardware do nosso Console
A sequência de inicialização de todo o hardware do nosso console é dada pelo código abaixo.

```
import board # Interface com os pinos 
import time # Atrasos, medidas de intervalos
import random # Eventos aleatórios
import gc # Garbage Colector,  limpa a RAM

from analogio import AnalogIn # Entradas analógicas
from digitalio import DigitalInOut, Direction, Pull # Entradas e saídas digitais
from simpleio import map_range # Regra de Três

import adafruit_rtttl # Sons, no formato RTTTL

import neopixel # Fita de LED
from adafruit_pixel_framebuf import PixelFramebuf, VERTICAL # Usar fita led como Tela

from rainbowio import colorwheel # Cores e animações por cor
import framebufferio # Framebuffer

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

# As cores podem ser passadas em Hexadecimal. 0xRRGGBB 
COLORS = [
    0x000000,  # Black (0,0,0)
    0xFF0000,  # Red (255,0,0)
    0xFF7F00,  # Orange (255,127,0)
    0xFFFF00,  # Yellow (255,255,0)
    0x00FF00,  # Green (0,255,0)
    0x0000FF,  # Blue (0,0,255)
    0x4B0082,  # Indigo
    0x8B00FF   # Violet
]

# Pega o valor das entradas analógicas e converte em direções
def get_joystick():
    x_coord = int(map_range(joystick_x.value, 200, 65535, -2, 2))
    y_coord = int(map_range(joystick_y.value, 200, 65535, -2, 2))
    return x_coord, y_coord


# Uma coleção de sons no formato RTTTL
def shoot_sound():
    adafruit_rtttl.play(buzzer, "shoot:d=4,o=5,b=880:8c6")
    
def xevious_sound():
    adafruit_rtttl.play(buzzer, "Xevious:d=4,o=5,b=160:16c,16c6,16b,16c6,16e6,16c6,16b,16c6,16c,16c6,16a#,16c6,16e6,16c6,16a#,16c6,16c,16c6,16a,16c6,16e6,16c6,16a,16c6,16c,16c6,16g#,16c6,16e6,16c6,16g#,16c6")

def galaga_sound():
    adafruit_rtttl.play(buzzer, "Galaga:d=4,o=5,b=125:8g4,32c,32p,8d,32f,32p,8e,32c,32p,8d,32a,32p,8g,32c,32p,8d,32f,32p,8e,32c,32p,8g,32b,32p,8c6,32a#,32p,8g#,32g,32p,8f,32d#,32p,8d,32a#4,32p,8a#,32c6,32p,8a#,32g,32p,16a,16f,16d,16g,16e,16d")

```
# **🎮 SPACE INVADERS - EXPLICAÇÃO COMPLETA DE POO**

## **🤔 O QUE É PROGRAMAÇÃO ORIENTADA A OBJETOS?**

**POO é como criar "mini-mundos" no código** onde cada coisa é um objeto que sabe:
- **O que é** (seus dados/atributos)
- **O que faz** (seus comportamentos/métodos)

**Analogia:** Pense em uma fábrica de carros:
- **Classe** = Projeto/Planta do carro 📋
- **Objeto** = Carro real que você dirige 🚗  
- **Atributos** = Cor, modelo, velocidade 🎨
- **Métodos** = Acelerar, frear, buzinar ⚡

## **🏗️ COMO AS BIBLIOTECAS USAM POO**

### **Biblioteca NeoPixel (Controle de LEDs)**
```python
# A biblioteca cria uma CLASSE NeoPixel que encapsula a complexidade
pixels = neopixel.NeoPixel(  # Criando OBJETO da CLASSE NeoPixel
    pixel_pin,               # Atributo: pino de conexão
    pixel_width * pixel_height,  # Atributo: quantidade de LEDs
    brightness=0.1,          # Atributo: brilho
    auto_write=False         # Atributo: atualização automática
)

# Métodos simples para usar:
pixels[0] = (255, 0, 0)  # Muda cor do LED 0 para vermelho
pixels.show()            # Atualiza todos LEDs de uma vez
```

**Por que usam POO aqui:**
- **Escondem complexidade**: Você não precisa saber como os LEDs funcionam internamente
- **Interface intuitiva**: `pixels[0] = cor` funciona como uma lista normal
- **Reutilização**: Posso criar várias matrizes de LEDs com a mesma classe

### **Biblioteca PixelFramebuf (Tela virtual)**
```python
screen = PixelFramebuf(  # OBJETO que representa uma tela
    pixels,              # Atributo: LEDs físicos
    pixel_width,         # Atributo: largura
    pixel_height,        # Atributo: altura
    orientation=VERTICAL # Atributo: orientação
)

# Métodos para desenhar:
screen.fill(0)           # Limpa tela (preto)
screen.pixel(5, 5, 0xFF0000)  # Desenha pixel vermelho na posição (5,5)
```

**Vantagem do POO:** A tela virtual abstrai a complexidade de mapear coordenadas para LEDs físicos

## **🎯 NOSSO JOGO USANDO POO**

### **Classe Invader - Cada inimigo é um objeto inteligente**
```python
class Invader:
    def __init__(self, x, y):
        self.x = x          # Atributo: posição X
        self.y = y          # Atributo: posição Y
        self.width = 2      # Atributo: largura
        self.color = random.choice(COLORS[1:])  # Atributo: cor aleatória

    def draw(self):         # Método: sabe se desenhar
        for i in range(self.width):
            screen.pixel(self.x + i, self.y, self.color)

    def move(self, dx):     # Método: sabe se mover
        self.x += dx
        if self.x < 0: 
            self.x = 0

# Criando vários inimigos facilmente:
inimigo1 = Invader(5, 2)    # Objeto 1
inimigo2 = Invader(10, 2)   # Objeto 2 - mesmo molde, objeto diferente
```

### **Classe PlayerShip - A nave do jogador**
```python
class PlayerShip:
    def __init__(self):
        self.x = (screen.width - 3) // 2  # Centralizado
        self.y = screen.height - 2        # Base da tela
        self.lives = 3                    # Vidas
        self.exploding = False            # Estado

    def move(self, dx):     # Método: movimento horizontal
        self.x += dx
        # Ele mesmo cuida dos limites:
        if self.x < 0: 
            self.x = 0
        if self.x > screen.width - 3: 
            self.x = screen.width - 3

    def draw(self):         # Método: auto-desenho
        screen.pixel(self.x, self.y, COLORS[5])
        screen.pixel(self.x + 1, self.y, COLORS[5])
        # ... etc
```

### **Classe Projectile - Tiros do jogo**
```python
class Projectile:
    def __init__(self, x, y, color):
        self.x = x      # Posição atual
        self.y = y      # Posição atual
        self.color = color

    def move(self, dy): # Sabe se mover
        self.y += dy
        # Sabe quando deve ser removido:
        if self.y < 0 or self.y >= screen.height:
            self.y = -1  # Marca para remoção
```

## **⚡ VANTAGENS NO NOSSO JOGO**

### **1. ORGANIZAÇÃO NATURAL**
```python
# SEM POO: Tudo misturado
player_x = 10
player_y = 14
player_lives = 3

def move_player(dx):
    global player_x
    player_x += dx

# COM POO: Tudo junto e organizado
class PlayerShip:
    def __init__(self):
        self.x = 10
        self.y = 14
        self.lives = 3
        
    def move(self, dx):
        self.x += dx
```

### **2. FÁCIL EXPANSÃO**
```python
# Adicionar novo tipo de inimigo é fácil:
class InimigoRapido(Invader):  # Herda tudo do Invader normal
    def __init__(self, x, y):
        super().__init__(x, y)
        self.velocidade = 2    # Mais rápido
        self.pontos = 20       # Vale mais pontos
```

### **3. CÓDIGO AUTO-EXPLICATIVO**
```python
# Em vez de funções genéricas:
mover_objeto(inimigo1, 1, 0)
desenhar_objeto(inimigo1)

# Temos métodos específicos:
inimigo1.move(1)    # "Inimigo, mova-se!"
inimigo1.draw()     # "Inimigo, desenhe-se!"
```

### **4. CONTROLE DE ESTADO**
```python
# Cada objeto gerencia seu próprio estado:
if inimigo1.x >= screen.width:  # O inimigo sabe sua posição
    inimigo1.x = 0              # E pode se ajustar
```

## **🎮 COMO TUDO SE CONECTA**

1. **Bibliotecas** usam POO para nos dar ferramentas simples (`pixels`, `screen`)
2. **Nosso jogo** usa POO para criar personagens inteligentes
3. **Cada objeto** cuida de si mesmo: sabe onde está, como se desenhar, como se mover
4. **O código principal** fica limpo: só orquestra os objetos

**Resultado:** Código organizado, fácil de entender e de modificar! 🚀

## **📊 COMPARAÇÃO FINAL**

| **Abordagem Tradicional** | **Programação Orientada a Objetos** |
|--------------------------|-----------------------------------|
| Variáveis soltas | Dados organizados em objetos |
| Funções grandes | Métodos específicos para cada objeto |
| Dificil manutenção | Fácil modificar e expandir |
| Código confuso | Código claro e intuitivo |
| Propenso a erros | Menos bugs, mais controle |

**POO transforma programação em "gerenciar uma equipe" onde cada objeto sabe exatamente seu trabalho!** 👨💼👩💼

## **🏗️ ESTRUTURA DAS CLASSES PRINCIPAIS**

### **👾 CLASSE INVADER (INIMIGO)**
```python
class Invader:
    def __init__(self, x, y):
        self.x = x          # Posição horizontal (coluna)
        self.y = y          # Posição vertical (linha)
        self.width = 2      # Largura do invasor (2 pixels)
        self.height = 2     # Altura do invasor (2 pixels)
        self.color = random.choice(COLORS[1:])  # Cor aleatória (exceto preto)
```

**Trajetória e Movimento:**
```python
def move(self, dx, dy):
    self.x += dx  # Move horizontalmente
    self.y += dy  # Move verticalmente
    # Se sair da tela horizontalmente, marca para remover
    if self.x < 0 or self.x >= screen.width - 1:
        self.x = -1
```

**Desenho do Inimigo:**
```python
def draw(self):
    for i in range(self.width):      # Percorre largura (2 pixels)
        for j in range(self.height): # Percorre altura (2 pixels)
            # Desenha cada pixel do invasor
            screen.pixel(self.x + i, self.y + j, self.color)
```

**Tiro do Inimigo:**
```python
def shoot(self):
    # Cria projétil no centro do invasor (x + 1) e abaixo dele (y + 2)
    return Projectile(self.x + 1, self.y + 2, COLORS[1])  # Vermelho
```

### **🚀 CLASSE PLAYERSHIP (NAVE DO JOGADOR)**
```python
class PlayerShip:
    def __init__(self):
        self.x = (screen.width - 3) // 2  # Centralizado horizontalmente
        self.y = screen.height - 2        # Base da tela
        self.lives = 3                    # Vidas iniciais
        self.exploding = False            # Estado de explosão
        self.explode_timer = 0            # Tempo de explosão
```

**Desenho da Nave (Formato de Triângulo):**
```python
def draw(self):
    if self.exploding:
        self.draw_explosion()  # Desenha explosão
    else:
        # Desenha nave em forma de triângulo - veja outro método...:
        screen.pixel(self.x, self.y, COLORS[5])        # ⬅️ Esquerda inferior
        screen.pixel(self.x + 1, self.y, COLORS[5])    # ⬇️ Centro inferior  
        screen.pixel(self.x + 1, self.y - 1, COLORS[5]) # ⬆️ Centro superior
        screen.pixel(self.x + 2, self.y, COLORS[5])    # ➡️ Direita inferior
```

**Movimento da Nave:**
```python
def move(self, dx):
    self.x += dx  # Move horizontalmente conforme joystick
    # Limites da tela:
    if self.x < 0: self.x = 0  # Não passa da borda esquerda
    if self.x >= screen.width - 3:  # Não passa da borda direita
        self.x = screen.width - 4
```

**Vidas na Interface:**
```python
def draw_lives(self):
    for i in range(self.lives):  # Para cada vida restante
        x_offset = start_x + i * 3  # Espaça as vidas
        for dx in range(2):      # Desenha mininave 2x2 pixels
            for dy in range(2):
                screen.pixel(x_offset + dx, screen.height - 2 + dy, COLORS[5])
```

### **💥 CLASSE PROJECTILE (TIRO)**
```python
class Projectile:
    def __init__(self, x, y, color):
        self.x = x      # Posição horizontal
        self.y = y      # Posição vertical  
        self.color = color  # Cor do projétil
```

**Movimento do Tiro:**
```python
def move(self, dy):
    self.y += dy  # Move verticalmente (+1 para baixo, -1 para cima)
    if self.y < 0 or self.y >= screen.height:  # Se sair da tela
        self.y = -1  # Marca para remover
```

## **🎮 FUNÇÕES PRINCIPAIS DO JOGO**

### **🎯 DETECÇÃO DE COLIÇÕES**

**Colisão Tiro-Jogador vs Inimigo:**
```python
for invader in invaders[:]:  # Percorre todos os invasores
    # Verifica se o tiro está dentro da área do invasor
    if (invader.x <= projectile.x < invader.x + 2 and 
        invader.y <= projectile.y < invader.y + 2):
        invaders.remove(invader)    # Remove invasor
        projectiles.remove(projectile)  # Remove tiro
        score += 10  # Adiciona 10 pontos
        print('{0:04}'.format(score))  # Mostra pontuação formatada
```

**Colisão Tiro-Inimigo vs Jogador:**
```python
if (player_ship.x <= projectile.x < player_ship.x + 3 and 
    player_ship.y <= projectile.y < player_ship.y + 3):
    player_ship.lives -= 1      # Perde uma vida
    player_ship.explode()       # Ativa animação de explosão
    enemy_projectiles.remove(projectile)  # Remove tiro inimigo
    if player_ship.lives <= 0:  # Se acabaram as vidas
        game_over = True        # Fim de jogo
```

### **🔄 MOVIMENTAÇÃO DOS INIMIGOS**

**Mudança de Direção:**
```python
# Se algum invasor chegar nas bordas laterais
if any(invader.x >= screen.width - 2 or invader.x <= 0 for invader in invaders):
    invader_move_direction *= -1  # Inverte direção horizontal
    for invader in invaders:
        if not reverse:
            invader.move(0, 1)   # Move para baixo
        else:
            invader.move(0, -1)  # Move para cima (modo reverso)
```

**Sistema de Invasão Reversa:**
```python
# Se invasores chegarem perto do jogador
if any(invader.y >= player_ship.y - 1 for invader in invaders):
    reverse = True  # Ativa modo reverso (sobem)
# Se invasores voltarem muito para cima  
if any(invader.y <= 0 for invader in invaders):
    reverse = False  # Desativa modo reverso (descem)
```

### **🎯 SISTEMA DE PONTUAÇÃO E FASE**

**Bônus de Vida:**
```python
if score % 1000 == 0:    # A cada 1000 pontos
    player_ship.lives += 1  # Ganha uma vida extra
```

**Próxima Fase:**
```python
if not invaders:  # Se não há mais invasores
    screen.fill(0)  # Limpa tela
    resetinvaders()  # Reseta inimigos
    xevious_sound()  # Toca som de vitória
    # Os inimigos voltam mais rápidos na próxima fase
```

### **🎮 LOOP PRINCIPAL DO JOGO**

```python
while True:
    if not game_over:
        current_time = time.monotonic()
        dt = current_time - last_update_time  # Calcula tempo decorrido
        last_update_time = current_time
        
        update_game(dt)   # Atualiza lógica do jogo
        draw_game()       # Desenha tudo na tela
        time.sleep(0.02)  # Pequena pausa (50 FPS)
    else:
        time.sleep(1)     # Espera antes de reiniciar
        # reset_game()    # Descomente para reinício automático
```

## **📊 FLUXO DO JOGO:**
1. **Inicialização** → Cria jogador, inimigos, zera pontuação
2. **Loop Principal** → Atualiza → Desenha → Repete
3. **Colisões** → Verifica tiros, movimentos, limites
4. **Pontuação** → Aumenta pontos, verifica bônus
5. **Fase Completa** → Reseta inimigos, toca som
6. **Game Over** → Para o jogo, aguarda reinício
