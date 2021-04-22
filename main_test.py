
import sys
import os
envpath = '/home/gr/.local/lib/python3.8/site-packages/cv2/qt/plugins/platforms'
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = envpath
sys.path.append('./src/python')
sys.path.append("./")
from Test import Test
from Common import XSetting

if __name__ == "__main__":
    XSetting.XSetting.loadSettingFile()
    Test.test_robot()