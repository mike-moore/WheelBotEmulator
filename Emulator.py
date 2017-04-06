import logging, sys, threading, time, math
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
from variable_server import VariableServer, Variable


class Emulator(object):
	def __init__(self):
		self.serialEmulator = SerialEmulator()
		self.simThread = threading.Thread(target=self.runSim) 
		self.simThread.daemon = True
		self.simUpdatePeriod = 0.1
		self.runSimThread = False
		self.variableServer = None
		self.varServerSamplingPeriod = 0.1
		self.SimHeading = 0.0
		self.SimDistance = 0.0
		self.WayPointReached = 0.0
		self.ActiveWayPoint = comm_packet_pb2.WayPoint(Name="", Distance=0.0, Heading=0.0)
		self.WayPointList = []
		self.WbTlmPacket = comm_packet_pb2.TelemetryPacket(MeasuredHeading=0.0, MeasuredDistance=0.0)

	def run(self):
		self.runSimThread = True
		self.simThread.start()

	def stop(self):
		self.runSimThread = False
		if self.variableServer:
			self.variableServer.close()

	def runSim(self):
		self.setupVariableServer()
		while self.runSimThread:
			raw_cmd = self.serialEmulator.read()
			if raw_cmd:
				# Construct a new tlm packet to send back
				self.WbTlmPacket = comm_packet_pb2.TelemetryPacket()
			    # Handle commands
				rcvd_cmd = self.unpackCmdRcvd(raw_cmd)
				self.handleCmd(rcvd_cmd)
				self.sendWheelBotTlm()
			time.sleep(self.simUpdatePeriod)

	def setupVariableServer(self):
		try:
			logging.info("Attempting to make variable server connection ... ")
			self.variableServer = VariableServer('localhost', 45442)
			self.TrickSimMeasuredHeading = Variable('veh.vehicle.heading', type_=float)
			self.TrickSimMeasuredDistance = Variable('veh.vehicle.arrivalDistance',  type_=float, units='ft')
			self.TrickSimWayPointReached = Variable('veh.vehicle.vehicleController[0].WayPointReached', type_=int)
			self.variableServer.add_variables(self.TrickSimMeasuredHeading, self.TrickSimMeasuredDistance, self.TrickSimWayPointReached)
			self.variableServer.set_period(self.varServerSamplingPeriod)
			self.variableServer.register_callback(self.processSimData)
		except:
			logging.error("Failed to make variable server connection. Be sure to run the Trick sim first.")
			self.stop()
			raise IOError

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
		# point (we're not currently navigating to a waypoint)
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
		waypt_x =  self.ActiveWayPoint.Distance * math.cos(self.ActiveWayPoint.Heading)
		waypt_y =  self.ActiveWayPoint.Distance * math.sin(self.ActiveWayPoint.Heading)
		self.variableServer.send('veh.vehicle.vehicleController[0].add_waypoint({0}, {1})'.format(waypt_x, waypt_y))

	def handleRoverCmd(self, cmd):
		if cmd.Id == WP_GET_ACTIVE:
			self.WbTlmPacket.ActiveWayPoint = self.ActiveWayPoint.Name

	def sendWheelBotTlm(self):
		self.serialEmulator.write(self.packTelemetry())

	def processSimData(self):
		# Fill with data received from Trick sim
		self.SimHeading = self.TrickSimMeasuredHeading.value
		self.SimDistance = self.TrickSimMeasuredDistance.value
		self.WayPointReached = self.TrickSimWayPointReached.value
		# Check if we reached our way point yet. If so, clear the 
		# active way point
		if self.WayPointReached == 1:
			logging.info("Waypoint reached")
			self.ActiveWayPoint.Name = ''
			self.WayPointReached = 0

	def packTelemetry(self):
		self.WbTlmPacket.MeasuredHeading = self.SimHeading
		self.WbTlmPacket.MeasuredDistance = self.SimDistance
		return self.WbTlmPacket.SerializeToString()


# Used if you want to run the emulator as a main program.
def main():
	emulator = Emulator()
	emulator.run()
	while threading.active_count() > 0:
	    time.sleep(0.02)

if __name__ == "__main__":
    main()