
class WayPoint(object):
	def __init__(self, distance=0.0, heading=0.0):
		self.Distance = distance
		self.Heading = heading
		self.Active = False
		self.Reached = False

	def activate(self):
		self.Active = True