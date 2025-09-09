'''
No primeiro exercício, nós descobrimos os valores mínimo e máximos do
joystick. Como temos limitações mecânicas, pode ser que o valor mínimo
fique acima de 0 e o máximo, abaixo de 65535. Nos meus testes, o mínimo
estava em 200, por exemplo.
'''
import board, time
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn

botao = DigitalInOut (board.D6)

eixo_x = AnalogIn (board.A1)
eixo_y = AnalogIn (board.A2)

while True:
    print (eixo_x.value, eixo_y.value)
    time.sleep(0.2)