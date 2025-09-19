# Exemplo de comunicação entre duas plaquinhas usando o barramento UART
# Nesse caso, eu estou utilizando duas XIAO RP2040 nas Expansion Board
# Para adaptar para Raspberry Pi Pico, como seria?

import board, busio, time

# ---------------------------------------------------------------
# Os módulos abaixo são para utilizar o display ssd1306 on board
import displayio, terminalio, adafruit_displayio_ssd1306
from adafruit_display_text import label

# Libera qualquer display antes de inicializar
displayio.release_displays()

# Cria um Bus I2C - Para usar o Display
i2c = busio.I2C (scl=board.SCL, sda=board.SDA)

# Cria um barramento para Display, em I2C usando o endereço 0x3C
display_bus = displayio.I2CDisplay (i2c, device_address = 0x3C)

# Configura o display Oled da placa de expansão
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Cria um Grupo de elementos a ser exibido
splash = displayio.Group()

# Exibe esses elementos no Display
display.root_group = splash
# ---------------------------------------------------------------

# Cria um Bus UART para se comunicar entre as duas plaquinhas
uart = busio.UART(board.TX, board.RX, baudrate=115200)

while True:

    data = uart.read(32)  # read up to 32 bytes
    if data is not None:   
        text = ''.join([chr(b) for b in data])
        print ('B Received >' + text)
        # Para imprimir no display onboard
        text_area = label.Label(terminalio.FONT, text=text +"\n", color=0xFFFF00, x=10, y=10)   
        splash.append(text_area)
        time.sleep(0.5)
        text = 'B send to A'
        print ('Enviando para A > ' + text)
        # Para imprimir no display onboard
        text_area = label.Label(terminalio.FONT, text=text +"\n", color=0xFFFF00, x=10, y=30)
      
        uart.write(bytes (text,'ascii'))
        time.sleep(0.5)

        








