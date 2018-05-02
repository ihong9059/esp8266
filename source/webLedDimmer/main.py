import usocket as socket
import machine
import network
from dispOled import dispOled
from machine import Pin
from machine import UART
from time import sleep
import os

from frame import Frame

p0 = Pin(0, Pin.IN)
uart = UART(1, 115200)

gCount = 0
def callback(p):
    global gCount
    gCount += 1
    print('pin change', p)
    print('gCount:{}'.format(gCount))
    receive = input('Wait, input your request now==> ')
    sleep(0.2)
    print('I received from Machine:{}'.format(receive))
    # input


p0.irq(trigger = Pin.IRQ_FALLING, handler = callback)

def wifiAp():
    import ubinascii
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)
    essid = b"UTTEC-%s" % ubinascii.hexlify(ap_if.config("mac")[-3:])
    ap_if.config(essid=essid, authmode=network.AUTH_WPA_WPA2_PSK, password=b"123456789a")
    print('mac:',b"UTTEC-%s" % ubinascii.hexlify(ap_if.config("mac")[:]))

def wifiSta():
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    # 8764b1
    # sta.connect("UTTEC-8764b1", "123456789a")
    # sta.connect("uttecSale4", "123456789a")
    sta.connect("utsol_tc140", "09090909")
    # sleep(3)
    count = 0
    while sta.isconnected() == False:
        sleep(1)
        print('wait wifi connection, elapsed Time:{}'.format(count))
        count +=1
    print('My ip Address:{}'.format(sta.ifconfig()))
    print('********************End of wifiSta')

wifiAp()
# wifiSta()

def mySend(conn, msg, MSGLEN):
    # print('MSGLEN:{}'.format(MSGLEN))
    totalsent = 0
    while totalsent < MSGLEN:
        sent = conn.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent
    print('totalsent:{}'.format(totalsent))
    # conn.close()

def sendFrame(gid, pid, level):
    rxtx = 1; sub = 103;
    myFrame = Frame()
    myFrame.rate[0] = 1; myFrame.status[0] = 0;
    myFrame.Type[0] = 1;
    myFrame.setLevel(int(level));

    myFrame.setRxTx(int(rxtx)); myFrame.setSub(int(sub))
    myFrame.setGid(int(gid)); myFrame.setPid(int(pid));
    myFrame.setFrame()
    print('gid:{} pid:{} level:{}'.format(gid, pid, level))
    uart.write('------------ Ctr Start ----------------\r\n')
    uart.write('SendFrame:{}\r\n'.format(myFrame.frame))
    # bslCtrClient.sendSocket(myFrame.getFrame())

def webServer():
    print('------------------------- Setup Ap End -------------')
    print('Files:{}'.format(os.listdir()))
    # html_org = ''
    head = ''
    body = ''
    with open('head.html','r') as f:
        head=f.read()
    with open('body.html','r') as f:
        body=f.read()

    html = head + body

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind(('', 80))
    s.bind(addr)
    s.listen(1)
    print('My Addr:{}'.format(addr))
    count = 0
    dispList = ['SeJu FA','20180425','Red  Off', 'Blue Off','Ex   Off']
    dispOled(dispList)

    while True:
        # html = html_org
        cl, addr = s.accept()
        # toggle = !toggle
        count += 1
        if count%2:
            print("connection from %s, count %d" % (str(addr), int(count/2)))
            # print("Content = %s" % str(request))
        cl_file = cl.makefile('rwb', 0)
        request = ''
        while True:
            line = cl_file.readline()
            request += str(line)
            if not line or line == b'\r\n':
                break
        print('End of receive')
        # request = str(line)
        # print(request)
        ledRedOn = request.find('/?LED=ON_Red')
        ledRedOff = request.find('/?LED=OFF_Red')
        ledBlueOn = request.find('/?LED=ON_Blue')
        ledBlueOff = request.find('/?LED=OFF_Blue')
        ledExOn = request.find('/?LED=ON_Ex')
        ledExOff = request.find('/?LED=OFF_Ex')
        Exit = request.find('/?LED=Exit')

        if ledRedOn == 6 :
            print('Red On')
            sendFrame(3, 3, 100)
            dispList[2] = 'Red   On'
        elif ledRedOff == 6:
            sendFrame(3, 3, 0)
            print('Red Off')
            dispList[2] = 'Red  Off'
        elif ledBlueOn == 6:
            print('Blue On')
            sendFrame(3, 4, 100)
            dispList[3] = 'Blue  On'
        elif ledBlueOff == 6:
            print('Blue Off')
            sendFrame(3, 4, 0)
            dispList[3] = 'Blue Off'
        elif ledExOn == 6:
            print('Ex On')
            sendFrame(3, 5, 100)
            dispList[4] = 'Ex    On'
        elif ledExOff == 6:
            print('Ex Off')
            sendFrame(3, 5, 0)
            dispList[4] = 'Ex   Off'
        elif Exit == 6:
            print('Exit')

        length = cl.write(html)
        # print('Send length:{}'.format(length))
        cl.close()
        dispOled(dispList)
        print('End of connection')

if __name__ == '__main__':
    webServer()
