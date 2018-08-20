import time
from PyQt5 import QtCore, QtGui, QtWidgets


class BillAcceptor:

    def __init__(self, parent_terminal):
        self.terminal = parent_terminal
        self.ui = self.terminal.ui
        self.timer = QtCore.QTimer()
        self.state = 0
        self.timer.timeout.connect(self.change_image)
        self.amount = 0
        self.active = False
        self.buttons = [
            self.ui.pushButton_bill_acceptor_icon,
            self.ui.pushButton_10,
            self.ui.pushButton_50,
            self.ui.pushButton_100,
            self.ui.pushButton_200,
            self.ui.pushButton_500,
            self.ui.pushButton_1000,
            self.ui.pushButton_2000,
            self.ui.pushButton_5000,
        ]

    def activate(self):
        '''
        start main process, enables all elements of bill acceptor
        :return:
        '''
        self.active = True
        for btn in self.buttons:
            btn.setEnabled(True)
        while self.active:
            self.change_image()
            time.sleep(1)

    def deactivate(self):
        '''
        stop main process
        :return:
        '''
        for btn in self.buttons:
            btn.setEnabled(False)
        self.active = False
        self.amount = 0
        self.ui.pushButton_bill_acceptor_icon.setEnabled(False)

    def change_image(self):
        '''
        change image of bill acceptor icon
        :return:
        '''
        if self.state:
            icon8 = QtGui.QIcon()
            icon8.addPixmap(QtGui.QPixmap("img/terminal/bill_acceptor_2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_bill_acceptor_icon.setIcon(icon8)
            self.ui.pushButton_bill_acceptor_icon.setIconSize(QtCore.QSize(151, 201))
            self.state = 0
        else:
            icon8 = QtGui.QIcon()
            icon8.addPixmap(QtGui.QPixmap("img/terminal/bill_acceptor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_bill_acceptor_icon.setIcon(icon8)
            self.ui.pushButton_bill_acceptor_icon.setIconSize(QtCore.QSize(151, 201))
            self.state = 1

    def make_connections(self):
        '''
        create connections to click event on all buttons
        :return:
        '''
        pass