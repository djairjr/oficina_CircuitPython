import time
import board
import neopixel
from adafruit_display_text.bitmap_label import Label
from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap
from rainbowio import colorwheel

pixel_pin = board.GP19
width = 64
height = 8
num_pixels = width * height
# Y offset, from the top of the display
offset = 2
# whether to mirror horizontally (test both values)
upside_down = True

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False)
pixels.fill(0)
pixels.show()

import terminalio
font = bitmap_font.load_font("/fonts/tom-thumb.pcf", Bitmap)
# font = terminalio.FONT
label = Label(text="Matrix Neopixel 32x8 - Hello World Example     ", font=font, scale=2)
bitmap = label.bitmap

def coords(x,y):
    if bool(x % 2) == upside_down:
        y = height - y - 1
    return x * height + y

def pixel_test():
    # quick test for pixel order, should fill from top to bottom
    for y in range(height):
        for x in range(width):
            pixels[coords(x,y)] = 0xFF0080
            pixels.show()
            # time.sleep(0.05)

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
        for a in range(0,width-1):
            pixels[height*a:height*(a+1)] = list(reversed(pixels[height*(a+1):height*(a+2)]))
        # pixels[0:num_pixels-height] = pixels[height:num_pixels]

        # Draw in the next line of text
        for y in range(height):
            # select the pixel inside the bitmap
            bm_y = y - offset
            # Select black or color depending on the bitmap pixel
            if bm_y >= 0 and bm_y < bitmap.height:
                color_index = bitmap[x,bm_y]
            else:
                color_index = 0
            pos = coords(width-1, y)
            pixels[pos] = colors[color_index]

        # update
        pixels.show()
        time.sleep(.08)