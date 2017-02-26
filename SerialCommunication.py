import serial, time 

class SerialCommunication(object):
	def __init__(self, portName):
	    self.serialPort = serial.Serial(port=portName, baudrate=9600, rtscts=True,dsrdtr=True)
	    if self.serialPort.isOpen():
  	    	print 'WheelBot serial communication running on port : ' + portName

	def runComm(self):
		while True:
			self.sendCommands()
			self.readTelemetry()
			time.sleep(1.0)

	def sendCommands(self):
		print 'Sending commands ... '
		self.serialPort.write("CMD1, CMD2, CMD3 \n")

	def readTelemetry(self):
		bytes_read = ''
		while self.serialPort.inWaiting() > 0:
			bytes_read += self.serialPort.read(1)
		if bytes_read:
			print "Telemetry received ... "
  			print bytes_read

