import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from progress import *
from slider import *


class ProgressBar(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Progress()
        self.ui.setupUi(self)

    @pyqtSlot(int)
    def slot(self, value):
        self.ui.progressBar.setValue(value)

    def make_connect(self, slider):
        slider.changedValue.connect(self.slot)


class Slider(QtWidgets.QDialog):

    changedValue = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Slider()
        self.ui.setupUi(self)
        self.ui.horizontalSlider.valueChanged.connect(self.on_changed)

    def on_changed(self, value):
        self.changedValue.emit(value)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    progress = ProgressBar()
    slider = Slider()
    progress.make_connect(slider)
    slider.show()
    progress.show()
    app.exec_()