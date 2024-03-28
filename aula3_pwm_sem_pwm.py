# Para todos os exemplos nesse código, utilize as ligações no diagrama aula3_bb.png
# Como diminuir o brilho do LED usando persistencia da visão
# Dê uma olhada nesse artigo aqui: https://en.wikipedia.org/wiki/Flicker_fusion_threshold

import time, board
from digitalio import DigitalInOut, Pull, Direction

led = DigitalInOut (board.LED)
led.direction = Direction.OUTPUT

frequencia = 60 # de 60 a 90hz a visão humana registra os pulsos como continuidade.
periodo_total = 1 / frequencia

duty_cicle = int (input ( 'Digite a intensidade do LED em porcentagem (0 a 100%: )')) / 100
inactive_time = 1 - duty_cicle

while True:
  led.value = True
  time.sleep (duty_cicle * periodo_total) 
  led.value = False
  time.sleep (inactive_time * periodo_total)



