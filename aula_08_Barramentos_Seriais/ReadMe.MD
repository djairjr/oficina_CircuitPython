## Apêndice - Barramentos Seriais: UART, I2C, SPI

### Introdução aos Barramentos Seriais

Nosso console Neopixel funcionou bastante bem, dadas as suas limitações. Conseguimos realizar o controle de movimento usando entradas analógicas, disparar eventos usando uma entrada digital, emulamos uma tela simples usando uma fita de LED **Neopixel**, escrevemos texto na tela, exibimos bitmaps e construímos uma série de jogos diferentes.

Mas e se precisássemos utilizar dispositivos com maior complexidade? Telas de maior resolução, com comunicação ultra rápida, ou mesmo sensores digitais, com diversas informações sendo comunicadas ao mesmo tempo?

É aqui que os **barramentos seriais** se tornam essenciais. No nosso jogo de Batalha Naval, utilizamos o **I2C** para comunicação entre as duas placas RP2040, mas existem outras opções igualmente importantes.

### 1. UART (Universal Asynchronous Receiver/Transmitter)

#### Conceito Básico
O UART é um protocolo **assíncrono** ponto-a-ponto, meaning que não há clock compartilhado entre os dispositivos.

```python
# Exemplo de UART no CircuitPython
import busio
uart = busio.UART(board.TX, board.RX, baudrate=9600)

# Enviando dados
uart.write(b"Hello World!\n")

# Recebendo dados
data = uart.read(32)  # Lê até 32 bytes
```

#### Características Principais:
- **Conexão**: TX (Transmissor) → RX (Receptor) e vice-versa
- **Velocidade**: Baud rate configurável (9600, 115200, etc.)
- **Sincronização**: Cada byte tem bits de start e stop
- **Vantagens**: Simples, robusto, amplamente suportado
- **Desvantagens**: Apenas ponto-a-ponto, velocidade moderada

#### Aplicações Típicas:
- Comunicação com módulos GPS
- Interfaces com computadores (USB-Serial)
- Módulos Bluetooth e WiFi
- Debugging e logging

### 2. I2C (Inter-Integrated Circuit)

#### Conceito Básico
O I2C é um protocolo **síncrono** multi-dispositivo que usa apenas dois fios.

```python
# Exemplo I2C do nosso jogo
import busio
i2c = busio.I2C(board.SCL, board.SDA)

# Escaneando dispositivos na rede
i2c.try_lock()
devices = i2c.scan()
i2c.unlock()

# Enviando dados para um dispositivo específico
i2c.writeto(0x40, b"\x01\x02\x03")
```

#### Características Principais:
- **Conexão**: SCL (Clock) + SDA (Dados) + GND
- **Endereçamento**: Cada dispositivo tem um endereço único (7 ou 10 bits)
- **Velocidade**: Standard (100kHz), Fast (400kHz), High-Speed (3.4MHz)
- **Topologia**: Barramento multi-mestre, multi-escravo

#### Vantagens:
- **Economia de pinos**: Apenas 2 fios para múltiplos dispositivos
- **Endereçamento**: Até 128 dispositivos no mesmo barramento
- **Padronização**: Protocolo bem definido

#### Desvantagens:
- **Velocidade moderada**: Comparado ao SPI
- **Overhead**: Bits de acknowledge/start/stop
- **Distância limitada**: Para comunicação local

### 3. SPI (Serial Peripheral Interface)

#### Conceito Básico
O SPI é um protocolo **síncrono** full-duplex de alta velocidade.

```python
# Exemplo SPI no CircuitPython
import busio
import digitalio

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.D10)
cs.direction = digitalio.Direction.OUTPUT

# Comunicação SPI
cs.value = False  # Seleciona dispositivo
spi.write(b"\x01\x02\x03")
cs.value = True   # Desseleciona
```

#### Características Principais:
- **Conexão**: SCK (Clock), MOSI (Master Out Slave In), MISO (Master In Slave Out), CS (Chip Select)
- **Velocidade**: Muito alta (até 10MHz+ em microcontroladores)
- **Modos**: 4 modos de clock (polaridade e fase)
- **Topologia**: Ponto-a-ponto com seleção individual

#### Vantagens:
- **Alta velocidade**: Full-duplex simultâneo
- **Flexibilidade**: Tamanho de palavra variável
- **Simplicidade**: Hardware mais simples que UART

#### Desvantagens:
- **Mais pinos**: 3-4 fios por dispositivo
- **Sem acknowledgment**: Sem confirmação nativa
- **Sem endereçamento**: Requer pinos CS individuais

### Comparação Prática

| Característica | UART | I2C | SPI |
|----------------|------|-----|-----|
| **Velocidade** | Baixa-Média | Média | Alta |
| **Pinos** | 2 | 2 | 3-4+ |
| **Dispositivos** | 2 | Múltiplos | Múltiplos |
| **Complexidade** | Baixa | Média | Média |
| **Custo** | Baixo | Baixo | Moderado |

### Aplicações no Contexto de Jogos

#### UART para Debugging
```python
# Durante desenvolvimento do jogo
def debug_game_state(game):
    uart.write(f"Player: {game.player_id}, State: {game.state}\n".encode())
    uart.write(f"Ships remaining: {game.my_ships_remaining}\n".encode())
```

#### I2C para Sensores Adicionais
```python
# Adding Accelerometer support
import adafruit_lis3dh

# Acelerometer config
i2c = board.I2C()
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)
lis3dh.range = adafruit_lis3dh.RANGE_2_G

def get_joystick(): # Using Accelerometer
    # Reads accelerometer values ​​and converts them to G
    x, y, z = (value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration)
    
    # Calculates the magnitude of the tilt on each axis
    x_mag = abs(x)
    y_mag = abs(y)
    
    # Determine which axis has the greatest inclination
    if x_mag > y_mag:
        # X Axis (Left/Right)
        if x > 0.1:
            dx = 2  # Right
        elif x < -0.01:
            dx = -2  # Left
        else:
            dx = 0
        dy = 0  # Block Y
    else:
        # Y Axis (UP/Down)
        if y > 0.2:
            dy = 2  # Down
        elif y < -0.2:
            dy = -2  # UP
        else:
            dy = 0
        dx = 0  # Block X
    
    return dx, dy
```

#### SPI para Tela de Alta Resolução
```python
# Conectando display TFT via SPI
import adafruit_ili9341
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
display = adafruit_ili9341.ILI9341(spi, cs=board.D9, dc=board.D10)

# Desenhando gráficos complexos
display.fill(0x0000FF)  # Fundo azul
```

### Por que Escolhemos I2C para o Batalha Naval?

No nosso jogo, o I2C foi a escolha ideal porque:

1. **Economia de Pinos**: Apenas 2 fios conectam as duas placas
2. **Comunicação Bidirecional**: Ambas as placas podem enviar e receber
3. **Endereçamento Simples**: Cada placa tem um endereço único
4. **Adequado à Aplicação**: Velocidade suficiente para turnos de jogo


### Conclusão

Cada barramento serial tem seu propósito ideal. O entendimento dessas tecnologias permite escolher a melhor ferramenta para cada projeto, equilibrando velocidade, complexidade e requisitos de hardware.

No desenvolvimento de sistemas embarcados modernos, o domínio desses protocolos é tão fundamental quanto o conhecimento da linguagem de programação em si. São as "artérias" que permitem que diferentes componentes do sistema se comuniquem eficientemente.

Este conhecimento não apenas melhora nossos projetos atuais, mas abre portas para sistemas muito mais complexos e interessantes no futuro!




