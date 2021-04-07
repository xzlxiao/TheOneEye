from Algorithm.ImageProc import ImageProcColorReverse, ImageRotate, ImageQR



class ImageProcRegister:
    register = None
    def __init__(self) -> None:
        self.mAlgorithmList = [
            ImageProcColorReverse.ImageProcColorReverse(),
            ImageRotate.ImageRotate(),
            ImageQR.ImageQR(),
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


def getImageProcRegister() -> ImageProcRegister:
    if not ImageProcRegister.register:
        ImageProcRegister.register = ImageProcRegister()
    return ImageProcRegister.register