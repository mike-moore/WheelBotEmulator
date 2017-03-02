#!/usr/bin/python

import unittest
from time import sleep
# Use the WheelBot Emulator for this test
from Emulator import Emulator
# Need a serial communication component for this test
from SerialCommunication import SerialCommunication
# Import the module under test
from CommandAndTracking import CommandAndTracking
from WayPoint import WayPoint

# Define a list of way-points for the purpose of testing
test_route_1 = [WayPoint(3.0, 90.0),
                WayPoint(1.0, 0.0),
                WayPoint(2.0, 0.0),
                WayPoint(1.0, 90.0),
                WayPoint(1.0, 0.0),
                WayPoint(1.0, 0.0),
                WayPoint(0.0, 45.0),
                WayPoint(0.0, 45.0),
                WayPoint(3.0, 0.0)]

class UtCommandAndTracking(unittest.TestCase):

    def setUp(self):
        self.wbEmulator = Emulator()
        self.wbEmulator.run()
        self.serialComm = SerialCommunication("./ttyclient")
        self.testArticle = CommandAndTracking()
        self.testArticle.connectToWheelBot(self.serialComm)

    def tearDown(self):
        self.wbEmulator.stop()
        self.testArticle.disconnectFromWheelBot()

    def test_commandRoute1(self):
        self.testArticle.loadWayPoints(test_route_1)
        self.testArticle.commandRoute()


if __name__ == '__main__':
    # Run the unit-tests
    suite = unittest.TestLoader().loadTestsFromTestCase(UtCommandAndTracking)
    unittest.TextTestRunner(verbosity=2).run(suite)
