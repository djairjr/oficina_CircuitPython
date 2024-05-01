"""
Eu estou trabalhando ainda nesse código. 
O original está aqui: https://github.com/stuartm2/CircuitPython_BMP_Reader

Foi feito para pegar um arquivo BMP de 8x8 e colocar numa matriz de Neopixel 8x8
Eu estou dando um jeito de ele interpretar a altura e largura do arquivo e converter
no array Neopixel automaticamente.

Talvez nem seja preciso, se eu entender direito a biblioteca Adafruit_Imageload...

"""

class BMPReader(object):
    def __init__(self, filename):
        self._filename = filename
        self._read_img_data()

    def get_pixels(self):
        """
        Retorna uma matriz bidimensional dos valores RGB de cada pixel na imagem,
        organizada por linhas e colunas a partir do canto superior esquerdo.
        """
        pixel_grid = []
        pixel_data = list(self._pixel_data)  # Trabalhando em uma cópia dos dados

        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                b = pixel_data.pop(0)
                g = pixel_data.pop(0)
                r = pixel_data.pop(0)
                row.append((r, g, b))
            pixel_grid.append(row)
        return pixel_grid

    def _read_img_data(self):
        with open(self._filename, 'rb') as f:
            img_bytes = list(f.read())

        # Verifica se é um arquivo BMP válido
        if img_bytes[0:2] != [66, 77]:
            raise ValueError("Não é um arquivo BMP válido")

        # Verifica se a compressão é suportada (deve ser 0 para sem compressão)
        if img_bytes[30:34] != [0, 0, 0, 0]:
            raise ValueError("Compressão não suportada")

        # Verifica se a profundidade de cor é 24 bits
        if img_bytes[28:30] != [24, 0]:
            raise ValueError("Profundidade de cor não suportada (deve ser 24 bits)")

        # Determina o início e o fim dos dados de pixel
        start_pos = int.from_bytes(img_bytes[10:14], byteorder='little')
        end_pos = start_pos + int.from_bytes(img_bytes[34:38], byteorder='little')

        # Lê a largura e altura da imagem
        self.width = int.from_bytes(img_bytes[18:22], byteorder='little')
        self.height = int.from_bytes(img_bytes[22:26], byteorder='little')

        # Extrai os dados de pixel
        self._pixel_data = img_bytes[start_pos:end_pos]
