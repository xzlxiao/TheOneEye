"""
       .==.        .==.
      //`^\\      //^`\\
     // ^ ^\(\__/)/^ ^^\\
    //^ ^^ ^/+  0\ ^^ ^ \\
   //^ ^^ ^/( >< )\^ ^ ^ \\
  // ^^ ^/\| v''v |/\^ ^ ^\\
 // ^^/\/ /  `~~`  \ \/\^ ^\\
 ----------------------------
BE CAREFULL! THERE IS A DRAGON.

Function：XLabel

Modules：
pass

(c) 肖镇龙(xzl) 2021

Dependencies：
pass

Updating Records:
2021-01-22 09:38:15 xzl
"""
import sys
import cv2
from Control import MainController
from Test import Test
from Common import XSetting
sys.path.append("./")
from PyQt5.QtWidgets import QApplication, QWidget


def main():
    app = QApplication(sys.argv)
    XSetting.XSetting.loadSettingFile()
    if XSetting.XSetting.isDebug.isPrintDebug:
        Test.UnitTest()
    print('Load mainController')
    mainController = MainController.MainController()
    mainController.start()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()