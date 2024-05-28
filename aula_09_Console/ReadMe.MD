# Console Arcade

# Esquema de montagem para o nosso Console Arcade
![Esquema de Montagem](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_09_Console/images/Xiao_Neopixel_bb.png)

O sistema do nosso console vai ser o mesmo para todos os nossos jogos.
Na aula de hoje, vamos montar todo o sistema e testar cada um dos módulos isoladamente.

Em seguida, vamos estabelecer relações entre eles e verificar como funcionam juntos.
No final da aula, vamos montar um Etch a Sketch (Lousa Mágica) para testar tudo junto.

Para exibir as mensagens de jogo, placar e contagem regressiva, vamos utilizar um display I2C
com 14 Segmentos e 4 Caracteres, que utiliza o chip HT16K33.

A conexão para esse módulo é um pouco confusa...

VI2C é igual à tensão do barramento I2C utilizado. No nosso caso, 3.3 V
VCC é sempre 5V (quando ligamos VCC em 3V3 no RP2040, o display não é reconhecido).
GND é Terra.
SCL e SDA são os pinos de I2C Padrão.

Para utilizarmos o módulo, precisamos instalar a biblioteca adafruit_ht16k33

