import time
import board
import neopixel_spi as neopixel
from bmp_reader import BMPReader

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

# Read all frames
frame_file = ['frame_1.bmp', 'frame_2.bmp', 'frame_3.bmp', 'frame_4.bmp']

def getframe (framefile):
    frame_img = BMPReader ("images/" + framefile)
    frame = frame_img.get_pixels()
    return frame_img.width, frame_img.height, frame

while True:
    screen.fill(0)
    for file in frame_file:
        frame_width, frame_height, myframe = getframe(file)
        for x in range (frame_width):
            for y in range (frame_height):
                screen.pixel (y,x,myframe[y][x])

        screen.display()       
        # time.sleep (0.05)
