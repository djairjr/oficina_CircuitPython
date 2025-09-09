import time
import board
import neopixel_spi as neopixel
from rainbowio import colorwheel
from adafruit_pixel_framebuf import PixelFramebuffer

#Essas bibliotecas trabalham em interface com a DisplayIO
from displayio import Bitmap
from adafruit_display_text.bitmap_label import Label
from adafruit_bitmap_font import bitmap_font
import terminalio

pixel_pin = board.A0
pixel_width = 16
pixel_height = 16
num_tiles = 1
num_pixels = pixel_width * pixel_height * num_tiles

# Y offset, from the top of the display
offset = 4
# whether to mirror horizontally (test both values)
upside_down = True

pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height * num_tiles, 
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

# Como estamos usando DisplayIO, podemos usar fontes Bitmap
font = bitmap_font.load_font("/fonts/tom-thumb.pcf", Bitmap)
# Crio um Label, com texto customizado, usando a fonte e uma escala para ela
label = Label(text="Sesc Av. Paulista     ", font=font, scale=2)
# Leio o bitmap que está em Label, no caso, o texto na fonte especificada montado como Bitmap
bitmap = label.bitmap

colors = [0, 0]
hue = 0
while True:
    # Para cada pixel na largura do bitmap
    for x in range(bitmap.width):
        # Uso uma cor do arco-iris para cada coluna do bitmap
        hue = hue + 7
        if hue >= 256:
            hue = hue - 256
        colors[1] = colorwheel(hue)

        # Desloco o texto antigo para a esquerda
        for a in range(screen.width - 1):
            # Para cada linha
            for y in range(screen.height):
                screen.pixel(a, y, screen.pixel(a + 1, y))  # Desloco os pixels na horizontal

        # Desenho a próxima linha
        for y in range(screen.height):
            # Pego o pixel dentro do bitmap
            bm_y = y - offset
            # Vejo se é preto ou colorido
            if 0 <= bm_y < bitmap.height:
                color_index = bitmap[x, bm_y] # colorido
            else:
                color_index = 0 # preto
            screen.pixel(screen.width - 1, y, colors[color_index])  # Gravo o valor

        # Update the display
        screen.display()
        #time.sleep(0.04)