# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'terminal.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TerminalWindow(object):
    def setupUi(self, TerminalWindow):
        TerminalWindow.setObjectName("TerminalWindow")
        TerminalWindow.resize(462, 431)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("terminal.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TerminalWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(TerminalWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(40, 200, 371, 171))
        self.groupBox.setObjectName("groupBox")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 350, 141))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.push50rub = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.push50rub.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("img/50_rub_1.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push50rub.setIcon(icon1)
        self.push50rub.setIconSize(QtCore.QSize(100, 50))
        self.push50rub.setObjectName("push50rub")
        self.gridLayout.addWidget(self.push50rub, 1, 0, 1, 1)
        self.push500rub = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.push500rub.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("img/500_rub_1.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push500rub.setIcon(icon2)
        self.push500rub.setIconSize(QtCore.QSize(100, 50))
        self.push500rub.setObjectName("push500rub")
        self.gridLayout.addWidget(self.push500rub, 1, 1, 1, 1)
        self.push100rub = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.push100rub.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("img/100_rub_1.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push100rub.setIcon(icon3)
        self.push100rub.setIconSize(QtCore.QSize(100, 50))
        self.push100rub.setObjectName("push100rub")
        self.gridLayout.addWidget(self.push100rub, 0, 1, 1, 1)
        self.push10rub = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.push10rub.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("img/10_rub_1.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push10rub.setIcon(icon4)
        self.push10rub.setIconSize(QtCore.QSize(100, 50))
        self.push10rub.setObjectName("push10rub")
        self.gridLayout.addWidget(self.push10rub, 0, 0, 1, 1)
        self.push1000rub = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.push1000rub.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("img/1000_rub_1.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push1000rub.setIcon(icon5)
        self.push1000rub.setIconSize(QtCore.QSize(100, 50))
        self.push1000rub.setObjectName("push1000rub")
        self.gridLayout.addWidget(self.push1000rub, 0, 2, 1, 1)
        self.push5000rub = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.push5000rub.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("img/5000_rub_1.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push5000rub.setIcon(icon6)
        self.push5000rub.setIconSize(QtCore.QSize(100, 50))
        self.push5000rub.setObjectName("push5000rub")
        self.gridLayout.addWidget(self.push5000rub, 1, 2, 1, 1)
        self.editSumm = QtWidgets.QLineEdit(self.centralwidget)
        self.editSumm.setGeometry(QtCore.QRect(40, 140, 211, 41))
        font = QtGui.QFont()
        font.setFamily("DisplayOTF")
        font.setPointSize(40)
        self.editSumm.setFont(font)
        self.editSumm.setReadOnly(True)
        self.editSumm.setObjectName("editSumm")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 105, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 40, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 0, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(240, 0, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.editPhone = QtWidgets.QLineEdit(self.centralwidget)
        self.editPhone.setGeometry(QtCore.QRect(240, 40, 211, 41))
        font = QtGui.QFont()
        font.setFamily("DisplayOTF")
        font.setPointSize(16)
        self.editPhone.setFont(font)
        self.editPhone.setReadOnly(False)
        self.editPhone.setObjectName("editPhone")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(40, 380, 371, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.pushPay = QtWidgets.QPushButton(self.centralwidget)
        self.pushPay.setGeometry(QtCore.QRect(260, 140, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushPay.setFont(font)
        self.pushPay.setObjectName("pushPay")
        TerminalWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(TerminalWindow)
        self.statusbar.setObjectName("statusbar")
        TerminalWindow.setStatusBar(self.statusbar)

        self.retranslateUi(TerminalWindow)
        QtCore.QMetaObject.connectSlotsByName(TerminalWindow)

    def retranslateUi(self, TerminalWindow):
        _translate = QtCore.QCoreApplication.translate
        TerminalWindow.setWindowTitle(_translate("TerminalWindow", "Терминал"))
        self.groupBox.setTitle(_translate("TerminalWindow", "Купюроприемник"))
        self.editSumm.setText(_translate("TerminalWindow", "0"))
        self.label.setText(_translate("TerminalWindow", "Внесено"))
        self.comboBox.setItemText(0, _translate("TerminalWindow", "------"))
        self.comboBox.setItemText(1, _translate("TerminalWindow", "Билайн"))
        self.comboBox.setItemText(2, _translate("TerminalWindow", "МТС"))
        self.comboBox.setItemText(3, _translate("TerminalWindow", "Мегафон"))
        self.label_2.setText(_translate("TerminalWindow", "Оператор"))
        self.label_3.setText(_translate("TerminalWindow", "Номер телефона"))
        self.editPhone.setInputMask(_translate("TerminalWindow", "(000)000-00-00"))
        self.editPhone.setText(_translate("TerminalWindow", "()--"))
        self.editPhone.setPlaceholderText(_translate("TerminalWindow", "Введите номер"))
        self.pushPay.setText(_translate("TerminalWindow", "Оплатить"))

