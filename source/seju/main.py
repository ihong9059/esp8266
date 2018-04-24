import usocket as socket
import machine
import network
from dispOled import dispOled

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
    sta.connect("utsol_tc140", "09090909")

wifiAp()
wifiSta()

def webServer():
    print('------------------------- Setup Ap End -------------')
    # sta = network.WLAN(network.STA_IF)
    # sta.active(True)
    # sta.connect("utsol_tc140", "09090909")
    # staIp = sta.ifconfig()[0]
    # print('My Ip Address:{}'.format(staIp))

    #HTML to send to browsers
    html = """<!DOCTYPE html>
    <html>
    <head> <title>ESP8266 LED ON/OFF</title>
        <meta charset="utf-8">
    </head>
    <h2> 위브 하늘채 휘트니스 센터 </h2>
    <h2>세주 런닝 머신 컨트롤</h2>

    <h3>made by UTTEC and 세주에프에이</h3>
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
    <button name="LED" value="OFF_EX" type="submit">LED OFF</button><br><br>

    Stop Demo:
    <button name="LED" value="ON_STOP" type="submit">EXIT</button>

    </form>
    </html>
    """
    #Setup Socket WebServer
    # addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    # addr = socket.getaddrinfo('192.168.185.14', 80)[0][-1]
    addr = socket.getaddrinfo('192.168.4.1', 80)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind(('', 80))
    s.bind(addr)
    s.listen(5)
    print('My Addr:{}'.format(addr))
    count = 0
    dispList = ['SeJu FA','20180425','Red  Off', 'Blue Off','Ex   Off']
    dispOled(dispList)

    while True:
        conn, addr = s.accept()
        request = conn.recv(1024)
        count += 1
        if count%2:
            print("connection from %s" % str(addr))
            print("Content = %s" % str(request))
        request = str(request)
        LEDON_RED = request.find('/?LED=ON_RED')
        LEDOFF_RED = request.find('/?LED=OFF_RED')
        LEDON_BLUE = request.find('/?LED=ON_BLUE')
        LEDOFF_BLUE = request.find('/?LED=OFF_BLUE')
        LEDON_EX = request.find('/?LED=ON_EX')
        LEDOFF_EX = request.find('/?LED=OFF_EX')
        EXIT = request.find('/?LED=ON_STOP')
        # print('LEDON_RED:{}'.format(LEDON_RED))
        if LEDON_RED == 6:
            print('Red Led ON')
            dispList[2]='Red   On'
        if LEDOFF_RED == 6:
            print('Red Led OFF')
            dispList[2]='Red  Off'

        if LEDON_BLUE == 6:
            print('Blue Led ON')
            dispList[3]='Blue  On'
        if LEDOFF_BLUE == 6:
            print('Blue Led OFF')
            dispList[3]='Blue Off'

        if LEDON_EX == 6:
            print('External Led ON')
            dispList[4]='Ex    On'
            # LED_EX.on()
        if LEDOFF_EX == 6:
            print('External Led OFF')
            dispList[4]='Ex   Off'
            # LED_EX.off()
        if EXIT == 6:
            print('Bye Bye Seju Demo')
            dispList[2]='Bye Bye'
            dispList[3]='SejuDemo'
            dispList[4]='Good Job'

            dispOled(dispList)
            response = html
            conn.send(response)
            conn.close()
            break

        response = html
        conn.send(response)
        conn.close()

        dispOled(dispList)
if __name__ == '__main__':
    webServer()
