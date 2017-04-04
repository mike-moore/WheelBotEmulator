import time, threading
from SerialEmulator import SerialEmulator
from CmdResponseDefinitions import *
import comm_packet_pb2
import logging

class Emulator(object):
	def __init__(self):
		self.serialEmulator = SerialEmulator()
		self.listenThread = threading.Thread(target=self.listen) 
		self.listenThread.daemon = True
		self.runThread = False
		self.ActiveWayPoint = comm_packet_pb2.WayPoint(Name="", Distance=0.0, Heading=0.0)
		self.WayPointList = []
		self.WbTlmPacket = None

	def run(self):
		self.runThread = True
		self.listenThread.start()

	def stop(self):
		self.runThread = False

	def listen(self):
		while self.runThread:
			raw_cmd = self.serialEmulator.read()
			if raw_cmd:
				# Construct a new tlm packet to send back
				self.WbTlmPacket = comm_packet_pb2.TelemetryPacket()
				rcvd_cmd = self.unpackCmdRcvd(raw_cmd)
				self.handleCmd(rcvd_cmd)
				self.sendWheelBotTlm()
			time.sleep(0.02)

	def unpackCmdRcvd(self, cmd):
		logging.debug("Bytes to be unpacked :")
		logging.debug(":".join("{:02x}".format(ord(c)) for c in cmd))
		# Remove the footer (last four bytes...)
		cmd = cmd[:-4]
		cmd_rcvd = comm_packet_pb2.CommandPacket()
		cmd_rcvd.ParseFromString(cmd)
		return cmd_rcvd

	def handleCmd(self, cmd):
		if cmd.HasField("WayPointCmd"):
			self.handleWayPointCmd(cmd)
		for rover_cmd in cmd.RoverCmds:
			self.handleRoverCmd(rover_cmd)

	def handleWayPointCmd(self, cmd):
		# Reject the waypoint command unless we have an empty active way
		# point (IE we're not currently navigating to a waypoint)
		if self.ActiveWayPoint.Name != "":
			self.rejectWayPointCmd()
		else:
			self.acceptWayPointCmd(cmd.WayPointCmd)

	def rejectWayPointCmd(self):
		logging.info("Rejecting commanded waypoint")
		wp_reject_msg = self.WbTlmPacket.RoverStatus.add()
		wp_reject_msg.Id = WP_CMD_REJECT

	def acceptWayPointCmd(self, way_point):
		logging.info("Accepting commanded waypoint")
		wp_accept_msg = self.WbTlmPacket.RoverStatus.add()
		wp_accept_msg.Id = WP_CMD_ACCEPT
		self.ActiveWayPoint = way_point

	def handleRoverCmd(self, cmd):
		if cmd.Id == WP_GET_ACTIVE:
			self.WbTlmPacket.ActiveWayPoint = self.ActiveWayPoint.Name

	def sendWheelBotTlm(self):
		self.serialEmulator.write(self.packTelemetry())

	def packTelemetry(self):
		self.WbTlmPacket.MeasuredDistance = 2.5
		self.WbTlmPacket.MeasuredHeading = 45.125
		return self.WbTlmPacket.SerializeToString()

# Used if you want to run the emulator as a main program.
def main():
	emulator = Emulator()
	emulator.run()
	while threading.active_count() > 0:
	    time.sleep(0.02)

if __name__ == "__main__":
    main()