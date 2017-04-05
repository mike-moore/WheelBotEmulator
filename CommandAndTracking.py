import argparse, time, logging
from SerialCommunication import SerialCommunication
from CmdResponseDefinitions import *
import comm_packet_pb2

class CommandAndTracking(object):
	def __init__(self):
		self.SerialComm = None
		self.WayPointList = []
		self.ConnectedToWheelBot = False
		self.ActiveWayPointName = "None"

	def connectToWheelBot(self, serial_comm):
		self.SerialComm = serial_comm
		if self.SerialComm.serialPort.isOpen():
			self.ConnectedToWheelBot = True

	def isConnected(self):
		if not self.ConnectedToWheelBot:
			print 'Not connected to WheelBot. Cannot get telemetry data.'	
			return False
		else:
			return True

	def loadWayPoints(self, list_way_points):
		self.WayPointList = list_way_points

	def commandRoute(self):
		if self.isConnected():
			for way_point in self.WayPointList:
				self.reachWayPoint(way_point)
				logging.info("Attempting to command WayPoint : " + way_point.Name)
				time.sleep(5.0)

	def getActiveWayPoint(self):
		cmd_packet = comm_packet_pb2.CommandPacket()
		request_active_waypoint = cmd_packet.RoverCmds.add()
		request_active_waypoint.Id = WP_GET_ACTIVE
		response = self.SerialComm.commandArduino(cmd_packet)
		if response:
			logging.info("WheelBot's Active WayPoint is : " + response.ActiveWayPoint)
			logging.info("WheelBot's Measured Heading is : " + str(response.MeasuredHeading))
			logging.info("WheelBot's Measured Distance is : " + str(response.MeasuredDistance))
			return response.ActiveWayPoint
		else:
			return "None"

	def reachWayPoint(self, way_point):
		self.ActiveWayPointName = self.getActiveWayPoint()
		if self.ActiveWayPointName != way_point.Name:
			cmd_packet = comm_packet_pb2.CommandPacket()
			cmd_packet.WayPointCmd.Heading = way_point.Heading
			cmd_packet.WayPointCmd.Distance = way_point.Distance
			cmd_packet.WayPointCmd.Name = way_point.Name
			self.SerialComm.commandArduino(cmd_packet)


		

		

