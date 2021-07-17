#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
"""
PyQt5 教程
 
在这个例子中，我们在窗口的右下角放置两个按钮。
 
作者：我的世界你曾经来过
博客：http://blog.csdn.net/weiaitaowang
最后编辑：2016年7月31日
"""
 
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget,
  QPushButton, QVBoxLayout, QHBoxLayout)
 
class Example(QWidget):
 
 def __init__(self):
  super().__init__()
 
  self.initUI()
 
 def initUI(self):
 
##okButton = QPushButton('确定')
##cancelButton = QPushButton('取消')
##hbox = QHBoxLayout()hbox.addStretch(1)
##hbox.addWidget(okButton)
##hbox.addWidget(cancelButton)
    self.layout1=QtWidgets.QVBoxLayout()
    self.layout2=QtWidgets.QHBoxLayout()
    self.button1=QtWidgets.QPushButton('1',self)
    self.label1=QtWidgets.QLabel()
    self.label1.setText('label')
    self.button2=QtWidgets.QPushButton('2',self)
    self.button3=QtWidgets.QPushButton('3',self)
    self.layout2.addWidget(self.button1)
    self.layout2.addWidget(self.button2)
    self.layout2.addWidget(self.button3)
    self.layout2.addWidget(self.label1)
    self.layout1.addLayout(self.layout2)
    self.setLayout(self.layout1)
 
##  vbox = QVBoxLayout()
##  vbox.addStretch(1)
##  vbox.addLayout(hbox)
 
##  self.setLayout(vbox)
## 
##  self.setGeometry(300, 300, 350, 150)
##  self.setWindowTitle('Box布局')  
##  self.show()
 
if __name__ == '__main__':
 
 app = QApplication(sys.argv)
 ex = Example()
 ex.show()
 sys.exit(app.exec_())
