import time
import board
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer

# A biblioteca bmp_reader é customizada
# ela lê um arquivo bitmap e faz as conversões necessárias.
from bmp_reader import BMPReader

# Lê o Bitmap como arquivo
friend_img = BMPReader ("images\Mario.bmp")

# Pega os pixels do Bitmap e grava no objeto friend
friend = friend_img.get_pixels()

pixel_pin = board.A0
pixel_width = 16
pixel_height = 16
num_tiles = 2
num_pixels = pixel_width * pixel_height * num_tiles

pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height * num_tiles, # dont forget to multiply for num_tiles
    brightness=0.2,
    auto_write=False,
)

screen = PixelFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation = 0
)

# Percorre o objeto friend (colunas e linhas)
for x in range (friend_img.width):
    for y in range (friend_img.height):
        # atribui a cor ao pixel na tela.
        screen.pixel (y,x,friend[y][x])


screen.display()
