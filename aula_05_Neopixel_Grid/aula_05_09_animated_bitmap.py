# Usando BMPReader
import time
import board
import neopixel_spi as neopixel
from bmp_reader import BMPReader
from adafruit_pixel_framebuf import PixelFramebuffer

pixel_pin = board.A0
pixel_width = 16
pixel_height = 16
num_tiles = 2
num_pixels = pixel_width * pixel_height * num_tiles

pixels = neopixel.NeoPixel(
    spi,
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

# Cada um dos frames é um arquivo 16x32 separado
frame_file = ['frame_1.bmp', 'frame_2.bmp', 'frame_3.bmp', 'frame_4.bmp']

# Criei uma rotina para ler cada um dos frames e me retornar
# largura, altura e a matriz de cores
def getframe (framefile):
    frame_img = BMPReader ("images/" + framefile)
    frame = frame_img.get_pixels()
    return frame_img.width, frame_img.height, frame

while True:
    screen.fill(0) # limpo a tela
    # Para cada arquivo da lista de frames
    for file in frame_file:
        # Recupero os valores usando minha função getframe
        frame_width, frame_height, myframe = getframe(file)
        for x in range (frame_width):
            for y in range (frame_height):
                #Atribuo o valor de cor na coordenada correta
                screen.pixel (y,x,myframe[y][x])

        screen.display() # Mostro a imagem     
        # time.sleep (0.05)
