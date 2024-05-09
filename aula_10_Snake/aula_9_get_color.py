"""
Um dos modos de checar colisão é detectar a cor do pixel que vai ser sobreposto.
Outro modo, é checar se os dois objetos ocupam as mesmas coordenadas x e y.
A vantagem de usar a cor, é não precisar criar um objeto para cenário, por exemplo.
"""
import time
import board
import neopixel_spi as neopixel
import displayio
import adafruit_imageload

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
    brightness=0.5,
    auto_write=False,
)

screen = TileFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation = 3
)

def get_color(x, y):
    # Essa função vai retornar uma tupla RGB
    # com a cor do Pixel na posição x,y
    # Ela faz os ajustes de coordenada, dependendo
    # da rotação na tela.
    
    if screen.rotation == 1:
        x, y = y, x
        x = screen._width - x - 1
    elif screen.rotation == 2:
        x = screen._width - x - 1
        y = screen._height * screen._tile_num - y - 1
    elif screen.rotation == 3:
        x, y = y, x
        y = screen._height * screen._tile_num - y - 1

    # Verifica se as coordenadas ajustadas estão dentro dos limites válidos
    if (0 <= x < screen._width) and (0 <= y < screen._height * screen._tile_num):
        
        # Obtém o pixel ajustado da tela
        rgbint = screen.format.get_pixel(screen, x, y)
        return (rgbint // 256 // 256 % 256, rgbint // 256 % 256, rgbint % 256)

    # Retorna preto (0, 0, 0) se estiver fora dos limites
    return (0, 0, 0)

# Essa sequência coloca quatro pontos de cores diferentes
# nos limites da tela e testa a exibição das cores para ver
# se tudo está calibrado.
# Na rotação 0, assume-se width = 32 e height = 16

for n in range (4):
    screen.rotation = n
    screen.fill (0x00000)
    screen.pixel (0,0,0xff0000)
    screen.pixel (31,0,0xffff00)
    screen.pixel (31,15,0xff00ff)
    screen.pixel (0,15,0x0000ff)
    screen.display()

    print ('0,0   Rotation :', n, get_color(0,0))
    print ('31,0  Rotation :', n, get_color(31,0))
    print ('31,15 Rotation :', n, get_color(31,15))
    print ('0,15  Rotation :', n, get_color(0,15))
    print()
    time.sleep(1)