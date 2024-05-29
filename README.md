# Oficina de Circuitpython

O CircuitPython, desenvolvido pela equipe da Adafruit Industries, 
é uma versão otimizada da linguagem de programação Python, projetada
para o ambiente dos microcontroladores e plataformas de desenvolvimento 
para computação embarcada.

Foi pensado para iniciantes, sem nenhuma experiência em programação, 
facilitando a criação de projetos de hardware, com suporte abrangente
para diversos componentes eletrônicos.

É construído de forma modular, com funcionalidades separadas em diferentes
módulos. Isso inclui módulos para manipulação de pinos,
comunicação com buses, sensores, displays  e muitos outros.

Cada módulo é projetado para ser intuitivo e fácil de usar. Os módulos encapsulam
a complexidade de lidar com hardware específico, expondo uma interface de alto
nível que é fácil de entender e usar. 

Isso permite que o código seja facilmente portátil entre diferentes projetos
e plataformas. Você pode reutilizar módulos em diferentes projetos sem precisar
modificar o código para se adaptar a diferentes hardwares.

Cada módulo pode ser atualizado ou melhorado independentemente, e essas atualizações 
podem ser feitas sem impactar outros módulos. Isso também facilita a correção de bugs 
e a adição de novas funcionalidades.

Além disso, a Adafruit fornece extensa documentação e exemplos para cada módulo, 
ajudando os usuários a entender como usar cada funcionalidade. 
Isso acelera o aprendizado e facilita a implementação de novas ideias.

# Não sei nada de programação. Nem de Python. E agora?

Não tem problema! Se você consegue entender uma sentença em inglês, ou ler um dicionário
é moleza!

Python é uma linguagem super bem documentada, com amplo suporte e uma comunidade engajada.
CircuitPython é Python, com toda a facilidade do Python, mas com um conjunto reduzido de
suas funcionalidades. 

