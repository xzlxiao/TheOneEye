# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/xiaozhenlong/Code/TheOneEye/src/python/Views/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1207, 686)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.lbBackground2 = QtWidgets.QLabel(self.centralwidget)
        self.lbBackground2.setText("")
        self.lbBackground2.setObjectName("lbBackground2")
        self.gridLayout.addWidget(self.lbBackground2, 0, 1, 1, 1)
        self.lbBackground3 = QtWidgets.QLabel(self.centralwidget)
        self.lbBackground3.setText("")
        self.lbBackground3.setObjectName("lbBackground3")
        self.gridLayout.addWidget(self.lbBackground3, 1, 0, 1, 1)
        self.lbBackground5 = QtWidgets.QLabel(self.centralwidget)
        self.lbBackground5.setText("")
        self.lbBackground5.setObjectName("lbBackground5")
        self.gridLayout.addWidget(self.lbBackground5, 2, 0, 1, 1)
        self.lbBackground4 = QtWidgets.QLabel(self.centralwidget)
        self.lbBackground4.setText("")
        self.lbBackground4.setObjectName("lbBackground4")
        self.gridLayout.addWidget(self.lbBackground4, 1, 1, 1, 1)
        self.lbBackground1 = QtWidgets.QLabel(self.centralwidget)
        self.lbBackground1.setAutoFillBackground(False)
        self.lbBackground1.setStyleSheet("")
        self.lbBackground1.setText("")
        self.lbBackground1.setScaledContents(False)
        self.lbBackground1.setObjectName("lbBackground1")
        self.gridLayout.addWidget(self.lbBackground1, 0, 0, 1, 1)
        self.lbBackground6 = QtWidgets.QLabel(self.centralwidget)
        self.lbBackground6.setText("")
        self.lbBackground6.setObjectName("lbBackground6")
        self.gridLayout.addWidget(self.lbBackground6, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1207, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "The One Eye"))
