
import sys
import asyncio

from PyQt5 import QtCore, QtGui, QtWidgets

from terminal import *


class TerminalWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_TerminalWindow()
        self.ui.setupUi(self)

        self._temp_summ = 0
        self._loop = asyncio.get_event_loop()
        self.ui.push10rub.clicked.connect(lambda: self.insert_banknote(10))
        self.ui.push50rub.clicked.connect(lambda: self.insert_banknote(50))

        self.ui.pushPay.clicked.connect(self.ui.editSumm.clear)


    def closeEvent(self, event):
        self._loop.close()

    def test(self, x):
        pass

    def insert_banknote(self, banknote):
        '''
            Запускаем режим ввода купюр в купюроприемник
        '''
        self._loop.run_until_complete(self.banknotes(banknote))

    async def banknotes(self, banknote):
        '''
            Купюроприемник ждёт купюру
        '''
        summ = await self._money_process(banknote)
        self.ui.editSumm.setText(str(summ))

    async def _money_process(self, banknote):
        ''' Купюроприёмник думает...
        '''    
        for i in range(100):
            self.ui.progressBar.setValue(i)
            try:
                await asyncio.sleep(0.01)
            except asyncio.CanceledError:
                pass

        self.ui.progressBar.setValue(0)            
        self._temp_summ += banknote
        return self._temp_summ


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_win = TerminalWin()
    main_win.show()
    sys.exit(app.exec_())
