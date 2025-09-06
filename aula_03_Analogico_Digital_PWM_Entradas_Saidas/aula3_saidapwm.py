
import array, math
import board, time, digitalio

from audiocore import RawSample # para tratar amostras binárias puras

try:
    # Se houver AudioOut na plaquinha
    from audioio import AudioOut 
except ImportError:
    try:
        # Senão, vamos por PWM mesmo
        from audiopwmio import PWMAudioOut as AudioOut 
    except ImportError:
        pass  # Nem toda placa dá conta de fazer isso

button = digitalio.DigitalInOut(board.GP7)
button.switch_to_input(pull=digitalio.Pull.UP)

tone_volume = 0.1  # Volume do tom
frequency = 440  # Frequência em Hertz, do tom a ser gerado
length = 8000 // frequency # Duração arredondado

# Cria um array zerado, em Hexa do tamanho do comprimento
sine_wave = array.array("H", [0] * length)

# Preenche esse array com valores gerando onda senoidal
for i in range(length):
    # para cada indice do array, gera uma amplitude
    sine_wave[i] = int((1 + math.sin(math.pi * 2 * i / length)) * tone_volume * (2 ** 15 - 1))

audio = AudioOut(board.A0)
sine_wave_sample = RawSample(sine_wave)

while True:
    if not button.value:
        audio.play(sine_wave_sample, loop=True)
        time.sleep(1)
        audio.stop()
