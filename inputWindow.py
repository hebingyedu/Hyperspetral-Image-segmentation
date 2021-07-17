# coding = utf-8
from PySide2 import QtWidgets,QtCore,QtGui
import sys
import copy
import os.path
import imp
import numpy as np
import cv2
from imShowWindow import imShow

#global debug=True

class Mycombobox(QtWidgets.QWidget):
    def __init__(self, parent=None,treeView=None,childTree=True,checked=True):
        super().__init__(parent)
        self.parent=parent
        self.childTree=childTree
        self.layout=QtWidgets.QHBoxLayout()
        self.layout1=QtWidgets.QVBoxLayout(self)
        self.isShow=False
        #本来应该设置成不可编辑状态
        #print (self.geometry().x())
        self.lineEdit=QtWidgets.QLineEdit(self)
        self.popButton=QtWidgets.QToolButton(self)
        self.popButton.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_TitleBarUnshadeButton))
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.popButton)
        #self.treeView=QtWidgets.QWidget()
        self.tree,self.treemodel=self.copyTree(treeView,childTree,checked)

        
        #self.tree.setParent(self)
        
        self.tree.setWindowFlag(QtCore.Qt.SplashScreen)
        
        #self.tree.setWindowFlag(QtCore.Qt.SplashScreen)
        self.tree.hide()
        self.layout1.addLayout(self.layout)
        self.layout1.addWidget(self.tree)
        self.setLayout(self.layout1)
        self.popButton.clicked.connect(self.showtree)
        self.tree.clicked.connect(self.showselect)
        #self.tree.show()
    def showtree(self):
        self.isShow= not self.isShow
        if(self.isShow):
            self.tree.show()
            self.tree.setFixedWidth(self.lineEdit.width())
            self.tree.move(
                self.mapToGlobal(QtCore.QPoint(self.lineEdit.x(),
                            self.lineEdit.y()+self.lineEdit.height())))


        else:
            self.tree.hide()
            #self.setLayout(layout)
            #self.layout1.adjustSize()
    def movetree(self):
        if(self.isShow):
            #self.tree.hide()
            self.tree.setFixedWidth(self.lineEdit.width())
            self.tree.move(
                self.mapToGlobal(QtCore.QPoint(self.lineEdit.x(),
                                self.lineEdit.y()+self.lineEdit.height())))
            self.tree.show()
    def closetree(self):
        self.tree.close()
##    def closeEvent(self,event):
##        self.tree.close()
    def showselect(self):
        if(self.childTree):
            self.lineEdit.setText('')
            model=self.tree.model()
            for i in range(0,model.rowCount()):
                child=self.getcheckeditem(model.item(i))
                if(child):
                    path,text=os.path.split(model.item(i).text())
                    self.lineEdit.setText(self.lineEdit.text()+text+':'+str(child)+'; ')
                    
                    
        else:
            item=self.tree.currentIndex()
            path,text=os.path.split(item.data())
            self.lineEdit.setText(text)
            #print(item.data())
    #获得一个根文件哪几个波段被选择了
    def getcheckeditem(self,rootItem):
        child=[]
        for i in range(0,rootItem.rowCount()):
            if (rootItem.child(i).checkState()==QtCore.Qt.CheckState.Checked):
                child.append(i+1)
        #print (child)
        return child
    #拷贝一下树
    def copyTree(self,treeView,childTree=True,checked=True):
        newTree=QtWidgets.QTreeView(self)
        newTree.setHeaderHidden(True)
        #standmodel也要拷贝一下
        newmodel=QtGui.QStandardItemModel(self)
        oldmodel=treeView.model()
        if(not oldmodel):
            newTree.setModel(newmodel)
            return newTree,newmodel
        #newTree.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        #判断是否需要子节点
        for i in range(0,oldmodel.rowCount()):
            newmodel.setItem(i,oldmodel.item(i).clone())
            if(childTree):
                for j in range(0,oldmodel.item(i).rowCount()):
                    newmodel.item(i).setChild(j,oldmodel.item(i).child(j).clone())
                    #判断是否需要复选框
                    if(checked):
                        newmodel.item(i).child(j).setCheckState(QtCore.Qt.Unchecked)
                        newmodel.item(i).child(j).setCheckable(True)
                    else:
                        newmodel.item(i).child(j).setCheckable(False)
        newTree.setModel(newmodel)
        newTree.expandAll()

        #return newTree,newmodel
        return newTree,newmodel
class sendChild(QtCore.QObject):
    moveSignal=QtCore.Signal()
    closeSignal=QtCore.Signal()
        
