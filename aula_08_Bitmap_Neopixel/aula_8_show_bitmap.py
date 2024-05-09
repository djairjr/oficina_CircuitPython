import time
import board
import neopixel_spi as neopixel
from bmp_reader import BMPReader

friend_img = BMPReader ("images\Mario.bmp") # My BMP File
friend = friend_img.get_pixels()

# My custom version
from tile_framebuf import TileFramebuffer
spi = board.SPI()

pixel_pin = board.D10
pixel_width = 32
pixel_height = 8
num_tiles = 2
num_pixels = pixel_width * pixel_height * num_tiles

pixels = neopixel.NeoPixel_SPI(
    spi,
    pixel_width * pixel_height * num_tiles, # dont forget to multiply for num_tiles
    brightness=0.2,
    auto_write=False,
)

screen = TileFramebuffer(
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
