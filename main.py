# coding=utf-8
from PySide2 import QtWidgets, QtCore, QtGui
import sys
import setdialog
import processRS

import cv2
#from skimage import io
import numpy as np
import inputWindow
import os
import os.path
import myTreeView
    

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self,parent=None):
        super().__init__(parent)
        #初始化menubar
        self.menubar=self.menuBar()
        self.menubar.setNativeMenuBar(False)

        #工具图标初始大小
        self.iconSize=QtCore.QSize(64,64)
        #保存所有的action
        self.toolList={}
        #保存所有的工具，方便知道有哪些工具箱
        self.toolBarList={}
        otherToolBar=QtWidgets.QToolBar('others')
        otherToolBar.setIconSize(self.iconSize)
        self.toolBarList['others']=otherToolBar

        
        #默认使用工具箱模式
        #self.toolBox=QtWidgets.QToolBox()
        self.toolBox=QtWidgets.QTabWidget()
        self.toolBox.setWindowTitle('ToolBox')
        self.toolBox.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

        #用来保存打开的gdal对象
        self.treeList=[]
        #判断是不是第一次打开文件
        self.firstOpen=False
        
        
        #加载路径设置的对话框
        self.Dialog1=QtWidgets.QDialog(self)
        self.pathDialog=setdialog.Ui_Dialog()
        self.pathDialog.setupUi(self.Dialog1)
        #self.Dialog1.center()
        #self.toolBar=self.addToolBar('1')
        #self.toolBar.setIconSize(QtCore.QSize(64,64))
        #self.toolBox=QtWidgets.QToolBox()
        #self.toolBox.addItem(self.toolBar,'1')
        #self.toolBox.show()

        self.loadMenu(self.menubar)
        #添加工具栏
        
        #self.addToolBar('2')
        #树状视图
        #self.pushbutton=QtWidgets.QPushButton('test')
        self.dockWidget=myTreeView.myTreeView(self.treeList,self)
        self.dockWidget.setWindowTitle('Image List')
        self.treeWidget=self.dockWidget.treeWidget
        self.fileModel=self.dockWidget.fileModel
    def resizeEvent(self,pos):
        self.toolBox.move(self.geometry().width()-self.toolBox.width(),self.geometry().y()+100)
        self.toolBox.show()
    def closeEvent(self,event):
        self.toolBox.close()
        
    def loadMenu(self,menuBar):
        self.menufile=QtWidgets.QMenu(self.tr('file'))
        self.menuview=QtWidgets.QMenu(self.tr('view'))
        self.menusetting=QtWidgets.QMenu(self.tr('setting'))
        self.menutools=QtWidgets.QMenu(self.tr('tools'))
        self.loadToolMenu(self.menutools)
        #路径设置的动作
        self.pathSetAction=QtWidgets.QAction(self.tr('path setting'),self)
        self.pathSetAction.triggered.connect(self.Dialog1.exec_)
        self.menusetting.addAction(self.pathSetAction)
        #打开文件的动作
        self.openFileAction=QtWidgets.QAction(QtGui.QIcon('./icon/open_file.bmp'),
                                              self.tr('open'),self)
        self.openFileAction.triggered.connect(self.openFile)
        self.menufile.addAction(self.openFileAction)
        menuBar.addMenu(self.menufile)
        menuBar.addMenu(self.menuview)
        menuBar.addMenu(self.menusetting)
        menuBar.addMenu(self.menutools)
        return True
    #此处逻辑复杂。。。。尽量不要改动
    def findtools(self,path,menu):
        list1=os.listdir(path)
        flag=False
        child=False
        for path2 in list1:
            if(path2[0:2]=='__'):
                continue
            if(os.path.isdir(os.path.join(path,path2))):
                menu2=QtWidgets.QMenu(self.tr(path2))
                flag1,child1=self.findtools(os.path.join(path,path2),menu2)
                if(flag1):
                    menu.addMenu(menu2)
                    flag=True
                if(child1):
                    name=path2
                    action2=QtWidgets.QAction(self.tr(name),self)
                    methodInfo=self.readInfo(os.path.join(path,path2,'methodinfo'))
                    if(methodInfo['icon']==''):
                        action2.setIconText(self.tr(name))
                    else:
                        if os.path.exists(os.path.join(path,path2,methodInfo['icon'])):
                            icon=QtGui.QIcon(os.path.join(path,path2,methodInfo['icon']))
                            action2.setIcon(icon)
                        else:
                            action2.setIconText(self.tr(name))
                    
                    self.toolList[action2]=os.path.join(path,path2)
                    action2.triggered.connect(self.showTools)
                    #self.toolBar.addAction(action2)
                    
                    if(flag):
                        menu2.addAction(action2)
                    else:
                        menu.addAction(action2)
                        
                    #工具类型的判断，可能有通用工具箱，每个人的工具箱之类的
                    if(methodInfo['toolclass']):
                        if self.toolBarList.__contains__(methodInfo['toolclass']):
                            toolBar=self.toolBarList[methodInfo['toolclass']]
                            toolBar.addAction(action2)
                        else:
                            toolBar=QtWidgets.QToolBar(methodInfo['toolclass'])
                            toolBar.setIconSize(self.iconSize)
                            toolBar.addAction(action2)
                            self.toolBarList[methodInfo['toolclass']]=toolBar
                    else:
                        toolBar=self.toolBarList['others']
                        toolBar.addAction(action2)
                        
                    
            else:
                if(path2=="methodinfo"):
                    child=True
        return flag,child
                    
    #加载工具箱或工具条    
    def loadToolMenu(self,menu):
        self.findtools('./tools',menu)
        for index in self.toolBarList:
            toolBar=self.toolBarList[index]
            #self.toolBox.addItem(toolBar,index)
            if(index=='custom'):
                self.toolBox.insertTab(0,toolBar,index)
            else:
                if(index!='others'):
                    self.toolBox.addTab(toolBar,index)
            self.toolBox.addTab(self.toolBarList['others'],'others')
            #self.addToolBar(toolBar)

        

    def showTools(self):
        action2=self.sender()
        path=self.toolList[action2]
        print(path)
        methodInfo=self.readInfo(path+'/methodinfo')
        toolWindow=inputWindow.inputWindow(path,methodInfo,self.treeWidget,self.treeList,self)
        toolWindow.setWindowTitle(self.tr(u'Input Parameters'))
        #action2.setWindowIconText('param')
        toolWindow.show()
        
        
    def openFile(self):
        self.openFilename,self.openFiletype=QtWidgets.QFileDialog.getOpenFileName(self,
                        'Open file...', "./","All Files(*.*);;Envi Files(*.img);;Tiff Files(*.tiff *.tif)")
        print (self.openFilename, self.openFiletype)
        #此处应该有文件是否能够使用的判决，暂时忽略
        if (self.openFilename):
            GdalObject=processRS.processRS(self.openFilename)
            self.dockWidget.treeList.append(GdalObject)
            
            self.dockWidget.showTree()
        if(not self.firstOpen):
            self.showDockWidget()
        
    def readSetting(self):
        return True
    def setSetting(self):
        return True



    def showDockWidget(self):
        self.dockWidget.setGeometry(self.geometry().x(),self.geometry().y()+100,
                                    self.geometry().width()/6,self.geometry().height()-200)
        self.dockWidget.show()
        self.firstOpen=True            
        return True
