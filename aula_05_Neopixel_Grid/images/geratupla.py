import struct
import sys

def read_bmp_16x16(filename):
    """
    Lê um arquivo BMP 16x16 e retorna uma lista de tuplas RGB
    """
    try:
        with open(filename, 'rb') as bmp_file:
            # Verifica o cabeçalho BMP (primeiros 2 bytes devem ser 'BM')
            header = bmp_file.read(2)
            if header != b'BM':
                raise ValueError("Arquivo não é um BMP válido")
            
            # Pula para a informação do tamanho do arquivo (bytes 2-6)
            bmp_file.seek(2)
            file_size = struct.unpack('<I', bmp_file.read(4))[0]
            
            # Pula para o offset dos dados da imagem (bytes 10-14)
            bmp_file.seek(10)
            data_offset = struct.unpack('<I', bmp_file.read(4))[0]
            
            # Lê o cabeçalho DIB (tamanho mínimo 40 bytes)
            dib_header_size = struct.unpack('<I', bmp_file.read(4))[0]
            
            # Lê largura e altura (bytes 18-26)
            width = struct.unpack('<i', bmp_file.read(4))[0]
            height = struct.unpack('<i', bmp_file.read(4))[0]
            
            # Verifica se a imagem é 16x16
            if width != 16 or height != 16:
                raise ValueError("A imagem deve ser 16x16 pixels")
            
            # Lê bits por pixel (bytes 28-30)
            bmp_file.seek(28)
            bits_per_pixel = struct.unpack('<H', bmp_file.read(2))[0]
            
            if bits_per_pixel != 24:
                raise ValueError("O BMP deve ter 24 bits por pixel (RGB)")
            
            # Vai para o início dos dados da imagem
            bmp_file.seek(data_offset)
            
            # Calcula o padding por linha (cada linha deve ser múltiplo de 4 bytes)
            row_padding = (4 - (width * 3) % 4) % 4
            
            # Lista para armazenar os pixels
            pixel_grid = []
            
            # Lê a imagem de baixo para cima (BMP armazena de baixo para cima)
            for y in range(height - 1, -1, -1):
                row = []
                for x in range(width):
                    # Lê os bytes BGR (BMP armazena em ordem B, G, R)
                    blue = struct.unpack('<B', bmp_file.read(1))[0]
                    green = struct.unpack('<B', bmp_file.read(1))[0]
                    red = struct.unpack('<B', bmp_file.read(1))[0]
                    
                    # Adiciona a tupla RGB
                    row.append((red, green, blue))
                
                # Pula o padding da linha
                bmp_file.read(row_padding)
                pixel_grid.append(row)
            
            return pixel_grid
            
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao ler o arquivo BMP: {e}")
        return None

def main():
    if len(sys.argv) != 2:
        print("Uso: python ler_bmp.py <arquivo.bmp>")
        return
    
    filename = sys.argv[1]
    pixel_grid = read_bmp_16x16(filename)
    
    if pixel_grid:
        # Imprime a lista no formato desejado
        print("mario_grid = [")
        for i, row in enumerate(pixel_grid):
            if i < len(pixel_grid) - 1:
                print(f"    {row},")
            else:
                print(f"    {row}")
        print("]")

if __name__ == "__main__":
    main()