class inputWindow(QtWidgets.QDialog):
    dump=[]
    def __init__(self,path,methodInfo,treeView=None,gdallist=None,parent=None):
        super().__init__(parent)
        self.treeView=treeView
        self.gdallist=gdallist
        self.okButton=QtWidgets.QPushButton(self.tr("ok"))
        self.okButton.clicked.connect(self.okclicked)
        #self.cancelButton=QtWidgets.QPushButton(self,self.tr("cancel"))
        self.path=path
        #self.methodInfo=self.readInfo(path+'/methodinfo')
        self.methodInfo=methodInfo
        self.inputParam=[]
        self.layout=QtWidgets.QGridLayout()
        self.parentMove=sendChild()
        #输入参数的序号，设置大概5行，然后添加列
        i=0
        j=0
        #输入参数的个数+2，2是后面哪个ok按钮和间隔。以方便布局
        numInput=len(self.methodInfo["input"])+1
        print('numInput:',numInput)
        for inputInfo in self.methodInfo["input"]:
            #注意，更正确的写法together应该是个字典，也不应该这么带，应该总体查询式的连接
            #together保存相关联的控件在methodinfo里面方便使用
            together=[]
            together.append(i)
            layout1=QtWidgets.QHBoxLayout()
            combox=None
            #如果参数是文件名类型的
            if inputInfo['type']=="filename":               
                label1=QtWidgets.QLabel(self)
                label1.setText(inputInfo["show"])
                together.append(label1)
                editline=QtWidgets.QLineEdit(self)
                editline.setText(inputInfo["default"])
                together.append(editline)
                QOpentoolButton=QtWidgets.QToolButton(self)
                QOpentoolButton.setText('...')
                together.append(QOpentoolButton)
                #可以通过按钮的friends找到相关的控件
                QOpentoolButton.friends=together
                QOpentoolButton.clicked.connect(self.getfilename)
                layout1.addWidget(label1)
                layout1.addWidget(editline)
                layout1.addWidget(QOpentoolButton)

                
            #如果参数是目录类型的
            if inputInfo['type']=="fold":               
                label1=QtWidgets.QLabel(self)
                label1.setText(inputInfo["show"])
                together.append(label1)
                editline=QtWidgets.QLineEdit(self)
                editline.setText(inputInfo["default"])
                together.append(editline)
                QOpentoolButton=QtWidgets.QToolButton(self)
                QOpentoolButton.setText('...')
                together.append(QOpentoolButton)
                #可以通过按钮的friends找到相关的控件
                QOpentoolButton.friends=together
                QOpentoolButton.clicked.connect(self.getfilepath)
                layout1.addWidget(label1)
                layout1.addWidget(editline)
                layout1.addWidget(QOpentoolButton)
                
            #如果参数是字符串类型的
            if inputInfo['type']=="str":               
                label1=QtWidgets.QLabel(self)
                label1.setText(inputInfo["show"])
                together.append(label1)
                editline=QtWidgets.QLineEdit(self)
                editline.setText(inputInfo["default"])
                together.append(editline)
                layout1.addWidget(label1)
                layout1.addWidget(editline)
                
            #如果参数是数值类型的，本来应该更细的，但没必要
            if inputInfo['type']=="num":               
                label1=QtWidgets.QLabel(self)
                label1.setText(inputInfo["show"])
                together.append(label1)
                editline=QtWidgets.QLineEdit(self)
                editline.setText(inputInfo["default"])
                together.append(editline)
                layout1.addWidget(label1)
                layout1.addWidget(editline)

                
            #如果参数是一个gdal对象，要求方法支持opengdal
            if inputInfo['type']=="gdalobject":
                label1=QtWidgets.QLabel(self)
                label1.setText(inputInfo["show"])
                together.append(label1)
                combox=Mycombobox(self,self.treeView,False)
                #editline.setText(inputInfo["default"])
                together.append(combox)
                layout1.addWidget(label1)
                layout1.addWidget(combox)
                
            #如果参数是一个image对象，选择一个图像，输出所有波段,没有设置范围，可以加
            if inputInfo['type']=="image":
                label1=QtWidgets.QLabel(self)
                label1.setText(inputInfo["show"])
                together.append(label1)
                combox=Mycombobox(self,self.treeView,False)
                #editline.setText(inputInfo["default"])
                together.append(combox)
                layout1.addWidget(label1)
                layout1.addWidget(combox)
            #如果参数是一个bands对象，选择多个波段作为输入
            if inputInfo['type']=="bands":
                label1=QtWidgets.QLabel(self)
                label1.setText(inputInfo["show"])
                together.append(label1)
                combox=Mycombobox(self,self.treeView)
                #editline.setText(inputInfo["default"])
                together.append(combox)
                layout1.addWidget(label1)
                layout1.addWidget(combox)
            #如果参数是一个band对象，选择一个波段作为输入
            if inputInfo['type']=="band":
                label1=QtWidgets.QLabel(self)
                label1.setText(inputInfo["show"])
                together.append(label1)
                combox=Mycombobox(self,self.treeView,True,True)
                together.append(combox)
                layout1.addWidget(label1)
                layout1.addWidget(combox)
            if(combox):
                self.parentMove.moveSignal.connect(combox.movetree)
                self.parentMove.closeSignal.connect(combox.closetree)
            inputInfo["control"]=together
            self.layout.addLayout(layout1,i%6,int(i/6))
            i=i+1
            
        
        self.layout2=QtWidgets.QHBoxLayout()
        self.layout2.addStretch()
        self.layout2.addWidget(self.okButton)
        self.layout.addLayout(self.layout2,5,int(numInput/6))
        self.setLayout(self.layout)

    def setchildcheck(self,model):
        return
    def closeEvent(self,event):
        self.parentMove.closeSignal.emit()
        
    def resizeEvent(self,event):
        #print('parent resize')
        self.parentMove.moveSignal.emit()
    def moveEvent(self,event):
        #print('parent move')
        self.parentMove.moveSignal.emit()
    #确定按钮事件
    def okclicked(self):
        debug=True
        #m=QtWidgets.QMessageBox.information(self,'note','The image will be processing,please wait',QtWidgets.QMessageBox.Yes)
        if (debug):
            #加载自定义方法
            ###############################################################################################

