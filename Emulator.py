import time
from SerialEmulator import SerialEmulator

class Emulator(object):
	def __init__(self):
		self.serialEmulator = SerialEmulator()
		if self.serialEmulator.serial.isOpen():
			print 'WheelBot emulator running on port : ' + self.serialEmulator.device_port

	def listen(self):
		while True:
			cmds = self.serialEmulator.read()
			if cmds:
			    print 'Cmds received '
			    print cmds
			    self.sendWheelBotTlm()

	def sendWheelBotTlm(self):
	    self.serialEmulator.write('distance, heading, waypt_reached\n')

def main():
	emulator = Emulator()
	emulator.listen()

if __name__ == "__main__":
    main()