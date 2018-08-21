import time
import fpdf
from PyQt5 import QtGui, QtCore


class CheckPrinter:
    def __init__(self, parent, *args, **kwargs):
        self.terminal = parent
        self.ui = parent.ui
        self.main_button = self.ui.pushCheckPrinter
        self.state = 0
        self.active = False
        self.main_button.clicked.connect(self.print_check)
        self.data = dict()

    def activate(self, data):
        self.data = data
        self.active = True
        self.main_button.setEnabled(True)
        while self.active:
            time.sleep(.5)
            self.change_image()

    def deactivate(self):
        self.active = False
        self.main_button.setEnabled(False)

    def change_image(self):
        if self.state:
            icon8 = QtGui.QIcon()
            icon8.addPixmap(QtGui.QPixmap("img/terminal/check_printer_2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.main_button.setIcon(icon8)
            self.main_button.setIconSize(QtCore.QSize(200, 200))
            self.state = 0
        else:
            icon8 = QtGui.QIcon()
            icon8.addPixmap(QtGui.QPixmap("img/terminal/check_printer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.main_button.setIcon(icon8)
            self.main_button.setIconSize(QtCore.QSize(200, 200))
            self.state = 1

    def print_check(self):
        print(self.data)
        self.deactivate()
