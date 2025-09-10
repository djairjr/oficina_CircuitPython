
# Script Python para fazer o ajuste automático de Gamma de qualquer imagem.
# Para executar: python gamma.py nomedaimagem.jpg -o nomedamimagem.bmp

# Esse Script roda em Python mesmo, e não Circuitpython.


import argparse
from PIL import Image
import os
import sys

def ajustar_gamma(imagem, gamma):
    """
    Ajusta o gamma de uma imagem
    
    Args:
        imagem: Objeto PIL Image
        gamma: Fator de gamma (float)
    
    Returns:
        Imagem com gamma ajustado
    """
    if gamma == 1.0:
        return imagem  # Nenhum ajuste necessário
    
    # Cria a tabela LUT para correção de gamma
    tabela_gamma = []
    for i in range(256):
        # Aplica a correção de gamma: valor^(1/gamma)
        valor_ajustado = int(((i / 255.0) ** (1.0 / gamma)) * 255 + 0.5)
        # Garante que o valor esteja no intervalo [0, 255]
        valor_ajustado = max(0, min(255, valor_ajustado))
        tabela_gamma.append(valor_ajustado)
    
    # Converte a imagem para um modo compatível com a LUT se necessário
    if imagem.mode in ['1', 'L', 'P', 'I']:
        # Modos de banda única
        return imagem.point(tabela_gamma)
    elif imagem.mode in ['RGB', 'RGBA', 'CMYK', 'YCbCr']:
        # Modos de múltiplas bandas - aplica a mesma LUT a todos os canais
        # Cria uma LUT com entradas para todos os canais
        tabela_completa = []
        for _ in range(len(imagem.getbands())):
            tabela_completa.extend(tabela_gamma)
        return imagem.point(tabela_completa)
    else:
        # Para outros modos, converte para RGB primeiro
        img_rgb = imagem.convert('RGB')
        tabela_completa = tabela_gamma * 3  # Para R, G, B
        return img_rgb.point(tabela_completa)

def processar_imagem(arquivo_entrada, arquivo_saida):
    """
    Processa a imagem: converte para BMP e ajusta gamma para 0.4
    
    Args:
        arquivo_entrada: Caminho do arquivo de entrada
        arquivo_saida: Caminho do arquivo de saída
    """
    try:
        # Abre a imagem
        with Image.open(arquivo_entrada) as img:
            print(f"Modo da imagem original: {img.mode}")
            
            # Ajusta o gamma para 0.4 (fixo)
            img_ajustada = ajustar_gamma(img, 0.4)
            
            # Converte para RGB se não estiver já nesse modo (para garantir compatibilidade com BMP)
            if img_ajustada.mode not in ['RGB', 'RGBA']:
                img_ajustada = img_ajustada.convert('RGB')
            
            # Salva como BMP
            img_ajustada.save(arquivo_saida, 'BMP')
            
            print(f"Imagem processada com sucesso!")
            print(f"Entrada: {arquivo_entrada}")
            print(f"Saída: {arquivo_saida}")
            print(f"Modo da imagem final: {img_ajustada.mode}")
            print(f"Gamma aplicado: 0.4 (fixo)")
            
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Converte imagem para BMP e ajusta gamma para 0.4')
    parser.add_argument('entrada', help='Arquivo de imagem de entrada')
    parser.add_argument('-o', '--output', help='Arquivo de saída BMP (opcional)')
    
    args = parser.parse_args()
    
    # Verifica se o arquivo de entrada existe
    if not os.path.exists(args.entrada):
        print(f"Erro: Arquivo '{args.entrada}' não encontrado!")
        sys.exit(1)
    
    # Define o nome do arquivo de saída
    if args.output:
        arquivo_saida = args.output
        # Garante que a extensão seja .bmp
        if not arquivo_saida.lower().endswith('.bmp'):
            arquivo_saida = os.path.splitext(arquivo_saida)[0] + '.bmp'
    else:
        # Se não for especificado, usa o mesmo nome com extensão .bmp
        nome_base = os.path.splitext(args.entrada)[0]
        arquivo_saida = f"{nome_base}.bmp"
    
    # Processa a imagem
    processar_imagem(args.entrada, arquivo_saida)

if __name__ == "__main__":
    main()