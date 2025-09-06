import time, math, random
import board, busio
import displayio
import adafruit_imageload
from adafruit_st7789 import ST7789
from fourwire import FourWire

tft_lite = board.GP7
tft_dc = board.GP6
tft_cs = board.GP5
sck=board.GP2
mosi=board.GP3

spi = busio.SPI(clock=sck, MOSI=mosi)

# load our eye and iris bitmaps
dw, dh = 240,240  # display dimensions
eyeball_bitmap, eyeball_pal = adafruit_imageload.load("images/eye0_ball2.bmp")
iris_bitmap, iris_pal = adafruit_imageload.load("images/eye0_iris0.bmp")
iris_pal.make_transparent(0)

# compute or' declare some useful info about the eyes
iris_w, iris_h = iris_bitmap.width, iris_bitmap.height  # iris is normally 110x110
iris_cx, iris_cy = dw//2 - iris_w//2, dh//2 - iris_h//2
r = 25  # allowable deviation from center for iris

# class to help us track eye info (not needed for this use exactly, but I find it interesting)
class Eye:
    def __init__(self, spi, dc, cs, rot=0, eye_speed=0.3, twitch=2):
        display_bus = FourWire(spi, command=dc, chip_select=cs, reset=board.GP4)
        display = ST7789(display_bus, width=dw, height=dh, rotation=rot)
        main = displayio.Group()
        display.root_group = main
        self.display = display
        self.eyeball = displayio.TileGrid(eyeball_bitmap, pixel_shader=eyeball_pal)
        self.iris = displayio.TileGrid(iris_bitmap, pixel_shader=iris_pal, x=iris_cx,y=iris_cy)
        main.append(self.eyeball)
        main.append(self.iris)
        self.x, self.y = iris_cx, iris_cy
        self.tx, self.ty = self.x, self.y
        self.next_time = time.monotonic()
        self.eye_speed = eye_speed
        self.twitch = twitch

    def update(self):
        self.x = self.x * (1-self.eye_speed) + self.tx * self.eye_speed # "easing"
        self.y = self.y * (1-self.eye_speed) + self.ty * self.eye_speed
        self.iris.x = int( self.x )
        self.iris.y = int( self.y )
        if time.monotonic() > self.next_time:
            t = random.uniform(0.25,self.twitch)
            self.next_time = time.monotonic() + t
            self.tx = iris_cx + random.uniform(-r,r)
            self.ty = iris_cy + random.uniform(-r,r) 
        self.display.refresh()

# a list of all the eyes, in this case, only one
the_eyes = [
    Eye( spi, tft_dc, tft_cs,  rot=0),
]

while True:
    for eye in the_eyes:
        eye.update()