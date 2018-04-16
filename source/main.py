import os
import time

print(os.listdir())
with open('myfile.txt', 'w') as f:
    f.write('This is hong 8266')
print(os.listdir())
with open('myfile.txt','r') as f:
    print(f.read())

count = 0
while True:
    if count > 5:
        break
    print('count{}'.format(count))
    count += 1
    time.sleep(1)

# Echo server program
import socket
print('now start server')
HOST = ''                 # Symbolic name meaning the local host
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
while 1:
    data = conn.recv(1024)
    if not data:
        break
    print('return data to client',str(data))
    conn.send(data)
print('close socket')
conn.close()

s = input('wait input -->')
