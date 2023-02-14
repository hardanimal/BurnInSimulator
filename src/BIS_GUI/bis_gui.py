# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bis_gui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BIS_GUI(object):
    def setupUi(self, BIS_GUI):
        BIS_GUI.setObjectName("BIS_GUI")
        BIS_GUI.resize(894, 181)
        self.btn_START = QtWidgets.QPushButton(BIS_GUI)
        self.btn_START.setGeometry(QtCore.QRect(20, 130, 99, 30))
        self.btn_START.setObjectName("btn_START")
        self.btn_PAUSE = QtWidgets.QPushButton(BIS_GUI)
        self.btn_PAUSE.setGeometry(QtCore.QRect(130, 130, 99, 30))
        self.btn_PAUSE.setObjectName("btn_PAUSE")
        self.btn_STUCK = QtWidgets.QPushButton(BIS_GUI)
        self.btn_STUCK.setGeometry(QtCore.QRect(240, 130, 99, 30))
        self.btn_STUCK.setObjectName("btn_STUCK")
        self.lbl_Status = QtWidgets.QLabel(BIS_GUI)
        self.lbl_Status.setGeometry(QtCore.QRect(90, 70, 221, 36))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lbl_Status.setFont(font)
        self.lbl_Status.setObjectName("lbl_Status")
        self.rtbLog = QtWidgets.QTextEdit(BIS_GUI)
        self.rtbLog.setGeometry(QtCore.QRect(350, 30, 531, 131))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.rtbLog.setFont(font)
        self.rtbLog.setObjectName("rtbLog")
        self.btn_LoadConfig = QtWidgets.QPushButton(BIS_GUI)
        self.btn_LoadConfig.setGeometry(QtCore.QRect(20, 30, 99, 30))
        self.btn_LoadConfig.setObjectName("btn_LoadConfig")

        self.retranslateUi(BIS_GUI)
        QtCore.QMetaObject.connectSlotsByName(BIS_GUI)

    def retranslateUi(self, BIS_GUI):
        _translate = QtCore.QCoreApplication.translate
        BIS_GUI.setWindowTitle(_translate("BIS_GUI", "BIS_GUI"))
        self.btn_START.setText(_translate("BIS_GUI", "START"))
        self.btn_PAUSE.setText(_translate("BIS_GUI", "PAUSE"))
        self.btn_STUCK.setText(_translate("BIS_GUI", "STUCK"))
        self.lbl_Status.setText(_translate("BIS_GUI", "Status:INIT"))
        self.btn_LoadConfig.setText(_translate("BIS_GUI", "LoadConfig"))

