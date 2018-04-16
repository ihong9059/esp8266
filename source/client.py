# Echo client program
import socket

HOST = '192.168.4.255'    # The remote host
# HOST = '192.168.4.1'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.send(b'Hello, world')
data = s.recv(1024)
s.close()
print( 'Client Received from server', repr(data))
