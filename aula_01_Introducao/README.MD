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


# Listar todos os módulos disponíveis
help ('modules')

# Importar o Módulo 'builtins' que contém todas as palavras chave de Python
import builtins

# Mostrar uma lista com todas as palavras chave

```
for palavra_chave in dir (builtins):
  
    print (palavra_chave)
```

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






  

