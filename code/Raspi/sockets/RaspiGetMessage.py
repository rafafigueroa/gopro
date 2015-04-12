import socket
import serial
import time

ser = serial.Serial("/dev/ttyAMA0",19200)
HOST = 'turtlercv' 
PORT = 50050              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print "Connected to Host!"

while (1):
	msg = ser.read(10) + "\n"
	print "Received {0}".format(setup)

	print "Sending to Agent..."
	s.sendall(msg)
