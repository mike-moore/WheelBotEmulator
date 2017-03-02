import argparse, time
from SerialCommunication import SerialCommunication
from WayPoint import WayPoint

class CommandAndTracking(object):
	def __init__(self):
		self.SerialComm = None
		self.WayPointList = []
		self.ActiveWayPoint = WayPoint(3.0, 45.0)
		self.ConnectedToWheelBot = False

	def connectToWheelBot(self, serial_comm):
		self.SerialComm = serial_comm
		self.SerialComm.run()
		self.ConnectedToWheelBot = True

	def disconnectFromWheelBot(self):
		self.SerialComm.stop()
		self.ConnectedToWheelBot = False

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
				self.ActiveWayPoint = way_point
				self.reachWayPoint()

	def getWheelBotData(self):
		 if self.isConnected():
			return self.SerialComm.getTelemetry()

	def reachWayPoint(self):
		while not self.ActiveWayPoint.Reached:
			self.printActiveWayPoint()
			self.commandActiveWayPoint()
			time.sleep(1.0)
			wbData = self.getWheelBotData()
			self.printWbData(wbData)
			self.ActiveWayPoint.Reached = wbData.WayPointCmdReached

	def commandActiveWayPoint(self):
		self.SerialComm.commandWayPoint(self.ActiveWayPoint)

	def printActiveWayPoint(self):
		print "Tracking way-point : "
		self.ActiveWayPoint.displayWayPoint()

	def printWbData(self, wbData):
		print "WheelBot Data Received ... "
		print "Obstacle Distance         : " + str(wbData.ObstacleDistance)
		print "Heading                   : " + str(wbData.Heading)
		print "Drive Distance Estimate   : " + str(wbData.DriveDistanceEstimate)
		print "WayPoint Command Accepted : " + str(wbData.WayPointCmdAccepted)
		print "WayPoint Command Rejected : " + str(wbData.WayPointCmdRejected)
		print "WayPoint Command Reached  : " + str(wbData.WayPointCmdReached)
		

		

