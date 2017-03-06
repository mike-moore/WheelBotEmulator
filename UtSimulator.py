#!/usr/bin/python

import unittest
import time
# Use the WheelBot Simulator for this test
from Simulator import Simulator
from WayPoint import WayPoint

# Define a list of way-points for the purpose of testing
test_route_1 = [WayPoint("WayPoint A", 3.0, 90.0),
                WayPoint("WayPoint B", 1.0, 0.0),
                WayPoint("WayPoint C", 2.0, 0.0),
                WayPoint("WayPoint D", 1.0, 90.0),
                WayPoint("WayPoint E", 1.0, 0.0),
                WayPoint("WayPoint F", 1.0, 0.0),
                WayPoint("WayPoint G", 0.0, 45.0),
                WayPoint("WayPoint H", 0.0, 45.0),
                WayPoint("WayPoint I", 3.0, 0.0)]

class UtSimulator(unittest.TestCase):

    def setUp(self):
        self.simTimeStep = 0.1
        self.testArticle = Simulator()
        self.testArticle.rotationalVel = 20.0
        self.testArticle.translationalVel = 3.0
        self.testArticle.setTimeStep(self.simTimeStep)
        self.testArticle.run()

    def tearDown(self):
        self.testArticle.stop()

    def commandWayPointHelper(self, way_point):
        print "\nCommanding way point: "
        print way_point.displayWayPoint()
        self.testArticle.addWayPoint(way_point)
        # Sleep for a bit before checking active way point
        time.sleep(self.simTimeStep)
        while not self.testArticle.ActiveWayPoint.Reached:
            wbTlmData = self.testArticle.getSimData()
            print wbTlmData
            time.sleep(self.simTimeStep)

    def test_addWayPoint(self):
        self.commandWayPointHelper(test_route_1.pop(0))
        print self.assertAlmostEqual(self.testArticle.positionX, 3.0, delta=self.testArticle.distanceTolerance)
        print self.assertAlmostEqual(self.testArticle.positionY, 0.0, delta=self.testArticle.distanceTolerance)
        print self.assertAlmostEqual(self.testArticle.heading, 90.0, delta=self.testArticle.headingTolerance)

        self.commandWayPointHelper(test_route_1.pop(0))
        print self.assertAlmostEqual(self.testArticle.positionX, 4.0, delta=self.testArticle.distanceTolerance)
        print self.assertAlmostEqual(self.testArticle.positionY, 0.0, delta=self.testArticle.distanceTolerance)
        print self.assertAlmostEqual(self.testArticle.heading, 90.0, delta=self.testArticle.headingTolerance)

        self.commandWayPointHelper(test_route_1.pop(0))
        print self.assertAlmostEqual(self.testArticle.positionX, 6.0, delta=self.testArticle.distanceTolerance)
        print self.assertAlmostEqual(self.testArticle.positionY, 0.0, delta=self.testArticle.distanceTolerance)
        print self.assertAlmostEqual(self.testArticle.heading, 90.0, delta=self.testArticle.headingTolerance)

        self.commandWayPointHelper(test_route_1.pop(0))
        print self.assertAlmostEqual(self.testArticle.positionX, 6.0, delta=self.testArticle.distanceTolerance)
        print self.assertAlmostEqual(self.testArticle.positionY, -1.0, delta=self.testArticle.distanceTolerance)
        print self.assertAlmostEqual(self.testArticle.heading, 180.0, delta=self.testArticle.headingTolerance)

        self.commandWayPointHelper(test_route_1.pop(0))
        print self.assertAlmostEqual(self.testArticle.positionX, 6.0, delta=self.testArticle.distanceTolerance)
        print self.assertAlmostEqual(self.testArticle.positionY, -2.0, delta=self.testArticle.distanceTolerance)
        print self.assertAlmostEqual(self.testArticle.heading, 180.0, delta=self.testArticle.headingTolerance)

        self.commandWayPointHelper(test_route_1.pop(0))
        print self.assertAlmostEqual(self.testArticle.positionX, 6.0, delta=self.testArticle.distanceTolerance)
        print self.assertAlmostEqual(self.testArticle.positionY, -3.0, delta=self.testArticle.distanceTolerance)
        print self.assertAlmostEqual(self.testArticle.heading, 180.0, delta=self.testArticle.headingTolerance)

        self.commandWayPointHelper(test_route_1.pop(0))
        print self.assertAlmostEqual(self.testArticle.positionX, 6.0, delta=self.testArticle.distanceTolerance)
        print self.assertAlmostEqual(self.testArticle.positionY, -3.0, delta=self.testArticle.distanceTolerance)
        print self.assertAlmostEqual(self.testArticle.heading, 225.0, delta=self.testArticle.headingTolerance)

        self.commandWayPointHelper(test_route_1.pop(0))
        print self.assertAlmostEqual(self.testArticle.positionX, 3.0, delta=self.testArticle.distanceTolerance)
        print self.assertAlmostEqual(self.testArticle.positionY, -3.0, delta=self.testArticle.distanceTolerance)
        print self.assertAlmostEqual(self.testArticle.heading, 270.0, delta=self.testArticle.headingTolerance)


if __name__ == '__main__':
    # Run the unit-tests
    suite = unittest.TestLoader().loadTestsFromTestCase(UtSimulator)
    unittest.TextTestRunner(verbosity=2).run(suite)
