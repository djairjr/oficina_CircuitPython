Nessa aula, vamos aprender a utilizar a biblioteca DISPLAYIO, que uniformiza e faz a ponte
entre os diversos tipos de display que existem no mercado.

Eu vou compartilhar alguns códigos, com diferentes tipos de display existentes e na nossa
aula, vamos fazer um experimento usando o display ST7789, LCD colorido com 240x240 pixels.

Independentemente de qual seja o display e o tipo de interface que você está utilizando, 
o Circuitpython vai tratar da mesma forma, o que facilita muito a nossa memorização.

Basicamente o algoritmo para usar um display é sempre o mesmo:

1- Importar o módulo board, para utilizar os pinos da placa
2- Importar o módulo busio, para gerenciar os buses a serem utilizados (opcional)
3- Importar o módulo displayio
4- Importar biblioteca de inicialização específica do display utilizado
5- Importar bibliotecas auxiliares para fontes, bitmaps, textos, figuras geométricas
6- Liberar os displays
7- Inicializar os Buses (SPI ou I2C)
8- Configurar o Bus utilizado pelo Display
9- Configurar o display em si.


  

