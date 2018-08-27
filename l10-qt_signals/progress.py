# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progress.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Progress(object):
    def setupUi(self, Progress):
        Progress.setObjectName("Progress")
        Progress.resize(357, 111)
        self.progressBar = QtWidgets.QProgressBar(Progress)
        self.progressBar.setGeometry(QtCore.QRect(30, 30, 291, 51))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(Progress)
        QtCore.QMetaObject.connectSlotsByName(Progress)

    def retranslateUi(self, Progress):
        _translate = QtCore.QCoreApplication.translate
        Progress.setWindowTitle(_translate("Progress", "Dialog"))

