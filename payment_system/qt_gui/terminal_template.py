# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'terminal.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TerminalMainWindow(object):
    def setupUi(self, TerminalMainWindow):
        TerminalMainWindow.setObjectName("TerminalMainWindow")
        TerminalMainWindow.setEnabled(True)
        TerminalMainWindow.resize(1210, 843)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TerminalMainWindow.sizePolicy().hasHeightForWidth())
        TerminalMainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(TerminalMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1211, 801))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_main = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_main.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_main.setHorizontalSpacing(6)
        self.gridLayout_main.setObjectName("gridLayout_main")
        self.display_widget = QtWidgets.QWidget(self.gridLayoutWidget)
        self.display_widget.setAutoFillBackground(False)
        self.display_widget.setStyleSheet("border-image: url(img/terminal/display.png) 0 0 0 0 stretch stretch;")
        self.display_widget.setObjectName("display_widget")
        self.widget_2 = QtWidgets.QWidget(self.display_widget)
        self.widget_2.setGeometry(QtCore.QRect(90, 160, 1021, 311))
        self.widget_2.setStyleSheet("border-image: none;")
        self.widget_2.setObjectName("widget_2")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.widget_2)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 1021, 311))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.grid_bottom = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.grid_bottom.setContentsMargins(0, 0, 0, 0)
        self.grid_bottom.setObjectName("grid_bottom")
        self.widget_top = QtWidgets.QWidget(self.display_widget)
        self.widget_top.setGeometry(QtCore.QRect(90, 90, 969, 49))
        self.widget_top.setStyleSheet("border-image: none;")
        self.widget_top.setObjectName("widget_top")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.widget_top)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 971, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_top = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_top.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_top.setObjectName("horizontalLayout_top")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_top.addItem(spacerItem)
        self.label_status = QtWidgets.QLabel(self.display_widget)
        self.label_status.setGeometry(QtCore.QRect(590, 50, 391, 31))
        self.label_status.setStyleSheet("color: blue;\n"
"font-size: 9pt;\n"
"font-weight: 600;\n"
"border-image: none;")
        self.label_status.setObjectName("label_status")
        self.widget_2.raise_()
        self.widget_top.raise_()
        self.label_status.raise_()
        self.gridLayout_main.addWidget(self.display_widget, 0, 0, 1, 3)
        self.pushStrongBox = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushStrongBox.setMinimumSize(QtCore.QSize(0, 250))
        self.pushStrongBox.setObjectName("pushStrongBox")
        self.gridLayout_main.addWidget(self.pushStrongBox, 1, 1, 1, 1)
        self.pushCheckPrinter = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushCheckPrinter.setMinimumSize(QtCore.QSize(0, 250))
        self.pushCheckPrinter.setObjectName("pushCheckPrinter")
        self.gridLayout_main.addWidget(self.pushCheckPrinter, 1, 0, 1, 1)
        self.widget_bill_acceptor = QtWidgets.QWidget(self.gridLayoutWidget)
        self.widget_bill_acceptor.setObjectName("widget_bill_acceptor")
        self.pushButton_10 = QtWidgets.QPushButton(self.widget_bill_acceptor)
        self.pushButton_10.setEnabled(False)
        self.pushButton_10.setGeometry(QtCore.QRect(160, 0, 105, 45))
        self.pushButton_10.setMinimumSize(QtCore.QSize(105, 45))
        self.pushButton_10.setMaximumSize(QtCore.QSize(105, 45))
        self.pushButton_10.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/terminal/10rubles.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_10.setIcon(icon)
        self.pushButton_10.setIconSize(QtCore.QSize(95, 42))
        self.pushButton_10.setObjectName("pushButton_10")
        self.progressBar_bill_acceptor = QtWidgets.QProgressBar(self.widget_bill_acceptor)
        self.progressBar_bill_acceptor.setGeometry(QtCore.QRect(0, 212, 381, 31))
        self.progressBar_bill_acceptor.setProperty("value", 0)
        self.progressBar_bill_acceptor.setObjectName("progressBar_bill_acceptor")
        self.pushButton_50 = QtWidgets.QPushButton(self.widget_bill_acceptor)
        self.pushButton_50.setEnabled(False)
        self.pushButton_50.setGeometry(QtCore.QRect(270, 0, 105, 45))
        self.pushButton_50.setMinimumSize(QtCore.QSize(105, 45))
        self.pushButton_50.setMaximumSize(QtCore.QSize(105, 45))
        self.pushButton_50.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("img/terminal/50rubles.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_50.setIcon(icon1)
        self.pushButton_50.setIconSize(QtCore.QSize(95, 42))
        self.pushButton_50.setObjectName("pushButton_50")
        self.pushButton_200 = QtWidgets.QPushButton(self.widget_bill_acceptor)
        self.pushButton_200.setEnabled(False)
        self.pushButton_200.setGeometry(QtCore.QRect(270, 50, 105, 45))
        self.pushButton_200.setMinimumSize(QtCore.QSize(105, 45))
        self.pushButton_200.setMaximumSize(QtCore.QSize(105, 45))
        self.pushButton_200.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("img/terminal/200rubles.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_200.setIcon(icon2)
        self.pushButton_200.setIconSize(QtCore.QSize(95, 42))
        self.pushButton_200.setObjectName("pushButton_200")
        self.pushButton_100 = QtWidgets.QPushButton(self.widget_bill_acceptor)
        self.pushButton_100.setEnabled(False)
        self.pushButton_100.setGeometry(QtCore.QRect(160, 50, 105, 45))
        self.pushButton_100.setMinimumSize(QtCore.QSize(105, 45))
        self.pushButton_100.setMaximumSize(QtCore.QSize(105, 45))
        self.pushButton_100.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("img/terminal/100rubles.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_100.setIcon(icon3)
        self.pushButton_100.setIconSize(QtCore.QSize(95, 42))
        self.pushButton_100.setObjectName("pushButton_100")
        self.pushButton_1000 = QtWidgets.QPushButton(self.widget_bill_acceptor)
        self.pushButton_1000.setEnabled(False)
        self.pushButton_1000.setGeometry(QtCore.QRect(270, 100, 105, 45))
        self.pushButton_1000.setMinimumSize(QtCore.QSize(105, 45))
        self.pushButton_1000.setMaximumSize(QtCore.QSize(105, 45))
        self.pushButton_1000.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("img/terminal/1000rubles.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_1000.setIcon(icon4)
        self.pushButton_1000.setIconSize(QtCore.QSize(95, 41))
        self.pushButton_1000.setObjectName("pushButton_1000")
        self.pushButton_500 = QtWidgets.QPushButton(self.widget_bill_acceptor)
        self.pushButton_500.setEnabled(False)
        self.pushButton_500.setGeometry(QtCore.QRect(160, 100, 105, 45))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_500.sizePolicy().hasHeightForWidth())
        self.pushButton_500.setSizePolicy(sizePolicy)
        self.pushButton_500.setMinimumSize(QtCore.QSize(105, 45))
        self.pushButton_500.setMaximumSize(QtCore.QSize(105, 45))
        self.pushButton_500.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("img/terminal/500rubles.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_500.setIcon(icon5)
        self.pushButton_500.setIconSize(QtCore.QSize(95, 42))
        self.pushButton_500.setObjectName("pushButton_500")
        self.pushButton_5000 = QtWidgets.QPushButton(self.widget_bill_acceptor)
        self.pushButton_5000.setEnabled(False)
        self.pushButton_5000.setGeometry(QtCore.QRect(270, 150, 105, 45))
        self.pushButton_5000.setMinimumSize(QtCore.QSize(105, 45))
        self.pushButton_5000.setMaximumSize(QtCore.QSize(105, 45))
        self.pushButton_5000.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("img/terminal/5000rubles.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5000.setIcon(icon6)
        self.pushButton_5000.setIconSize(QtCore.QSize(95, 41))
        self.pushButton_5000.setObjectName("pushButton_5000")
        self.pushButton_2000 = QtWidgets.QPushButton(self.widget_bill_acceptor)
        self.pushButton_2000.setEnabled(False)
        self.pushButton_2000.setGeometry(QtCore.QRect(160, 150, 105, 45))
        self.pushButton_2000.setMinimumSize(QtCore.QSize(105, 45))
        self.pushButton_2000.setMaximumSize(QtCore.QSize(105, 45))
        self.pushButton_2000.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("img/terminal/2000rubles.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2000.setIcon(icon7)
        self.pushButton_2000.setIconSize(QtCore.QSize(95, 41))
        self.pushButton_2000.setObjectName("pushButton_2000")
        self.pushButton_bill_acceptor_icon = QtWidgets.QPushButton(self.widget_bill_acceptor)
        self.pushButton_bill_acceptor_icon.setEnabled(False)
        self.pushButton_bill_acceptor_icon.setGeometry(QtCore.QRect(0, 0, 151, 201))
        self.pushButton_bill_acceptor_icon.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("img/terminal/bill_acceptor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_bill_acceptor_icon.setIcon(icon8)
        self.pushButton_bill_acceptor_icon.setIconSize(QtCore.QSize(151, 201))
        self.pushButton_bill_acceptor_icon.setObjectName("pushButton_bill_acceptor_icon")
        self.gridLayout_main.addWidget(self.widget_bill_acceptor, 1, 2, 1, 1)
        TerminalMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TerminalMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1210, 25))
        self.menubar.setObjectName("menubar")
        TerminalMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(TerminalMainWindow)
        self.statusbar.setObjectName("statusbar")
        TerminalMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(TerminalMainWindow)
        QtCore.QMetaObject.connectSlotsByName(TerminalMainWindow)

    def retranslateUi(self, TerminalMainWindow):
        _translate = QtCore.QCoreApplication.translate
        TerminalMainWindow.setWindowTitle(_translate("TerminalMainWindow", "MainWindow"))
        self.label_status.setText(_translate("TerminalMainWindow", "TextLabel"))
        self.pushStrongBox.setText(_translate("TerminalMainWindow", "Strong Box"))
        self.pushCheckPrinter.setText(_translate("TerminalMainWindow", "Check Printer"))

