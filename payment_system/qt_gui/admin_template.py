# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'admin.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AdminWindow(object):
    def setupUi(self, AdminWindow):
        AdminWindow.setObjectName("AdminWindow")
        AdminWindow.setEnabled(True)
        AdminWindow.resize(999, 655)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../../../../.designer/backup/img/admin/admin_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AdminWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(AdminWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushPreviousPage = QtWidgets.QPushButton(self.centralwidget)
        self.pushPreviousPage.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushPreviousPage.setObjectName("pushPreviousPage")
        self.gridLayout.addWidget(self.pushPreviousPage, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.pushExit = QtWidgets.QPushButton(self.centralwidget)
        self.pushExit.setObjectName("pushExit")
        self.gridLayout.addWidget(self.pushExit, 3, 8, 1, 1)
        self.labelPage = QtWidgets.QLabel(self.centralwidget)
        self.labelPage.setMaximumSize(QtCore.QSize(100, 16777215))
        self.labelPage.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPage.setObjectName("labelPage")
        self.gridLayout.addWidget(self.labelPage, 1, 1, 1, 1)
        self.pushNextPage = QtWidgets.QPushButton(self.centralwidget)
        self.pushNextPage.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushNextPage.setObjectName("pushNextPage")
        self.gridLayout.addWidget(self.pushNextPage, 1, 2, 1, 1, QtCore.Qt.AlignLeft)
        self.lineEditPage = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditPage.sizePolicy().hasHeightForWidth())
        self.lineEditPage.setSizePolicy(sizePolicy)
        self.lineEditPage.setMaximumSize(QtCore.QSize(40, 16777215))
        self.lineEditPage.setObjectName("lineEditPage")
        self.gridLayout.addWidget(self.lineEditPage, 1, 8, 1, 1)
        self.comboBoxPerPage = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxPerPage.setMaximumSize(QtCore.QSize(70, 16777215))
        self.comboBoxPerPage.setMaxVisibleItems(10)
        self.comboBoxPerPage.setObjectName("comboBoxPerPage")
        self.comboBoxPerPage.addItem("")
        self.comboBoxPerPage.addItem("")
        self.comboBoxPerPage.addItem("")
        self.comboBoxPerPage.addItem("")
        self.comboBoxPerPage.addItem("")
        self.gridLayout.addWidget(self.comboBoxPerPage, 1, 4, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 9)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 3, 1, 1, QtCore.Qt.AlignRight)
        self.labelInfo = QtWidgets.QLabel(self.centralwidget)
        self.labelInfo.setObjectName("labelInfo")
        self.gridLayout.addWidget(self.labelInfo, 3, 0, 1, 5)
        self.labelRecordInfo = QtWidgets.QLabel(self.centralwidget)
        self.labelRecordInfo.setObjectName("labelRecordInfo")
        self.gridLayout.addWidget(self.labelRecordInfo, 3, 5, 1, 3)
        self.pushGoToPage = QtWidgets.QPushButton(self.centralwidget)
        self.pushGoToPage.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushGoToPage.setObjectName("pushGoToPage")
        self.gridLayout.addWidget(self.pushGoToPage, 1, 7, 1, 1)
        self.pushButton_add_record = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_add_record.setObjectName("pushButton_add_record")
        self.gridLayout.addWidget(self.pushButton_add_record, 1, 5, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        AdminWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AdminWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 999, 25))
        self.menubar.setObjectName("menubar")
        self.menuTerminals = QtWidgets.QMenu(self.menubar)
        self.menuTerminals.setObjectName("menuTerminals")
        self.menuOrganizations_DB = QtWidgets.QMenu(self.menubar)
        self.menuOrganizations_DB.setObjectName("menuOrganizations_DB")
        self.menuReports = QtWidgets.QMenu(self.menubar)
        self.menuReports.setObjectName("menuReports")
        self.menuReports_2 = QtWidgets.QMenu(self.menubar)
        self.menuReports_2.setObjectName("menuReports_2")
        AdminWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(AdminWindow)
        self.statusbar.setObjectName("statusbar")
        AdminWindow.setStatusBar(self.statusbar)
        self.actionTransactions_DB = QtWidgets.QAction(AdminWindow)
        self.actionTransactions_DB.setObjectName("actionTransactions_DB")
        self.actionAbout = QtWidgets.QAction(AdminWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExit = QtWidgets.QAction(AdminWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionTransactions = QtWidgets.QAction(AdminWindow)
        self.actionTransactions.setObjectName("actionTransactions")
        self.actionTerminals = QtWidgets.QAction(AdminWindow)
        self.actionTerminals.setObjectName("actionTerminals")
        self.actionOrganizations = QtWidgets.QAction(AdminWindow)
        self.actionOrganizations.setObjectName("actionOrganizations")
        self.actionOrganization_Types = QtWidgets.QAction(AdminWindow)
        self.actionOrganization_Types.setObjectName("actionOrganization_Types")
        self.actionCollectors = QtWidgets.QAction(AdminWindow)
        self.actionCollectors.setObjectName("actionCollectors")
        self.actionTransactionsReport = QtWidgets.QAction(AdminWindow)
        self.actionTransactionsReport.setObjectName("actionTransactionsReport")
        self.actionBy_terminal = QtWidgets.QAction(AdminWindow)
        self.actionBy_terminal.setObjectName("actionBy_terminal")
        self.actionTimespan_by_terminal = QtWidgets.QAction(AdminWindow)
        self.actionTimespan_by_terminal.setObjectName("actionTimespan_by_terminal")
        self.menuTerminals.addAction(self.actionAbout)
        self.menuTerminals.addSeparator()
        self.menuTerminals.addAction(self.actionExit)
        self.menuOrganizations_DB.addAction(self.actionTransactions)
        self.menuOrganizations_DB.addAction(self.actionTerminals)
        self.menuReports.addAction(self.actionOrganizations)
        self.menuReports.addAction(self.actionOrganization_Types)
        self.menuReports.addAction(self.actionCollectors)
        self.menuReports_2.addAction(self.actionTransactionsReport)
        self.menuReports_2.addAction(self.actionBy_terminal)
        self.menuReports_2.addAction(self.actionTimespan_by_terminal)
        self.menubar.addAction(self.menuTerminals.menuAction())
        self.menubar.addAction(self.menuOrganizations_DB.menuAction())
        self.menubar.addAction(self.menuReports.menuAction())
        self.menubar.addAction(self.menuReports_2.menuAction())

        self.retranslateUi(AdminWindow)
        self.comboBoxPerPage.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(AdminWindow)

    def retranslateUi(self, AdminWindow):
        _translate = QtCore.QCoreApplication.translate
        AdminWindow.setWindowTitle(_translate("AdminWindow", "Database administration"))
        self.pushPreviousPage.setText(_translate("AdminWindow", "<<"))
        self.pushExit.setText(_translate("AdminWindow", "Exit"))
        self.labelPage.setText(_translate("AdminWindow", "1 of 1"))
        self.pushNextPage.setText(_translate("AdminWindow", ">>"))
        self.lineEditPage.setText(_translate("AdminWindow", "1"))
        self.comboBoxPerPage.setItemText(0, _translate("AdminWindow", "10"))
        self.comboBoxPerPage.setItemText(1, _translate("AdminWindow", "25"))
        self.comboBoxPerPage.setItemText(2, _translate("AdminWindow", "50"))
        self.comboBoxPerPage.setItemText(3, _translate("AdminWindow", "100"))
        self.comboBoxPerPage.setItemText(4, _translate("AdminWindow", "200"))
        self.label.setText(_translate("AdminWindow", "Records per page: "))
        self.labelInfo.setText(_translate("AdminWindow", "Database and time information"))
        self.labelRecordInfo.setText(_translate("AdminWindow", "Record from 0000 to 50000. Total: 50000"))
        self.pushGoToPage.setText(_translate("AdminWindow", "Go to page"))
        self.pushButton_add_record.setText(_translate("AdminWindow", "Add record"))
        self.menuTerminals.setTitle(_translate("AdminWindow", "File"))
        self.menuOrganizations_DB.setTitle(_translate("AdminWindow", "Transactions DB"))
        self.menuReports.setTitle(_translate("AdminWindow", "Organizations DB"))
        self.menuReports_2.setTitle(_translate("AdminWindow", "Reports"))
        self.actionTransactions_DB.setText(_translate("AdminWindow", "Transactions DB"))
        self.actionAbout.setText(_translate("AdminWindow", "About"))
        self.actionExit.setText(_translate("AdminWindow", "Exit"))
        self.actionTransactions.setText(_translate("AdminWindow", "Transactions"))
        self.actionTerminals.setText(_translate("AdminWindow", "Terminals"))
        self.actionOrganizations.setText(_translate("AdminWindow", "Organizations"))
        self.actionOrganization_Types.setText(_translate("AdminWindow", "Organization Types"))
        self.actionCollectors.setText(_translate("AdminWindow", "Collectors"))
        self.actionTransactionsReport.setText(_translate("AdminWindow", "Transactions"))
        self.actionBy_terminal.setText(_translate("AdminWindow", "By terminal"))
        self.actionTimespan_by_terminal.setText(_translate("AdminWindow", "Timespan by terminal"))

