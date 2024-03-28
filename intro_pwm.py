import board, digitalio, time
led = digitalio.DigitalInOut (board.LED)
led.switch_to_output()
frequency = 60 # 60Hz
duty = 0.05
active = duty * (1 / frequency)
inactive = (1 - duty) * (1 / frequency)
while True:
    led.value = True
    time.sleep (active)
    led.value = False
    time.sleep (inactive)
    


