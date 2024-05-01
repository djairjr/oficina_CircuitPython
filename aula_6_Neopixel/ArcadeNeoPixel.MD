# Recriando Clássicos dos Arcades com Neopixel e Circuitpython

O primeiro desafio para a oficina de Arcades é transformar as fitas de led num display mínimo.
O pessoal da Adafruit já fez um trabalho incrível, desenvolvendo a biblioteca Pixel_Framebuf.
Mas ela não suporta todo tipo de arranjo com os paineis. Por exemplo, você até consegue fazer
um arranjo de duas placas 8x32 de modo a conseguir 8x64, porque esse é  o  fluxo natural  das
conexões numa Fita Led. Mas se você quiser arranjar algo com 16x32, não vai conseguir ter  as
coordenadas da tela corretas.

(https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_6_Neopixel/Array%20Neopixel%20-%20Coordenadas.png?raw=true)
