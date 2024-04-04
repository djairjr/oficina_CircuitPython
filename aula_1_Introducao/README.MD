Na primeira aula a gente aprendeu a instalar o CircuitPython
na plaquinha e ir descobrindo o que fazer com ela através da
ajuda no REPL.

# Listar todos os módulos disponíveis
help ('modules')

# Importar o Módulo 'builtins' que contém todas as palavras chave de Python
import builtins

# Mostrar uma lista com todos as palavras chave

for palavra_chave in dir (builtins):
  
  print (palavra_chave)


  

