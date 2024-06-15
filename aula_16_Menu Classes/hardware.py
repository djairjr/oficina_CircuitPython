'''
    Classe para gerenciamento de todo o hardware.
    O default é usar dois painéis de 16x16 e a biblioteca padrão.
    O sistema está preparado para identificar a placa usada
    e ajustar as pinagens de acordo.
    Ainda devo testar na Franzinho Wifi e nas Xiao ESP32 da Seeed
'''

import time, asyncio,supervisor, os
import board, random, busio, gc
import displayio
import adafruit_imageload
# Treating Joystick
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range
import adafruit_rtttl
from adafruit_ht16k33 import segments
        

class Hardware():
    ''' A class to init all hardware on my Console '''   
    
    def __init__(self, panel_16x16 = True, triggerSPI = True):
                
        # Check Board Family and machine - only Xiao and Pico
        self.board_family = os.uname().sysname
        self.board_type = os.uname().machine
        self.board_content = str(dir(board))
                
        self.triggerSPI = triggerSPI
        
        if self.board_family == 'rp2040': # Is RP2040 Hardware?
            
            if 'XIAO' in self.board_type: # Is XIAO
                self.pin_0 = board.A0
                self.pin_1 = board.A1
                self.pin_2 = board.D2
                self.pin_3 = board.D3
                self.pin_6 = board.D10
                self.pin_7 = board.D6 # Reset
            else:
                self.pin_0 = board.GP0 # Supposed to be a Pico
                self.pin_1 = board.GP1
                self.pin_2 = board.GP2
                self.pin_3 = board.GP3
                self.pin_6 = board.GP10
                self.pin_7 = board.GP6 #Reset
            
            if 'SDA' in self.board_content:
                self.pin_4 = board.SDA
            else:
                self.pin_4 = board.GP4
                
            if 'SCL' in self.board_content:
                self.pin_5 = board.SCL
            else:
                self.pin_5 = board.GP5
            
            if 'I2C' in self.board_content:
                self.i2c = board.I2C()
            else:
                self.i2c = busio.I2C(self.pin_5, self.pin_4)
            
            if 'SPI' in self.board_content:
                if self.triggerSPI:
                    self.spi = board.SPI()
                else:
                    # Raspberry pi pico
                    if not 'XIAO' in self.board_type:
                        self.spi = busio.SPI(board.GP16, MOSI=board.GP17)
                    else:
                        # This maybe not work. Is for boards that is not Xiao or Pico. Improve later
                        self.spi = busio.SPI(board.SCK, MOSI=board.MOSI)
        else:            
            if 'XIAO' in self.board_type:
                # Any XIAO ESP32 has same pin names.
                self.pin_0 = board.A0
                self.pin_1 = board.A1
                self.pin_2 = board.D2
                self.pin_3 = board.D3
                self.pin_6 = board.D10
                self.pin_7 = board.D6 # Reset
            else:
                # Supposing only Franzinho WIFI ESP32S2
                self.pin_0 = board.IO1 
                self.pin_1 = board.IO2
                self.pin_2 = board.IO3
                self.pin_3 = board.IO4
                self.pin_4 = board.IO8 	#SDA
                self.pin_5 = board.IO9 	#SCL
                self.pin_6 = board.IO18  #NEOPIXEL
                self.pin_7 = board.IO7 # Reset
            
            self.triggerSPI = False
        
        # Prepare Joystick in Analog Pins
        self.joystick_x = AnalogIn(self.pin_0)
        self.joystick_y = AnalogIn(self.pin_1)

        # Prepare Trigger Switch 
        self.trigger = DigitalInOut(self.pin_2)
        self.trigger.direction = Direction.INPUT
        self.trigger.pull = Pull.UP

        # Setup Buzzer. Can be any digital Pin
        self.buzzer = self.pin_3
        self.mute_sound = False
        
        # Score display
        self.display = segments.Seg14x4(self.i2c)

        # Prepare Neopixel Config
        self.panel_16x16 = panel_16x16
        self.panel_num = 2
        self.panel_rotation = 3
        
        if self.panel_16x16:
            self.panel_width = 16
            self.panel_height = 16
            self.pixel_width = self.panel_width
            self.pixel_height = self.panel_num * self.panel_height
        else:
            self.panel_width = 32
            self.panel_height = 8
            self.pixel_width = self.panel_width
            self.pixel_height = self.panel_num * self.panel_height
            
        self.num_pixels = self.pixel_width * self.pixel_height

        if supervisor.runtime.usb_connected:
            # Check if USB is connected to a computer and lower the brightness
            self.pixel_brightness = 0.2
        else:
            self.pixel_brightness = 0.6
            
        if self.triggerSPI:
            # Using SPI Hack to improve speed
            import neopixel_spi as neopixel
            
            self.pixels = neopixel.NeoPixel_SPI(
                self.spi,
                self.pixel_width * self.pixel_height, 
                brightness=self.pixel_brightness,
                auto_write=False,
            )
        else:
            import neopixel
            self.pixel_pin = self.pin_6
            self.pixels = neopixel.NeoPixel(
                self.pixel_pin,
                self.pixel_width * self.pixel_height, 
                brightness=self.pixel_brightness,
                auto_write=False,
            )
        
        # Neopixel as Screen
        if self.panel_16x16:
            # Import original Adafruit Library
            from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL
            self.screen= PixelFramebuffer(
                self.pixels,
                self.pixel_width,
                self.pixel_height,
                rotation=self.panel_rotation,
            )
        else:
            # Import my custom version
            from tile_framebuf import TileFramebuffer
            self.screen = TileFramebuffer(
                self.pixels,
                self.panel_width,
                self.panel_height,
                self.panel_num,
                rotation = self.panel_rotation 
            )
    
    def __str__(self):
        self.hardware_config = {
            "Pin_Joystick_X": [self.pin_0, self.joystick_x],
            "Pin_Joystick_Y": [self.pin_1, self.joystick_y],
            "Pin_Joystick_TRIG": [self.pin_2, self.trigger],
            "Pin_Buzzer": self.pin_3,
            "Sound_On": not self.mute_sound,
            "Using_SPI": self.triggerSPI,
            "Pin_Neopixel":self.pin_6,
            "Panel_16x16": self.panel_16x16,
            "Panel_Width": self.panel_width,
            "Panel_Height": self.panel_height,
            "Panel_Rotation": self.panel_rotation,
            "Panel_Num": self.panel_num,
            "Num_Pixels": self.num_pixels,
            "NeoPixel_Brightness": self.pixel_brightness,
            "Screen_Width": self.screen.width,
            "Screen_Height": self.screen.height
            }
        # Crie uma lista de strings formatadas para cada item no dicionário
        lines = [f"{key}: {value}" for key, value in sorted(self.hardware_config.items())]
        
        # Junte as linhas com quebras de linha
        string_format = "\n".join(lines)
    
        return f'Expected Hardware Configuration:\n{string_format}'
    
    def play_rttl (self, song):
        if not self.mute_sound:
            adafruit_rtttl.play (self.buzzer, song)
        
    def get_joystick(self):
        # Returns -1, 0, or 1 depending on joystick position
        x_coord = int(map_range(self.joystick_x.value, 200, 65535, -2, 2))
        y_coord = int(map_range(self.joystick_y.value, 200, 65535, -2, 2))
        return x_coord, y_coord

    def get_direction(self):
        # This function is a little bit different than usual joystick function
        x = int(map_range(self.joystick_x.value, 200, 65535, -1.5, 1.5)) # X up down
        y = int(map_range(self.joystick_y.value, 200, 65535,  -1.5, 1.5)) # Y Left Right
        if abs(x) > abs(y):
            return (x, 0)  # Horizontal Move
        else:
            return (0, y)  # Vertical Move
    
    def get_pixel_color(self, x, y):
        # Check if coordinates are within valid limits
        if (0 <= x < self.screen.height) and (0 <= y < self.screen.width):
            # Get pixel color
            rgbint = self.screen.pixel(x, y)
            return (rgbint >> 16 & 0xFF, rgbint >> 8 & 0xFF, rgbint & 0xFF)

        # Return black (0, 0, 0) if out of bounds
        return (0, 0, 0)
    
    def check_wall(self,x, y, wall_color):
        # Check Screen Limits First
        
        if x < 0 or x >= self.screen.height or y < 0 or y >= self.screen.width:
            return False
        # Then check color
        color = self.get_pixel_color(x, y)
        return color != wall_color

    def check_color(self, x, y, colorcheck):
           # Convert colorcheck to RGB tuple if it's an integer
        if isinstance(colorcheck, int):      
            colorcheck = ((colorcheck >> 16) & 0xFF, (colorcheck >> 8) & 0xFF, colorcheck & 0xFF)
        color = self.get_pixel_color(x, y)
        return color == colorcheck

    def display_bitmap(self,tile_width, tile_height, bitmap, frame_index=0):
        gc.collect()
        bitmap_width = bitmap.width
        bitmap_height = bitmap.height
        tiles_per_row = bitmap_width // tile_width
        tiles_per_column = bitmap_height // tile_height
        
        if tiles_per_row * tiles_per_column > 1:
            total_tiles = tiles_per_row * tiles_per_column
            if frame_index >= total_tiles:
                raise ValueError("Tile index out of range")
            tile_x = (frame_index % tiles_per_row) * tile_width
            tile_y = (frame_index // tiles_per_row) * tile_height
        else:
            tile_x = 0
            tile_y = 0
        
        for x in range(tile_width):
            for y in range(tile_height):

                pixel_color = bitmap[tile_x + x, tile_y + y]
                # Extrair os componentes RGB (vermelho, verde, azul) de 16 bits
                r = (pixel_color >> 11) & 0x1F  # Componente vermelho
                g = (pixel_color >> 5) & 0x3F   # Componente verde
                b = pixel_color & 0x1F          # Componente azul
                # Converter os componentes de 16 bits em 8 bits (0-255)
                r = (r * 255) // 31
                g = (g * 255) // 63
                b = (b * 255) // 31
                # Ajustar as coordenadas para a tela de 32x16 de acordo com a rotação
                # Isso não está funcionando para todas as rotações
                
                if self.screen.rotation == 0: 
                    self.screen.pixel(x, y, (r, g, b))
                elif self.screen.rotation == 1:
                    self.screen.pixel(15 - x, y, (r, g, b))
                elif self.screen.rotation == 2:
                    self.screen.pixel(y, x, (r, g, b))
                elif self.screen.rotation == 3: # Consegui resolver esse.
                    self.screen.pixel(15 - x, 31 - y, (r, g, b))
        
        del pixel_color
        gc.collect()
