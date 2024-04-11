Nessa aula nós vamos estudar o módulo Busio, que auxilia no uso dos barramentos Seriais de vários tipos.

O primeiro deles é o UART: Universal Asynchronous Receiver Transmitter, significando Transmissor/Receptor Universal Assíncrono. É um formato padrão para comunicação de dados de forma serial. Em forma assíncrona, dois fios (TX e RX) são usados para transmitir dados, um em cada direção, em regime full-duplex, ou seja, totalmente bi-direcional. Para isso, cada dispositivo deve ter seu clock, e as velocidades devem ser iguais.

A primeira experiência é fazer com que dois Raspberry Pi Pico se comuniquem usando a UART.

O segundo protocolo é o I2C: Inter-Integrated Circuit ou barramento serial multimestre. Foi desenvolvido pela Philips e é usado para conectar periféricos de baixa velocidade a uma placa mãe, a um sistema embarcado ou a um telefone celular. O nome significa Circuito Inter-integrado e é pronunciado I-ao quadrado-C, ou I-dois-C. 

Para este vamos utilizar alguns módulos como o Real Time Clock, Expansor de portas, LCD e outros.

Por fim, utilizaremos o SPI: Serial Peripheral Interface ou SPI é um protocolo que permite a comunicação do microcontrolador com diversos outros componentes, formando uma rede. É uma especificação de interface de comunicação série síncrona usada para comunicação de curta distância, principalmente em sistemas embarcados. A interface foi desenvolvida pela Motorola e tornou-se um padrão de facto. Aplicações típicas incluem cartões SD e mostradores de cristal líquido.

Os dispositivos SPI comunicam entre si em modo "full duplex" usando uma arquitectura "master-slave" com um único mestre. O dispositivo mestre origina a trama para a leitura e a escrita. Múltiplos dispositivos escravos são suportados através de selecção com linhas de selecção de escravos individuais (SS).

Às vezes SPI é chamado de barramento serial de quatro fios, contrastando com os barramentos seriais de três, dois (como o I2C) e um (como o One Wire) fio. O SPI pode ser descrito com precisão como uma interface de série síncrona, mas é diferente do protocolo síncrono de interface de série (SSI), que também é um síncrono protocolo de comunicação em série de quatro fios, mas emprega sinal diferencial e fornece apenas um único canal de comunicação simples.

Nesse caso, utilizaremos um leitor de RFID.


