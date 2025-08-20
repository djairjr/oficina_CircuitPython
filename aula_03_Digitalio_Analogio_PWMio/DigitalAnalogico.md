### **Explicação Simplificada para Leigos - CircuitPython no Seeed Xiao RP2040**


#### **1. Conceitos Fundamentais**
**Sinais Digitais vs Analógicos**
- **Digital**: Valores exatos (0 ou 1) - como um interruptor de luz
- **Analógico**: Variação contínua ampla faixa de valores - como um dimmer de luz

#### **2. Componentes da Experiência**
![Pinagem do Seeed Xiao RP2040](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_03_Digitalio_Analogio_PWMio/Seeedstudio-Seeeduino-XIAO-RP2040-Microcontroller-Board-Pinout-Diagram-1-1536x1046.jpg)

![Montagem da Aula](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_03_Digitalio_Analogio_PWMio/Montagem_Aula_3.png)

**Botão (Digital)**
- Apertado = 0 / Solto = 1
- Exemplo: interruptor simples
```
import board # Módulo que faz a interface entre o Circuitpython e os nomes dos pinos na plaquinha
import digitalio # Módulo que cuida das entradas e saídas digitais
from digitalio import DigitalInOut, Direction, Pull # ou você pode importar somente aquilo que vai usar

led = DigitalInOut (board.D7) # Indica que a variável led vai representar uma entrada ou saída digital no pino D7 da placa

led.direction = Direction.OUTPUT # Determina que a variável led vai representar especificamente uma saída digital
led.value = False # Atribui o valor False (Zero) ao led, fazendo com que ele apague.

botao = DigitalInOut (board.D6) # Indica que a variavel botao vai representar uma entrada ou saída digital no pino D6 da placa
botao.direction = Direction.INPUT # Determina que a variável botão vai representar específicamente uma entrada digital
botao.pull = Pull.UP # Determina que, quando o botão não estiver sendo pressionado, o valor dele será UP (True).

print (botao.value) # deve exibir True, se o botão não estiver pressionado e False, se estiver.

while True: # crio um loop infinito
  if botao.value == False:  # Se o botão estiver pressionado
    print ('Botão Pressionado')
    led.value = True # Acende o Led
  else:
    led.value = False # Apaga o Led
```

**Potenciômetro (Analógico)**
- Gira → varia tensão (0V a 3.3V)
- Exemplo: controle de volume ou de intensidade. Controle de direção (Joystick Analógico)

```
# Lê o valor de tensão no pino analógico

import time, board
from analogio import AnalogIn

potenciometro = AnalogIn (board.A2)

# Criando uma função com def
def get_voltage (pin):
  # pin.value vai retornar um valor entre 0 e 65536. 
  # 3.3 é a tensão máxima.
  return (pin.value * 3.3) / 65536

while True:
  print (get_voltage (potenciometro)) # Usando a minha função definida
  time.sleep (0.1)
```

**LED com PWM**
- Brilho controlado por pulsos rápidos
- Exemplo: dimmer digital

```
import time, board
from digitalio import DigitalInOut, Pull, Direction

led = DigitalInOut (board.D7) # Se quiser usar os Leds da plaquinha board.LED
led.direction = Direction.OUTPUT

# Frequência é medida em Hertz. Indica a quantidade de ciclos de um evento por segundo
# Nós estamos considerando como ciclo, o tempo em que o LED acende e apaga.

frequencia = 60 # de 60 a 90hz a visão humana registra os pulsos como continuidade.
periodo_total = 1 / frequencia

# Você consegue usar o potenciômetro para variar a intensidade do LED? Como?
duty_cicle = int (input ( 'Digite a intensidade do LED em porcentagem (0 a 100%: )')) / 100
inactive_time = 1 - duty_cicle

while True:
  led.value = True
  time.sleep (duty_cicle * periodo_total) 
  led.value = False
  time.sleep (inactive_time * periodo_total)
```

#### **3. Conversores (Conceitos Importantes)**
**ADC (Conversor Analógico-Digital)**
- Transforma tensão do potenciômetro em números (0-65535)
- Como funciona:
  - 0V → 0
  - 1.65V → 32768
  - 3.3V → 65535

**DAC (Conversor Digital-Analógico) - Conceito Geral**
- Faz o inverso do ADC: transforma números em tensão analógica
- Exemplo de uso:
  - Gerar sinais de áudio
  - Controlar motores com precisão
- *Observação: Nosso Xiao RP2040 não tem DAC, mas é importante conhecer o conceito*

**PWM (Modulação por Largura de Pulso)**
- "Engana" criando efeito analógico com digital
- Controla brilho do LED variando tempo ligado/desligado

#### **4. Fluxo Completo (Nosso Projeto)**
1. Potenciômetro gera tensão analógica
2. ADC converte para número digital
3. Número é usado no PWM para controlar LED
4. LED brilha conforme posição do potenciômetro

### **Comparação Didática**
| Dispositivo | Entrada | Saída | Analogia |
|-------------|---------|-------|----------|
| ADC | Tensão (0-3.3V) | Número (0-65535) | Tradutor de voltagem para números |
| DAC* | Número | Tensão | Tradutor de números para voltagem |
| PWM | Número | Pulsos digitais | Dimmer digital |

*Conceito geral (não presente no nosso hardware)

### **Por Que Isso Importa?**
Entender esses conceitos ajuda a:
- Ler sensores analógicos (como o potenciômetro)
- Controlar dispositivos com precisão
- Compreender como dispositivos eletrônicos conversam entre si

### **Lembrete Importante**
No Seeed Xiao RP2040:
- Temos ADC para ler o potenciômetro
- Usamos PWM para controlar o LED
- **Não temos DAC** - é apenas um conceito importante para conhecer
