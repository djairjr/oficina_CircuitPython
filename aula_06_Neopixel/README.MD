## Instalando as bibliotecas Neopixel e Adafruit_Simpleio
Até o momento, nós estamos lidando apenas com os módulos nativos da nossa placa. Não foi preciso fazer a instalação de nenhum módulo adicional. 
Convencionalmente, nós chamamos esses módulos adicionais para a programação de **bibliotecas (ou libraries)**.
Nós podemos instalar essas bibliotecas simplesmente copiando os arquivos .py ou .mpy para a pasta lib da sua placa.
Mas a maneira mais segura de fazer isso é utilizar o gerenciador de pacotes CircUP, da Adafruit.

Para instalar esse gerenciador, abra o Thonny e acesse o menu Tools (Ferramentas) >> Open System Shell. 

Você deve ver a janela de comandos do seu Windows, com alguma coisa similar a **C:\Users\Usuario\Pasta>**

Nesta janela, digite o comando a seguir:
```
python -m pip install circup
```

Isso deve instalar o gerenciador de pacotes Circup, da Adafruit.
Agora, vamos instalar duas bibliotecas que vamos utilizar para os próximos exercícios:

```
circup install neopixel, adafruit_simpleio
```

## Neopixels, Listas, Tuplas, Dicionários
As fitas de Led Neopixel são muito versáteis. Cada led possui um controlador de cores isolado e pode ser acessado individualmente.
Os leds são ligados em cascata e possuem sempre quatro pinos: VCC e GND, que são os pinos de energia e DI e DO, que são os pinos
de entrada de dados (DI) e saída de dados (DO). Para criar uma fita de leds, basta conectar os pinos DO de um led ao pino DI de outro.
O primeiro led vai ser o que tiver o seu pino DI conectado ao controlador.

Você pode cortar a fita Led e usar pequenos pedaços. Ou montar diversos arranjos diferentes. No mercado, encontramos anéis, matrizes,
leds individuais.

Eu gosto muito de usar as fitas de Led porque consigo um grande efeito visual usando apenas um pino do meu controlador.

Nós vamos adaptar a nossa montagem de sempre, só que ao invés de usar um LED, vamos usar uma fita com dez leds diferentes.
![Montagem com Fitas Led Neopixel](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_06_Neopixel/Diagrama%20Aula%204_bb.png)

Vamos aproveitar o uso das fitas Neopixel para retomar um conceito que eu trabalhei bem rapidamente na nossa primeira aula, que é a habilidade do Python para tratar de dados estruturados.
Em Python, nós temos três tipos de dados estruturados.
Listas, que são conjuntos de informações que podem ser modificadas em tempo real.
Tuplas, que são conjuntos de informações imutáveis (você pode ler, mas não modificar)
e Dicionários, que são conjuntos de informações que podem ser modificadas, mas que são acessadas através de um par key:value.

A biblioteca Neopixel do Circuitpython faz com que cada um dos leds da fita seja um elemento dentro de uma lista. Cada um desses elementos pode receber um valor na forma de uma tupla, que vai conter as cores no formato (Red, Green, Blue) com Red, Green e Blue variando entre 0 e 255.

No exercício a seguir, vamos criar uma lista com cores e aplicar as cores à medida em que giramos o potenciômetro.

```
import board, time
import neopixel
from simpleio import map_range # map_range é a regra de três
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn

pot = AnalogIn (board.A2)
botao = DigitalInOut (board.D6)

led_pin = board.D7
num_led = 10
brilho = 0.3 # varia de 0 a 1 em décimos

pixels = neopixel.NeoPixel (led_pin, num_led , brightness=brilho, auto_write=False )

# Uma lista de Tuplas, com as cores.
color_list = [ (0,0,0), (255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255),(255,255,255)] 

while True:
    cor = map_range (pot.value, 0, 65535, 0, 7)
    pixels.fill (color_list[cor])
    pixels.show()
```


