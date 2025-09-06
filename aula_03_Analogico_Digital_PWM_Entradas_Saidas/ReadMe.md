# Digital, Analógico, PWM

**Links para Compra da Seeed Xiao RP2040 ou RP2350**

[Plaquinha Seeed Xiao RP2040 na loja oficial](https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html?sensecap_affiliate=TXM32IP&referring_service=link)

[Kit com três Xiao RP2040](https://www.seeedstudio.com/Seeed-Studio-XIAO-RP2040-3PCS-p-5942.html?sensecap_affiliate=TXM32IP&referring_service=link)

[Plaquinha Seeed Xiao RP2350 - equivale a Pico 2](https://www.seeedstudio.com/Seeed-XIAO-RP2350-p-5944.html?sensecap_affiliate=TXM32IP&referring_service=link)

Procurem a versão **Pre-Soldered**, porque já vem com os pinos todos soldados.

[Loja no AliExpress](https://seeedstudio.aliexpress.com/store/1103741821?spm=a2g0o.detail.0.0.3f5crJUrrJUrzd)

**Links para Compra da Raspberry Pi Pico RP2040 ou RP2350**

[Raspberry Pi Pico na Maker Hero](https://www.makerhero.com/produto/raspberry-pi-pico/)

[Raspberry Pi Pico 2 na Maker Hero](https://www.makerhero.com/produto/raspberry-pi-pico-2/)

[Raspberry Pi Pico W (com Wifi)](https://www.makerhero.com/produto/raspberry-pi-pico-w/)

[Raspberry Pi Pico 2W (com Wifi)](https://www.makerhero.com/produto/raspberry-pi-pico-2-w/)


**Links para Compra da Franzininho Wifi - ESP32 S2 que roda CircuitPython**

[Franzininho Wifi ESP32-S2 - Placa nacional com wifi integrado](https://www.robocore.net/wifi/franzininho-wifi)

## Pinagem da Seeed Xiao RP2040

Todo dispositivo eletrônico que você for utilizar terá um manual técnico chamado de **datasheet**.
No CircuitPython, o módulo board é uma interface que permite que você acesse os pinos da plaquinha que você está utilizando com os mesmos nomes que você lê no **datasheet** do fabricante. Isso parece óbvio, mas nem sempre isso é feito em todas as linguagens. Para acessar qualquer um dos pinos indicados no diagrama abaixo, você vai precisar importar o módulo board e em seguida, identificar o pino com o nome board.PINO

![Datasheet da Xiao RP2040](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_03_Digitalio_Analogio_PWMio/Seeedstudio-Seeeduino-XIAO-RP2040-Microcontroller-Board-Pinout-Diagram-1-1536x1046.jpg?raw=true)

Na nossa montagem de aula, vamos ligar um botão como entrada no pino D6 e um LED como saída no pino D7. Nós podemos criar duas variáveis e indicar isso, por exemplo.
```
import board
botao_pin = board.D6
led_pin = board.D7
```
![Diagrama de Montagem da Aula](https://github.com/djairjr/oficina_CircuitPython/raw/main/aula_03_Digitalio_Analogio_PWMio/Montagem_Aula_3.png)

## Módulos digitalio e analogio
O código do exemplo acima ainda não faz nada com os pinos da nossa plaquinha. Os microcontroladores possuem pinos chamados GPIO, sigla que significa Generic Pin Input Output.
Os pinos servem tanto para entrada como para saída. Nós precisamos indicar o que queremos fazer com esses pinos. No caso da Xiao, temos quatro pinos especiais, que podem ser configurados como analógicos ou digitais. São os pinos A0-A3, que também são os pinos D0-D3. No caso específico dos microcontroladores RP2040 e RP2350, nós não temos nenhuma saída do tipo analógica, apenas as entradas.
Apesar disso, o módulo que lida com as entradas analógicas é o **Analogio** e o que lida com as entradas e saídas digitais é o **Digitalio**.
No código a seguir, nós iremos importar o módulo board para endereçar os pinos da mesma maneira que lemos no diagrama do fabricante e em seguida, vamos importar os módulos digitalio e analogio para poder tratar as entradas e saídas digitais (botão e Led) e a entrada analógica (Potenciômetro).
```
import board

# Lembrando que a gente pode importar todos objetos da módulo com
# import digitalio
# ou podemos importar somente as coisas que iremos utilizar (o que economiza memória e facilita a chamada)

from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn

botao = DigitalInOut (board.D6) # com o comando >>> import digitalio, seria botao = digitalio.DigitalInOut (board.D6)
led = DigitalInOut (board.D7) # Botao e Led são objetos, do tipo DigitalInOut
pot = AnalogIn (board.A2) # Pot é um objeto do tipo AnalogIn

# Com isso, nós temos as definições de que pinos serão analógicos e digitais.
led.direction = Direction.OUTPUT # digo ao circuitpython que meu led é uma saída.
botao.direction = Direction.INPUT # digo a ele que meu botão é uma entrada

# Quando o botão não estiver sendo pressionado, não tenho nenhuma garantia de que o nível dele vai ser Alto ou Baixo.
# No nosso circuito, nós fizemos uma ligação no botão que quando ele for pressionado vai acionar nível baixo. Mas não há nada
# ligado nele que garanta outro nível. Isso pode gerar falsos acionamentos. Para não fazer outra ligação e usar outro componente,
# nós usamos PULL

botao.pull = Pull.UP # indicando que, quando a entrada não receber nenhum sinal, nós vamos assumir que ela está em nível ALTO 
```
O código acima prepara as entradas e saídas do nosso sistema para funcionarem da maneira que esperamos. Mas ainda não dissemos a ele o que fazer com elas.

## Primeiro desafio: Acenda o Led quando o Botão for Pressionado
Nós agora vamos aproveitar toda a inicialização do código anterior, mas vamos adicionar a funcionalidade de acender o led quando o botão for pressionado.
Digite (ou copie e cole) o código abaixo e tente executá-lo no Thonny.
```
import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn

botao = DigitalInOut (board.D6)
led = DigitalInOut (board.D7)
pot = AnalogIn (board.A2)

led.direction = Direction.OUTPUT
botao.direction = Direction.INPUT

botao.pull = Pull.UP

# Loop Principal
# Executa até que vc pressione CTRL+C ou STOP, no Thonny

while True:
    # Se o valor do botão for Zero,
    if botao.value == False:
        led.value = True
    else:
        led.value = False
```
Digamos agora que nós queremos mudar apenas o Loop principal, mudando a funcionalidade do nosso botão.
Se o botão estiver pressionado, nós queremos que o nosso led fique piscando a cada 0.2s. Como fazemos?
Antes de tudo, temos que importar o módulo time, que cuida dos intervalos de tempo.
```
import board
import time # para lidar com os intervalos
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn

botao = DigitalInOut (board.D6)
led = DigitalInOut (board.D7)
pot = AnalogIn (board.A2)

led.direction = Direction.OUTPUT
botao.direction = Direction.INPUT

botao.pull = Pull.UP

# Loop Principal
# Executa até que vc pressione CTRL+C ou STOP, no Thonny

while True:
    # Se o valor do botão for Zero,
    if botao.value == False:
        led.value = not led.value # O que é isso?
        time.sleep(0.2)
    else:
        led.value = False
```
Veja que o código acima tem uma linha muito maluca: 
led.value = not led.value

O que quer dizer isso?
O Circuitpython vai atribuir um valor à propriedade led.value que vai ser o contrário do valor atual dessa propriedade.
Assim, se o valor atual da propriedade value, do objeto led for False, ele vai atribuir um valor True. E vice-versa.

Nós poderíamos escrever outro código para o loop principal que faz a mesma função:
```
# Somente o loop principal, não esqueça do código anterior...
while True:
    # Se o valor do botão for Zero,
    if botao.value == False:
        led.value = True # Acende
        time.sleep(0.2) # Espera
        led.value = False # Apaga
        time.sleep(0.2) # Espera
    else:
        led.value = False
```
E se nós quiséssemos manter o led piscando, enquanto o botão não for pressionado? E quando o botão fosse pressionado, o led apagasse
e o programa termina?

```
# Como nós dissemos antes que o botão vai estar em nível alto se não for pressionado
# o loop a seguir fica rodando até que a gente pressione o botão, caso em que ele recebe o valor False

while botao.value == True:
    led.value = not led.value
    time.sleep(0.2) # Que tal se você diminuir bastante esse valor aqui? Quando você chegar perto de 0.04 vai ver uma coisa estranha...

led.value = False
print ('Terminei tudo') # Só pra gente ver que o programa chegou aqui
```
## Segundo desafio: imprimir o valor da entrada analógica
No segundo exercício, nós vamos imprimir o valor da entrada analógica. 
Digite o código abaixo e execute. Varie o valor do potenciometro girando-o e anote os valores mínimo e máximo.

```
# O começo do nosso código é sempre o mesmo:
import board, time
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn

# Nós não vamos usar botão e led por enquanto, mas deixe eles aqui
botao = DigitalInOut (board.D6)
led = DigitalInOut (board.D7)

# Essa é a estrela do momento...
pot = AnalogIn (board.A2)

# Não vamos fazer nada com eles, por enquanto
led.direction = Direction.OUTPUT
botao.direction = Direction.INPUT

botao.pull = Pull.UP

while True:
    print (pot.value)
    time.sleep(0.5)

```
Se tudo correu bem na montagem, o valor do potenciômetro deve estar na faixa de 0 a 65535. Porque esses números?
Na Raspberry Pi Pico, as saídas analógicas possuem uma resolução de 16 bits. Um bit é uma unidade binária que pode ter valores entre 0 e 1 (dois valores).
Se nós temos uma resolução de 16 bits, significa que nós temos 2^16 combinações possíveis entre 0 e 1, o que dá 65536 valores.

Claro, como seu potenciômetro tem uma tolerência (às vezes 1%, 2% e até 10%), pode ser que os valores obtidos no seu código não sejam exatamente esses.

A essa altura, você deve estar se perguntando se poderia usar o potenciômetro para mudar o brilho do LED. A resposta é sim.

Vamos fazer uma experiência com esse código:

```
import board, time
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn

while True:
    # Se o valor do botão for Zero,
    if botao.value == False:
        led.value = not led.value # O que é isso?
        time.sleep(0.2) # diminua esse valor gradativamente até 0.04
    else:
        led.value = False
```
O que acontece com Led quando time.sleep(0.04) ?
Parece que ele está acendendo mais fraco e não apaga mais.
Na realidade, ele está acendendo e apagando tão rápido, que a nossa visão não capta. Então temos a percepção de que ele está meio apagado.

Essa abordagem é chamada de Modulação Por Comprimento do Pulso, ou em inglês PWM. É uma maneira de usar um sinal digital para simular uma saída analógica.
Isso é usado para tocar sons, diminuir a intensidade e a velocidade de dispositivos e até enviar comandos de direção, no caso dos servo-motores.

Em CircuitPython, nós temos um módulo nativo para lidar com esse tipo de sinal. É o PWMio.

O código abaixo altera o brilho do Led, conforme você gira o potenciômetro.

```
import board, time
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
from pwmio import PWMOut

led = PWMOut (board.D7, frequency=5000, duty_cycle=0)
pot = AnalogIn (board.A2)

while True:
    led.duty_cycle = pot.value

```
Como led.duty_cicle também varia entre 0 e 65535, nós não precisamos fazer nenhum tratamento dos valores recebidos pelo potenciômetro. 
Basta copiar o valor pot.value para a propriedade led.duty_cycle e pronto!

Mas algumas vezes, precisamos lidar com o potenciômetro para fazer a variação entre valores diferentes dos que são obtidos na entrada analógica.
Por exemplo, no Joystick que vamos utilizar, os eixos X e Y do movimento são obtidos por dois potenciômetros. Como é que transformamos isso em
valores de movimento? Em alguns casos, queremos usar o potenciômetro para alterar valores na faixa de 0 a 100, por exemplo. Como fazemos isso?

### **Usando Regra de Três Simples:**
Seja:
- **Faixa Original**: de `min` até `max`
- **Faixa Nova**: de `new_min` até `new_max`
- **Valor a transformar**: `valor_lido`

Queremos descobrir qual valor na **Faixa Nova** corresponde à mesma "posição proporcional" do `valor_lido` na **Faixa Original**.

Imagine uma régua:
```
min ---------------------- valor_lido ---------------------- max
```
A distância do `min` até o `valor_lido` é:  
`distancia_original = valor_lido - min`

O tamanho total da Faixa Original é:  
`tamanho_original = max - min`

Então, a **proporção** do `valor_lido` na Faixa Original é:  
`proporcao = distancia_original / tamanho_original`

Exemplo:  
Se `min=0`, `max=100`, e `valor_lido=50`:  
`proporcao = (50 - 0) / (100 - 0) = 50/100 = 0.5`  
(ou seja, 50% do caminho na Faixa Original).


Agora, use essa proporção na **Faixa Nova**:
```
new_min ---------------------- ? ---------------------- new_max
```
O tamanho total da Faixa Nova é:  
`tamanho_novo = new_max - new_min`

Multiplicamos a proporção pelo tamanho novo:  
`distancia_nova = proporcao × tamanho_novo`

E adicionamos ao `new_min` para encontrar o valor final:  
`valor_final = new_min + distancia_nova`

Exemplo:  
Se `new_min=10`, `new_max=20`, e `proporcao=0.5`:  
`tamanho_novo = 20 - 10 = 10`  
`distancia_nova = 0.5 × 10 = 5`  
`valor_final = 10 + 5 = 15`

```
valor_final = new_min + [(valor_lido - min) / (max - min)] × (new_max - new_min)
```

Transformar a temperatura de **Celsius para Fahrenheit**:  
- Faixa Original: `min=0°C`, `max=100°C`  
- Faixa Nova: `new_min=32°F`, `new_max=212°F`  
- Valor: `valor_lido=50°C`

**Cálculo:**  
1. Proporção: `(50 - 0) / (100 - 0) = 0.5`  
2. Distância na Faixa Nova: `0.5 × (212 - 32) = 0.5 × 180 = 90`  
3. Valor Final: `32 + 90 = 122°F`  

*(Nota: Na verdade, 50°C = 122°F! A fórmula funcionou!)*

**Por que isso é útil?**
- **Sensores**: Converter leituras de um sensor (ex: 0-1023) para uma faixa útil (ex: 0-100%).  
- **Gráficos**: Mapear coordenadas de uma tela para outra.  
- **Jogos**: Ajustar valores de jogo (ex: vida de 0-100 para uma barra de 0-255).  

**Atenção!**
- Se `min == max`, a divisão por zero causa erro. Nesse caso, retorne `new_min` (pois a faixa original é um único ponto).  
- Valores fora da Faixa Original (ex: menor que `min` ou maior que `max`) serão extrapolados na Faixa Nova. Isso é intencional!

## Criando uma função Python específica para a Regra de Três

Bem, vamos criar uma função em Python, para resolver a nossa regra de três simples.

```
def regra_de_tres(valor_lido, min_original, max_original, nova_faixa_min, nova_faixa_max):
    # Evitar divisão por zero se min_original == max_original
    if min_original == max_original:
        return nova_faixa_min
    
    # Aplicar a fórmula de mapeamento
    return ((valor_lido - min_original) / (max_original - min_original)) * \
           (nova_faixa_max - nova_faixa_min) + nova_faixa_min

# Mapear 50 da faixa [0, 100] para a faixa [10, 20]
print(regra_de_tres(50, 0, 100, 10, 20))  # Saída: 15.0

# Mapear 25 da faixa [-10, 10] para a faixa [0, 100]
print(regra_de_tres(25, -10, 10, 0, 100))  # Saída: 175.0

```
Ótimo! Agora sabemos de que jeito é possível mapear um valor na faixa de 0 a 65535 para um valor de 0 a 9, por exemplo.

