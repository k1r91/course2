
import sys

from slider import slider
from progress import progress

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

class SliderDialog(QtWidgets.QDialog):

    # Добавляем Qt-сигнал
    changedValue = pyqtSignal(int)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = slider.Ui_SliderDialog()
        self.ui.setupUi(self)
        # Связываем оригинальный сигнал слайдера с функцией данного класса
        self.ui.horizontalSlider.valueChanged.connect(self.on_changed_value)        

    def on_changed_value(self, value):
        # Активируем сигнал
        self.changedValue.emit(value)


class ProgressDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = progress.Ui_ProgressDialog()
        self.ui.setupUi(self)

    # Создаём Qt-слот
    @pyqtSlot(int)
    def get_slider_value(self, val):
        self.ui.progressBar.setValue(val)

    def make_connection(self, slider_object):
        # Связываем "свой" сигнал со "своим" слотом
        slider_object.changedValue.connect(self.get_slider_value)        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    slider = SliderDialog()
    progress = ProgressDialog()
    
    progress.make_connection(slider)

    progress.show()
    slider.show()
    sys.exit(app.exec_()) 