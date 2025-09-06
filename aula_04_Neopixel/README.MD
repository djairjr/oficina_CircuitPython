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

## Mudando as cores da fita inteira

No exercício a seguir, vamos criar uma lista com cores e aplicar as cores à fita inteira, usando o método fill().
O potenciômetro vai trocar a cor da fita à medida em que for girado.

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

Você poderia mapear o potenciômetro e usá-lo para duas coisas distintas. Por exemplo, acender um led específico, com uma cor específica.

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
color_list = [ (10,20,30), (255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255), (100,100,100), (128, 128, 50), (255,255,255)] 

while True:
    cor = map_range (pot.value, 0, 65535, 0, 9) # Mapeando para a faixa de cores
    pixel =  map_range (pot.value, 0, 65535, 0, num_led -1) # Mapeando para a faixa de pixels
    pixels.fill ((0,0,0)) # Apaga todos os leds
    pixels[pixel] = (color_list[cor]) # acende apenas um led com a cor especificada
    pixels.show()
```

## Um dicionário para acessar as cores pelos nomes
Como você já deve estar pensando, é muito complicado lidar com as cores nesse formato de tuplas numéricas. Nós normalmente chamamos as cores pelos nomes, 
e seria muito mais interessante se houvesse uma maneira de fazer isso.

O Dicionário abaixo implementa as cores de acordo com o padrão HTML.
[Nomes das Cores em HTML](https://www.w3schools.com/colors/colors_names.asp)

```
# Para encontrar a tupla da cor específica faça
# cor["Beige"] e o resultado será a tupla da cor indicada.

