# Script para exibir o dinossauro no display 16x2 com I2C

import board, busio, time
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

def print_dino(column, row):
    
    lcd.set_cursor_pos(column,row)
    for counter in range(4):
        if row+counter < 20:
            lcd.write(counter)
    lcd.set_cursor_pos(column+1,row)
    for counter in range(4):
        if row+counter < 20:
            lcd.write(counter+4)

# Caractere customizado vai ser usado na animação
dino1 = (0x00,0x00,0x00,0x00,0x10,0x10,0x18,0x1F)
dino2 = (0x00,0x01,0x01,0x01,0x01,0x03,0x0F,0x1F)
dino3 = (0x1F,0x17,0x1F,0x1F,0x1C,0x1F,0x1C,0x1C)
dino4 = (0x10,0x18,0x18,0x18,0x00,0x10,0x00,0x00)
dino5 = (0x1F,0x0F,0x07,0x03,0x03,0x03,0x02,0x03)
dino6 = (0x1F,0x1F,0x1F,0x1F,0x17,0x03,0x02,0x03)
dino7 = (0x1F,0x19,0x10,0x00,0x00,0x00,0x00,0x00)
dino8 = (0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00)

sda, scl = board.GP0, board.GP1

i2c = busio.I2C(scl, sda)
lcd = LCD(I2CPCF8574Interface(i2c, 0x27), num_rows=4, num_cols=20)
#lcd = LCD(I2CPCF8574Interface(i2c, 0x27), num_rows=2, num_cols=16)

lcd.create_char(0,dino1)
lcd.create_char(1,dino2)
lcd.create_char(2,dino3)
lcd.create_char(3,dino4)
lcd.create_char(4,dino5)
lcd.create_char(5,dino6)
lcd.create_char(6,dino7)
lcd.create_char(7,dino8)

column = 2

for counter in range(20):
    print_dino(column,counter)
    time.sleep(.5)
    if counter in range(10,11):
        column = 1
    else:
        column = 2
    lcd.clear() 