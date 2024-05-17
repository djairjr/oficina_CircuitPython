'''
Tratando o Joystick
Checando a gama de valores que os dois eixos do joystick retornam
'''

import board, time, os
from analogio import AnalogIn # Para os dois eixos do joystick 
from digitalio import DigitalInOut, Direction, Pull # para o botão
from simpleio import map_range # para converter faixa de valores

joystick_x = AnalogIn(board.A0)
joystick_y = AnalogIn(board.A1)

trigger = DigitalInOut (board.D2)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

# Aqui eu escrevi duas rotinas auxiliares que não vamos usar a princípio

def get_x(pin, number):
    return map_range (pin.value, 200, 65535, - number //2 , number // 2) 

def get_y(pin, number):
    return map_range (pin.value, 65535, 200, - number //2 , number // 2)

while True:
    # Eixo x - cima baixo
    # Eixo y - esquerda direita
    print (joystick_x.value) 
    time.sleep(0.05)
    