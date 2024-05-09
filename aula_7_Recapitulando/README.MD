# Introdução ao Circuitpython
Circuitpython é um firmware para microcontroladores que contém um interpretador Python
embarcado. Ele permite, por exemplo, que você vá executando o seu código e vendo o 
funcionamento dele imediatamente, eliminando o tempo de compilação e debug do código,
característicos do desenvolvimento em Arduino, por exemplo.

É excelente para o aprendizado e muito bem suportado pela empresa que o desenvolveu
a Adafruit Industries.

# Instalando o Circuitpython
O firmware do Circuitpython pode ser instalado em uma gama bastante grande de placas
de desenvolvimento. E se a sua placa não for suportada ainda, você pode baixar o código
fonte e compilar você mesmo. O código está disponível no site:
https://github.com/adafruit/circuitpython

As etapas de instalação diferem um pouco, dependendo da placa de desenvolvimento que você
possui. Para as placas com o microcontrolador RP2040, como a Raspberry Pi Pico e a Seeed
Xiao RP2040, o procedimento é sempre o mesmo:

1. Baixe o firmware compatível com sua placa no link: https://circuitpython.org/downloads
o download vai baixar o firmware com a extensão .uf2

2. Conecte o cabo USB na sua placa. Mantenha o botão BOOT pressionado e em seguida, conecte
o cabo USB no seu computador. Um novo drive externo vai abrir, com o label RPI-RP2, que indica
que a placa está em modo UPLOAD.

3. Arraste o arquivo com a extensão .uf2 para o novo drive RPI-RP2. Depois da cópia, a placa
vai ser reiniciada e o drive externo passará a ter o label CIRCUITPY.

4. Pronto!

# Instale também o Python mais recente e o circup (no seu computador)
Para instalar algumas bibliotecas na plaquinha, o modo mais simples é utilizar o interpretador 
Python. A Adafruit desenvolveu um sistema de instalação chamado Circup, que depende do Python
para ser executado.

Isso também é bem simples:

1. Baixe a versão mais recente do Python no site:  https://www.python.org/downloads/

2. Abra o terminal padrão do Windows e execute o comando: 
```
pip install circup
```
3. O sistema vai baixar o pacote circup e instalar na sua máquina (Windows, Linux ou MacOS)

# Instale o Thonny IDE
O Thonny IDE é um ambiente de Desenvolvimento em Python, que é bem enxuto e fácil de usar.
Possui suporte a Micropython e Circuitpython e é o ambiente que vamos utilizar na oficina.

1. Baixe e instale a versão mais recente no site: http://thonny.org/downloads

# Configurando o Thonny para usar Circuitpython
Por padrão, Thonny é executado com um interpretador Python embutido. Mas você pode configurá-lo
para utilizar o interpretador Python que você baixou antes e também para utilizar o interpretador
Python embarcado na sua plaquinha.

1. Abra o Thonny e clique em Ferramentas > Opções.
2. A janela com Opções do Thonny vai se abrir. Clique na aba Interpretador.
3. Que tipo de intrepretador você vai executar o seu código? Selecione Circuitpython Genérico
4. Selecione a Porta USB onde a sua plaquinha está conectada.
5. Pronto!

# Usando o Shell do Thonny
Na janela padrão do Thonny, na parte inferior vai estar o shell Python que está rodando na sua
plaquinha.
```
Adafruit CircuitPython 9.0.4 on 2024-04-16; Seeeduino XIAO RP2040 with rp2040

>>> 
```

Qualquer comando que você digitar após >>> vai ser executado na sua plaquinha.

# Listar todos os módulos disponíveis

```
help ('modules')

```
# Importar o Módulo 'builtins' que contém todas as palavras chave de Python

```
import builtins

```

# Mostrar uma lista com todas as palavras chave

```
for palavra_chave in dir (builtins):
  
    print (palavra_chave)
```
# Uma lista de possibilidades para o Shell
O shell de Python já possibilita fazer de modo direto uma série de operações.
Experimente digitar cada um dos comandos abaixo:

