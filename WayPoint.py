
class WayPoint(object):
	def __init__(self, name="NoName", distance=0.0, heading=0.0):
		self.Name = name
		self.Distance = distance
		self.Heading = heading
		self.Active = False
		self.Reached = False

	def activate(self):
		self.Active = True

	def displayWayPoint(self):
		print "WayPoint : " + self.Name
		print "WayPoint Active : " + str(self.Active)
		print "WayPoint Reached : " + str(self.Reached)
		print "Desired distance : " + str(self.Distance) + " ft "
		print "Desired heading : " + str(self.Heading) + " degrees "