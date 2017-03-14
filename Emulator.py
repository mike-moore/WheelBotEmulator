import time, threading
from SerialEmulator import SerialEmulator
from Simulator import Simulator
from WayPoint import WayPoint
import wb_comm_if_pb2

class Emulator(object):
	def __init__(self):
		self.serialEmulator = SerialEmulator()
		self.wbSimulator = Simulator()
		self.listenThread = threading.Thread(target=self.listen) 
		self.listenThread.daemon = True
		self.runThread = False
		self.activeWayPoint = None
		if self.serialEmulator.serial.isOpen():
			print 'WheelBot emulator running on port : ' + self.serialEmulator.device_port
			print 'WheelBot emulator clients should connect through port : ' + self.serialEmulator.client_port

	def run(self):
		self.runThread = True
		self.listenThread.start()

	def stop(self):
		self.runThread = False

	def setSimulator(self, wbSimulator):
		self.wbSimulator = wbSimulator

	def listen(self):
		while self.runThread:
			cmd = self.serialEmulator.read()
			if cmd:
				self.processCmdRcvd(cmd)
			self.sendWheelBotTlm()
			time.sleep(0.1)

	def processCmdRcvd(self, cmd):
		self.activeWayPoint = self.unpackRawCmd(cmd)
		self.wbSimulator.addWayPoint(self.activeWayPoint)

	def unpackRawCmd(self, raw_cmd):
		way_point_cmd = wb_comm_if_pb2.WayPoint()
		way_point_cmd.ParseFromString(raw_cmd)
		return WayPoint(distance=way_point_cmd.Distance,heading=way_point_cmd.Heading)

	def sendWheelBotTlm(self):
		self.serialEmulator.write(self.packTelemetry())

	def packTelemetry(self):
		return self.wbSimulator.getSimData().SerializeToString()



# Used if you want to run the emulator as a main program.
def main():
	emulator = Emulator()
	emulator.run()
	while threading.active_count() > 0:
	    time.sleep(0.1)

if __name__ == "__main__":
    main()