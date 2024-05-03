# Audio em Circuitpython
Nossa oficina no Sesc Santana acabou, mas semana que vem vamos seguir com Circuitpython no Sesc 24 de maio.
Se você perdeu as inscrições, não tem problema. Toda semana eu vou compartilhar por aqui os códigos fonte
das experiências que a gente fizer nas oficinas.

# Players de MP3 Externos, controlados por UART
Acho que o mais conhecido deles é o DFPlayer Mini, da DF Robot https://wiki.dfrobot.com/DFPlayer_Mini_SKU_DFR0299. É super-barato, eficiente e pode ser usado sem nenhum microcontrolador. 
Existem algumas opções de biblioteca para controlar esse player usando CircuitPython:
https://github.com/DocSilveri/DFPlayer_Mini
https://github.com/bablokb/circuitpython-dfplayer

Outro modelo bastante conhecido, também controlado por UART é o MD YX5300 (às vezes só Serial Mp3 Player HW-311).
Os bytes de controle são praticamente os mesmos do DF Player Mini, então a mesma biblioteca funciona.

O incoveniente desse tipo de player é a ausência de possibilidade de se acessar o SD Card diretamente. Você também precisa seguir um protocolo correto para nomear os arquivos e não consegue acessá-los pelo nome.

# Players de MP3 Externos, funcionando por SPI
O que eu mais utilizei foi o VS1053, que é uma excelente alternativa. Você consegue acesso direto ao SD Card, possui suporte a arquivos midi e OGG e é bem mais rápido que as versões Seriais. O maior problema é o custo. É bastante comum você encontrá-lo como um Shield para Arduino https://www.sparkfun.com/products/12660, mas existe a opção de comprar a placa em outro formato também.
A biblioteca para ele é essa aqui: https://github.com/adafruit/Adafruit_CircuitPython_VS1053

# Tocando arquivos MP3 e WAV Direto na controladora, via Decoder e saída PWM
Essa novidade começou a aparecer com microcontroladores mais rápidos, como o RP2040 e até a ESP32.
Ainda não é a melhor coisa do mundo. E se você precisar utilizar outro dispositivo que demande velocidade, como um display, por exemplo, vai ter ruído pra caramba. Mas também é algo possível.
https://learn.adafruit.com/mp3-playback-rp2040/pico-mp3

# Tocando arquivos MP3 e WAV direto na controladora, via barramento I2S
A mesma observação sobre velocidade e ruídos vale aqui. Funciona bem se for apenas um player de audio. Mas eu acho a melhor solução, porque a plaquinha MAX98357A já é um amplificador Mono de 3W e a resposta sonora é muito boa! Eu sugiro que você compre da China, em quantidade superior a 5 peças. Vai sair o preço de duas, no Mercado Livre.