```
# Alguns comandos básicos de Python

# Operações matemáticas simples
4 + 4	# Soma
4 - 2	# Subtração
4 * 5	# Multiplicação
2 ** 3 	# Exponenciação
20 / 2	# Divisão
21 // 2 # Divisão arredondada (sem parte fracional)
20 % 3	# Módulo (Retorna o resto da divisão)

# Variáveis e Atribuição de valores
a = 1
b = 2
c = 'Texto'			# Não faz distinção de tipo na atribuição
lição = 'Outro Texto' 	# Existe a possibilidade de acentuação nas variáveis

print (b * lição)	# Escreve no prompt

# Nomes de variáveis válidos
a1 = 1
velocidade = 60
velocidade90 = 90
salario_medio = 1200
salário_médio = 1200
# salário médio = 1200 Não pode usar espaços
_variável = 10
# 1a = 1200 Não pode  começar com números

# Tipos de Variáveis Numéricas
a = 5 		# int
b = 3.0 	# float
c = -4		# int
d = - 8.0	# float

# Variáveis do tipo lógico
Verdadeiro = True
Falso = False

# Operadores Relacionais
Verdadeiro == Verdadeiro
Falso == Falso
Verdadeiro != True
Verdadeiro != False
a > b
a < b
a >= b
a <= b

# Operadores Lógicos
not Verdadeiro
not Falso
Verdadeiro and Verdadeiro
Verdadeiro or Falso

# Strings (Sequencia literal de caracteres)
texto = 'Isso é uma String 1234'
len (texto)
texto [7: 17] 	# Fatiamento
texto + '5678'	# Concatenação

composição = 'O resultado é %d'
composição % a

composição = 'O resultado é %02d'
composição % a

composição = 'O resultado é %5.2f'
composição % b

composição = 'O resultado é %s'
composição % texto

composição_mista = 'O resultado total é %d, %02d, %5.2f e %s' 
composição_mista % (a,a,b,texto)

# Entrada de Dados
a = input ('Digite alguma coisa ') # Sempre String
print ('Você digitou  %s' % a)

# Convertendo a entrada de dados em outro tipo
anos = int (input ('Entre a sua idade atual '))
nascimento = 2024 - anos
print ('Você nasceu no ano de %d '  %nascimento)

# Checando o tipo de uma variável
type (anos)
type (a)
type (Verdadeiro)

# Checando condições
a = int (input ('Digite um numero qualquer '))
if a == 1:
        print ('Aqui deu um')
    elif a == 2:
        print ('Aqui deu dois')
    else:
        print ('Aqui não deu nem um nem dois')
    
# Repetições:
x = 0
while x<3:
    print (x)
    x = x+1

for n in range (10):
        print (n)

# Tuplas, Listas, Dicionários

tupla = (0,1,2,3) # conjunto de dados imutável. Você pode acessar, mas não alterar
tupla[2] # resulta 2
tupla[2] = 3 # resulta em erro

lista = ['palavra 1', '0', 2 ] # conjunto mutável de dados
lista[0] = 0
lista # resulta em [0,'0', 2]

# Cria uma lista com numeros na faixa de 0 a 9
lista = [n for n in range (10)]
lista.append (10)
lista.remove (0)
lista.reverse()
for x,e in enumerate(lista):
    print (x, e)

# vê tudo que é possível fazer com a lista
dir (lista)

# conjunto mutável de dados, acesso é feito pelo nome da chave
dicionário = { 'Chave 1': 'Valor 1', 'Chave 2': 'Valor 2', 'Chave 3': 'Valor 3' }
dicionário [0] # Resulta em erro. A chave não pode ser endereçada por índices
dicionário ['Chave 1'] # Resulta 'Valor 1'

# Lembrando que eu posso fazer qualquer combinação de lista de tuplas, tuplas de listas,
# dicionários de tuplas, etc...
cores = {'BLACK': (0,0,0), 'RED': (255,0,0), 'GREEN':(0,255,0), 'BLUE':(0,0,255)}
red_amount, green_amount, blue_amount = cores['BLACK']
red_amount # resulta em 0

```
# Quer aprender mais sobre Python?
Para essa oficina, eu estou supondo que você já tenha algum conhecimento de Python.
Mas se esse não for o seu caso, dê uma conferida nos links que eu deixei na página
principal.
https://github.com/djairjr/oficina_CircuitPython/blob/main/README.md


