import os, pty, serial, time


class Emulator(object):
	def __init__(self):
	    master, slave = pty.openpty()
	    masterPortName = os.ttyname(master)
	    slavePortName = os.ttyname(slave)
	    print 'MASTER: ' + str(masterPortName)
	    print 'SLAVE: ' + str(slavePortName)
	    self.serialPort = serial.Serial(port=masterPortName, baudrate=115200, rtscts=True, dsrdtr=True)
	    if self.serialPort.isOpen():
  	    	print 'WheelBot emulator running on port : ' + masterPortName

	def listen(self):
		while True:
			print 'Waiting for data...'
			while self.serialPort.inWaiting() > 0:
				print 'Received message'
				out += self.serialPort.read(1)
			time.sleep(0.5)
			self.sendWheelBotTlm()

	def sendWheelBotTlm(self):
	    self.serialPort.write('Hello world\n')


def main():
	emulator = Emulator()
	emulator.listen()


if __name__ == "__main__":
    main()