from PyQt5.QtWidgets import QLabel, QFrame, QMenu, QAction, QGridLayout, QInputDialog, QComboBox
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

class ImageProcViewFrame(ViewFrameBase):
    def __init__(self, *args):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(ImageProcViewFrame, self).__init__(*args)
        self.mLayout = QGridLayout(self)
        self.mLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mLayout)
        self.mActiveBorderStyle = 'border:1px solid rgba(200, 50, 50, 255);'
        self.mUnactiveBorderStyle = 'border:1px solid rgba(200, 200, 200, 150);'
        self.deactive()
        self.mInputFlow = None
        self.mImageHandle = ImageHandle()
        self.controller = MainController.getController()
        self.controller.addImageHandle(self.mImageHandle)
        self.insertOptionList('添加图像流', self.addImageFlowFunc)
        self.mLayout.addWidget(self.mImageHandle.image_label)
        
        self.mImageHandle.image_label.show()

    def on_del_view(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        super().on_del_view()
        self.controller.removeImageHandle(self.mImageHandle)
    
    # def 

    def contextMenuEvent(self, event: QContextMenuEvent):
        myDebug(self.__class__.__name__, get_current_function_name())
        # print(event.type(), ' ', QContextMenuEvent.MouseButtonRelease)
        # if event.type() == QContextMenuEvent.MouseButtonRelease:
        #     if event.button() == QtCore.Qt.RightButton:
        menu=self.mkQMenu()
        menu.exec_(event.globalPos())

    def setImageFlowInput(self, flow):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mInputFlow = flow 
        self.mImageHandle.setImageFlow(flow)
        flow.signalReleased.connect(self.slot_removeImageFlowInput)

    def removeImageFlowInput(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mInputFlow = None
        self.mImageHandle.setImageFlow(None)
        self.deleteOptionList(0)
        self.insertOptionList('添加图像流', self.addImageFlowFunc, 0)
    
    def slot_removeImageFlowInput(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.removeImageFlowInput()
        self.signalFocusedChanged.emit(self, True)
    
    def addImageFlowFunc(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        input_flow_list = self.controller.getInputFlowList()
        items = [item.getName() for item in input_flow_list]
        # print(input_flow_list)
        dialog = QInputDialog(self)
        dialog.setModal(True)
        dialog.setStyleSheet("""
        background-color: rgba(0, 0, 0, 200);
        border:1px solid rgba(0, 200, 200, 150);
        """)
        dialog.setFixedSize(350,250)
        dialog.setWindowTitle('Set Input Flow for Improcessor')
        dialog.setComboBoxItems(items)
        dialog.textValueSelected.connect(lambda x: self._addImageFlow(input_flow_list[dialog.findChild(QComboBox).currentIndex()]) if dialog.findChild(QComboBox).currentIndex() >= 0 else None)
        dialog.show()

    def _addImageFlow(self, flow):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.setImageFlowInput(flow)
        self.deleteOptionList(0)
        self.insertOptionList(flow.getName(), self.addImageFlowFunc, 0)
        if self.getOptionListLen() == 1:
            self.insertOptionList('添加图像处理模块', self.addImageProcFunc)
        self.signalFocusedChanged.emit(self, True)

    def addImageProcFunc(self):
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
        dialog.textValueSelected.connect(lambda x: self._addImageProc(x, register[dialog.findChild(QComboBox).currentIndex()]) if dialog.findChild(QComboBox).currentIndex() >= 0 else None)
        dialog.show()

    def _addImageProc(self, ind:int, algori:ImageProcBase):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mImageHandle.addImageProcess(algori)
        self.insertOptionList(algori.Name, self.defaultFunc, 1)
        self.signalFocusedChanged.emit(self, True)
