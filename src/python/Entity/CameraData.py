
class CameraData:
    def __init__(self) -> None:
        self.data = {}

    def setData(self, data_name: str, data_id: int, _data):
        if data_name in self.data:
            self.data[data_name][data_id] = _data
        else:
            self.data[data_name] = {}

    def getData(self, data_name: str, data_id: int):
        try:
            return self.data[data_name][data_id]
        except:
            return None 