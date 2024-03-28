# Para todos os exemplos nesse código, utilize as ligações no diagrama aula3_bb.png
# Entrada e saída digital simples:
# Lê o valor de tensão no pino analógico

import time, board
from analogio import AnalogIn

analog_in = AnalogIn (board.A1) # board.GP27

# Criando uma função com def
def get_voltage (pin):
  # pin.value vai retornar um valor entre 0 e 65536. 
  # 3.3 é a tensão máxima.
  return (pin.value * 3.3) / 65536

while True:
  print (get_voltage (analog_in))
  time.sleep (0.1)
