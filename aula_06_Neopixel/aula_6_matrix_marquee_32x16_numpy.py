import time
import board
import neopixel_spi as neopixel
from adafruit_display_text.bitmap_label import Label
from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap
from rainbowio import colorwheel
import terminalio
# My custom version
from tile_framebuf import TileFramebuffer

#Trying to speed up stuff...
from ulab import numpy as np


spi = board.SPI()

pixel_pin = board.D10
pixel_width = 32
pixel_height = 8
num_tiles = 2
num_pixels = pixel_width * pixel_height * num_tiles

# Y offset, from the top of the display
offset = 4
# whether to mirror horizontally (test both values)
upside_down = True

pixels = neopixel.NeoPixel_SPI(
    spi,
    pixel_width * pixel_height * num_tiles, # dont forget to multiply for num_tiles
    brightness=0.5,
    auto_write=False,
)

screen = TileFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation = 0
)

font = bitmap_font.load_font("/fonts/tom-thumb.pcf", Bitmap)
label = Label(text="Hackster.io Neopixel Display     ", font=font, scale=1)
bitmap = label.bitmap

colors = [0, 0]
hue = 0

# Calcular o tamanho total do buffer de pixels
total_pixels = pixel_width * pixel_height * num_tiles

# Inicializar array numpy para representar o buffer de pixels
screen_np = np.zeros(total_pixels, dtype=np.uint16)

while True:
    for x in range(bitmap.width):
        # Use a rainbow of colors, shifting each column of pixels
        hue = hue + 7
        if hue >= 256:
            hue = hue - 256
        colors[1] = colorwheel(hue)

        # Shift pixels horizontalmente
        screen_np = np.roll(screen_np, -pixel_height, axis=0)

        # Definir os novos pixels na última coluna com base na imagem de bitmap
        for y in range(screen.height):
            bm_y = y - offset
            if 0 <= bm_y < bitmap.height:
                color_index = bitmap[x, bm_y]
            else:
                color_index = 0
            # Calcular o índice correspondente no buffer unidimensional
            pixel_index = (num_tiles - 1) * pixel_width * pixel_height + y * pixel_width + (pixel_width - 1)
            screen_np[pixel_index] = colors[color_index]

        # Atualizar o buffer do `screen` com o array numpy modificado
        screen._buffer[:] = screen_np.tolist()

        # Atualizar a tela para exibir os pixels modificados
        screen.display()

        # Aguardar um curto intervalo
        time.sleep(0.08)  # Ajuste conforme necessário