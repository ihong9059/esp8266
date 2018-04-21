import socket
import network
import time

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
#    sta.connect("UTTEC-8764b1", "123456789a")
    sta.connect("utsol_tc140", "09090909")

wifiAp()
wifiSta()

def Server():
    print('--------------- start Server -------------')    #Setup Socket WebServer
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    sock.bind(('192.168.4.1', 80))
    sock.bind('',80)
#    sock.bind(addr)
    sock.listen(5)
    print('listening on', addr)
    count = 0

    while True:
        conn, addr = sock.accept()
        print("Got a connection from %s" % str(addr))
        request = conn.recv(1024)
        print("Content = %s" % str(request))
        response = 'I Received:: {}'.format(count)
        count += 1
        conn.send(response)
        conn.close()
        print(str(addr)+'close')

def Client():
    print('--------------- Wait 5Sec -------------')    #Setup Socket WebServer
    time.sleep(5)
    print('--------------- start Client -------------')    #Setup Socket WebServer
    # host='192.168.4.1'    #my Computer Address
    host='192.168.185.12'  #Windows Address
    port=80
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    while True:
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((host,port))
        sock.send(b'Hello, python Server')
        data=sock.recv(1024)
        sock.close()
        print('Received',repr(data))
        time.sleep(1)

Server()
#Client()
