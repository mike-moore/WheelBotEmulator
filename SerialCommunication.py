import serial, time, threading
from collections import deque
import wb_comm_if_pb2

class SerialCommunication(object):
	def __init__(self, portName):
		self.serialPort = serial.Serial(port=portName, baudrate=9600, rtscts=True,dsrdtr=True)
		self.readTelemetryThread = threading.Thread(target=self.readTelemetry) 
		self.readTelemetryThread.daemon = True
		self.active = False
		self.wbTlmQueue = deque(maxlen=10)
		if self.serialPort.isOpen():
			print 'WheelBot serial communication running on port : ' + portName

	def run(self):
		self.active = True
		self.readTelemetryThread.start()

	def stop(self):
		self.active = False

	def getTelemetry(self):
		try:
			return self.wbTlmQueue.popleft()
		except IndexError:
			print 'No telemetry data available. Is your WheelBot connection active?'

	def readTelemetry(self):
		while self.active:
			bytes_rcvd = self.readRawBytes()
			if bytes_rcvd:
				self.unpackTelemetry(bytes_rcvd)
			time.sleep(0.1)

	def sendCommand(self, cmd):
		self.serialPort.write(cmd)

	def commandWayPoint(self, way_point):
		# Create a proto-buf WayPoint command based on the one
		# passed in to this function.
		waypoint_msg_cmd = wb_comm_if_pb2.WayPoint()
		# Populate all required fields
		waypoint_msg_cmd.Distance = way_point.Distance
		waypoint_msg_cmd.Heading = way_point.Heading
		# Send down the serialized command
		self.sendCommand(waypoint_msg_cmd.SerializeToString())

	def readRawBytes(self):
		bytes_read = ''
		while self.serialPort.inWaiting() > 0:
			bytes_read += self.serialPort.read(1)
		return bytes_read

	def unpackTelemetry(self, raw_bytes):
		wb_tlm = wb_comm_if_pb2.WheelBotTelemetry()
		wb_tlm.ParseFromString(raw_bytes)
		self.wbTlmQueue.appendleft(wb_tlm)


