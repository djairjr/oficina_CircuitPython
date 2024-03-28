import board, microcontroller

for pin in dir (microcontroller.pin):
    # isinstance testa o tipo de um objeto
    # getattr, retorna o valor de um determinado atributo de um objeto
    # no caso abaixo, vai retornar o nome do pino no módulo microcontroller.pin
    if isinstance (getattr(microcontroller.pin, pin), microcontroller.Pin):
        print ("".join (("microcontroller.pin.", pin, '\t')), end = " ")
        for alias in dir(board):
            if getattr(board, alias) is getattr(microcontroller.pin, pin):
                print ("".join(("", "board.", alias)), end = " ")
        print()
        
        