#读取方法的输入输出，配置，python没有c那么方便
    def readInfo(self,filename):
        f=open(filename,'r')
        dic={}
        dic['input']=[]
        dic['output']=[]
        dic['icon']=''
        dic['toolclass']=''
        strline=f.readline()
        while(strline):
            strline=strline.replace('\n','')
            strline=strline.replace('\r','')
            strline=strline.replace(' ','')
            strline=strline.replace('"','')
            strline=strline.replace('-',' ')
            if(strline==''):
                strline=f.readline()
                continue
            if(strline[0]=='#'):
                strline=strline[1:len(strline)].split(':')
                if(strline[0]=='methodtype'):
                   dic['methodtype']=strline[1]
                if(strline[0]=='mainfile'):
                   dic['mainfile']=strline[1]
                if(strline[0]=='mainmethod'):
                   dic['mainmethod']=strline[1]
                if(strline[0]=='toolclass'):
                   dic['toolclass']=strline[1]
                if(strline[0]=='icon'):
                   dic['icon']=strline[1]
                if(strline[0]=='input'):
                   strinput=strline[1]
                   strinput=strinput.split(',')
                   inputpar={}
                   inputpar['default']=''
                   for str1 in strinput:
                       str1=str1.split('=')
                       inputpar[str1[0]]=str1[1]
                   dic['input'].append(inputpar)
                if(strline[0]=='output'):
                   strinput=strline[1]
                   strinput=strinput.split(',')
                   inputpar={}
                   inputpar['default']=''
                   for str1 in strinput:
                       str1=str1.split('=')
                       inputpar[str1[0]]=str1[1]
                   dic['output'].append(inputpar)
            strline=f.readline()
        f.close()
        return dic 
    
    def __del__(self):
        #self.dockWidget.close()
        return True
    
app=QtWidgets.QApplication(sys.argv)
w=MainWindow()
w.showMaximized()
sys.exit(app.exec_())
