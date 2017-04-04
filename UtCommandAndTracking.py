#!/usr/bin/python

import unittest
import logging, sys
from time import sleep
# Use the WheelBot Emulator for this test
from Emulator import Emulator
# Need a serial communication component for this test
from SerialCommunication import SerialCommunication
# Import the module under test
from CommandAndTracking import CommandAndTracking
import comm_packet_pb2

# Define a list of way-points for the purpose of testing
test_route_1 = [comm_packet_pb2.WayPoint(Name="WayPoint A", Distance=3.0, Heading=90.0),
                comm_packet_pb2.WayPoint(Name="WayPoint B", Distance=1.0, Heading=0.0),
                comm_packet_pb2.WayPoint(Name="WayPoint C", Distance=2.0, Heading=0.0)]

# Use one global Emulator instance for all tests
wbEmulator = Emulator()
class UtCommandAndTracking(unittest.TestCase):

    def setUp(self):
        self.serialComm = SerialCommunication("./ttyclient")
        self.testArticle = CommandAndTracking()
        self.testArticle.connectToWheelBot(self.serialComm)

    def test_commandRoute1(self):
        self.testArticle.loadWayPoints(test_route_1)
        self.testArticle.commandRoute()

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format='%(levelname)s:%(message)s')
    wbEmulator.run()
    # add some wait time between tests to give the emulated serial port time to
    # be opened
    sleep(1.0)
    # Run the unit-tests
    suite = unittest.TestLoader().loadTestsFromTestCase(UtCommandAndTracking)
    unittest.TextTestRunner(verbosity=2).run(suite)
