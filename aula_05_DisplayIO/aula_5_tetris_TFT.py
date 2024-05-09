import board
import random
import displayio
import time
import keypad
import digitalio
import terminalio


class Brick:
    BRICKS = b'ftqr\xf0'
    ROTATIONS = [
        (1, 0, 0, 1, -1, -1),
        (0, 1, -1, 0, -1, 0),
        (-1, 0, 0, -1, -2, 0),
        (0, -1, 1, 0, -2, -1),
    ]

    def __init__(self, kind):
        self.x = 1
        self.y = 2
        self.color = kind % 5 + 1
        self.rotation = 0
        self.kind = kind

    def draw(self, image, color=None):
        if color is None:
            color = self.color
        data = self.BRICKS[self.kind]
        rot = self.ROTATIONS[self.rotation]
        mask = 0x01
        for y in range(2):
            y += rot[5]
            for x in range(4):
                x += rot[4]
                if data & mask:
                    try:
                        image[self.x + x * rot[0] + y * rot[1],
                              self.y + x * rot[2] + y * rot[3]] = color
                    except IndexError:
                        pass
                mask <<= 1

    def hit(self, image, dx=0, dy=0, dr=0):
        data = self.BRICKS[self.kind]
        rot = self.ROTATIONS[(self.rotation + dr) % 4]
        mask = 0x01
        for y in range(2):
            y += rot[5]
            for x in range(4):
                x += rot[4]
                if data & mask:
                    try:
                        if image[self.x + dx + x * rot[0] + y * rot[1],
                                 self.y + dy + x * rot[2] + y * rot[3]]:
                            return True
                    except IndexError:
                        return True
                mask <<= 1
        return False


palette = displayio.Palette(6)
palette[0] = 0x111111
palette[1] = 0xaa0099
palette[2] = 0x22aa00
palette[3] = 0xee00bb
palette[4] = 0xbbee00
palette[5] = 0xbb00ee
text_palette = displayio.Palette(2)
text_palette[0] = 0x111111
text_palette[1] = 0xffeedd
w, h = terminalio.FONT.get_bounding_box()
text_grid = displayio.TileGrid(terminalio.FONT.bitmap,
    tile_width=w, tile_height=h, pixel_shader=text_palette, width=8, height=1)
text_grid.x = 96
text_grid.y = 48
text = terminalio.Terminal(text_grid, terminalio.FONT)
screen = displayio.Bitmap(10, 20, 6)
preview = displayio.Bitmap(4, 4, 6)
bricks = displayio.Group(scale=8)
bricks.append(displayio.TileGrid(screen, pixel_shader=palette, x=0, y=-4))
bricks.append(displayio.TileGrid(preview, pixel_shader=palette, x=12, y=0))
root = displayio.Group()
root.append(bricks)
root.append(text_grid)
root[0] = displayio.Group()
root[0] = bricks
board.DISPLAY.show(root)
buttons = keypad.Keys((
    board.BUTTON_O,
    board.BUTTON_X,
    board.BUTTON_Z,
    board.BUTTON_DOWN,
    board.BUTTON_LEFT,
    board.BUTTON_RIGHT,
    board.BUTTON_UP,
), value_when_pressed=False)

brick = None
score = 0
next_brick = Brick(random.randint(0, 4))
tick = time.monotonic()
while True:
    if brick is None:
        text.write("\r\n%08d" % score)
        next_brick.draw(preview, 0)
        brick = next_brick
        brick.x = screen.width // 2
        next_brick = Brick(random.randint(0, 4))
        next_brick.draw(preview)
        if brick.hit(screen, 0, 0):
            break
    tick += 0.5
    pressed = 0
    event = keypad.Event()
    while True:
        board.DISPLAY.refresh()
        time.sleep(0.075)
        if tick <= time.monotonic():
            break
        brick.draw(screen, 0)
        while buttons.events:
            buttons.events.get_into(event)
            if event.pressed:
                pressed |= 1 << event.key_number
            else:
                pressed &= ~(1 << event.key_number)
        if pressed & 0x08 and not brick.hit(screen, 0, 1):
            brick.y += 1
        if pressed & 0x20 and not brick.hit(screen, 1, 0):
            brick.x += 1
        if pressed & 0x10 and not brick.hit(screen, -1, 0):
            brick.x -= 1
        if pressed & 0x01 and not brick.hit(screen, 0, 0, 1) and not debounce:
            brick.rotation = (brick.rotation + 1) % 4
            debounce = True
        if pressed & 0x02 and not brick.hit(screen, 0, 0, -1) and not debounce:
            brick.rotation = (brick.rotation - 1) % 4
            debounce = True
        if not pressed:
            debounce = False
        brick.draw(screen)
    brick.draw(screen, 0)
    if brick.hit(screen, 0, 1):
        brick.draw(screen)
        combo = 0
        for y in range(screen.height):
            for x in range(screen.width):
                if not screen[x, y]:
                    break
            else:
                combo += 1
                score += combo
                for yy in range(y, 0, -1):
                    for x in range(screen.width):
                        screen[x, yy] = screen[x, yy - 1]
        brick = None
    else:
        brick.y += 1
        brick.draw(screen)