Eu indico o curso gratuito da Solyd, do Guilherme Junqueira. O Guilherme é muito engraçado
e o curso tem uma didática incrível. Foi através desse curso que eu comecei a programar
em Python.
(https://solyd.com.br/cursos/python-basico/)

Também gosto muito de literatura específica para Python. O melhor livro para iniciantes é o 
do professor Nilo Ney Coutinho Menezes. "Introdução a Programação com Python". É vendido
pela Novatec, mas pode ser encontrado on-line na Archive.org.

(https://ia804504.us.archive.org/8/items/nilo-ney-coutinho-menezes-introducao-a-programacao-com-python-algoritmos-e-logic/Nilo%20Ney%20Coutinho%20Menezes%20-%20Introdu%C3%A7%C3%A3o%20%C3%A0%20programa%C3%A7%C3%A3o%20com%20Python_%20algoritmos%20e%20l%C3%B3gica%20de%20programa%C3%A7%C3%A3o%20para%20iniciantes-Novatec%20%282014%29.pdf)

Essa lista possui os principais comandos de Python e a maioria deles vai funcionar em Circuitpython.
Python CheatSheet.(https://www.pythoncheatsheet.org/)

No site da Adafruit você vai encontrar toda sorte de tutoriais para utilizar CircuitPython.
Tudo é bastante modular, cada biblioteca é bem explicada com exemplos úteis e funcionais.

Indico especialmente esses três: 

Welcome to CircuitPython. (https://learn.adafruit.com/welcome-to-circuitpython/overview)

CircuitPython Essentials. (https://learn.adafruit.com/circuitpython-essentials/circuitpython-essentials)

Getting Started with Raspberry Pi Pico and CircuitPython. 
(https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython?view=all)

Além disso, o TodBot compilou uma série de dicas úteis no seu Github. Mais para frente, elas
vão agilizar a sua vida...

Tod Bot CircuitPython Tricks. (https://github.com/todbot/circuitpython-tricks)

# Tenho que instalar alguma coisa no meu computador? Como eu faço para começar?

O Circuitpython é um firmware específico que você vai precisar instalar na sua plaquinha
de desenvolvimento. Depois disso, ele vai ficar rodando na placa e você vai se comunicar
com ela utilizando a interface USB do seu computador.

Toda a comunicação entre o seu computador e a placa de desenvolvimento é feita via
USB, o que permite ver a funcionalidade implementada em tempo real, sem a 
necessidade de compilação adicional.

1. Baixe o firmware específico para a sua placa em http://circuitpython.org/downloads
2. Coloque a sua placa em modo Bootloader (normalmente a placa possui um botão BOOT), que 
deve ser pressionado na inicialização.
3. Se a sua placa for baseada no Microcontrolador RP2040, surgirá um drive USB RPI-RP2. 
Arraste ou copie o arquivo '.uf2' para essa nova unidade. O sistema ira reiniciar e 
haverá uma unidade USB chamada CIRCUITPY. Pronto! Circuitpython instalado!
4. Se a sua placa for baseada em ESP32, no próprio site do Circuitpython haverá o instalador.
Você deverá utilizar o Chrome e permitir o acesso à USB. 
5. Na sua nova unidade USB você verá algumas pastas e arquivos com extensão '.py'. O arquivo 
'code.py' é executado automaticamente. Outros arquivos especiais são o 'boot.py' e 'repl.py'.
Em algumas placas, você verá o arquivo de configurações 'settings.toml'. 
6. A pasta 'lib' vai conter todas as bibliotecas instaladas. Nós falaremos sobre isso depois.

# REPL e IDE (Ambiente de Desenvolvimento Integrado)

O arquivo 'code.py' que está na sua nova unidade CIRCUITPY pode ser aberto com um programa
de edição de texto simples, como por exemplo, o bloco de notas do Windows.

Ele vai ser executado toda vez que a sua placa for ligada e normalmente, vai ser programa
que você gostaria que ficasse executando sempre. Se você não fez nenhuma edição nesse código,
provavelmente ele vai ser algo como print ('Hello world').

Por enquanto, não existe maneira de você ver a execução desse comando. Ele está sendo executado,
mas retorna alguma coisa na comunicação serial entre o seu computador e a placa.

Nós vamos instalar um ambiente de desenvolvimento integrado, ou IDE. Esse aplicativo vai nos
possibilitar acessar essa comunicação direta com a placa, além de disponibilizar um editor
de texto simples, com correção de sintaxe e sistema de autocompletar.

Eu gosto muito do Thonny, que pode ser baixado em http://www.thonny.org

Mas existem outras opções, inclusive um editor de código online. https://code.circuitpython.org/

No site da Adafruit você verá que eles indicam o MU https://codewith.mu/

# Instalando e configurando o Thonny IDE

A instalação é muito simples. Basta fazer o download do arquivo e seguir as etapas de sempre.
https://github.com/thonny/thonny/releases/download/v4.1.4/thonny-4.1.4.exe

Depois que o Thonny estiver instalado, você vai precisar mexer na sua configuração para ter 
acesso à porta USB onde a plaquinha está conectada.

1. Conecte a sua plaquinha à porta USB.
2. Abra o aplicativo Thonny.
3. No Thonny abra o menu Ferramentas > Opções.
4. Na janela que se abre, clique na segunda aba: Interpretador.
5. Na seleção 'Que tipo de interpretador o Thonny deve usar para executar seu código', procure
'Circuitpython genérico'
6. Na seleção 'Porta', procure a porta USB onde está conectada a sua placa. Ou <Tente detectar 
a porta automaticamente>.
7. Se não for detectada automaticamente, deve ser algo como 'Circuitpython CDC control @ COM...'
8. Pronto!

Na janela principal do Thonny, você verá duas áreas distintas. Na parte superior, está o seu
editor de código. Tudo o que for digitado nessa área precisa ser salvo e será executado quando
você pressionar o botão no menu 'Executar programa atual (F5)' ou pressionar a tecla F5.

Na área inferior da tela, você verá uma aba escrito 'Shell'. Essa aba mostra tudo o que está 
sendo executado na placa de desenvolvimento. Ela mostra a comunicação via USB em tempo real.
E pode ser utilizada para executar comandos na placa e obter resultados imediatos.

# Usando o Shell para aprender 

Antes de botarmos a mão na massa e criarmos o nosso primeiro programa, vamos descobrir o que 
a nossa plaquinha pode fazer, explorando os mecanismos de ajuda disponíveis no Python.

Clique logo depois de '>>>' na aba do Shell e digite o comando abaixo
```
help ()
```

Você deve ver uma mensagem como essa:
```
Bem-vindo ao Adafruit CircuitPython 9.0.5!

Visite o site circuitpython.org para obter mais informações.

Para listar os módulos existente digite `help("modules")`.
```

Então você pode tentar seguir essa dica:
```
help ("modules")
```

O que você vê na tela agora é uma lista de todos os módulos built-ins, isto é, todos os módulos
pré instalados na sua placa. Para utilizá-los num programa, você precisa importá-los.

Vamos usar o módulo board, como exemplo. 

```
import board
dir (board)
```

O comando dir é uma função embutida que é usada para inspecionar o conteúdo de objetos, módulos,
classes e instâncias. Ele retorna uma lista de atributos válidos para o objeto que é passado 
como argumento.

Usando esse comando, podemos descobrir alguma coisa sobre o módulo board. 

Para acessar qualquer elemento desse módulo, nós precisamos indicar o módulo e depois o elemento
separado por um ponto. Por exemplo, board.D1.

Nós podemos executar o comando dir (board.D1). Se ele retornar apenas ['__class__'], significa que
não há mais nenhum nível de atributos.

Nesse caso, você pode tentar entender que tipo de coisa é board.D1.
```
help (board.D1)
```

E verá a resposta: objeto board.D1 é do tipo Pin

Vejamos agora com uma função. Vamos verificar uma função de tempo, no módulo time.
Digite os comandos abaixo:

```
import time
dir (time)
```

Você deve ver a resposta:
['__class__', '__name__', '__dict__', 'localtime', 'mktime', 'monotonic', 'monotonic_ns', 'sleep', 'struct_time', 'time']

Vamos ver o que é time.time, por exemplo.

```
dir (time.time)
```

['__class__']

Ótimo. Chegamos no maior nível. 

```
help (time.time)
```

E teremos:
objeto <function> é do tipo function

Em Python, tudo é considerado um objeto. Para diferenciar as funções de outros tipos de objeto,
nós utilizamos parênteses. 

Experimente digitar:
```
time.time()
```

E o resultado é o número de segundos entre o tempo atual e a meia noite do dia 1 de janeiro de 1970.
Essa data é uma data de referência conhecida como UNIX Epoch.

Vamos tentar com outro. Digite agora o comando abaixo.

```
help (time.sleep)
```

E novamente teremos:
objeto <function> é do tipo function

Então:

```
time.sleep()
```

E teremos a indicação de um erro:

Traceback (a última chamada mais recente):
  Arquivo "<stdin>", linha 1, em <module>
TypeError: função leva 1 argumentos posicionais, mas apenas 0 foram passadas

O que está dizendo? Que a função necessita de um argumento. Mas nós não passamos nenhum.
Ok. Então vamos tentar de outro modo.

```
time.sleep('a')
```

E teremos outro erro:

Traceback (a última chamada mais recente):
  Arquivo "<stdin>", linha 1, em <module>
TypeError: Não é possível converter str para float

Hmm. Parece que ele não conseguiu converter str para float. O que quer dizer?


Deixe eu ver o que ele entende por 'a', que foi o que eu coloquei como parâmetro.

```
type ('a')
```
E ele retorna:
<class 'str'>

Alguma coisa na função time talvez precise de um float e não de um str.
O que é um float? É qualquer número com ponto flutuante. Por exemplo 5.0.

```
time.sleep (5.0)
print ('E se passaram 5s')
```

Aprender a programar é principalmente, aprender a interpretar mensagens de erro.
Elas são valiosas ferramentas de aprendizado que oferecem feedback imediato, 
ajudam a diagnosticar problemas específicos, ensinam as regras e a sintaxe da linguagem, 
promovendo o aprendizado contextual e desenvolvendo habilidades de depuração.

É preciso ter paciência com elas e lê-las atentamente.

Em alguns casos, a mensagem de erro não é suficiente para solucionar o problema. Mas
ela é suficiente para pedir ajuda corretamente.

# Uma lista de possibilidades para o Shell
O shell de Python já possibilita fazer de modo direto uma série de operações.
Experimente digitar cada um dos comandos abaixo:

```
# Alguns comandos básicos de Python

# Operações matemáticas simples
4 + 4	# Soma
4 - 2	# Subtração
4 * 5	# Multiplicação
2 ** 3 	# Exponenciação
20 / 2	# Divisão
21 // 2 # Divisão arredondada (sem parte fracional)
20 % 3	# Módulo (Retorna o resto da divisão)

# Variáveis e Atribuição de valores
a = 1
b = 2
c = 'Texto'			# Não faz distinção de tipo na atribuição
lição = 'Outro Texto' 	# Existe a possibilidade de acentuação nas variáveis

print (b * lição)	# Escreve no prompt

# Nomes de variáveis válidos
a1 = 1
velocidade = 60
velocidade90 = 90
salario_medio = 1200
salário_médio = 1200
# salário médio = 1200 Não pode usar espaços
_variável = 10
# 1a = 1200 Não pode  começar com números

# Tipos de Variáveis Numéricas
a = 5 		# int
b = 3.0 	# float
c = -4		# int
d = - 8.0	# float

# Variáveis do tipo lógico
Verdadeiro = True
Falso = False

# Operadores Relacionais
Verdadeiro == Verdadeiro
Falso == Falso
Verdadeiro != True
Verdadeiro != False
a > b
a < b
a >= b
a <= b

# Operadores Lógicos
not Verdadeiro
not Falso
Verdadeiro and Verdadeiro
Verdadeiro or Falso

# Strings (Sequencia literal de caracteres)
texto = 'Isso é uma String 1234'
len (texto)
texto [7: 17] 	# Fatiamento
texto + '5678'	# Concatenação

composição = 'O resultado é %d'
composição % a

composição = 'O resultado é %02d'
composição % a

composição = 'O resultado é %5.2f'
composição % b

composição = 'O resultado é %s'
composição % texto

composição_mista = 'O resultado total é %d, %02d, %5.2f e %s' 
composição_mista % (a,a,b,texto)

# Entrada de Dados
a = input ('Digite alguma coisa ') # Sempre String
print ('Você digitou  %s' % a)

# Convertendo a entrada de dados em outro tipo
anos = int (input ('Entre a sua idade atual '))
nascimento = 2024 - anos
print ('Você nasceu no ano de %d '  %nascimento)

# Checando o tipo de uma variável
type (anos)
type (a)
type (Verdadeiro)

# Checando condições
a = int (input ('Digite um numero qualquer '))
if a == 1:
        print ('Aqui deu um')
    elif a == 2:
        print ('Aqui deu dois')
    else:
        print ('Aqui não deu nem um nem dois')
    
# Repetições:
x = 0
while x<3:
    print (x)
    x = x+1

for n in range (10):
        print (n)

# Tuplas, Listas, Dicionários

tupla = (0,1,2,3) # conjunto de dados imutável. Você pode acessar, mas não alterar
tupla[2] # resulta 2
tupla[2] = 3 # resulta em erro

lista = ['palavra 1', '0', 2 ] # conjunto mutável de dados
lista[0] = 0
lista # resulta em [0,'0', 2]

# Cria uma lista com numeros na faixa de 0 a 9
lista = [n for n in range (10)]
lista.append (10)
lista.remove (0)
lista.reverse()
for x,e in enumerate(lista):
    print (x, e)

# vê tudo que é possível fazer com a lista
dir (lista)

# conjunto mutável de dados, acesso é feito pelo nome da chave
dicionário = { 'Chave 1': 'Valor 1', 'Chave 2': 'Valor 2', 'Chave 3': 'Valor 3' }
dicionário [0] # Resulta em erro. A chave não pode ser endereçada por índices
dicionário ['Chave 1'] # Resulta 'Valor 1'

# Lembrando que eu posso fazer qualquer combinação de lista de tuplas, tuplas de listas,
# dicionários de tuplas, etc...
cores = {'BLACK': (0,0,0), 'RED': (255,0,0), 'GREEN':(0,255,0), 'BLUE':(0,0,255)}
red_amount, green_amount, blue_amount = cores['BLACK']
red_amount # resulta em 0

```
