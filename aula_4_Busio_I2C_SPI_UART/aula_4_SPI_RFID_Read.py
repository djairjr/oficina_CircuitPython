import mfrc522
import board
import time
from os import uname
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

def do_read():

  if uname()[0] == 'rp2040':
    # rdr = mfrc522.MFRC522(sck=board.SCK, mosi=board.MOSI, miso=board.MISO, cs=board.D9, rst=board.D8)
    rdr = mfrc522.MFRC522(sck=board.SCK, mosi=board.MOSI, miso=board.MISO, cs=board.D7, rst=board.D6)
  else:
    raise RuntimeError("Plataforma não suportada")

  print("")
  print("Coloque uma Tag no Leitor")
  print("")

  try:
    while True:
      (stat, tag_type) = rdr.request(rdr.REQIDL)

      if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
          led.value = False
          print("Detectei Nova TAG")
          print("  - Tipo : 0x%02x" % tag_type)
          print("  - uid   : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
          print("")

          if rdr.select_tag(raw_uid) == rdr.OK:
              
            # Abaixo, coloque a sequência da TAG Correta
            key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

            if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
              print("Address 8 data: %s" % rdr.read(8))
              rdr.stop_crypto1()
            else:
              print("Autenticado")
          else:
            print("Acesso Negado")
            
          #time.sleep(.5)
          led.value = True
          
  except KeyboardInterrupt:
      print("Fim do Programa")