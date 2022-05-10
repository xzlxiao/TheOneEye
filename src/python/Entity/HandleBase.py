import typing
from PyQt5.QtCore import QTimer, QThread, QObject
from Views import XLabel

class HandleBase(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.image_label = XLabel.XLabel()