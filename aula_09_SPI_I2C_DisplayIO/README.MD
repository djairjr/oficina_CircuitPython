## Coleção de exemplos usando I2C e SPI para comunicação com displays
Nesta pasta vou deixar alguns exemplos de comunicação com displays diferentes, usando os protocolos I2C e SPI.
Normalmente, displays mais simples, como os OLED e LCD monocromáticos são interfaceados via I2C ou paralelo.
As telas de maior resolução, mais cores e que possuem a necessidade de taxas de atualização mais rápidas, utilizam o protocolo SPI.
A biblioteca DisplayIO da Adafruit faz toda a abstração para escrita, desenho e atualização de todas as telas.

Os nomes dos arquivos seguem a seguinte estrututura:

**aula_09_PROTOCOLO_TIPO_DISPLAY_APLICAÇÃO**
onde PROTOCOLO pode ser I2C ou SPI
TIPO_DISPLAY, pode ser LCD 20x4, OLED, TFT
APLICAÇÃO, é o nome do jogo ou aplicação simples.

São apenas exemplos que necessitam de hardware adicional e estão aqui para exemplificar as aplicações.
Nós não chegamos a esse conteúdo durante o curso.