# Para todos os exemplos nesse código, utilize as ligações no diagrama aula3_bb.png

# Como diminuir o brilho do LED usando persistencia da visão

import time, board
from digitalio import DigitalInOut, Pull, Direction

led = DigitalInOut (board.LED)
led.direction = Direction.OUTPUT

frequencia = 50
periodo_total = 1 / frequencia

duty_cicle = int (input ( 'Digite a intensidade do LED em porcentagem (0 a 100%: )')) / 100
inactive_time = 1 - duty_cicle

while True:
  led.value = True
  time.sleep (duty_cicle) # altere para duty_cicle * periodo_total
  led.value = False
  time.sleep (inactive_time) # altere para inactive_time * periodo total



