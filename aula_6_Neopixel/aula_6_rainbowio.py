# CircuitPython 7 with or without rainbowio module
import time, board, neopixel
try:
    from rainbowio import colorwheel
except:
    def colorwheel(pos):
        if pos < 0 or pos > 255:  return (0, 0, 0)
        if pos < 85: return (255 - pos * 3, pos * 3, 0)
        if pos < 170: pos -= 85; return (0, 255 - pos * 3, pos * 3)
        pos -= 170; return (pos * 3, 0, 255 - pos * 3)

led = neopixel.NeoPixel(board.GP19, 5, brightness=0.3)
while True:
    led.fill( colorwheel((time.monotonic()*50)%255) )
    time.sleep(0.05)