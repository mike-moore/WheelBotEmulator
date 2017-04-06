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
test_route_1 = [comm_packet_pb2.WayPoint(Name="WayPoint A", Distance=0.707107, Heading=-45.0), #0.5, -0.5
                comm_packet_pb2.WayPoint(Name="WayPoint B", Distance=1.58113, Heading=-18.43494), #1.5, -0.5
                comm_packet_pb2.WayPoint(Name="WayPoint C", Distance=1.58113, Heading=-18.43494)] # 1.5, 0.5

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
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format='%(levelname)s:%(message)s')
    try:
        wbEmulator.run()
    except IOError:
        wbEmulator.stop()
        logging.error("Failed to connect to sim. Is the Trick sim running?")
        sys.exit()

    # add some wait time between tests to give the emulated serial port time to
    # be opened
    sleep(5.0)
    # Run the unit-tests
    suite = unittest.TestLoader().loadTestsFromTestCase(UtCommandAndTracking)
    unittest.TextTestRunner(verbosity=2).run(suite)
    wbEmulator.stop()
