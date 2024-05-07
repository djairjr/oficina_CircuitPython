"""
My Tile_framebuf
"""

# imports
try:
    from circuitpython_typing.led import FillBasedColorUnion
except ImportError:
    pass

import my_framebuf # My changed library

# This is the original import. 
# from adafruit_led_animation.grid import PixelGrid

# But i am using my custom tilegrid module
from tilegrid import TileGrid
from micropython import const

HORIZONTAL: int = const(1)
VERTICAL: int = const(2)


# pylint: disable=too-many-function-args
class TileFramebuffer(my_framebuf.FrameBuffer):
    """
    NeoPixel and Dotstar FrameBuffer for easy drawing and text on a
    tile grid of either kind of pixel

    :param strip: An object that implements the Neopixel or Dotstar protocol.
    :param width: Framebuffer width.
    :param height: Framebuffer height.
    :param tile_num: Number of identical tiles
    
    :param int rotation: A value of 0-3 representing the rotation of the framebuffer (default 0)

    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        pixels: FillBasedColorUnion,
        width: int,
        height: int,
        tile_num: int,
        
        # Cant use this orientation stuff yet
        orientation: int = HORIZONTAL,
        alternating: bool = True,
        reverse_x: bool = False,
        reverse_y: bool = False,
        top: int = 0,
        bottom: int = 0,
        rotation: int = 0,
    ) -> None:
        self._width = width
        self._height = height
        self._tile_num = tile_num 
        
        # My Custom Class
        self._grid = TileGrid(
            pixels,
            width,
            height,
            tile_num, 
        )
        
        # Need to multiply buffer for tile_num
        self._buffer = bytearray(width * height * tile_num * 3)
        self._double_buffer = bytearray(width * height * tile_num *  3)
        super().__init__(
            self._buffer, width, height * tile_num, buf_format=my_framebuf.RGB888
        )
        self.rotation = rotation

    def blit(self) -> None:
        """blit is not yet implemented"""
        raise NotImplementedError()

    def display(self) -> None:
        """Copy the raw buffer changes to the grid and show"""
        
        # don't forget to multiply for tile_num
        for _y in range(self._height * self._tile_num):
            for _x in range(self._width):
                index = (_y * self.stride + _x) * 3
                if (
                    self._buffer[index : index + 3]
                    != self._double_buffer[index : index + 3]
                ):
                    self._grid[(_x, _y)] = tuple(self._buffer[index : index + 3])
                    self._double_buffer[index : index + 3] = self._buffer[
                        index : index + 3
                    ]
        self._grid.show()

