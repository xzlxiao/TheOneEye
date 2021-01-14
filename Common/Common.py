from Common.DebugPrint import myDebug, get_current_function_name
import sys
import numpy as np
sys.path.append("../")

class Common:
    def __init__(self):
        pass

    @staticmethod
    def getTime() -> str:
        pass

    @staticmethod
    def getSimilarity(A: np.ndarray, B: np.ndarray) -> bool:
        pass


class XRect:
    def __init__(self, x=0, y=0, width=0, height=0):
        self.width: int = width
        self.height: int = height
        self.x: int = x
        self.y: int = y

