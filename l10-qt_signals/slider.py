# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'slider.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Slider(object):
    def setupUi(self, Slider):
        Slider.setObjectName("Slider")
        Slider.resize(354, 112)
        self.horizontalSlider = QtWidgets.QSlider(Slider)
        self.horizontalSlider.setGeometry(QtCore.QRect(50, 28, 271, 51))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")

        self.retranslateUi(Slider)
        QtCore.QMetaObject.connectSlotsByName(Slider)

    def retranslateUi(self, Slider):
        _translate = QtCore.QCoreApplication.translate
        Slider.setWindowTitle(_translate("Slider", "Dialog"))

