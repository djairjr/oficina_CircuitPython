import board, busio, time, os
import displayio
import terminalio
import gifio
from fourwire import FourWire

from adafruit_display_text import label
from adafruit_st7789 import ST7789

tft_lite = board.GP7
tft_dc = board.GP6
tft_cs = board.GP5
sck=board.GP2
mosi=board.GP3

spi = busio.SPI(clock=sck, MOSI=mosi)
while not spi.try_lock():
    pass
spi.configure(baudrate=24000000) # Configure SPI for 24MHz
spi.unlock()

display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.GP4)
display = ST7789(
    display_bus,
    width=240,
    height=240,
    rowstart=80,
    rotation=0,
    backlight_pin=tft_lite,
)
# Make the display context
splash = displayio.Group()
display.root_group = splash

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




