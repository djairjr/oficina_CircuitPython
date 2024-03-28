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
a = input ('Digite um numero qualquer ')
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
    
lista = [n for n in range (10)]
lista.append (10)
lista.remove (0)
lista.reverse()
for x,e in enumerate(lista):
    print (x, e)
dir (lista) # vê tudo que é possível fazer com a lista


    
