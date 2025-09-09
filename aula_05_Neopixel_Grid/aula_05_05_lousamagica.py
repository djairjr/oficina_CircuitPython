import board, time
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range
import neopixel
from rainbowio import colorwheel

import adafruit_rtttl
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

pixel_pin = board.A0
pixel_width = 16
pixel_height = 16
num_tiles = 2

joystick_x = AnalogIn(board.A1)
joystick_y = AnalogIn(board.A2)

trigger = DigitalInOut (board.D6)
trigger.direction = Direction.INPUT
trigger.pull = Pull.UP

buzzer = board.D7

pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height * num_tiles, # dont forget to multiply for num_tiles
    brightness=0.1,
    auto_write=False,
)

screen = PixelFramebuffer(
    pixels,
    pixel_width * num_tiles,
    pixel_height,
    orientation = VERTICAL,
    rotation = 0
)


def moveSound():
    adafruit_rtttl.play (buzzer, "move:d=4,o=5,b=880:8c6")

def deleteSound():
    adafruit_rtttl.play (buzzer, "delete:d=4,o=5,b=330:8c6,8d6")

def get_joystick():
    # Returns -1 0 or 1 depending on joystick position
    x_coord = int (map_range (joystick_x.value, 200, 65535, 2 , -2))
    y_coord = int (map_range (joystick_y.value, 200, 65535, 2 , -2))
    return x_coord, y_coord

# Center Screen
old_x = screen.width //2
old_y = screen.height // 2
x_pos, y_pos = old_x, old_y


while True:
    if (not trigger.value):
        screen.fill (0x000000)
        deleteSound()
    else:
        x,y = get_joystick()
        x_pos = old_x + x
        y_pos = old_y + y
        if x_pos != old_x or y_pos != old_y:
            moveSound()
        screen.line (old_x, old_y, x_pos, y_pos, colorwheel((time.monotonic()*50)%255))
        screen.display()
        time.sleep(0.1)
        old_x = x_pos
        old_y = y_pos
        
        """ Tratando os limites da tela """
        if (old_x < 0):
            old_x = 0
        if (old_x > screen.width - 1):
            old_x = screen.width - 1
        if (old_y < 0):
            old_y = 0
        if (old_y > screen.height - 1):
            old_y = screen.height - 1
    
