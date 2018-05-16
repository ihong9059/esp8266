import usocket as socket
import machine
import network
from machine import Pin
from machine import UART
from time import sleep
import os
# import crc
from frame import Frame
from dispOled import dispOled
# from crc import Crc

# myHks = Crc()

p0 = Pin(0, Pin.IN)
pinRed=Pin(5, machine.Pin.OUT)
pinBlue=Pin(4, machine.Pin.OUT)
pinEx=Pin(14, machine.Pin.OUT)

uart = UART(1, 115200)

# uartInput = ''
gCount = 0

def uartCallback(p):
    global gCount
    gCount += 1
    print('pin change', p)
    print('gCount:{}'.format(gCount))
    uartInput = input('Wait, input your request now==> ')
    print('I received from Machine:{}'.format(uartInput))
    myFrame.parseFrame(uartInput)
    # input

p0.irq(trigger = Pin.IRQ_FALLING, handler = uartCallback)

def wifiAp():
    import ubinascii
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)
    essid = b"UTTEC-%s" % ubinascii.hexlify(ap_if.config("mac")[-3:])
    ap_if.config(essid=essid, authmode=network.AUTH_WPA_WPA2_PSK, password=b"123456789a")
    print('mac:',b"UTTEC-%s" % ubinascii.hexlify(ap_if.config("mac")[:]))

def wifiStationOn():
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    # 8764b1
    # sta.connect("UTTEC-8764b1", "123456789a")
    # sta.connect("uttecSale4", "123456789a")
    sta.connect("utsol_tc140", "09090909")
    count = 0
    while sta.isconnected() == False:
        sleep(1)
        print('wait wifi connection, elapsed Time:{}'.format(count))
        count +=1
    print('My ip Address:{}'.format(sta.ifconfig()))
    print('Files:{}'.format(os.listdir()))
    print('********************End of wifiStation')

def wifiStationOff():
    sta = network.WLAN(network.STA_IF)
    sta.active(False)

wifiAp()
wifiStationOn()

myFrame = Frame()

def sendFrame(gid, pid, level):
    rxtx = 1; sub = 103;
    myFrame = Frame()
    myFrame.rate[0] = 1; myFrame.status[0] = 0;
    myFrame.Type[0] = 1;
    myFrame.level[0] = int(level);

    myFrame.rxtx[0]= int(rxtx); myFrame.sub[0] = int(sub);
    myFrame.gid[0] = int(gid); myFrame.pid[0] = int(pid);
    myFrame.setFrame()
    # print('gid:{} pid:{} level:{}'.format(gid, pid, level))
    uart.write('------------ Ctr Start ----------------\r\n')
    uart.write('SendFrame:{}\r\n'.format(myFrame.frame))

count = 0
dispList = ['SeJu FA','20180425','Red  Off', 'Blue Off','Ex   Off']

def procMain(cl,addr):
    global count
    global dispList

    returnList = list()
    count += 1
    if count%2:
        print("connection from %s, count %d" % (str(addr), int(count/2)))
    cl_file = cl.makefile('rwb', 0)
    request = ''
    while True:
        line = cl_file.readline()
        request += str(line)
        if not line or line == b'\r\n':
            break
    print(request)
    ledRedOn = request.find('/?LED=ON_Red')
    ledRedOff = request.find('/?LED=OFF_Red')
    ledBlueOn = request.find('/?LED=ON_Blue')
    ledBlueOff = request.find('/?LED=OFF_Blue')
    ledExOn = request.find('/?LED=ON_Ex')
    ledExOff = request.find('/?LED=OFF_Ex')
    Exit = request.find('/?LED=Exit')
    result = ''
    if ledRedOn == 6 :
        result = 'Red On'
        print('Red On')
        sendFrame(3, 3, 100)
        dispList[2] = 'Red   On'
        pinRed.off()
    elif ledRedOff == 6:
        result = 'Red Off'
        sendFrame(3, 3, 0)
        print('Red Off')
        dispList[2] = 'Red  Off'
        pinRed.on()
    elif ledBlueOn == 6:
        result = 'Blue On'
        print('Blue On')
        sendFrame(3, 4, 100)
        dispList[3] = 'Blue  On'
        pinBlue.off()
    elif ledBlueOff == 6:
        result = 'Blue Off'
        print('Blue Off')
        sendFrame(3, 4, 0)
        dispList[3] = 'Blue Off'
        pinBlue.on()
    elif ledExOn == 6:
        result = 'Ex On'
        print('Ex On')
        sendFrame(3, 5, 100)
        dispList[4] = 'Ex    On'
        pinEx.off()
    elif ledExOff == 6:
        result = 'Ex Off'
        print('Ex Off')
        sendFrame(3, 5, 0)
        dispList[4] = 'Ex   Off'
        pinEx.on()
    elif Exit == 6:
        result = 'Exit'
        pinBlue.on()
        pinRed.on()
        pinEx.on()
        exitFlag = True
        print('Exit')
    dispOled(dispList)

    return result

def procHtml(cl, html, result):
    findStr = '<h3>2018.05.03</h3>'
    findIndex = html.find(findStr)

    # global uartInput
    uartInput = 'I Received'
    print()
    newHtml = html[:findIndex]+'<h2>New String:::'+result+'</h2>'+html[findIndex:]
    length = cl.write(newHtml)
    print('length:{}'.format(length))
    cl.close()

def webServer():
    global dispList
    print('------------------------- Setup Ap End -------------')
    print('Files:{}'.format(os.listdir()))
    # uart2IRQ = uart.irq(trigger = UART.RX_ANY, priority = 1, handler = irq_uart, wake=machine.IDLE)
    # html_org = ''
    # head = ''
    # body = ''
    with open('head.html','r') as f:
        html=f.read()
    with open('body.html','r') as f:
        html += f.read()

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind(('', 80))
    s.bind(addr)
    s.listen(1)
    print('My Addr:{}'.format(addr))
    dispOled(dispList)

    exitFlag = False
    while not exitFlag:
        cl, addr = s.accept()
        procHtml(cl, html, procMain(cl, addr))

if __name__ == '__main__':
    webServer()
