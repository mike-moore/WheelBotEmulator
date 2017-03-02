import wb_comm_if_pb2

class Simulator(object):
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
