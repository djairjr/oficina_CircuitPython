"""
Nesse caso, vamos descobrir como escrever algumas informações
Nas TAGS RFID
"""
import board
import mfrc522


def do_write():

	rdr = mfrc522.MFRC522(board.SCK, board.MOSI, board.MISO, board.D2, board.D3)
	rdr.set_antenna_gain(0x07 << 4)

	print('')
	print("Coloque o Cartão para Escrever no Endereço 0x08")
	print('')

	try:
		while True:

			(stat, tag_type) = rdr.request(rdr.REQIDL)

			if stat == rdr.OK:

				(stat, raw_uid) = rdr.anticoll()

				if stat == rdr.OK:
					print("Novo Cartão Detectado ")
					print("  - tipo da tag: 0x%02x" % tag_type)
					print("  - uid\t : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
					print('')

					if rdr.select_tag(raw_uid) == rdr.OK:

						key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

						if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
							stat = rdr.write(
									8, b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
									)
							rdr.stop_crypto1()
							if stat == rdr.OK:
								print("Dados Escritos no Cartão")
							else:
								print("Falha ao Escrever Dados")
						else:
							print("Erro de Autenticação")
					else:
						print("Falha ao selecionar Cartão")

	except KeyboardInterrupt:
		print("Bye")
