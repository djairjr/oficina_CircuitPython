import board
import time
import neopixel

pixel_pin = board.A0
pixel_width = 16
pixel_height = 16
num_tiles = 1 # se você ligar mais que um painel, altere aqui
num_pixels = pixel_width * pixel_height * num_tiles

print (num_pixels) # Mostra quantos pixels nós temos

pixels = neopixel.NeoPixel(
    pixel_pin,
    num_pixels, 
    brightness=0.1, # matenha o brilho baixo se a fonte for menor que 1A
    auto_write=False,
)

pixels.fill((0,0,0))
pixels.show()

while True:
    for idx in range(num_pixels):
        pixels[idx] = (255,0,0)
        pixels.show()
        time.sleep(0.2)
        pixels.fill((0,0,0))
        pixels.show()
        time.sleep(0.05)