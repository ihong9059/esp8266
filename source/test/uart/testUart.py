from machine import UART

uart = UART(0, 115200)
uart.init(115200, bits=8, parity=None, stop=1)

hks = uart.readline()

print(hks)
