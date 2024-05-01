# Recriando Clássicos dos Arcades com Neopixel e Circuitpython

O primeiro desafio para a oficina de Arcades é transformar as fitas de led num display mínimo.
O pessoal da Adafruit já fez um trabalho incrível, desenvolvendo a biblioteca Pixel_Framebuf.
Mas ela não suporta todo tipo de arranjo com os paineis. Por exemplo, você até consegue fazer
um arranjo de duas placas 8x32 de modo a conseguir 8x64, porque esse é  o  fluxo natural  das
conexões numa Fita Led. Mas se você quiser arranjar algo com 16x32, não vai conseguir ter  as
coordenadas da tela corretas.

Os painéis são arranjados da maneira abaixo, em Zig Zag.

![Arranjo Atual](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_6_Neopixel/images/Array%20Neopixel%20-%20Coordenadas.png)

Quando você os conecta em cascata, o endereço do primeiro pixel (0) no próximo painel vai ser 
256. Faz sentido se você for conectando os painéis em cascata horizontalmente. 

![Dois Painéis](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_6_Neopixel/images/Default%20Framebuf%20Library.png)

Mas se você for usar outra disposição, por exemplo, com os paíneis posicionados verticalmente, 
um em cima  do  outro, o ideal era que o primeiro pixel do segundo painel tivesse o endereço 8. 

![Melhor assim](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_6_Neopixel/images/New%20Coords.png)

Na biblioteca padrão, isso não é possível. Por isso eu tive que escrever  uma  rotina  python
para resolver esse problema.

```
def generate_grid(width, height, tile_num):
    # Primeiro vai colocar as coordenadas do primeiro painel
    # A função original até faz isso, mas não gera a lista que eu preciso
    def single_tile_coord():
        single_tile = []

        for i in range(width * height):
            group_index = i // height
            # Olha só que legal esse jeito de checar se a coluna é par ou impar...
            ascending = (group_index % 2) == 0
            number_within_group = i % height

            if ascending: # Se for par - lembrando que começa no 0
                number = group_index * height + number_within_group
            else: # se for impar
                number = (group_index + 1) * height - 1 - number_within_group

            if number_within_group == 0:
                temp = []

            temp.append (number)

            if number_within_group == height - 1:
                single_tile.append(tuple(temp))

        return single_tile

    def multi_tile(original_matrix):
        # Aqui começa o meu arranjo.
        multi_temp = []
        factor = tile_num - 1
        
        if factor == 0: # se tiver só um painel, deixa quieto. Segue igual.
            multi_temp = original_matrix
        else:
            # Tem mais de um painel? Beleza...
            for tup in original_matrix:
                modified_tuple = tup[:height]  

                for n in range (factor): 
                    # Para cada painel adicional, cria uma tupla multiplicando a quantidade de paineis, pela largura e altura
                    # Daí soma o valor da posição da tupla original.
                    modified_tuple += tuple(num + (factor * (width * height)) for num in tup[:height])          
                    multi_temp.append(modified_tuple)

        return multi_temp

    default_tile = single_tile_coord()
    return multi_tile(default_tile) 
```

Então eu embuti isso aí numa cópia da PixelGrid. E criei a tilegrid.

A maratona toda dessa adaptação eu estou compartilhando no Hackster.io https://www.hackster.io/nicolaudosbrinquedos/circuitpython-tiled-neopixel-panel-446b73

Para criar os jogos, ainda falta trabalhar em detecção de colisões, velocidade de atualização da tela, som, movimento usando joystick e cálculo de pontuação...
