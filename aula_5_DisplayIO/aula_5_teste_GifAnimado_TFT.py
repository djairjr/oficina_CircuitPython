import board
import busio
import gifio
import displayio
import time
# Aqui você vai importar a biblioteca para o seu display
# import adafruit_ili9341
# import gc9a01
import adafruit_st7789

dc=board.D1
rst=board.D0	
cs=board.D2 #My display does not have it...
i2c = busio.I2C( board.SCL, board.SDA, frequency=200_000)
displayio.release_displays()
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)


display_bus = displayio.FourWire(spi, command = dc, chip_select=cs, reset=rst)

display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)
display.root_group.hidden = True # HIDE REPL
display.auto_refresh = False
splash = displayio.Group()
display.show(splash)

odg = gifio.OnDiskGif('/images/circlescv.gif')
odg.next_frame() # Load the first frame

#face = displayio.TileGrid(odg.bitmap, pixel_shader=displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565))
face = displayio.TileGrid(odg.bitmap, pixel_shader=displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565))
splash.append(face)


# Wait forever
while True:
    odg.next_frame()
    display.refresh()
    #time.sleep(0.1)


