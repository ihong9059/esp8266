import machine
spi = machine.SPI(1, baudrate=5000000, polarity=0, phase=0)

spi = machine.SPI(0, baudrate=5000000, polarity=0, phase=0)

cs = machine.Pin(15, machine.Pin.OUT)
cs.high()

cs.low()
data = spi.read(4)
cs.high()

data = bytearray(4)
cs.low()
spi.readinto(data)
cs.high()
