#coding=utf-8

from PySide2 import QtWidgets, QtCore, QtGui
import numpy as np
import os
import os.path
import processRS



class myTreeView(QtWidgets.QWidget):
    def __init__(self, treeList=[],parent=None):
        super().__init__(parent)
        self.treeWidget=QtWidgets.QTreeView(parent)
        self.fileModel=QtGui.QStandardItemModel(self)
        self.treeList=treeList
        #右键菜单
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.showTreeMenu)
        self.treeWidget.setHeaderHidden(True)
        #设置布局
        self.dockVLayout=QtWidgets.QVBoxLayout()
        self.dockHLayout=QtWidgets.QHBoxLayout()
        self.dockVLayout.addLayout(self.dockHLayout)
        self.dockVLayout.addWidget(self.treeWidget)

        self.setLayout(self.dockVLayout)
        
        self.setWindowFlag(QtCore.Qt.WindowType.Tool)
    def showTreeMenu(self,pos):
        #print('mouse rightclicked')
        curIndex=self.treeWidget.indexAt(pos)
        if(curIndex.parent):
            bandnum=curIndex.row()+1
            gdalobject=self.treeList[curIndex.parent().row()]
            print (gdalobject.filename,bandnum)
            r=gdalobject.GDALReadFile([bandnum])
            #img=np.zeros((gdalobject.XSize,gdalobject.YSize))
            img=r[0]
            print(img.shape)
            cv2.imshow('show grey',img.astype(np.uint8))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    def showTree(self):
        #self.treeWidget.clear()
        self.fileModel.clear()
        for gdalObject in self.treeList:
            gdalObject.Getparam()
            rootItem=QtGui.QStandardItem(gdalObject.filename)
            for bandi in gdalObject.bandindex:
                print(bandi)
                childItem=QtGui.QStandardItem('band '+ str(bandi))
                rootItem.setChild(bandi-1,childItem)
            self.fileModel.appendRow([rootItem])
        self.treeWidget.setModel(self.fileModel)
        self.treeWidget.show()

