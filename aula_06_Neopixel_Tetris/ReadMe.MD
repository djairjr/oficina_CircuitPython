# Jogo Tetris em CircuitPython
Eu estou compartilhando o código completo do jogo, mas achei útil explicar cada uma das funções e também como as peças ("tetrônimos") são desenhadas.

## 📐 Sistema de Desenho dos Tetrônimos

Os tetrônimos são representados como listas de tuplas, onde cada tupla `(linha, coluna)` indica a posição de um bloco dentro de uma grade 4x4. 
O sistema usa coordenadas relativas onde (0,0) é o canto superior esquerdo da peça. 
Por exemplo:

- **Peça O (quadrado)**: `[(0,0), (0,1), (1,0), (1,1)]` - forma um bloco 2x2
- **Peça I (bastão)**: `[(0,1), (1,1), (2,1), (3,1)]` - forma uma linha vertical de 4 blocos
- **Peça L**: `[(0,0), (0,1), (1,1), (2,1)]` - forma um L
- **Peça J**: `[(0,1), (1,1), (2,1), (2,0)]` - forma um J espelhado
- **Peça Z**: `[(0,1), (1,0), (1,1), (2,0)]` - forma um Z
- **Peça T**: `[(0,1), (1,0), (1,1), (2,1)]` - forma um T
- **Peça S**: `[(0,0), (1,0), (1,1), (2,1)]` - forma um S

Cada número nas tuplas representa uma coordenada relativa à posição inicial da peça. O sistema transforma essas coordenadas relativas em posições absolutas na tela usando o offset da peça.

# Explicação do Sistema de Coordenadas dos Tetrônimos

## 📊 Estrutura da Grade 4x4

Cada tetrônimo é definido dentro de uma **grade virtual 4x4**, onde:

- **Primeiro elemento da tupla (r)**: Número da **linha** (0 a 3)
- **Segundo elemento da tupla (c)**: Número da **coluna** (0 a 3)

## 🧩 Como Funciona na Prática

Cada tupla `(r, c)` representa a posição de **um bloco individual** dentro da peça. A lista completa de tuplas define todos os blocos que formam a peça.

### Exemplo: Peça T - `[(0,1), (1,0), (1,1), (2,1)]`

**Visualização da grade 4x4:**
```
Coluna: 0   1   2   3
Linha 0: □   ■   □   □
Linha 1: ■   ■   □   □  
Linha 2: □   ■   □   □
Linha 3: □   □   □   □
```

**Quebra da peça T:**
- `(0,1)` → Linha 0, Coluna 1 → ■
- `(1,0)` → Linha 1, Coluna 0 → ■
- `(1,1)` → Linha 1, Coluna 1 → ■
- `(2,1)` → Linha 2, Coluna 1 → ■

### Exemplo: Peça I - `[(0,1), (1,1), (2,1), (3,1)]`

**Visualização:**
```
Coluna: 0   1   2   3
Linha 0: □   ■   □   □
Linha 1: □   ■   □   □
Linha 2: □   ■   □   □  
Linha 3: □   ■   □   □
```

## 🔄 Transformação para Coordenadas da Tela

A função `get_tetromino_coords()` converte as coordenadas relativas (da grade 4x4) para coordenadas absolutas na tela:

```python
def get_tetromino_coords():
    return [(r + tetromino_offset[0], c + tetromino_offset[1]) 
            for (r, c) in tetromino]
```

**Exemplo:** Se `tetromino_offset = [5, 8]` e temos o bloco `(1, 2)`:
- Coordenada final: `(5 + 1, 8 + 2) = (6, 10)`

A grade 4x4 é apenas um sistema de coordenadas **relativo** para definir o formato de cada peça, que depois é posicionado na tela real através do offset.

## 🔧 Funções do Jogo

### `get_joystick()`
**O que faz:** Lê e interpreta a posição do joystick, convertendo valores analógicos em direções digitais (-1, 0, 1).
```
def get_joystick():
    x_coord = int(map_range(joystick_x.value, 200, 65535, -2, 2))
    y_coord = int(map_range(joystick_y.value, 200, 65535, -2, 2))
    return x_coord, y_coord
```


