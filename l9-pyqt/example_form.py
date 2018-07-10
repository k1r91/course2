# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'practice.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(774, 625)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("teamwork.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap("teamwork.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        self.gridLayoutWidget = QtWidgets.QWidget(MainWindow)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 60, 621, 331))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushTable = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushTable.setObjectName("pushTable")
        self.gridLayout.addWidget(self.pushTable, 1, 0, 1, 1)
        self.pushExit = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushExit.setObjectName("pushExit")
        self.gridLayout.addWidget(self.pushExit, 1, 1, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 2)
        self.groupBox = QtWidgets.QGroupBox(MainWindow)
        self.groupBox.setGeometry(QtCore.QRect(100, 420, 521, 141))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(40, 30, 67, 17))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(40, 50, 151, 27))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Lesson practice"))
        self.pushTable.setText(_translate("MainWindow", "Fill table"))
        self.pushExit.setText(_translate("MainWindow", "Exit"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Description"))
        self.groupBox.setTitle(_translate("MainWindow", "Groupbox"))
        self.label.setText(_translate("MainWindow", "TextLabel"))

