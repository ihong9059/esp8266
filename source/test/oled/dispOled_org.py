"""
Pi4IoT    -> https://www.youtube.com/pi4iot
draw symbol on the ssd1306 display
"""

import ssd1306
import machine
import sys
from machine import I2C, Pin

i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(64, 48, i2c)
# display = ssd1306.SSD1306_I2C(128, 64, i2c)
display.fill(0)

battery_emty = [
'00001111111111111111111111',
'00001000000000000000000001',
'11111000000000000000000001',
'10000000000000000000000001',
'10000000000000000000000001',
'10000000000000000000000001',
'10000000000000000000000001',
'10000000000000000000000001',
'11111000000000000000000001',
'00001000000000000000000001',
'00001111111111111111111111']

battery_full = [
'00001111111111111111111111',
'00001000000000000000000001',
'11111001111001111001111001',
'10000001111001111001111001',
'10000001111001111001111001',
'10000001111001111001111001',
'10000001111001111001111001',
'10000001111001111001111001',
'11111001111001111001111001',
'00001000000000000000000001',
'00001111111111111111111111']

ant = [
'1111111111100000',
'1000010000100000',
'0100010001000000',
'0010010010000000',
'0001010100000001',
'0000111000000101',
'0000010000010101',
'0000010001010101',
'0000010101010101',
'0000010101010101']

logo = [
'000000011111100000000',
'000001100000011000000',
'000110000000000110000',
'001100100100000011000',
'011001010000000001100',
'011010100000000001100',
'110101000000000000110',
'110101000100000000110',
'110101001110000001111',
'110000000100000000110',
'110000000000000000000',
'011010001011000111111',
'010100011011000001100',
'010110111011011001100',
'010110001011011001100',
'000000101000010000000',
'000000011111100000000']

# for x, row in enumerate(ant):
#     for y, col in enumerate(row):
#         if col == "1":
#             display.pixel(y+10, x, 1)
#
# for x, row in enumerate(logo):
#     for y, col in enumerate(row):
#         if col == "1":
#             display.pixel(y+105, x+16, 1)
#
# for x, row in enumerate(battery_full):
#     for y, col in enumerate(row):
#         if col == "1":
#             display.pixel(y+100, x, 1)
count = 0

# def dispOled(l1,l2,l3,l4):
#     display.fill(0)
#     display.text(l1, 1, 0)
#     display.text(str(machine.freq()/1000000) + 'MHz', 1, 10)
#     print('CPU: ' + str(machine.freq()/1000000) + 'MHz')
#     display.text(sys.platform + " " + sys.version, 1, 20)
#     display.text("V:" + sys.version, 1, 30)
#     display.text("C:{}".format(count), 1, 40)
#     print(sys.platform + " " + sys.version)
#     display.show()

def dispOled(strList):
    display.fill(0)
    lineY = 0
    for line in strList:
        display.text('L{}:{}'.format(lineY,line), 1, lineY*10)
        lineY += 1
    display.show()

import time
# import signal

while True:
    # if input() == 'q':
    #     print('End of loop')
    #     break
    count += 1
    if count > 2000:
        break
    strList = list()
    for i in range(6):
        strList.append(count+i)
    dispOled(strList)
    time.sleep(1)
