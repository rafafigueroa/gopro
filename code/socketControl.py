import socket
import time

HOST = '10.1.1.128'
PORT = 50007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.sendall('35')
#time.sleep(1)
s.sendall('50')
time.sleep(1)
s.sendall('0')
#s.sendall('0')
s.close()

