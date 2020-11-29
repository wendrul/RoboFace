import serial, time
arduino = serial.Serial('COM4', 115200, timeout=.1, write_timeout=.1)
time.sleep(3) #give the connection a second to settle
arduino.write(b"ask bound\r\n")
while True:
	data = arduino.readline()
	if data:
		print (data) #strip out the new lines for now
		# (better to do .read() in the long run for this reason