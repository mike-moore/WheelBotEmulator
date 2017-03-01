import os, pty, serial, time, argparse

class SerialCommunication(object):
	def __init__(self, portName):
	    self.serialPort = serial.Serial(port=portName, baudrate=115200, rtscts=True,dsrdtr=True)
	    if self.serialPort.isOpen():
  	    	print 'WheelBot CTS running on port : ' + portName

	def runComm(self):
		while True:
			out = ''
			while self.serialPort.inWaiting() > 0:
				print 'data received'
				out += self.serialPort.read(1)
			if out != '':
				print 'Received message'
				print ">> " + out
			self.sendCommands()
			time.sleep(1.0)

	def sendCommands(self):
		print 'Sending commands ... '
		self.serialPort.write("Sending commands \n")



# class CommandAndTracking(object):
# 	def __init__(self):
# 	    master, slave = pty.openpty()
# 	    portName = os.ttyname(slave)
# 	    self.serialPort = serial.Serial(portName)
# 	    print 'WheelBot CTS running on port : ' + portName

# 	def sendWheelBotTlm(self):
# 	    self.serialPort.write('Hello world\n')



def main():
	# Define command line options using argparse
	argParser = argparse.ArgumentParser()
	argParser.add_argument("-p",  "--port", type=str, help="Specify the serial port to use for communication with WheelBot.")
	args = argParser.parse_args()
	wb_comm = SerialCommunication(args.port)
	wb_comm.sendCommands()
	wb_comm.runComm()

if __name__ == "__main__":
	main()