cor = {
    "AliceBlue": (240, 248, 255),
    "Amethyst": (153, 102, 204),
    "AntiqueWhite": (250, 235, 215),
    "Aqua": (0, 255, 255),
    "Aquamarine": (127, 255, 212),
    "Azure": (240, 255, 255),
    "Beige": (245, 245, 220),
    "Bisque": (255, 228, 196),
    "Black": (0, 0, 0),
    "BlanchedAlmond": (255, 235, 205),
    "Blue": (0, 0, 255),
    "BlueViolet": (138, 43, 226),
    "Brown": (165, 42, 42),
    "BurlyWood": (222, 184, 135),
    "CadetBlue": (95, 158, 160),
    "Chartreuse": (127, 255, 0),
    "Chocolate": (210, 105, 30),
    "Coral": (255, 127, 80),
    "CornflowerBlue": (100, 149, 237),
    "Cornsilk": (255, 248, 220),
    "Crimson": (220, 20, 60),
    "Cyan": (0, 255, 255),
    "DarkBlue": (0, 0, 139),
    "DarkCyan": (0, 139, 139),
    "DarkGoldenrod": (184, 134, 11),
    "DarkGray": (169, 169, 169),
    "DarkGreen": (0, 100, 0),
    "DarkKhaki": (189, 183, 107),
    "DarkMagenta": (139, 0, 139),
    "DarkOliveGreen": (85, 107, 47),
    "DarkOrange": (255, 140, 0),
    "DarkOrchid": (153, 50, 204),
    "DarkRed": (139, 0, 0),
    "DarkSalmon": (233, 150, 122),
    "DarkSeaGreen": (143, 188, 143),
    "DarkSlateBlue": (72, 61, 139),
    "DarkSlateGray": (47, 79, 79),
    "DarkTurquoise": (0, 206, 209),
    "DarkViolet": (148, 0, 211),
    "DeepPink": (255, 20, 147),
    "DeepSkyBlue": (0, 191, 255),
    "DimGray": (105, 105, 105),
    "DodgerBlue": (30, 144, 255),
    "FireBrick": (178, 34, 34),
    "FloralWhite": (255, 250, 240),
    "ForestGreen": (34, 139, 34),
    "Fuchsia": (255, 0, 255),
    "Gainsboro": (220, 220, 220),
    "GhostWhite": (248, 248, 255),
    "Gold": (255, 215, 0),
    "Goldenrod": (218, 165, 32),
    "Gray": (128, 128, 128),
    "Green": (0, 128, 0),
    "GreenYellow": (173, 255, 47),
    "Honeydew": (240, 255, 240),
    "HotPink": (255, 105, 180),
    "IndianRed": (205, 92, 92),
    "Indigo": (75, 0, 130),
    "Ivory": (255, 255, 240),
    "Khaki": (240, 230, 140),
    "Lavender": (230, 230, 250),
    "LavenderBlush": (255, 240, 245),
    "LawnGreen": (124, 252, 0),
    "LemonChiffon": (255, 250, 205),
    "LightBlue": (173, 216, 230),
    "LightCoral": (240, 128, 128),
    "LightCyan": (224, 255, 255),
    "LightGoldenrodYellow": (250, 250, 210),
    "LightGreen": (144, 238, 144),
    "LightGrey": (211, 211, 211),
    "LightPink": (255, 182, 193),
    "LightSalmon": (255, 160, 122),
    "LightSeaGreen": (32, 178, 170),
    "LightSkyBlue": (135, 206, 250),
    "LightSlateGray": (119, 136, 153),
    "LightSteelBlue": (176, 196, 222),
    "LightYellow": (255, 255, 224),
    "Lime": (0, 255, 0),
    "LimeGreen": (50, 205, 50),
    "Linen": (250, 240, 230),
    "Magenta": (255, 0, 255),
    "Maroon": (128, 0, 0),
    "MediumAquamarine": (102, 205, 170),
    "MediumBlue": (0, 0, 205),
    "MediumOrchid": (186, 85, 211),
    "MediumPurple": (147, 112, 219),
    "MediumSeaGreen": (60, 179, 113),
    "MediumSlateBlue": (123, 104, 238),
    "MediumSpringGreen": (0, 250, 154),
    "MediumTurquoise": (72, 209, 204),
    "MediumVioletRed": (199, 21, 133),
    "MidnightBlue": (25, 25, 112),
    "MintCream": (245, 255, 250),
    "MistyRose": (255, 228, 225),
    "Moccasin": (255, 228, 181),
    "NavajoWhite": (255, 222, 173),
    "Navy": (0, 0, 128),
    "OldLace": (253, 245, 230),
    "Olive": (128, 128, 0),
    "OliveDrab": (107, 142, 35),
    "Orange": (255, 165, 0),
    "OrangeRed": (255, 69, 0),
    "Orchid": (218, 112, 214),
    "PaleGoldenrod": (238, 232, 170),
    "PaleGreen": (152, 251, 152),
    "PaleTurquoise": (175, 238, 238),
    "PaleVioletRed": (219, 112, 147),
    "PapayaWhip": (255, 239, 213),
    "PeachPuff": (255, 218, 185),
    "Peru": (205, 133, 63),
    "Pink": (255, 192, 203),
    "Plum": (221, 160, 221),
    "PowderBlue": (176, 224, 230),
    "Purple": (128, 0, 128),
    "Red": (255, 0, 0),
    "RosyBrown": (188, 143, 143),
    "RoyalBlue": (65, 105, 225),
    "SaddleBrown": (139, 69, 19),
    "Salmon": (250, 128, 114),
    "SandyBrown": (244, 164, 96),
    "SeaGreen": (46, 139, 87),
    "Seashell": (255, 245, 238),
    "Sienna": (160, 82, 45),
    "Silver": (192, 192, 192),
    "SkyBlue": (135, 206, 235),
    "SlateBlue": (106, 90, 205),
    "SlateGray": (112, 128, 144),
    "Snow": (255, 250, 250),
    "SpringGreen": (0, 255, 127),
    "SteelBlue": (70, 130, 180),
    "Tan": (210, 180, 140),
    "Teal": (0, 128, 128),
    "Thistle": (216, 191, 216),
    "Tomato": (255, 99, 71),
    "Turquoise": (64, 224, 208),
    "Violet": (238, 130, 238),
    "Wheat": (245, 222, 179),
    "White": (255, 255, 255),
    "WhiteSmoke": (245, 245, 245),
    "Yellow": (255, 255, 0),
    "YellowGreen": (154, 205, 50)
}
```


