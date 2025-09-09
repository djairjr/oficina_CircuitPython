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


    