### `reset_tetromino()`
**O que faz:** Seleciona aleatoriamente uma nova peça, define sua cor e posição inicial no topo da tela.
```
def reset_tetromino():
    global tetromino, tetromino_color, tetromino_offset, game_over
    
    tetromino = random.choice(TETROMINOS)[:]
    tetromino_color = random.randint(1, len(COLORS) - 1)
    tetromino_offset = [-2, FIELD_WIDTH // 2]
    
    game_over = any(not is_cell_free(r, c) for (r, c) in get_tetromino_coords())
```


### `get_tetromino_coords()`
**O que faz:** Calcula as coordenadas reais na tela para cada bloco da peça atual, somando o offset de posição.
```
def get_tetromino_coords():
    return [(r + tetromino_offset[0], c + tetromino_offset[1]) for (r, c) in tetromino]
```


### `is_cell_free(r, c)`
**O que faz:** Verifica se uma posição específica na grade do jogo está disponível para movimento.

```
def is_cell_free(r, c):
    return r < FIELD_HEIGHT and 0 <= c < FIELD_WIDTH and (r < 0 or field[r][c] == 0)
```

### `apply_tetromino()`
**O que faz:** Fixa a peça atual no campo, verifica e remove linhas completas, calcula a pontuação e atualiza o nível.

```
def apply_tetromino():
    global field, score, level, total_lines_eliminated
    
    for (r, c) in get_tetromino_coords():
        field[r][c] = tetromino_color

    new_field = [row for row in field if any(tile == 0 for tile in row)]
    lines_eliminated = len(field) - len(new_field)
    total_lines_eliminated += lines_eliminated
    
    score += SCORE_PER_ELIMINATED_LINES[lines_eliminated] * (level + 1)
    score += SCORE_PER_FIXED_PIECE
    
    level = total_lines_eliminated // 10
    
    field = [[0] * FIELD_WIDTH for _ in range(lines_eliminated)] + new_field
    
    reset_tetromino()
```

### `move_tetromino(dr, dc)`
**O que faz:** Move a peça na direção especificada (vertical/horizontal) se o movimento for possível.

```
def move_tetromino(dr, dc):
    global tetromino_offset, game_over
    
    if game_over:
        return
    
    if all(is_cell_free(r + dr, c + dc) for (r, c) in get_tetromino_coords()):
        tetromino_offset = [tetromino_offset[0] + dr, tetromino_offset[1] + dc]
    elif dr == 1 and dc == 0:
        game_over = any(r < 0 for (r, c) in get_tetromino_coords())
        if not game_over:
            apply_tetromino()
```

### `rotate_tetromino()`
**O que faz:** Gira a peça 90 graus no sentido horário, ajustando sua posição para não sair dos limites da tela.

```
def rotate_tetromino():
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
```

### `get_color(r, c)`
**O que faz:** Determina a cor a ser exibida em cada posição da tela, priorizando a peça em movimento.

```
def get_color(r, c):
    return tetromino_color if (r, c) in get_tetromino_coords() else field[r][c]
```

### `print_score_if_changed()`
**O que faz:** Exibe a pontuação no console apenas quando ela é alterada.

```
def print_score_if_changed():
    global last_printed_score
    
    if score != last_printed_score:
        print(f"Score: {score}")
        last_printed_score = score
```

### `draw_screen()`
**O que faz:** Renderiza todo o conteúdo gráfico do jogo na tela NeoPixel.

```
def draw_screen():
    gc.collect()
    screen.fill(0)
    
    print_score_if_changed()
    
    for r in range(FIELD_HEIGHT):
        for c in range(FIELD_WIDTH):
            color_num = get_color(r, c)
            if color_num != 0:
                screen.pixel(c, r, COLORS[color_num])
    
    screen.display()
```

### `init_game()`
**O que faz:** Inicializa ou reinicia o jogo, configurando todas as variáveis para seus valores iniciais.
```
def init_game():
    global field, score, level, total_lines_eliminated, game_over, last_printed_score
    
    screen.fill(0)
    field = [[0 for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]
    score = 0
    last_printed_score = -1
    level = 0
    total_lines_eliminated = 0
    game_over = False
    reset_tetromino()
    
    print_score_if_changed()
```
