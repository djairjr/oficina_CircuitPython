import board, busio
pin_scl = board.GP21
pin_sda = board.GP20
i2c = busio.I2C(scl=pin_scl,sda=pin_sda)
while not i2c.try_lock():  pass
print("Encontrei dispositivo :", [hex(device_address)
    for device_address in i2c.scan()])
i2c.unlock()
