# -*- coding: utf-8 -*-

'''
    【简介】
	PyQt5中 QListView 例子       
  
'''

from PyQt5.QtWidgets import QApplication, QWidget , QVBoxLayout , QListView, QMessageBox
from PyQt5.QtCore import QStringListModel  
import sys  

class ListViewDemo(QWidget):
	def __init__(self, parent=None):
		super(ListViewDemo, self).__init__(parent)
		self.setWindowTitle("QListView 例子")
		self.resize(300, 270)    
		layout = QVBoxLayout()
		
		listView = QListView()     #创建一个listview对象
		slm = QStringListModel(); #创建mode
		self.qList = ['Item 1','Item 2','Item 3','Item 4' ]	 #添加的数组数据
		slm.setStringList(self.qList) #将数据设置到model
		listView.setModel(slm )##绑定 listView 和 model
		listView.clicked.connect(self.clickedlist)		 #listview 的点击事件
		layout.addWidget( listView )#将list view添加到layout
		self.setLayout(layout) 		  #将lay 添加到窗口

	def clickedlist(self, qModelIndex):
		QMessageBox.information(self, "QListView", "你选择了: "+ self.qList[qModelIndex.row()])
		print("点击的是：" + str(qModelIndex.row()))
		
if __name__ == "__main__":       
	app = QApplication(sys.argv)
	win = ListViewDemo()	
	win.show()	
	sys.exit(app.exec_())
