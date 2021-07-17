#coding=utf-8

from PySide2 import QtWidgets,QtCore,QtGui
import sys
app=QtWidgets.QApplication(sys.argv)


treeView=QtWidgets.QTreeView()
rootItem=QtGui.QStandardItem('this')
childItem=QtGui.QStandardItem('1')
childItem1=QtGui.QStandardItem('2')
rootItem.setChild(1,childItem)
fileModel=QtGui.QStandardItemModel(treeView)
fileModel.setItem(0,rootItem)
fileModel.setItem(1,2,childItem1)
treeView.setModel(fileModel)
treeView.show()

sys.exit(app.exec_())
