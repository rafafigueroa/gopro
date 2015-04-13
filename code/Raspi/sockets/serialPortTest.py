import serial
import time

while (1):
	sp = serial.Serial('/dev/ttyAMA0',19200)
	sp.flush()
	setup = sp.read(10)
	print "Received {0}".format(setup)
	sp.close()

	#sp = serial.Serial('/dev/ttyAMA0', int(setup))
	#sp.flush()
	#print "Serial port opened at {0:d}".format(int(setup))
	#print "Reading 10 characters..."
	#recv = sp.read(10)
	#time.sleep(1)
	#sp.flush()
	#sp.close()
	#print recv

