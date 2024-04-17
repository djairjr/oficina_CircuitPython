"""
Exercício para Exibir as Imagens no Display SSD1306

Bibliotecas necessárias: 
- adafruit_displayio_ssd1306.mpy
- adafruit_display_text folder
- adafruit_display_shapes folder

Usando a XIAO Expansion board
I2C SDA = A4
I2C SCL = A5
"""

import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.circle import Circle
import adafruit_displayio_ssd1306
import time
import random

displayio.release_displays()

print(adafruit_displayio_ssd1306.__name__,
      adafruit_displayio_ssd1306.__version__)

# Use for I2C
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

DISP_WIDTH = 128
DISP_HEIGHT = 64
BORDER = 5

display = adafruit_displayio_ssd1306.SSD1306(
    display_bus,
    width=DISP_WIDTH,
    height=DISP_HEIGHT)

# Make the display context
splash = displayio.Group()
display.root_group = splash

bg_bitmap = displayio.Bitmap(DISP_WIDTH, DISP_HEIGHT, 2)
bg_palette = displayio.Palette(2)
bg_palette[0] = 0x000000  # Black
bg_palette[1] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(
    bg_bitmap,
    pixel_shader=bg_palette,
    x=0, y=0)

#===========================================
#prepare Label of title
title = " Sesc "
group_title = displayio.Group(scale=1)

label_title = label.Label(terminalio.FONT,
                        text=title,
                        color=0xFFFFFF)
label_title.anchor_point = (0.0, 0.0)
label_title.anchored_position = (0, 0)
label_title_width = label_title.bounding_box[2]
label_title_height = label_title.bounding_box[3]
shape_title_r = label_title_width//2

shape_title = Circle(x0=label_title_width//2,
                     y0=label_title_height//2,
                     r=shape_title_r,
                     fill=0x000000,
                     outline=0xFFFFFF, stroke=1)

group_title.x = (DISP_WIDTH-label_title_width)//2
group_title.y = (DISP_HEIGHT-label_title_height)//2
group_title.append(shape_title)
group_title.append(label_title)
#===========================================
splash.append(bg_sprite)
splash.append(group_title)
#===========================================
def background_random():
    global bg_bitmap
    x = random.randrange(DISP_WIDTH)
    y = random.randrange(DISP_HEIGHT)
    c = bg_bitmap[x, y]
    c = not c
    bg_bitmap[x, y] = c


aniXMove = +1
aniYMove = +1
aniXLim = DISP_WIDTH - 1 - shape_title.width

aniYdelta = (DISP_HEIGHT-1)//2 - shape_title_r
aniYLowLim = group_title.y - aniYdelta
aniYUppLim = group_title.y + aniYdelta

def title_animation():
    global group_title
    global aniXMove
    global aniYMove
    global aniXLim
    global aniYLim
    
    #Move Title group
    x = group_title.x + aniXMove
    group_title.x = x
    if aniXMove > 0:
        if x >= aniXLim:
            aniXMove = -1
    else:
        if x <= 0:
            aniXMove = +1
            
    y = group_title.y + aniYMove
    group_title.y = y
    if aniYMove > 0:
        if y >= aniYUppLim:
            aniYMove = -1
    else:
        if y <= aniYLowLim:
            aniYMove = +1


BG_CHANGE_DURATION = 0.05
bg_change_nx = time.monotonic() + BG_CHANGE_DURATION
TITLE_CHANGE_DURATION = 0.25
title_change_nx = time.monotonic() + TITLE_CHANGE_DURATION
while True:
    
    now = time.monotonic()
    
    if now >= bg_change_nx:
        bg_change_nx = now+BG_CHANGE_DURATION
        background_random()
    
    if now >= title_change_nx:
        title_change_nx = now+TITLE_CHANGE_DURATION
        title_animation()
    
    time.sleep(0.01)