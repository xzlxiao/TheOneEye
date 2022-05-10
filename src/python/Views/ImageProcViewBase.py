from PyQt5.QtWidgets import QLabel, QFrame, QMenu, QAction, QGridLayout, QInputDialog, QComboBox, QInputDialog, QDialog
from PyQt5 import QtCore, QtWidgets, QtGui, uic, QtMultimediaWidgets
from PyQt5.QtGui import QContextMenuEvent, QPixmap, QResizeEvent
from PyQt5.QtCore import pyqtSignal, QObject, QSize, QEvent
from Control import MainController
from Common.DebugPrint import myDebug, get_current_function_name
from Views.ViewFrameBase import ViewFrameBase
from Views.XLabel import XLabel
from Entity.ImageHandle import ImageHandle

from Algorithm.ImageProcRegister import getImageProcRegister
from Algorithm.ImageProc.ImageProcBase import ImageProcBase
import PyQt5
import copy

from functools import partial

class ImageProcViewBase(ViewFrameBase):
    def __init__(self, *args):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(ImageProcViewBase, self).__init__(*args)
        self.mActiveBorderStyle = 'border:1px solid rgba(200, 50, 50, 255);'
        self.mUnactiveBorderStyle = 'border:1px solid rgba(200, 200, 200, 150);'
        self.deactive()
        self.mImageSaveDir = "./general_image_save"
        self.mImageHandle = ImageHandle()
        self.mImageHandle.setImageSaveDir(self.mImageSaveDir)
        self.controller = MainController.getController()
        self.controller.addImageHandle(self.mImageHandle)
        self.mLayout.addWidget(self.mImageHandle.image_label)
        self.mImageHandle.image_label.show()

    def on_image_save_dir_set(self):
        dialog = QInputDialog()
        dialog.setModal(True)
        dialog.setStyleSheet("""
        background-color: rgba(0, 0, 0, 200);
        border:1px solid rgba(0, 200, 200, 150);
        color:rgb(255, 255, 255);
        """)
        dialog.setFixedSize(350,250) 
        dialog.setWindowTitle('Set save dir')
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setLabelText('请输入……（保存路径）')
        dialog.setTextValue('./general_image_save')
        dialog.setOkButtonText('Ok')
        dialog.setCancelButtonText('Cancel')
        if dialog.exec_() == QDialog.Accepted:
            self.mImageSaveDir = dialog.textValue()
            self.mImageHandle.setImageSaveDir(self.mImageSaveDir)
        else:
            print("dialog canceled")
        dialog.show()

    def on_del_view(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        super().on_del_view()
        self.controller.removeImageHandle(self.mImageHandle)

    def contextMenuEvent(self, event: QContextMenuEvent):
        myDebug(self.__class__.__name__, get_current_function_name())
        # print(event.type(), ' ', QContextMenuEvent.MouseButtonRelease)
        # if event.type() == QContextMenuEvent.MouseButtonRelease:
        #     if event.button() == QtCore.Qt.RightButton:
        menu=self.mkQMenu()
        image_save_dir_set_action = QAction('设置图片保存路径', menu)
        image_save_dir_set_action.triggered.connect(self.on_image_save_dir_set)
        menu.addAction(image_save_dir_set_action)

        menu.exec_(event.globalPos())

    def addImageProcFunc(self, ind:int):
        myDebug(self.__class__.__name__, get_current_function_name())
        register = getImageProcRegister()
        items = register.getNames()
        dialog = QInputDialog(self)
        dialog.setModal(True)
        dialog.setStyleSheet("""
        background-color: rgba(0, 0, 0, 200);
        border:1px solid rgba(0, 200, 200, 150);
        """)
        dialog.setFixedSize(350,250)
        dialog.setWindowTitle('Set Input Flow for Improcessor')
        dialog.setComboBoxItems(items)
        dialog.textValueSelected.connect(lambda: self._addImageProc(ind, register[dialog.findChild(QComboBox).currentIndex()]) if dialog.findChild(QComboBox).currentIndex() >= 0 else None)
        # dialog.textValueSelected.connect(partial(self._addImageProc, ind, register[dialog.findChild(QComboBox).currentIndex()]))
        dialog.show()

    def _addImageProc(self, ind:int, algori):
        myDebug(self.__class__.__name__, get_current_function_name())
        algori_proc = copy.deepcopy(algori)
        self.mImageHandle.addImageProcess(algori_proc)
        self.insertOptionList(algori_proc.Name, self.defaultFunc, ind)
        self.signalFocusedChanged.emit(self, True)