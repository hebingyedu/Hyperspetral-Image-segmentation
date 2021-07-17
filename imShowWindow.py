#coding=utf-8
from PySide2 import QtWidgets, QtCore, QtGui
import sys
import numpy as np
import cv2
import math
import processRS
import pascal_voc_io
import time

class imShow(QtWidgets.QWidget):
    def __init__(self,im=None,imtype='dump',band=[1,2,3],parent=None,baseSize=600):
        super().__init__(parent)


        #设置当前图片
        self.imtype=imtype
        self.im=im
        self._image=QtGui.QPixmap()
        self.band=band

        #用来框选
        self.boundbox=QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle,self)
        

        #定义图片大小
        self.width=self._image.size().width()
        self.height=self._image.size().height()

        
        #定义显示的偏移值（从图片中心算吧），缩放值，鼠标位置等
        
        self.wOff=0
        self.hOff=0
        self.scale=1
        #定义窗口的基础大小为600,一开始用这个初始化
        self.baseSize=baseSize

        #鼠标相对于图片的位置？



        #设置窗口大小，加载控件，一个菜单栏，一个label，一个状态栏，2个滚动条
        
        self.menuBar=QtWidgets.QMenuBar()
        self.menuBar.addMenu('img')

        self.statuBar=QtWidgets.QStatusBar()
        self.label1=QtWidgets.QLabel()
        self.label1.setText('pos:')
        self.label2=QtWidgets.QLabel()
        self.label3=QtWidgets.QLabel()
        self.label3.setText('Zoom out:')
        self.label4=QtWidgets.QLabel()
        self.statuBar.addWidget(self.label1)
        self.statuBar.addWidget(self.label2)
        self.statuBar.addWidget(self.label3)
        self.statuBar.addWidget(self.label4)
        self.fileToolBar=QtWidgets.QToolBar()
        self.toolBar=QtWidgets.QToolBar()
        self.boxToolBar=QtWidgets.QToolBar()
        self._initActions()
        
        
        self.picView=QtWidgets.QWidget(self)
        self.view=QtWidgets.QLabel(self.picView)

        self.sel={}

        self.hScrollBar=QtWidgets.QScrollBar(QtCore.Qt.Orientation.Horizontal)
        self.vScrollBar=QtWidgets.QScrollBar()
        #self.vScrollBar.setFixedWidth(self.vScrollBar.height())

        self.hScrollBar.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtCore.Qt.blue)
        self.hScrollBar.setPalette(palette)
        self.vScrollBar.setPalette(palette)

        #判断ctrl键
        self.ctrlPressed=False
        self.m_drag = False
        self.drawBox=False
        #self.hScrollBar.hide()
        #self.vScrollBar.hide()
        

        
        #设置布局
        #计算窗口初始大小
        
        #self.resize(600,600)
        self.resize(QtCore.QSize(self.baseSize,self.baseSize))
        self.menuBar.setNativeMenuBar(False)
        self.menuBar.setFixedHeight(self.menuBar.height())
        self.statuBar.setFixedHeight(20)
        
        self.layout1=QtWidgets.QGridLayout()
        self.layout1.setMargin(0)
        self.layout1.setSpacing(0)
        self.toollayout=QtWidgets.QHBoxLayout()
        #self.layout1.addWidget(self.menuBar,0,0,1,2)
        self.toollayout.addWidget(self.fileToolBar,1,QtCore.Qt.AlignLeft)
        self.toollayout.addWidget(self.toolBar,3,QtCore.Qt.AlignLeft)
        self.toollayout.addWidget(self.boxToolBar,3,QtCore.Qt.AlignLeft)
        self.layout1.addLayout(self.toollayout,1,0,1,2)
        
        self.layout1.addWidget(self.picView,2,0)
        self.layout1.addWidget(self.vScrollBar,2,1)
        self.layout1.addWidget(self.hScrollBar,3,0)
        self.layout1.addWidget(self.statuBar,4,0,1,2)

        self.setLayout(self.layout1)
        self._InitImage(im,imtype)
        #其实有点重复，但为了方便还是设置了，要注意。
        #这是缩放后图片的大小.这个大小可能比view大，也可能比他小，这时候用到scroll显示
        #self.nowSize=self.imSize/self.scale
        #self.view.resize(self.nowSize)

        #调用画图
        #self.drawImg(self.scale,self.wOff,self.hOff)
        self.picView.resize(QtCore.QSize(self.baseSize,self.baseSize))
        
        #self.picView.adjustSize()
        self.view.resize(self.picView.size())
        self.scale=min(self.imSize.width(),self.imSize.height())/self.baseSize
        #self.nowSize=self.imSize/self.scale
        #print(self.view.size())
        
        
        self.drawImg(self.scale,self.wOff,self.hOff)
        #self.hScrollBar.hide()
        #self.vScrollBar.hide()
        self.reset()
        print('init')
    def saveCurImg(self):
        #np.save()
        fileName_choose, filetype = QtWidgets.QFileDialog.getSaveFileName(self, "文件保存", './', "All Files (*);;jpg(*.jpg)")
        if fileName_choose == "":
            print("\n取消选择")
            return
        self.pic.save(fileName_choose,"jpg")
        print('save file:'+fileName_choose)


    #设置窗口toolbar中的工具
    def _initActions(self):


        self.saveAction=QtWidgets.QAction(self)
        self.saveAction.setIcon(QtGui.QIcon('./icon/save.png'))
        self.saveAction.triggered.connect(self.saveCurImg)
        self.fileToolBar.addAction(self.saveAction)

        #设置图标zoomin是放大，zoomout是缩小
        self.zoomInAction=QtWidgets.QAction(self)
        self.zoomInAction.setIcon(QtGui.QIcon('./icon/zoom_in.png'))
        self.zoomInAction.triggered.connect(self.zoomIn)
        self.zoomOutAction=QtWidgets.QAction(self)
        self.zoomOutAction.setIcon(QtGui.QIcon('./icon/zoom_out.png'))
        self.zoomOutAction.triggered.connect(self.zoomOut)
        self.viewResetAction=QtWidgets.QAction(self)
        self.viewResetAction.setIcon(QtGui.QIcon('./icon/view_reset.png'))
        self.toolBar.addAction(self.zoomInAction)
        self.toolBar.addAction(self.zoomOutAction)
        self.toolBar.addAction(self.viewResetAction)
        self.viewResetAction.triggered.connect(self.reset)

        #设置框选
        self.boxAction=QtWidgets.QAction(self)
        self.boxAction.setIcon(QtGui.QIcon('./icon/box.png'))
        self.boxAction.setCheckable(True)
        self.boxAction.setChecked(False)
        self.boxAction.triggered.connect(self.setBox)
        self.boxToolBar.addAction(self.boxAction)

    
    #设置是否启动框选的状态
    def setBox(self):
        if(self.boxAction.isChecked()):
            self.drawBox=True
        else:
            self.drawBox=False
            
        
    #获取图像原始大小，并根据初始窗口大小设置放缩及改变长宽比
    def _InitImage(self,im,imtype):
        if(imtype=='dump'):
            self.imSize=QtCore.QSize(im.shape[1],im.shape[0])
            if(len(self.im.shape)==2):
                self.bandnum=1
            if(len(self.im.shape)==3):
                self.bandnum=self.im.shape[2]
        if(imtype=='filename'):
            self.pic1=QtGui.QPixmap(im)
            self.imSize=self.pic.size()
        if(imtype=='gdalobject'):
            self.gdalobject=self.im
            self.imSize=QtCore.QSize(self.gdalobject.XSize,self.gdalobject.YSize)
            self.bandnum=len(self.band)
        if(imtype=='gdalfile'):
            self.gdalobject=processRS.processRS(im)
            self.imSize=QtCore.QSize(self.gdalobject.XSize,self.gdalobject.YSize)
            self.bandnum=len(self.band)


            
    def reset(self):
        self.wOff=0
        self.hOff=0
        self.picView.adjustSize()
        print(self.picView.size())
        self.view.resize(self.picView.size())
        self.scale=max(self.imSize.width()/self.view.width(),self.imSize.height()/self.view.height())

        
        
        self.drawImg(self.scale,self.wOff,self.hOff)


    #把内存图像np.array转换成QPixmap

    def _imtoPic(self,im):
        if(len(im.shape)==3):
            self.imdepth=im.shape[2]
        else:
            self.imdepth=1
        if(self.imdepth==3):
            image = QtGui.QImage(im[:],im.shape[1], im.shape[0],im.shape[1] * 3, QtGui.QImage.Format_RGB888)
        if(self.imdepth==1):
            image = QtGui.QImage(im[:],im.shape[1], im.shape[0],im.shape[1], QtGui.QImage.Format_Grayscale8)
        if(self.imdepth==4):
            image = QtGui.QImage(im[:],im.shape[1], im.shape[0],im.shape[1], QtGui.QImage.Format_RGBA8888)
        pic=QtGui.QPixmap.fromImage(image)
        return pic
    
    #计算view中的点在图像中的位置
    def _viewtoOrigin(self,w,h,scale,woff,hoff):
        w1=int((w-woff)*scale)
        h1=int((h-hoff)*scale)
        return w1,h1
    def _origintoView(self,w,h,scale,woff,hoff):
        w1=int(w/scale+woff)
        h1=int(h/scale+hoff)
        return w1,h1

    
    #根据放缩值，当前窗口大小，偏移值获得子图像，此处最好有个判断。gdal也在这里更改
    def _getImRange(self,im,viewSize,scale,wOff,hOff):
        #注意numpy先高度后宽度
        #放缩后的图片大小

        #放缩前图片应该有的大小，这是为了以防万一，用0来填充,把图像直接填充到这里
        #改成按窗口大小来弄吧
        #print(viewSize.width(),scale,im.shape[2])

        
        #计算图像放缩后的大小
        scaledSize=self.imSize/scale
        #计算重叠区域在窗口里的起始点以及宽度

        if(wOff<0):
            startW=0
            startW1=-wOff
        else:
            startW=wOff
            startW1=0
        if(hOff<0):
            startH=0
            startH1=-hOff
        else:
            startH=hOff
            startH1=0
        #计算交叠区域的长宽 |A|+|B|-|AB|,如果没重叠区域，则结果小于0
        #计算并的大小
        unionW=max(wOff+scaledSize.width(),viewSize.width())-min(wOff,0)
        unionH=max(hOff+scaledSize.height(),viewSize.height())-min(hOff,0)
        if scaledSize.width()>viewSize.width():
            self.hScrollBar.show()
            self.hScrollBar.setMaximum(scaledSize.width()-viewSize.width())
            self.hScrollBar.setValue(-wOff)
        if scaledSize.height()>viewSize.height():
            self.vScrollBar.show()
            self.vScrollBar.setMaximum(scaledSize.height()-viewSize.height())
            self.vScrollBar.setValue(-hOff)
        overSize=scaledSize+viewSize-QtCore.QSize(unionW,unionH)
        if(not overSize.isValid()):
            overSize=QtCore.QSize(0,0)
        #先放缩，先记算在放缩后在图像的映射位置，对于gdal，直接读放缩的坐标，如果需要插值，先读个1倍然后用cv2放缩
        #内存图像,对于gdal图像，直接读比较好，就是要判断尺度：
        #注意，opencv这里又反过来了，有点坑
        
        h=overSize.height()
        w=overSize.width()
        if((self.imtype=='dump')|(self.imtype=='filename')):
            if (self.bandnum!=1):
                imnew=np.zeros((viewSize.height(),viewSize.width(),self.bandnum))
            if (self.bandnum==1):
                imnew=np.zeros((viewSize.height(),viewSize.width()))
            scaleImg=cv2.resize(im,(math.ceil(im.shape[1]/scale),math.ceil(im.shape[0]/scale)))
            imnew[startH:startH+h,startW:startW+w]=scaleImg[startH1:startH1+h,startW1:startW1+w]
        if((self.imtype=='gdalobject')|(self.imtype=='gdalfile')):
            #print('gdal')
            if (self.bandnum!=1):
                imnew=np.zeros((viewSize.height(),viewSize.width(),self.bandnum))
            if (self.bandnum==1):
                imnew=np.zeros((viewSize.height(),viewSize.width()))
            #print(imnew.shape)
            scaleH=h*scale
            scaleW=w*scale
            if ((h+startH1)*scale> self.imSize.height()):
                scale=scale*0.95
            if ((w+startW1)*scale>self.imSize.width()):
                scale=scale*0.95
            databuf=self.gdalobject.GDALReadFile(self.band,
                                        int(startW1*scale),int(startH1*scale),int(w*scale),int(h*scale),w,h)
    

            for i in range(0,len(databuf)):
                #print(databuf[i].shape)
                imnew[startH:startH+h,startW:startW+w,i]=databuf[i]

        return imnew.astype(np.uint8)


           

        
    def drawImg(self,scale,wOff,hOff):
        self.view.resize(self.picView.size())
        self.label4.setText(str(round(1/self.scale,2)))
        #print(self.picView.size())
        imnew=self._getImRange(self.im,self.picView.size(),scale,wOff,hOff)
        self.pic=self._imtoPic(imnew)
        self.view.setPixmap(self.pic)
    def resizeEvent(self,event):
        #self.adjustSize()
        #self.picView.adjustSize()
        self.view.resize(self.picView.size())
        #print(self.view.size(),self.picView.size())
        self.drawImg(self.scale,self.wOff,self.hOff)
        return
    def wheelEvent(self, event):
        if self.ctrlPressed:
            delta=event.angleDelta()
            oriention= delta.y()/8
            #当前视窗中心在图像中的位置
            #中心点可能不是视窗/2
