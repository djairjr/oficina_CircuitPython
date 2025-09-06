'''
    Checking Joystick Range Values
    
    Wroted by Djair Guilherme (Nicolau dos Brinquedos)
    For the "Recriating Arcade Games in Circuitpython, Neopixel and Seeed Xiao RP2040"
    SESC Workshop - São Paulo - Brazil - May 2024
    Requirements: custom tilegrid, tile_framebuf, my_framebuf libraries
    Available at: https://github.com/djairjr/oficina_CircuitPython/tree/main/aula_6_Neopixel/libraries
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

def get_joystick():
    # Returns -1 0 or 1 depending on joystick position
    x_coord = int (map_range (joystick_x.value, 200, 65535, - 2 , 2))
    y_coord = int (map_range (joystick_y.value, 200, 65535, - 2 , 2))
    return x_coord, y_coord

while True:
    # Eixo x - cima baixo
    # Eixo y - esquerda direita
    print (joystick_x.value, joystick_y.value)
    print (get_joystick())
    time.sleep(0.05)
    