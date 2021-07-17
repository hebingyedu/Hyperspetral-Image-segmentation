# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui',
# licensing of 'setting.ui' applies.
#
# Created: Wed Mar  6 15:50:13 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(QtCore.QObject):
    def setupUi(self, Dialog):
        self.Dialog=Dialog
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(400, 189)
        
        self.buttonBox = QtWidgets.QDialogButtonBox(self.Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 150, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 361, 121))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label1 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label1.setObjectName("label1")
        self.horizontalLayout.addWidget(self.label1)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.button1 = QtWidgets.QToolButton(self.verticalLayoutWidget)
        self.button1.setObjectName("button1")
        self.horizontalLayout.addWidget(self.button1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label2.setObjectName("label2")
        self.horizontalLayout_2.addWidget(self.label2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.button2 = QtWidgets.QToolButton(self.verticalLayoutWidget)
        self.button2.setObjectName("button2")
        self.horizontalLayout_2.addWidget(self.button2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label3.setObjectName("label3")
        self.horizontalLayout_3.addWidget(self.label3)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_3.addWidget(self.lineEdit_3)
        self.button3 = QtWidgets.QToolButton(self.verticalLayoutWidget)
        self.button3.setObjectName("button3")
        self.horizontalLayout_3.addWidget(self.button3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        

        self.readSetting()
        self.retranslateUi(self.Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.writeSetting)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.Dialog.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.readSetting)
        QtCore.QObject.connect(self.button1, QtCore.SIGNAL("clicked()"), self.openFileDialog)
        QtCore.QObject.connect(self.button2, QtCore.SIGNAL("clicked()"), self.openFileDialog)
        QtCore.QObject.connect(self.button3, QtCore.SIGNAL("clicked()"), self.openFileDialog)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)

    def readSetting(self):
        setting=QtCore.QSettings("ImageProcessing","Wangtf")
        if(setting.value('plugpath')==""):
            setting.setValue('plugpath',"./")
        self.lineEdit.setText(setting.value('plugpath'))
    def writeSetting(self):
        print('defalt')
        setting=QtCore.QSettings("ImageProcessing","Wangtf")
        setting.setValue('plugpath',self.lineEdit.text())

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.label1.setText(QtWidgets.QApplication.translate("Dialog", "Plug path", None, -1))
        self.button1.setText(QtWidgets.QApplication.translate("Dialog", "...", None, -1))
        self.label2.setText(QtWidgets.QApplication.translate("Dialog", "TextLabel", None, -1))
        self.button2.setText(QtWidgets.QApplication.translate("Dialog", "...", None, -1))
        self.label3.setText(QtWidgets.QApplication.translate("Dialog", "TextLabel", None, -1))
        self.button3.setText(QtWidgets.QApplication.translate("Dialog", "...", None, -1))
        
    def openFileDialog(self):
        button=self.sender()
        self.path=QtWidgets.QFileDialog.getExistingDirectory(self.Dialog,'path...',"./")
        if (button.objectName()=='button1'):
            self.lineEdit.setText(self.path)
        if (button.objectName()=='button2'):
            self.lineEdit_2.setText(self.path)
        if (button.objectName()=='button3'):
            self.lineEdit_3.setText(self.path)
            

