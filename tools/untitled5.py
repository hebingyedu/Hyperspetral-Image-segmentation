# -*- coding: utf-8 -*-
import sys
"""
Created on Thu Mar 28 08:36:28 2019

@author: wangtf
"""

from PyQt5 import QtCore, QtGui, QtWidgets
# 
class CheckableComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QtGui.QStandardItemModel(self))

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)
    def getCheckItem(self):
        #getCheckItem可以获得选择的项目text
        checkedItems = []
        for index in range(self.count()):
            item = self.model().item(index)
            if item.checkState() == QtCore.Qt.Checked:
                checkedItems.append(item.text())
        return checkedItems
    def checkedItems(self):
        checkedItems = []
        for index in range(self.count()):
            item = self.model().item(index)
            if item.checkState() == QtCore.Qt.Checked:
                checkedItems.append(item)
        return checkedItems



app=QtWidgets.QApplication(sys.argv)
w=QtWidgets.QWidget()
itemList = (u'项目1',u'项目2',u'项目3')
checkableComboBox = CheckableComboBox(w)
for index, element in enumerate(itemList):
                    checkableComboBox.addItem(element[0])
                    item = checkableComboBox.model().item(index, 0)
                    item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    item.setCheckState(QtCore.Qt.Checked)
                    item.setCheckable(True)
#checkableComboBox.setRootModelIndex(item.index())
w.show()
sys.exit(app.exec_())
