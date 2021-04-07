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
sys.path.append('./src/python')
import cv2
from Control import MainController
from Test import Test
from Common import XSetting
sys.path.append("./")
from PyQt5.QtWidgets import QApplication, QWidget
import os
envpath = '/home/gr/.local/lib/python3.8/site-packages/cv2/qt/plugins/platforms'
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = envpath


def main():
    app = QApplication(sys.argv)
    XSetting.XSetting.loadSettingFile()
    if XSetting.XSetting.isDebug.isPrintDebug:
        Test.UnitTest()
    print('Load mainController')
    mainController = MainController.MainController()
    MainController.__controller = mainController 
    mainController.start()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
