"""
My Tile Grid version
"""
from micropython import const

# This change is because I am using the library outside of his correct folder.
# So I need to load the original adafruit_led_animation.Helper module.

#from .helper import PixelMap
from adafruit_led_animation.Helper import PixelMap

HORIZONTAL = const(1)
VERTICAL = const(2)

class TileGrid:
    """
    TileGrid lets you address a vertical tiled pixel panel with x and y coordinates.

    :param strip: An object that implements the Neopixel or Dotstar protocol.
    :param width: Grid width.
    :param height: Grid height.
    :param tile_num: Number of Tiles.
    
    :param orientation: Orientation of the strip pixels - HORIZONTAL (default) or VERTICAL.
    
    I still don't test this configurations.
    
    :param alternating: Whether the strip alternates direction from row to row (default True).
    :param reverse_x: Whether the strip X origin is on the right side (default False).
    :param reverse_y: Whether the strip Y origin is on the bottom (default False).
    :param tuple top: (x, y) coordinates of grid top left corner (Optional)
    :param tuple bottom: (x, y) coordinates of grid bottom right corner (Optional)

    """

    def __init__(
        self,
        strip,
        width, # of individual tile
        height, # of individual tile
        tile_num, # number of tiles
        orientation=HORIZONTAL,
        alternating=True,
        reverse_x=False,
        reverse_y=False,
        top=0,
        bottom=0,
    ):  # pylint: disable=too-many-arguments,too-many-locals
        self._pixels = strip
        self._x = []
        self.height = height
        self.width = width
        self.tile_num = tile_num
        self.generator = GridGenerator(self.width, self.height, self.tile_num)

        if self.tile_num > 1: # Check if you have more than one tile
            # And if you have, call that special function...
            mapper = self.generator.grid()
            for m in mapper:
                self._x.append(
                    PixelMap(
                        strip,
                        m,
                        individual_pixels=True,
                    )
                )
        self.n = len(self._x)

    def __repr__(self):
        return "[" + ", ".join([str(self[x]) for x in range(self.n)]) + "]"

    def __setitem__(self, index, val):
        if isinstance(index, slice):
            raise NotImplementedError("PixelGrid does not support slices")

        if isinstance(index, tuple):
            self._x[index[0]][index[1]] = val
        else:
            raise ValueError("PixelGrid assignment needs a sub-index or x,y coordinate")

        if self._pixels.auto_write:
            self.show()

    def __getitem__(self, index):
        if isinstance(index, slice):
            raise NotImplementedError("PixelGrid does not support slices")
        if index < 0:
            index += len(self)
        if index >= self.n or index < 0:
            raise IndexError("x is out of range")
        return self._x[index]

    def __len__(self):
        return self.n

    @property
    def brightness(self):
        """
        brightness from the underlying strip.
        """
        return self._pixels.brightness

    @brightness.setter
    def brightness(self, brightness):
        # pylint: disable=attribute-defined-outside-init
        self._pixels.brightness = min(max(brightness, 0.0), 1.0)

    def fill(self, color):
        """
        Fill the PixelGrid with the specified color.

        :param color: Color to use.
        """
        for strip in self._x:
            strip.fill(color)

    def show(self):
        """
        Shows the pixels on the underlying strip.
        """
        self._pixels.show()
    
    def get_pixel(self, x,y):
        """
        Return Pixel Position in Led Stripe
        """
        return self.generator.get_value (x,y)
    
    def get_color(self, x,y):
        """
        Return Pixel Color
        """
        return self._pixels[self.get_pixel (x,y)]

    @property
    def auto_write(self):
        """
        auto_write from the underlying strip.
        """
        return self._pixels.auto_write

    @auto_write.setter
    def auto_write(self, value):
        self._pixels.auto_write = value
    
def reverse_x_mapper(width, mapper):
    """
    Returns a coordinate mapper function for grids with reversed X coordinates.

    :param width: width of strip
    :param mapper: grid mapper to wrap
    :return: mapper(x, y)
    """
    max_x = width - 1

    def x_mapper(x, y):
        return mapper(max_x - x, y)

    return x_mapper


def reverse_y_mapper(height, mapper):
    """
    Returns a coordinate mapper function for grids with reversed Y coordinates.

    :param height: width of strip
    :param mapper: grid mapper to wrap
    :return: mapper(x, y)
    """
    max_y = height - 1

    def y_mapper(x, y):
        return mapper(x, max_y - y)

    return y_mapper

class GridGenerator:
    """ Gera o Grid sem computar a rotação """
    """ Checar Adafruit_Framebuf para ver como atualizar coordenadas dependendo da rotação """
    
    def __init__(self, width, height, tile_num):
        self.width = width
        self.height = height
        self.tile_num = tile_num

    def single_tile(self):
        # Gerador para um único tile
        for i in range(self.width * self.height):
            group_index = i // self.height
            ascending = (group_index % 2) == 0
            number_within_group = i % self.height

            if number_within_group == 0:
                temp = []

            if ascending:
                number = group_index * self.height + number_within_group
            else:
                number = (group_index + 1) * self.height - 1 - number_within_group

            temp.append(number)

            if number_within_group == self.height - 1:
                yield tuple(temp)

    def multi_tile(self, original_matrix):
        multi_temp = []
        factor = self.tile_num - 1

        if factor == 0:
            multi_temp = original_matrix
        else:
            for tup in original_matrix:
                modified_tuple = tup[:self.height]

                for n in range(factor):
                    modified_tuple += tuple(num + (factor * (self.width * self.height)) for num in tup[:self.height])
                multi_temp.append(modified_tuple)

        return multi_temp

    def grid(self):
        # Obter a matriz de tiles
        position = self.multi_tile(list(self.single_tile()))
        return position

    def get_value(self, x, y):
        # Obter o valor na posição (x, y) no grid
        pixel_value = self.grid()
        return pixel_value[x][y]
