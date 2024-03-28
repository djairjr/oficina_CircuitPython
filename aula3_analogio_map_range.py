# Para todos os exemplos nesse código, utilize as ligações no diagrama aula3_bb.png
# Entrada e saída digital simples:
# Lê o valor de tensão no pino analógico
# Converte o valor bruto para valor em tensão usando a função map_range

import time, board
from analogio import AnalogIn

analog_in = AnalogIn (board.A1) # board.GP27

# Criando uma função map_range que funciona como Arduino map

def map_range (valor_entrada, a_min, a_max, b_min, b_max):
  # Essa função é uma regra de três simples, na realidade
  return b_max + (( valor_entrada - a_min) * (b_max - b_min) / (a_max - a_min))

while True:
  # Pegue um valor de entrada que varia entre 0 e 65535
  # e me dê um valor que varie entre 0 e 3.3´que é a tensão de saída máxima.
  # Estou indicando a porcentagem aqui porque pode ser util depois...
  
  tensao_saida = map_range (analog_in, 0, 65535, 0, 3.3)
  porcentagem = map_range (analog_in, 0, 65535, 0, 100)
  print (tensao_saida)
  print ('Porcentagem %d' % porcentagem + "%")
  time.sleep(0.1)
