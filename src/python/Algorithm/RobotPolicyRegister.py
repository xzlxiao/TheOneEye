from Algorithm.RobotPolicy import RobotPolicyBase, RobotPolicyTest, RobotPolicyPos, RobotPolicyQR_pos


class RobotPolicyRegister:
    register = None
    def __init__(self) -> None:
        self.mAlgorithmList = [
            RobotPolicyTest.RobotPolicyTest(),
            RobotPolicyPos.RobotPolicyPos(),
            RobotPolicyQR_pos.RobotPolicyQR_pos(),
        ]

    def getNames(self):
        ret = []
        for i in self.mAlgorithmList:
            ret.append(i.Name)
        return ret 

    def __getitem__(self, key):
        return self.mAlgorithmList[key]

    def __len__(self):
        return len(self.mAlgorithmList)


def getRobotPolicyRegister() -> RobotPolicyRegister:
    if not RobotPolicyRegister.register:
        RobotPolicyRegister.register = RobotPolicyRegister()
    return RobotPolicyRegister.register