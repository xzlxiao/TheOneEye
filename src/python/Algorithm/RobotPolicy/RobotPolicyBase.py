# from Entity.RobotEpuck import RobotEpuck


class RobotPolicyBase:
    def __init__(self):
        self.mRobot = None 
        self.Name = 'RobotPolicyBase'
        
    def setRobot(self, robot):
        self.mRobot = robot 
        self.mRobot.mPolicy = self

    def update(self):
        pass

    def getName(self):
        return self.Name