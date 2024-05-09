"""
Exemplo com a adafruit_led_animation
Confira mais coisas legais aqui:https://learn.adafruit.com/circuitpython-led-animations?view=all
"""
import board
import neopixel
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import PURPLE, AMBER, JADE

pixel_pin = board.D10
pixel_num = 6

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)

blink = Blink(pixels, speed=0.5, color=JADE)
comet = Comet(pixels, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
chase = Chase(pixels, speed=0.1, size=3, spacing=6, color=AMBER)

animations = AnimationSequence(blink, comet, chase, advance_interval=3, auto_clear=True)

while True:
    animations.animate()