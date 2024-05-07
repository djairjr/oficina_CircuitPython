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
    brightness=0.2,
    auto_write=False,
)

screen = TileFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    num_tiles,
    rotation = 1
)

# Load the sprite sheet (bitmap)
sprite_sheet, palette = adafruit_imageload.load(
    # Image with 64 pixels width and 32 pixels height. Conteins four frames 16x32
    "images/all_frames.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette,
)

# make the color at 0 index transparent.
#palette.make_transparent(0)

# Create the sprite TileGrid
sprite = displayio.TileGrid(
    sprite_sheet,
    pixel_shader=palette,
    width=16,
    height=1,
    tile_width=16,
    tile_height=32,
    default_tile=0,
)

# Lógica para exibir os frames em sequência
frame_index = 0  # índice do frame atual
frame_delay = 0.02  # intervalo de tempo entre os frames (em segundos)
last_frame_time = time.monotonic()

while True:
    # Limpar a tela
    screen.fill(0)

    # Calcular o índice do tile atual dentro do bitmap
    tile_x = frame_index % sprite.width
    tile_y = frame_index // sprite.width

    # Exibir o tile atual na tela Neopixel
    for x in range(sprite.tile_width):
        for y in range(sprite.tile_height):
            pixel_color = sprite_sheet[tile_x * sprite.tile_width + x, tile_y * sprite.tile_height + y]
            # Extrair os componentes RGB (vermelho, verde, azul) de 16 bits
            r = (pixel_color >> 11) & 0x1F  # Componente vermelho
            g = (pixel_color >> 5) & 0x3F    # Componente verde
            b = pixel_color & 0x1F           # Componente azul
            # Converter os componentes de 16 bits em 8 bits (0-255)
            r = (r * 255) // 31
            g = (g * 255) // 63
            b = (b * 255) // 31
            # Exibir o pixel na tela Neopixel (formato RGB de 24 bits)
            neopixel_color = (r, g, b)
            screen.pixel(x, y, neopixel_color)
    # Atualizar a exibição
    screen.display()

    # Verifica se é hora de exibir o próximo frame
    current_time = time.monotonic()
    if current_time - last_frame_time >= frame_delay:
        # Atualizar o índice do frame para o próximo
        frame_index = (frame_index + 1) % (sprite.width * sprite.height)

        # Atualizar o tempo do último frame exibido
        last_frame_time = current_time
