''' Usando Expansor de Portas PCF8574 com Keypad '''
''' Vamos descobrir primeiro o endereço do PCF8574 ou PCF8575 '''
import board
import busio
import time
import adafruit_matrixkeypad
import adafruit_pcf8574

SDA_Pin = board.GP20
SCL_Pin = board.GP21

i2c = busio.I2C (scl=SCL_Pin, sda=SDA_Pin)
pcf = adafruit_pcf8574.PCF8574(i2c) # Talvez precise adicionar o Address

mypassword = ''

# Cada Keypad tem sua própria conexão. Cheque sempre o manual
# Veja que a ordem dos pinos é estranha...

rows = [pcf.get_pin(5), pcf.get_pin(0), pcf.get_pin(1), pcf.get_pin(3)]
cols = [pcf.get_pin(4), pcf.get_pin(6), pcf.get_pin(2)]
keys = (('1', '2', '3'),
        ('4', '5', '6'),
        ('7', '8', '9'),
        ('*', '0', '#'))

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

while True:
    keys = keypad.pressed_keys
    if keys:
        print("Pressionada: ", keys)
        if keys!='#':
            mypassword.append (keys)
        if keys == '*':
            mypassword = ''

        if mypassword = '1234':
            print ('Unlocked')
            
            break
                
    time.sleep(0.1)
