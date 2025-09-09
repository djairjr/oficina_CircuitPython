'''
A rotina get_joystick já nos devolve um valor de coordenada, dependendo do eixo
que nós movimentamos. Veja que ela usa map_range para converter os valores na faixa
de 0 a 65535 em valores de -2 a 2
'''
import board, time
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
from simpleio import map_range

botao = DigitalInOut (board.D6)

eixo_x = AnalogIn (board.A1)
eixo_y = AnalogIn (board.A2)

def get_joystick():
    # Returns -1 0 or 1 depending on joystick position
	# o formato de map_range (valor lido, min_lido, max_lido, min_desejado, max_desejado)
    x_coord = int (map_range (joystick_x.value, 0, 65535, - 2 , 2))
    y_coord = int (map_range (joystick_y.value, 0, 65535, - 2 , 2))
    return x_coord, y_coord

while True:
    print (get_joystick())
    time.sleep(0.2)