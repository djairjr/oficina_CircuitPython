""" 
Ligando nosso pirulito NeoPixel 
Mas antes...
circup install rainbowio, neopixel, neopixel_spi, adafruit_pixelframebuf

"""
import time
import board
from rainbowio import colorwheel
import neopixel

# pode ser qualquer pino, mas eu estou ligando nesse por uma razão...
pixel_pin = board.GP19 
num_pixels = 6

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

pixels[0] = 0xff0000
pixels[1] = 0x00ff00
pixels[2] = 0x0000ff
pixels[3] = 0xffff00
pixels[4] = 0x00ffff
pixels[5] = 0xff00ff
pixels.show()

