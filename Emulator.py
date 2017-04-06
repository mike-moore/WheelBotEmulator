import logging, sys, threading, time
from subprocess import Popen, PIPE, STDOUT

# Used for re-directing Trick sim output to /dev/null
try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

from SerialEmulator import SerialEmulator
from CmdResponseDefinitions import *
import comm_packet_pb2
from variable_server import VariableServer


class Emulator(object):
	def __init__(self):
		self.serialEmulator = SerialEmulator()
		self.simThread = threading.Thread(target=self.runSim) 
		self.simThread.daemon = True
		self.runSimThread = False
		self.variableServer = None
		self.ActiveWayPoint = comm_packet_pb2.WayPoint(Name="", Distance=0.0, Heading=0.0)
		self.WayPointList = []
		self.WbTlmPacket = None

	def run(self):
		self.runSimThread = True
		self.simThread.start()

	def stop(self):
		self.runSimThread = False
		self.variableServer.close()

	def runSim(self):
		print "Launching WheelBot Sim ... "
		self.launchSim("./trick_sim")
		time.sleep(2.0)
		print "Attempting to make variable server connection ... "
		self.variableServer = VariableServer('localhost', 45442)
		while self.runSimThread:
			raw_cmd = self.serialEmulator.read()
			if raw_cmd:
				# Construct a new tlm packet to send back
				self.WbTlmPacket = comm_packet_pb2.TelemetryPacket()
				# Fill with data received from Trick sim
				self.WbTlmPacket.MeasuredHeading = self.variableServer.get_value('veh.vehicle.heading', type_=float) 
				self.WbTlmPacket.MeasuredDistance = self.variableServer.get_value('veh.vehicle.arrivalDistance', type_=float, units='ft') 
			    # Handle commands
				rcvd_cmd = self.unpackCmdRcvd(raw_cmd)
				self.handleCmd(rcvd_cmd)
				self.sendWheelBotTlm()
			time.sleep(0.1)

	def launchSim(self, s_main_dir):
		try:
			Popen(["./S_main_Linux_5.4_x86_64.exe", "RUN_emulator/input.py"], cwd=s_main_dir, stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
		except OSError:
			logging.error("The WheelBot Trick sim has not been built. Change into the trick_sim directory \
                           and run the following command: \"make spotless; trick-CP\"")
		return

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
		if self.ActiveWayPoint.Name != "":
			logging.info("Busy targetting : " + self.ActiveWayPoint.Name)
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
		return self.WbTlmPacket.SerializeToString()

# Used if you want to run the emulator as a main program.
def main():
	emulator = Emulator()
	emulator.run()
	while threading.active_count() > 0:
	    time.sleep(0.02)

if __name__ == "__main__":
    main()