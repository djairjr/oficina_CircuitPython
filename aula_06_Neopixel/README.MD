## Instalando as bibliotecas Neopixel e Adafruit_Simpleio
Até o momento, nós estamos lidando apenas com os módulos nativos da nossa placa. Não foi preciso fazer a instalação de nenhum módulo adicional. 
Convencionalmente, nós chamamos esses módulos adicionais para a programação de **bibliotecas (ou libraries)**.
Nós podemos instalar essas bibliotecas simplesmente copiando os arquivos .py ou .mpy para a pasta lib da sua placa.
Mas a maneira mais segura de fazer isso é utilizar o gerenciador de pacotes CircUP, da Adafruit.

Para instalar esse gerenciador, abra o Thonny e acesse o menu Tools (Ferramentas) >> Open System Shell. 

Você deve ver a janela de comandos do seu Windows, com alguma coisa similar a **C:\Users\Usuario\Pasta>**

Nesta janela, digite o comando a seguir:
```
python -m pip install circup
```

Isso deve instalar o gerenciador de pacotes Circup, da Adafruit.
Agora, vamos instalar duas bibliotecas que vamos utilizar para os próximos exercícios:

```
circup install neopixel, adafruit_simpleio
```

## Neopixels, Listas, Tuplas, Dicionários
As fitas de Led Neopixel são muito versáteis. Cada led possui um controlador de cores isolado e pode ser acessado individualmente.
Os leds são ligados em cascata e possuem sempre quatro pinos: VCC e GND, que são os pinos de energia e DI e DO, que são os pinos
de entrada de dados (DI) e saída de dados (DO). Para criar uma fita de leds, basta conectar os pinos DO de um led ao pino DI de outro.
O primeiro led vai ser o que tiver o seu pino DI conectado ao controlador.

Você pode cortar a fita Led e usar pequenos pedaços. Ou montar diversos arranjos diferentes. No mercado, encontramos anéis, matrizes,
leds individuais.

Eu gosto muito de usar as fitas de Led porque consigo um grande efeito visual usando apenas um pino do meu controlador.

Nós vamos adaptar a nossa montagem de sempre, só que ao invés de usar um LED, vamos usar uma fita com dez leds diferentes.
![Montagem com Fitas Led Neopixel](https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_06_Neopixel/Diagrama%20Aula%204_bb.png)


