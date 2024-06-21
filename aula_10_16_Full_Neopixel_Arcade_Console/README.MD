## Full Console Code
Aqui está o código completo do sistema de console
usando as Matrizes de Led Neopixel, de 8x32 ou 16x16.

Foi amplamente testado usando o Seeed Xiao RP2040.
Mas a classe de Hardware que eu desenvolvi é capaz de
detectar a placa e adaptar a pinagem automaticamente.

Tá configurado para rodar Xiao RP2040 ou Xiao ESP32.
E também a Franzininho Wifi ESP32S2.

Estranhamente existem alguns problemas de estouro de
memória, apesar de estarmos usando uma tela de 16x32.
A solução mais tosca foi colocar gc.collect() aqui e 
ali e deletar algumas variáveis depois do uso.

Os códigos dos jogos podem melhorar, sobretudo porque
alguns estavam com questões referentes às coordenadas
da tela e eu achei mais rápido mudar a rotação do display.

--- English Captions Bellow ---

Here is the complete console system code
using Neopixel LED Matrices, 8x32 or 16x16.

It has been extensively tested using the Seeed Xiao RP2040.
But the Hardware class that I developed is capable of
detect the board and adapt the pinout automatically.

It is configured to run Xiao RP2040 or Xiao ESP32.
And also the Franzininho Wifi ESP32S2.

Strangely there are some overflow problems
memory, even though we are using a 16x32 screen.
The crudest solution was to put gc.collect() here and
there and delete some variables after use.

Game codes can improve, especially because
some had questions regarding the coordinates
of the screen and I found it faster to change the rotation of the display.