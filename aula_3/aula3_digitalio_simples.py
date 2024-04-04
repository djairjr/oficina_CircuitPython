# Para todos os exemplos nesse código, utilize as ligações no diagrama aula3_bb.png
# Entrada e saída digital simples:
# Piscando o Led enquanto o botão é pressionado

import board, time
from digitalio import DigitalInOut, Pull, Direction

led = DigitalInOut (board.GP22) # para usar led externo ou board.LED para o usar o default
led.direction = Direction.OUTPUT
# ou você pode usar led.switch_to_output()

button = DigitalInOut (board.GP7)
button.direction = Direction.INPUT
# ou você pode usar button.switch_to_input()
button.pull = Pull.UP

while True:
  if not button.value:
    led.value = not led.value # inverte o valor atual de led
    time.sleep (0.5) # aguarda meio segundo
