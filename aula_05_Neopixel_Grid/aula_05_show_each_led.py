import board
import time
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer

pixel_pin = board.A0
pixel_width = 16
pixel_height = 16
num_tiles = 1
num_pixels = pixel_width * pixel_height * num_tiles

pixels = neopixel.NeoPixel(
    pixel_pin,
    num_pixels, 
    brightness=0.1,
    auto_write=False,
)

# Cria um Grid a partir da Neopixel e um Framebuffer também
screen = PixelFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation = 0, #3
    reverse_x=True,
)

# E ai temos vários métodos que servem para desenhar nessa tela
screen.fill(0)
print (dir (screen))
# Copiar o Arquivo font5x8.bin para a raiz
# Ou tem esse erro: OSError: [Errno 2] Este arquivo/diretório não existe: font5x8.bin
screen.text ("HI", 1, 1, 0xFF0000)
#screen.rect (2,2, 5,5, 0xFF0000) # A cor é passada em Hexadecimal 0xRRGGBB
screen.display()