##            print('center',self.view.width()/2,self.picView.height()/2)
            wCen,hCen=self._viewtoOrigin(self.picView.width()/2,self.picView.height()/2,self.scale,self.wOff,self.hOff)
##            print('center in image',wCen,hCen)
            x,y=self._origintoView(wCen,hCen,self.scale,self.wOff,self.hOff)
##            print('yanzheng',x,y)
      
            if oriention>0:
                self.zoomOut()
            else:
                self.zoomIn()

        else:
            return super().wheelEvent(event)
    def zoomIn(self):
        wCen,hCen=self._viewtoOrigin(self.picView.width()/2,self.picView.height()/2,self.scale,self.wOff,self.hOff)
        self.scale=self.scale*0.9
        wCen1,hCen1=self._origintoView(wCen,hCen,self.scale,self.wOff,self.hOff)
        self.wOff=-wCen1+int(self.picView.width()/2)+self.wOff
        self.hOff=-hCen1+int(self.picView.height()/2)+self.hOff
        self.drawImg(self.scale,int(self.wOff),int(self.hOff))

    def zoomOut(self):
        wCen,hCen=self._viewtoOrigin(self.picView.width()/2,self.picView.height()/2,self.scale,self.wOff,self.hOff)
        self.scale=self.scale*1.1
        wCen1,hCen1=self._origintoView(wCen,hCen,self.scale,self.wOff,self.hOff)
        self.wOff=-wCen1+int(self.picView.width()/2)+self.wOff
        self.hOff=-hCen1+int(self.picView.height()/2)+self.hOff
        self.drawImg(self.scale,int(self.wOff),int(self.hOff))

        
    def keyReleaseEvent(self, QKeyEvent):
        if QKeyEvent.key()==QtCore.Qt.Key_Control:
            self.ctrlPressed=False
            self.label2.setText('')
            self.unsetCursor()
            return super().keyReleaseEvent(QKeyEvent)
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key()==QtCore.Qt.Key_Control:
            self.ctrlPressed=True
            pos=self.view.mapFromGlobal(QtGui.QCursor.pos())
            w,h=self._viewtoOrigin(pos.x(),pos.y(),self.scale,self.wOff,self.hOff)
            self.label2.setText(str(w)+','+str(h))
            
            self.setCursor(QtCore.Qt.CrossCursor)
            #print("The ctrl key is holding down")
            return super().keyPressEvent(QKeyEvent)
    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.setCursor(QtCore.Qt.OpenHandCursor)
            self.orginWOff=self.wOff
            self.orginHOff=self.hOff
            self.m_drag = True
            self.m_DragPosition = event.pos()
            event.accept()

    def mouseMoveEvent(self, event):       
        try:
            if event.buttons() and QtCore.Qt.LeftButton:
                movePos=event.pos()-self.m_DragPosition
                #print(movePos)
                self.wOff=self.orginWOff+int(movePos.x())
                self.hOff=self.orginHOff+int(movePos.y())
                #print(self.wOff)
                self.drawImg(self.scale,self.wOff,self.hOff)
                event.accept()
        except AttributeError:
            pass

    def mouseReleaseEvent(self, event):
    
        if event.button()==QtCore.Qt.LeftButton:
            self.m_drag = False
            self.unsetCursor()








##app=QtWidgets.QApplication(sys.argv)
##im=cv2.imread('./data/test3.jpg')
###m=QtWidgets.QMainWindow()
##
##w=imShow(im)
###m.show()
##w.show()
##sys.exit(app.exec_())
