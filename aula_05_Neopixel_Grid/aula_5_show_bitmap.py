import time
import board
import neopixel_spi as neopixel
from bmp_reader import BMPReader
from adafruit_pixel_framebuf import PixelFramebuffer

friend_img = BMPReader ("images\Mario.bmp") # My BMP File
friend = friend_img.get_pixels()

pixel_pin = board.A0
pixel_width = 16
pixel_height = 16
num_tiles = 1
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

for x in range (friend_img.width):
    for y in range (friend_img.height):
        screen.pixel (y,x,friend[y][x])


screen.display()
