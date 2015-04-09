import socket
import os 
import serial
import time

ser = serial.Serial("/dev/ttyMFD1",19200)
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50017              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
mtrCmd = bytearray()
mtrCmd.append(0xC2)
mtrCmd.append(0x00)
mtrStop = bytearray()
mtrStop.append(0xC2)
mtrStop.append(0x00)

def processData(conn):
	global mtrCmd
	global mtrStop
	global ser

	while 1:
		data = conn.recv(1024)
		if not data: break
		print "Recvd:" + data
		spd = int(float(data))
		spd = -spd
		if spd > 0 and spd < 30:
			spd =30 
		if spd < 0 and spd > -30:
			spd = -30 

		print "Speed: ", spd
		if spd < 0:
			mtrCmd[0] = 0xC1
			spd = -spd
		else:
			mtrCmd[0] = 0xC2

		mtrCmd[1]  = spd
		print "Motor Command:" +  mtrCmd
		print ser.write(mtrCmd) 
		time.sleep(.005)
		ser.write(mtrStop)
	
while 1:
	conn, addr = s.accept()
	processData(conn)
 
conn.close()
