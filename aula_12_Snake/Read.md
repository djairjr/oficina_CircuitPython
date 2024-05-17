#Snake Game
Esse é um clássico. Jogo muito simples de ser programado e que diverte por horas.
Também é bacana para a gente entender duas coisas: como ler o Joystick e o Botão e 
como detectar colisões, que é um elemento importante em qualquer jogo.

O exemplo da Lousa Mágica vai lidar com Joystick e Botão apenas.
https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_10_Snake/aula_9_lousa_magica.py

O código do Get Color, recupera o valor da cor do pixel através das coordenadas do display.
https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_10_Snake/aula_9_get_color.py

O código que está no exemplo não é para a plaquinha ainda. 
https://github.com/djairjr/oficina_CircuitPython/blob/main/aula_10_Snake/snake_no_pygame.py
É um exemplo em Python, feito para rodar em computadores Linux com a biblioteca 
ncurses instalada.

Vai requerer alguma adaptação para funcionar no nosso display especial, provavelmente contando
com get_color.py para ajudar a detectar a fruta...