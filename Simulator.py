import wb_comm_if_pb2
import time

class Simulator(object):
	def __init__(self):
		self.wayPointList = []
		self.rotationalVel = 0.1
		self.translationalVel = 0.1
		self.heading = 0.0
		self.distanceTraveled = 0.0
		self.positionX = 0.0
		self.positionY = 0.0
		self.timeStep = 0.1
		self.headingTolerance = 0.1
		self.distanceTolerance = 0.1
		return

	def run():
		if self.wayPointList:
			activeWayPoint = self.wayPointList.pop()
			rotateToWayPoint(activeWayPoint)
			translateToWayPoint(activeWayPoint)

	def rotateToWayPoint(self, way_point):
		errorHeading = way_point.Heading - self.heading
		while abs(errorHeading) > self.headingTolerance:
			if errorHeading > 0:
				self.heading += self.rotationalVel * self.timeStep
			else:
				self.heading -= self.rotationalVel * self.timeStep
			errorHeading = way_point.Heading - self.heading
			time.sleep(self.timeStep)

	def translateToWayPoint(self, way_point):
		errorDistance = way_point.Distance
		while abs(errorDistance) > self.distanceTolerance:
			if errorDistance > 0:
				self.distanceTraveled += self.translationalVel * self.timeStep
			else:
				self.distanceTraveled -= self.translationalVel * self.timeStep
			errorDistance = way_point.Distance - self.distanceTraveled
			time.sleep(self.timeStep)

	def addWayPoint(self, way_point):
		self.wayPointList.append(way_point)

	def getSimData(self):
		wb_data = wb_comm_if_pb2.WheelBotTelemetry()
		wb_data.ObstacleDistance = 2.5
		wb_data.Heading = self.heading
		wb_data.DriveDistanceEstimate = self.distanceTraveled
		wb_data.WayPointCmdReached = True
		return wb_data


#>>> from variable_server import VariableServer
#>>> variable_server = VariableServer('gheet', 34122)
#>>> variable_server.get_value('veh.vehicle.position[0]')
#'-0.2587201507823507'
#>>> variable_server.get_value('veh.vehicle.heading')

class TrickSimulator(object):
	def __init__(self):
		return

	def addWayPoint(self, way_point):
		return

	def getSimData(self):
		wb_data = wb_comm_if_pb2.WheelBotTelemetry()
		wb_data.ObstacleDistance = 2.5
		wb_data.Heading = 35.0
		wb_data.DriveDistanceEstimate = 1.5
		wb_data.WayPointCmdReached = True
		return wb_data
