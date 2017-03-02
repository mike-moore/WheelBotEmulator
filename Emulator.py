import time, threading
from SerialEmulator import SerialEmulator
from WayPoint import WayPoint
import wb_comm_if_pb2

class Emulator(object):
	def __init__(self):
		self.serialEmulator = SerialEmulator()
		self.listenThread = threading.Thread(target=self.listen) 
		self.listenThread.daemon = True
		self.runThread = False
		self.activeWayPoint = None
		self.wbTelemetry = wb_comm_if_pb2.WheelBotTelemetry()
		if self.serialEmulator.serial.isOpen():
			print 'WheelBot emulator running on port : ' + self.serialEmulator.device_port
			print 'WheelBot emulator clients should connect through port : ' + self.serialEmulator.client_port

	def run(self):
		self.runThread = True
		self.listenThread.start()

	def stop(self):
		self.runThread = False

	def listen(self):
		while self.runThread:
			cmd = self.serialEmulator.read()
			if cmd:
				self.processCmdRcvd(cmd)
			self.sendWheelBotTlm()
			time.sleep(0.1)

	def processCmdRcvd(self, cmd):
		print "Way-Point command received ... "
		self.activeWayPoint = self.unpackRawCmd(cmd)
		self.activeWayPoint.displayWayPoint()

	def unpackRawCmd(self, raw_cmd):
		# Create a proto-buf WayPoint command based on the one
		# passed in to this function.
		way_point_cmd = wb_comm_if_pb2.WayPoint()
		way_point_cmd.ParseFromString(raw_cmd)
		return WayPoint(way_point_cmd.Distance,way_point_cmd.Heading)

	def sendWheelBotTlm(self):
		self.packTelemetry()
		self.serialEmulator.write(self.wbTelemetry.SerializeToString())

	def packTelemetry(self):
		self.wbTelemetry.ObstacleDistance = 2.5
		self.wbTelemetry.Heading = 35.0
		self.wbTelemetry.DriveDistanceEstimate = 1.5
		self.wbTelemetry.WayPointCmdReached = True


# Used if you want to run the emulator as a main program.
def main():
	emulator = Emulator()
	emulator.run()
	while threading.active_count() > 0:
	    time.sleep(0.1)

if __name__ == "__main__":
    main()