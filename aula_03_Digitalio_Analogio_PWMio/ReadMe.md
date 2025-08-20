### **Explicação Simplificada para Leigos - CircuitPython no Seeed Xiao RP2040**

**Link para Compra da plaquinha no AliExpress**

[Plaquinha Seeed Xiao RP2040 na loja oficial](https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html?sensecap_affiliate=TXM32IP&referring_service=link)

[Kit com três Xiao RP2040](https://www.seeedstudio.com/Seeed-Studio-XIAO-RP2040-3PCS-p-5942.html?sensecap_affiliate=TXM32IP&referring_service=link)

[Plaquinha Seeed Xiao RP2350 - equivale a Pico 2](https://www.seeedstudio.com/Seeed-XIAO-RP2350-p-5944.html?sensecap_affiliate=TXM32IP&referring_service=link)

Procurem a versão **Pre-Soldered**, porque já vem com os pinos todos soldados.
[Loja no AliExpress](https://seeedstudio.aliexpress.com/store/1103741821?spm=a2g0o.detail.0.0.3f5crJUrrJUrzd)


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
**PWM (Modulação por Largura de Pulso)**
- "Engana" criando efeito analógico com digital
- Controla brilho do LED variando tempo ligado/desligado

**LED com PWM**
- Brilho controlado por pulsos rápidos
- Exemplo: dimmer digital

```
import time, board
from digitalio import DigitalInOut, Pull, Direction
from analogio import AnalogIn # Somente para ler o potenciometro

led = DigitalInOut (board.D7) # Se quiser usar os Leds da plaquinha board.LED
led.direction = Direction.OUTPUT

potenciometro = AnalogIn (board.A2)

# Frequência é medida em Hertz. Indica a quantidade de ciclos de um evento por segundo
# Nós estamos considerando como ciclo, o tempo em que o LED acende e apaga.

frequencia = 60 
periodo_total = 1 / frequencia

# Nosso sistema vai perguntar para o usuário, qual a intensidade do Led.
# Se você optar por usar o potenciômetro, vai precisar calcular duty_cicle usando
# uma leitura analógica do potenciômetro e a função get_voltage modificada
# para encontrar uma porcentagem
duty_cicle = int (input ( 'Digite a intensidade do LED em porcentagem (0 a 100%: )')) / 100

# duty_cycle = descubra um jeito de usar o valor do potenciometro e convertê-lo em porcentagem

# Ele vai fazer um cálculo, subtraindo o tempo total do ciclo (1), do tempo em que o ciclo
# está ativo (duty_cicle) e com isso, vai encontrar o tempo em que o led fica inativo.
inactive_time = 1 - duty_cicle

# Modifique essa função para que retorne um valor em porcentagem
def get_voltage (pin):
  # pin.value vai retornar um valor entre 0 e 65536. 
  # 3.3 é a tensão máxima. E se quiséssemos o valor em porcentagem? De 0.0 a 1.0, por exemplo?
  return (pin.value * 3.3) / 65536 # Você vai precisar mudar alguma coisa nessa linha aqui...

while True: # Esse é o nosso loop principal
  led.value = True # Acende o Led
  time.sleep (duty_cicle * periodo_total) # Espera o tempo de led ativo
  led.value = False # Apaga o Led
  time.sleep (inactive_time * periodo_total) # Espera o tempo de led inativo e volta pro começo do loop

# No código acima, como você faria para usar o potenciômetro para alterar a intensidade do brilho do led?
# Dica: ao invés de perguntar para o usuário antes do loop, você pode fazer a leitura analógica
# do potenciômetro e usar matemática para definir os valores de duty_cicle e inactive_time
# Que tal usar a função get_voltage e convertê-la para usar porcentagens, ao invés de tensões?
# Qual a diferença entre colocar a leitura do potenciômetro dentro do loop principal ou fora dele?
```
#### **3. Usando saídas em PWM do RP2040**
O RP2040 possui diversas saídas PWM. Neste caso, não precisamos fazer todo o cálculo do duty_cicle.
Nós podemos usar uma biblioteca, a pwmio, para cuidar disso para nós. No exemplo abaixo, vamos descobrir
quais são os pinos do Xiao que podem ser usados como saída PWM.

```
import board
import pwmio

for pin_name in dir(board): # Quais são os pinos do RP2040 que são PWM?
    pin = getattr(board, pin_name)
    try:
        p = pwmio.PWMOut(pin)
        p.deinit()
        print("PWM on:", pin_name)  # Prints the valid, PWM-capable pins!
    except ValueError:  # This is the error returned when the pin is invalid.
        print("No PWM on:", pin_name)  # Prints the invalid pins.
    except RuntimeError:  # Timer conflict error.
        print("Timers in use:", pin_name)  # Prints the timer conflict pins.
    except TypeError:  # Error returned when checking a non-pin object in dir(board).
        pass  # Passes over non-pin objects in dir(board).
```

No exemplo abaixo, vamos fazer o led piscar, com efeito de fade...

```
import time, pwmio, board
led = pwmio.PWMOut (board.LED, frequency=5000, duty_cycle=0)
while True:
    for i in range(100):
        # PWM LED up and down
        if i < 50:
            led.duty_cycle = int(i * 2 * 65535 / 100)  # Up
        else:
            led.duty_cycle = 65535 - int((i - 50) * 2 * 65535 / 100)  # Down
        time.sleep(0.01)
```


#### **4. Conversores (Conceitos Importantes)**
**ADC (Conversor Analógico-Digital)**
- Transforma tensão do potenciômetro em números (0-65535)
- Isso é algo que já está implementado na Xiao, nos pinos A0, A1, A2, A3
- Funciona assim, o sistema lê os valores de tensão nesses pinos e os converte numa faixa de valores de 0 a 65535.
  - 0V → 0
  - 1.65V → 32768
  - 3.3V → 65535

**DAC (Conversor Digital-Analógico) - Conceito Geral**
- Faz o inverso do ADC: transforma números em tensão analógica
- Exemplo de uso:
  - Gerar sinais de áudio
  - Controlar motores com precisão
- *Observação: Nosso Xiao RP2040 não tem DAC, mas é importante conhecer o conceito*


#### **5. Fluxo Completo (Nosso Projeto)**
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
