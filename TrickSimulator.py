from variable_server import VariableServer
from subprocess import call

class TrickSimulator(object):
    def __init__(self):
        return

    def launch(self, s_main_dir):
        #call(["make", "spotless"], cwd=self.trick_sim_home)
        #call(["CP", ""], cwd=self.trick_sim_home)
        call(["./S_main_Linux_5.4_x86_64.exe", "RUN_test/input.py"], cwd=s_main_dir)
        self.variable_server = VariableServer('localhost', 34122)
        return

    def addWayPoint(self, way_point):
        return

    def getSimData(self):
        print "Position X: " + variable_server.get_value('veh.vehicle.position[0]')
        print "Position Y: " + variable_server.get_value('veh.vehicle.position[1]')


# Used if you want to run the emulator as a main program.
def main():
    sim = TrickSimulator()
    sim.launch("/users/mmmoore2/wheel_bot/WheelBotEmulator/trick_sim")

if __name__ == "__main__":
      main()