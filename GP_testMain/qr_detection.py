import cv2
import qrcode
from pyzbar import pyzbar
import time
import numpy
import matplotlib.pyplot as plot


class QRGenerator:
    def __init__(self, message, version=1, box_size=10, border=1):
        self.qr = qrcode.QRCode(
            version=version,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=box_size,
            border=border
        )
        self.message = message

    def genStart(self):
        self.qr.add_data(self.message)
        self.qr.make(fit=True)
        img = self.qr.make_image()
        return img


def qrDectbyZbar(frame):
    start = int(round(time.time() * 1000))

    h1, w1 = frame.shape[0], frame.shape[1]

    texts = pyzbar.decode(frame)
    for text in texts:
        textdate = text.data.decode('utf-8')
        (x, y, w, h) = text.rect  # 获取二维码的外接矩形顶点坐标

        # 二维码中心坐标
        cx = int(x + w / 2)
        cy = int(y + h / 2)
        # cv2.circle(frame, (cx, cy), 2, (0, 255, 0), 8)  # 做出中心坐标
        # 画出画面中心与二维码中心的连接线
        cv2.line(frame, (cx, cy), (int(w1 / 2), int(h1 / 2)), (255, 0, 0), 10)
        # 二维码最小矩形
        # cv2.line(frame, text.polygon[0], text.polygon[1], (255, 0, 0), 2)
        # cv2.line(frame, text.polygon[1], text.polygon[2], (255, 0, 0), 2)
        # cv2.line(frame, text.polygon[2], text.polygon[3], (255, 0, 0), 2)
        # cv2.line(frame, text.polygon[3], text.polygon[0], (255, 0, 0), 2)
        # # 写出扫描内容
        # txt = '(' + text.type + ')  ' + textdate + 'center point: ' + '(' + str(cx) + ',' + str(cy) + ')'
        # print(txt)

    print(int(round(time.time() * 1000)) - start)


if __name__ == '__main__':
    qg1 = QRGenerator('1').genStart()
    qg1.show()
    qg1.save('./img/qrcode/qg1.jpg')
