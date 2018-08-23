import time
from PyQt5 import QtWidgets, QtCore, QtGui


class StrongBox:

    def __init__(self, parent):
        self.terminal = parent
        self.ui = parent.ui
        self.main_button = self.ui.pushStrongBox
        self.state = 0
        self.active = False
        self.cash = 0
        self.main_button.clicked.connect(self.take_money)

    def activate(self, cash):
        self.active = True
        self.main_button.setEnabled(True)
        self.cash = cash
        while self.active:
            self.change_image()
            time.sleep(1)

    def deactivate(self):
        self.main_button.setEnabled(False)
        self.active = False
        self.terminal.display.load_main_screen()

    def take_money(self):
        self.display_money_page()
        self.deactivate()

    def change_image(self):
        if self.state:
            icon8 = QtGui.QIcon()
            icon8.addPixmap(QtGui.QPixmap("img/terminal/strongbox_2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.main_button.setIcon(icon8)
            self.main_button.setIconSize(QtCore.QSize(200, 200))
            self.state = 0
        else:
            icon8 = QtGui.QIcon()
            icon8.addPixmap(QtGui.QPixmap("img/terminal/strongbox.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.main_button.setIcon(icon8)
            self.main_button.setIconSize(QtCore.QSize(200, 200))
            self.state = 1

    def display_money_page(self):
        money = QtWidgets.QDialog()
        money.setWindowTitle('Your money:')
        money_label = QtWidgets.QLabel('You have earned {} rubles!'.format(self.cash))
        money_layout = QtWidgets.QGridLayout(money)
        money_layout.addWidget(money_label, 0, 0, 1, 1, QtCore.Qt.AlignCenter)
        money.exec_()