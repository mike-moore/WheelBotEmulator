import argparse, time
from SerialCommunication import SerialCommunication
from WayPoint import WayPoint

class CommandAndTracking(object):
	def __init__(self):
		self.SerialComm = None
		self.WayPointList = []
		self.ActiveWayPoint = WayPoint(3.0, 45.0)

	def connectToWheelBot(self, serial_comm):
		self.SerialComm = serial_comm

	def loadWayPoints(self, list_way_points):
		self.WayPointList = list_way_points

	def commandRoute(self):
		for way_point in self.WayPointList:
			self.ActiveWayPoint = way_point
			self.reachWayPoint()

	def reachWayPoint(self):
		while not self.ActiveWayPoint.Reached:
			self.printActiveWayPoint()
			self.commandActiveWayPoint()
			time.sleep(1.0)

	def commandActiveWayPoint(self):
		self.SerialComm.sendCommands()

	def printActiveWayPoint(self):
		print "Tracking way-point : "
		print "Desired distance : " + str(self.ActiveWayPoint.Distance) + " ft "
		print "Desired heading : " + str(self.ActiveWayPoint.Heading) + " degrees "

# define a list of way-points for the purpose of testing
test_waypoint_list = [WayPoint(3.0, 90.0),
                      WayPoint(1.0, 0.0),
                      WayPoint(2.0, 0.0),
                      WayPoint(1.0, 90.0),
                      WayPoint(1.0, 0.0),
                      WayPoint(1.0, 0.0),
                      WayPoint(0.0, 45.0),
                      WayPoint(0.0, 45.0),
                      WayPoint(3.0, 0.0)]
def main():
	# Define command line options using argparse
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument("-p",  "--port", type=str, help="Specify the serial port to use for communication with WheelBot.")
	args = arg_parser.parse_args()
	# Setup WheelBot serial communication system.
	wb_comm = SerialCommunication(args.port)
	# Setup Command and Tracking system.
	wb_cts = CommandAndTracking()
	wb_cts.connectToWheelBot(wb_comm)
	wb_cts.loadWayPoints(test_waypoint_list)
	wb_cts.commandRoute()

if __name__ == "__main__":
	main()