from Algorithm.ImageProc import ImageProcColorReverse, \
ImageRotate, \
ImageQR, \
ImageCornerDetect, \
ImageAdaptiveThresholding, \
ImageOtsusBinarization, \
ImageForegroundExtraction, \
ImageOpticalFlow, \
ImageKmean8, \
ImageFaceDetect, \
ImageQR2, \
ImageYoloV3, \
ImageYoloV3_low_res, \
ImageSave, \
Image2Video, \
ImageQR_RobotMarker



class ImageProcRegister:
    register = None
    def __init__(self) -> None:
        self.mAlgorithmList = [
            ImageProcColorReverse.ImageProcColorReverse(),
            # ImageRotate.ImageRotate(),
            ImageQR_RobotMarker.ImageQR_RobotMarker(),
            ImageQR.ImageQR(),
            ImageQR2.ImageQR2(),
            ImageCornerDetect.ImageCornerDetect(),
            ImageAdaptiveThresholding.ImageAdaptiveThresholding(),
            ImageOtsusBinarization.ImageOtsusBinarization(),
            ImageForegroundExtraction.ImageForegroundExtraction(),
            ImageOpticalFlow.ImageOpticalFlow(),
            ImageKmean8.ImageKmean8(),
            ImageFaceDetect.ImageFaceDetect(),
            ImageYoloV3.ImageYoloV3(),
            ImageYoloV3_low_res.ImageYoloV3_low_res(),
            ImageSave.ImageSave(), 
            Image2Video.Image2Video(),
            
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