import socket
import machine
import network
from machine import PWM
from machine import ADC
from machine import UART

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
    sta.connect("UTTEC-8764b1", "123456789a")

# wifiAp()
wifiSta()

def webServer():
    print('------------------------- Setup Ap End -------------')
    uart1 = UART(1, 115200)#pin gpio2 only tx
    # uart2 = UART(2, 115200)
    adc = ADC(0) #max 1023

    #HTML to send to browsers
    html = """<!DOCTYPE html>
    <html>
    <head> <title>ESP8266 LED ON/OFF</title>
        <meta charset="utf-8">
    </head>
    <h2> 위브 하늘채 휘트니스 센터 </h2>
    <h2>세주 런닝 머신 컨트롤</h2>

    <h3>made by UTTEC, 임호균 선생 주문</h3>
    <h3>2018.04.19</h3>

    <form>
    LED RED&nbsp;&nbsp;:
    <button name="LED" value="ON_RED" type="submit">LED ON</button>
    <button name="LED" value="OFF_RED" type="submit">LED OFF</button><br><br>
    LED BLUE:
    <button name="LED" value="ON_BLUE" type="submit">LED ON</button>
    <button name="LED" value="OFF_BLUE" type="submit">LED OFF</button><br><br>
    LED Extern:
    <button name="LED" value="ON_EX" type="submit">LED ON</button>
    <button name="LED" value="OFF_EX" type="submit">LED OFF</button>
    </form>
    </html>
    """

    # spi = machine.SPI(1, baudrate=5000000, polarity=0, phase=0)

    spi = machine.SPI(1, baudrate=5000000, polarity=0, phase=0)

    cs = machine.Pin(15, machine.Pin.OUT)
    cs.on()


    #Setup PINS
    # LED_RED = machine.Pin(4, machine.Pin.OUT)
    LED_RED = machine.Pin(4, machine.Pin.OUT)
    button = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
    # LED_EX = machine.Pin(16, machine.Pin.OUT)
    LED_EX = PWM(machine.Pin(12)) # basic 500Hz
    # pins 0, 2, 4, 5, 12, 13, 14 and 15 all support PWM
    LED_EX.freq(1000) #1KHzO

    #Setup Socket WebServer
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind(('', 80))
    s.bind(addr)
    s.listen(5)
    print('listening on', addr)
    while True:
        conn, addr = s.accept()
        print("Got a connection from %s" % str(addr))
        request = conn.recv(1024)
        print("Content = %s" % str(request))
        request = str(request)
        LEDON_RED = request.find('ON_RED')
        # LEDON_RED = request.find('/?LED=ON_RED')
        LEDOFF_RED = request.find('/?LED=OFF_RED')
        LEDON_BLUE = request.find('/?LED=ON_BLUE')
        LEDOFF_BLUE = request.find('/?LED=OFF_BLUE')
        LEDON_EX = request.find('/?LED=ON_EX')
        LEDOFF_EX = request.find('/?LED=OFF_EX')
        print('LEDON_RED:{}'.format(LEDON_RED))
        if LEDON_RED == 6:
            print('TURN LED0 ON')
            LED_RED.on()
        if LEDOFF_RED == 6:
            print('TURN LED0 OFF')
            LED_RED.off()

        if LEDON_BLUE == 6 or LEDOFF_BLUE == 6:
            if button.value():
                print('button high')
            else:
                print('button low')
            print(adc.read())
            uart1.write('UU')

            cs.off()
            data = spi.read(4)
            cs.on()

        if LEDON_EX == 6:
            print('TURN LED12 ON')
            LED_EX.duty(700)
            # LED_EX.on()
        if LEDOFF_EX == 6:
            print('TURN LED12 OFF')
            LED_EX.duty(512)
            # LED_EX.off()

        response = html

        conn.send(response)
        conn.close()
webServer()
