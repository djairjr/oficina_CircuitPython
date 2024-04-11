''' Usando Expansor de Portas PCF8574 com Keypad '''
import board
import busio
import time
import adafruit_matrixkeypad
import adafruit_pcf8574

SDA_Pin = board.GP20
SCL_Pin = board.GP21

i2c = busio.I2C (scl=SCL_Pin, sda=SDA_Pin)
pcf = adafruit_pcf8574.PCF8574(i2c) # Talvez precise adicionar o Address

''' Eu costumo soldar o Keypad direto no PCF8574'''
rows = [pcf.get_pin(5), pcf.get_pin(0), pcf.get_pin(1), pcf.get_pin(3)]
cols = [pcf.get_pin(4), pcf.get_pin(6), pcf.get_pin(2)]
keys = ((1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        ('*', 0, '#'))

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

while True:
    keys = keypad.pressed_keys
    if keys:
        print("Pressionada: ", keys)
    time.sleep(0.1)
