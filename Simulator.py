import wb_comm_if_pb2
import time, math, threading
from WayPoint import WayPoint

class Simulator(object):
	def __init__(self):
		self.wayPointList = []
		self.ActiveWayPoint = WayPoint(name="NoName", distance=0.0, heading=0.0)
		self.rotationalVel = 10.0 # deg/s
		self.translationalVel = 0.25 # m/s
		self.heading = 0.0
		self.distanceTraveled = 0.0
		self.positionX = 0.0
		self.positionY = 0.0
		self.timeStep = 0.1
		self.simulationThread = threading.Thread(target=self.simThread) 
		self.simulationThread.daemon = True
		self.active = False
		self.lastPassPosError = False
		self.lastPassNegError = False
		return

	def run(self):
		self.active = True
		self.simulationThread.start()

	def stop(self):
		self.active = False

	def setTimeStep(self, timeStep):
		self.timeStep = timeStep

	def simThread(self):
		while self.active:
			if self.wayPointList:
				self.ActiveWayPoint = self.wayPointList.pop(0)
				self.ActiveWayPoint.Active = True
				self.rotateToWayPoint(self.ActiveWayPoint)
				self.translateToWayPoint(self.ActiveWayPoint)
				self.ActiveWayPoint.Reached = True

	def rotateToWayPoint(self, way_point):
		errorHeading = way_point.Heading - self.heading
		while abs(errorHeading) > self.rotationalVel*0.1:
			if errorHeading > 0:
				self.heading += self.rotationalVel * self.timeStep
			else:
				self.heading -= self.rotationalVel * self.timeStep
			errorHeading = way_point.Heading - self.heading
			time.sleep(self.timeStep)

	def translateToWayPoint(self, way_point):
		self.distanceTraveled = 0.0
		errorDistance = way_point.Distance
		while abs(errorDistance) > self.translationalVel*0.1:
			if errorDistance > 0:
				self.distanceTraveled += self.translationalVel * self.timeStep
				self.lastPassPosError = True
				# Check for oscillating error
				if self.lastPassNegError:
					self.lastPassPosError = False
					self.lastPassNegError = False
					return
			else:
				self.distanceTraveled -= self.translationalVel * self.timeStep
				self.lastPassNegError = True
				# Check for oscillating error
				if self.lastPassPosError:
					self.lastPassPosError = False
					self.lastPassNegError = False
					return
			errorDistance = way_point.Distance - self.distanceTraveled
			time.sleep(self.timeStep)
		self.positionX += self.distanceTraveled*math.sin(math.radians(self.heading))
		self.positionY += self.distanceTraveled*math.cos(math.radians(self.heading))


	def addWayPoint(self, way_point):
		if not self.active:
			print "Simulation is not active. Use Simulation.run() routine to start up the simulation."
			return
		self.wayPointList.append(way_point)

	def getSimData(self):
		wb_data = wb_comm_if_pb2.WheelBotTelemetry()
		wb_data.ObstacleDistance = 2.5
		wb_data.Heading = self.heading
		wb_data.DriveDistanceEstimate = self.distanceTraveled
		wb_data.WayPointCmdReached = self.ActiveWayPoint.Reached
		return wb_data


