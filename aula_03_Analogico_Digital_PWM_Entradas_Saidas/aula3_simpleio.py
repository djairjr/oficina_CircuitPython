# A Biblioteca Simpleio foi criada justamente para facilitar a transição
# para quem vem do mundo Arduino

import simpleio
from analogio import AnalogIn

potenciometro = AnalogIn (board.A1) # board.GP27
buzzer = board.A1

notas = (262, 294, 330, 349, 392, 440, 494, 523)

# Tone - toca os sons em ordem - utiliza a frequência das notas como parâmetro
for f in notas:
    simpleio.tone(buzzer, f, 0.25) # Pino de Saída, Nota, Duração

# Map Range - A mesma função que já usamos, embutida no Simple IO
repeat = len (notas)
count = 0
novanota = -1

while count < repeat:
    nota = simpleio.map_range (potenciometro.value, 0, 65535, 0, repeat)
    simpleio.tone(buzzer, nota, 0.25)
    if nota != novanota:
        count += 1 # incrementa a contagem quando muda de nota
        


