from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QListView
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSignal, QObject, QStringListModel, QEvent, Qt
from PyQt5.QtGui import QResizeEvent, QPixmap, QMovie, QMouseEvent
from Common.Common import Common
from Entity.RadioButtonGroup.RadioButton import RadioButton

class RadioButtonGroup(QWidget):
    signalActivedStateChanged = pyqtSignal()
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.mButtonGroup = {}
        self.mActivedButton = None 

    def addButton(self, name:str, button_label:QLabel, isActived=False, image_normal=None, image_hover=None, image_press=None, image_active=None):
        if name in self.mButtonGroup:
            raise Exception('Radio button name repeated.')
        button = RadioButton(button_label, self, name, image_normal=image_normal, image_hover=image_hover, image_press=image_press, image_active=image_active)
        self.mButtonGroup[name] = button
        Common.setQLabelImage(image_normal, button_label)
        if self.mActivedButton is None:
            self.mActivedButton = button
            self.mActivedButton.active()
        if isActived:
            self.mActivedButton.deactive()
            self.mActivedButton = button
            self.mActivedButton.active()
        button.signalButtonActived.connect(self.slotButtonActived)

    def getButton(self, name)->RadioButton:
        if name not in self.mButtonGroup:
            return None 
        else:
            return self.mButtonGroup[name]

    def activeButton(self, name):
        self.mActivedButton.deactive()
        button = self.getButton(name)
        self.mActivedButton = button
        if not self.mActivedButton.isActived():
            self.mActivedButton.active()

    def slotButtonActived(self, name):
        self.activeButton(name)
        self.signalActivedStateChanged.emit()