# Os Módulos Board e Microcontroller
O módulo board faz toda a interface com os pinos da sua plaquinha.
E o módulo microcontroller, se refere aos pinos do seu microcontrolador.
Cada fabricante tem sua própria maneira de conectar os pinos do microcontrolador
aos pinos externos da placa e a Adafruit diferencia essas duas instâncias.


```
import board, microcontroller

for pin in dir (microcontroller.pin):
    # isinstance testa o tipo de um objeto
    # getattr, retorna o valor de um determinado atributo de um objeto
    # no caso abaixo, vai retornar o nome do pino no módulo microcontroller.pin
    if isinstance (getattr(microcontroller.pin, pin), microcontroller.Pin):
        print ("".join (("microcontroller.pin.", pin, '\t')), end = " ")
        for alias in dir(board):
            if getattr(board, alias) is getattr(microcontroller.pin, pin):
                print ("".join(("", "board.", alias)), end = " ")
        print()
```

# Os Módulos Digitalio, Analogio e PWMio
Todo o material da oficina do Sesc Santana sobre o assunto está aqui:
https://github.com/djairjr/oficina_CircuitPython/tree/main/aula_3_Digitalio_Analogio_PWMio

No site da Adafruit, tem o excelente tutorial de Inicio em Circuitpython:
https://learn.adafruit.com/circuitpython-essentials

Esses três módulos dão conta de três tipos de Entrada/Saída disponíveis.

Digitalio, vai dar conta das entradas e saídas digitais. Nós vamos utilizar esse módulo para
fazer a detecção do pressionamento de um botão, por exemplo.
https://learn.adafruit.com/circuitpython-digital-inputs-and-outputs?view=all

Analogio, dá conta das entradas e saídas analógicas. Esse vai ser o módulo que vai detectar
o movimento no nosso joystick.
https://learn.adafruit.com/circuitpython-basics-analog-inputs-and-outputs?view=all

PWMIo, dá conta das saídas e entradas Moduladas por Pulso. No nosso caso, são a base do Módulo
de som RTTTL, que vai reproduzir os sons no Buzzer.

# O Módulo BUSIO e os Buses SPI, I2C e UART
https://github.com/djairjr/oficina_CircuitPython/tree/main/aula_4_Busio_I2C_SPI_UART
Para os nossos joguinhos, o único que vai nos interessar é o Bus SPI. Nós vamos usar um Hack
da biblioteca Neopixel que utiliza o barramento SPI para garantir maior velocidade nas
transações. 

No link acima você encontra todos os exercícios da outra oficina.

# DisplayIO
O módulo DisplayIO é uma interface geral para trabalhar com qualquer tipo de tela em
CircuitPython. Eu sugiro a você que entenda bem os Buses primeiro, antes de tentar utilizar
as telas. Cada uma delas é conectada ao microcontrolador usando um Bus diferente e se você
tentar utilizar sem entender o que é isso, vai perder um longo tempo...

Nós fizemos algumas experiências lá no Sesc Santana: 
https://github.com/djairjr/oficina_CircuitPython/tree/main/aula_5_DisplayIO

E se você quiser fazer um joguinho que utilize essas telas, vai encontrar bastante coisa
já trabalhada.

Pra você que já conhece Python, Displayio tem muito do Pygame.
Dê uma conferida aqui:
https://learn.adafruit.com/circuitpython-display-support-using-displayio?view=all 

Mas essa não é a nossa aventura...

# Neopixel - Fitas Led RGB endereçadas
O melhor guia para utilizar essas fitas é esse aqui:
https://learn.adafruit.com/adafruit-neopixel-uberguide

Dá conta de todo o recado, todas as explicações e todo o funcionamento das fitas LED.
Inclusive no Arduino.

No link abaixo, estão os exercícios da aula de Neopixel na oficina do Sesc Santana:
https://github.com/djairjr/oficina_CircuitPython/tree/main/aula_6_Neopixel

O painel 8x32 que estamos utilizando é um arranjo em zig zag de uma fita de Led Neopixel.

Eu tive que fazer algumas adaptações em bibliotecas da Adafruit para poder fazer outros
arranjos com essas matrizes. Também criei um método para importar e exibir bitmaps nelas.

Fiz um tutorial bacana lá no Hackster.io que você encontra aqui:
https://www.hackster.io/nicolaudosbrinquedos/circuitpython-tiled-neopixel-panel-446b73






  