#这个地方还没写完
            ##############################################################################################3
            param={}

            myMethod=imp.load_source('method',os.path.join(self.path,self.methodInfo["mainfile"]))            
            f=getattr(myMethod,self.methodInfo['mainmethod'])
            for i in range(0,len(self.methodInfo['input'])):
                a=self.methodInfo['input'][i]
                #获取参数值
                if((a['type']=="filename")|(a['type']=="str")|(a['type']=="num")|(a['type']=="fold")):
                    param[a['name']]=a['control'][2].text()
                else:
                    combo=a['control'][2]
                    print('combo',combo)
                if(a['type']=='gdalobject'):
                    item=combo.tree.currentIndex()
                    if(0<=item.row()<len(self.gdallist)):
                        param[a['name']]=gdallist[item.row()]
                    else:
                        print("input error")
                        
                if(a['type']=='image'):
                    print(u'注意内存')
                    item=combo.tree.currentIndex()
                    if(0<=item.row()<len(self.gdallist)):
                        gdalobject=self.gdallist[item.row()]
                        bandnum=gdalobject.bandnum
                        img=gdalobject.GDALReadFile(range(1,bandnum+1))
                        if(len(img)==1):
                            img=img[0]
                        else:
                            img=np.array(img)
                            img=img.transpose(1,2,0)
                            param[a['name']]=img
                        #该类的共有内存，万一内存占用过多，用来释放内存
                        #dump.append(img)
                    else:
                        print("input error")
                if((a['type']=='band')|(a['type']=='bands')):
                    print(u'注意内存')
                    model=combo.tree.model()
                    img=[]
                    for i in range(0,model.rowCount()):
                        child=combo.getcheckeditem(model.item(i))
                        if(child):
                            
                            if(0<=i<len(self.gdallist)):
                                gdalobject=self.gdallist[i]
                                buf=gdalobject.GDALReadFile(child)
                                img=img+buf
                        else:
                            print(u'检查gdal列表')
                    #print('img-min-max',img[0].min(),img[0].max())

                    if(len(img)==1):
                        img=img[0]
                    else:
                        img=np.array(img)
                        img=img.transpose(1,2,0)
                    print('img-min-max',img.min(),img.max())
                    print(param)
                    print(a)
                    param[a['name']]=img
                    
                    #该类的共有内存，万一内存占用过多，用来释放内存
                    #dump.append(img)
                    
                
            #输出
            #print(param['img_r'].max())
            #print(param['img_g'].max())
            output=f(**param)
            if(len(self.methodInfo['output'])==1):
                b=self.methodInfo['output'][0]
                
                if((b['type']=="filename")|(b['type']=="str")|(b['type']=="num")|(b['type']=="fold")):
                    print (b['show'],':',output)
                else:
                    print('plot')
                    d=output
                    print(d.shape)
                    if(d.any()):
                        #print('aaa')
                        self.m=imShow(d.astype(np.uint8))
                        #result.setWindowTitle(b['show'])
                        #print('1')
                        self.m.setWindowTitle(b['show'])
                        self.m.show()
                        #print('2')
 
            else:
                for j in range(0,len(self.methodInfo['output'])):
                    b=self.methodInfo['output'][j]
                
                    if((b['type']=="filename")|(b['type']=="str")|(b['type']=="num")|(b['type']=="fold")):
                        print (b['show'],':',output[j])
                    else:
                        print('plot')
                        d=output[j]
                        print(d.shape)
                        if(output[j].any()):
                            self.m=imShow(output[j])
                            self.m.setWindowTitle(b['show'])
                            
                            self.m.show()
                            
            self.close()
        return 

    def getfilename(self):
        button=self.sender()
        lineEdit1=button.friends[2]
        path=QtWidgets.QFileDialog.getOpenFileName(self,
                        'Open file...', "./","All Files(*.*)")
        print(path)
        lineEdit1.setText(path[0])
        return 1
    #pyqt不支持对象拷贝，当然可以通过选择combox时候改变视图，但是之后很多麻烦

    def getfilepath(self):
        button=self.sender()
        lineEdit1=button.friends[2]
        path=QtWidgets.QFileDialog.getExistingDirectory(self,'path...',"./")
        print(path)
        if(path):
            lineEdit1.setText(path[0])
        return 1
            
       
    
