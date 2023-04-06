from PyQt5.QtGui import QResizeEvent, QPixmap, QMovie, QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSignal, QObject, QSize, QEvent, Qt
from Views.ViewFrameBase import ViewFrameBase

class ViewListQItem(QStandardItem):
    # signalClicked = pyqtSignal()
    def __init__(self, *args):
        super().__init__(*args)
        self.setEditable(False)
        