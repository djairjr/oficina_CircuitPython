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
    rotation = 2
)


font = bitmap_font.load_font("/fonts/tom-thumb.pcf", Bitmap)
label = Label(text="Seeed Xiao with Neopixel Matrix     ", font=font, scale=2)
bitmap = label.bitmap

colors = [0, 0]
hue = 0
while True:
    for x in range(bitmap.width):
        # Use a rainbow of colors, shifting each column of pixels
        hue = hue + 7
        if hue >= 256:
            hue = hue - 256
        colors[1] = colorwheel(hue)

        # Scoot the old text left by 1 pixel
        for a in range(screen.width - 1):
            for y in range(screen.height):
                screen.pixel(a, y, screen.pixel(a + 1, y))  # Shift pixels horizontally

        # Draw in the next line of text
        for y in range(screen.height):
            # Select the pixel inside the bitmap
            bm_y = y - offset
            # Select black or color depending on the bitmap pixel
            if 0 <= bm_y < bitmap.height:
                color_index = bitmap[x, bm_y]
            else:
                color_index = 0
            screen.pixel(screen.width - 1, y, colors[color_index])  # Set new pixel

        # Update the display
        screen.display()
        #time.sleep(0.04)