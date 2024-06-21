"""
Working in progress code...
The original is here: https://github.com/stuartm2/CircuitPython_BMP_Reader

This version read files with any dimensions.
"""

class BMPReader(object):
    def __init__(self, filename):
        self._filename = filename
        self._read_img_data()

    def get_pixels(self):
        pixel_grid = []
        pixel_data = list(self._pixel_data)  # Trabalhamos com uma cópia

        bytes_per_pixel = 3  # Assumindo 24-bit color depth (RGB)
        row_size = self.width * bytes_per_pixel

        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Cálculo do índice do pixel no vetor de dados
                idx = (y * row_size) + (x * bytes_per_pixel)
                b = pixel_data[idx]
                g = pixel_data[idx + 1]
                r = pixel_data[idx + 2]
                row.append((r, g, b))
            pixel_grid.append(row)

        return pixel_grid

    def _read_img_data(self):
        def lebytes_to_int(bytes):
            n = 0x00
            for b in reversed(bytes):
                n = (n << 8) | b
            return n

        with open(self._filename, 'rb') as f:
            img_bytes = bytearray(f.read())

        # Verificação do formato BMP
        assert img_bytes[0:2] == b'BM', "Não é um arquivo BMP válido"
        assert lebytes_to_int(img_bytes[30:34]) == 0, \
            "A compressão não é suportada"
        assert lebytes_to_int(img_bytes[28:30]) == 24, \
            "A profundidade de cor de 24 bits é a única suportada"

        # Extração das dimensões da imagem
        start_pos = lebytes_to_int(img_bytes[10:14])
        self.width = lebytes_to_int(img_bytes[18:22])
        self.height = lebytes_to_int(img_bytes[22:26])

        # Extração dos dados dos pixels
        self._pixel_data = img_bytes[start_pos:]
