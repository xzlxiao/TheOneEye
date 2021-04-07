import Cam
import qr_detection as qrd
import cv2
import mvsdk


class DectMain:
    def __init__(self):
        self.usemethod1flag = 1

    def run(self):
        try:
            # 枚举相机
            DevList = mvsdk.CameraEnumerateDevice()
            nDev = len(DevList)
            if nDev < 1:
                print("No camera was found!")
                return

            for i, DevInfo in enumerate(DevList):
                print("{}: {} {}".format(i, DevInfo.GetFriendlyName(), DevInfo.GetPortType()))

            i = 0 if nDev == 1 else int(input("Select camera: "))
            cam = Cam.Camera(DevList[i])
            if not cam.open():
                print('cam open error...')
                return

            while (cv2.waitKey(1) & 0xFF) != ord('q'):
                frame = cam.grab()
                if frame is not None:
                    # -------------insert your own algorithms below--------------------
                    if self.usemethod1flag:
                        qrd.qrDectbyZbar(frame)
                    # -----------------------------end---------------------------------
                    cv2.imshow("{} Press q to end".format(cam.DevInfo.GetFriendlyName()), frame)

            cam.close()
        finally:
            cv2.destroyAllWindows()


if __name__ == '__main__':
    dm = DectMain()
    dm.run()
