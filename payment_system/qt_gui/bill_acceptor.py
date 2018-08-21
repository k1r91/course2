import sys
import time
import random
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot , QThread

sys.path.append('..')

from transaction import PaymentTransaction

class BillAcceptor(QtWidgets.QWidget):

    error_text = 'Banknote cannot be read!'

    def __init__(self, parent_terminal):
        super().__init__()
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
        self.progress_bar = self.ui.progressBar_bill_acceptor
        self.error_label = self.ui.label_error_bill_acceptor
        self.make_connections()
        self.__threads = list()

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
        denominations = [10, 50, 100, 200, 500, 1000, 2000, 5000]
        for i, btn in enumerate(self.buttons[1:]):
            btn.clicked.connect(self.insert_banknote(denominations[i]))

    def insert_banknote(self, banknote):
        def closure():
            for btn in self.buttons[1:]:
                btn.setEnabled(False)
            checker = BanknoteChecker(banknote)
            thread = QThread()
            self.__threads.append((thread, checker))
            checker.moveToThread(thread)
            checker.sig_step.connect(self.update_progress_bar)
            checker.sig_done.connect(self.accept_banknote)
            thread.started.connect(checker.simulate_banknote_checking)
            thread.start()
        return closure

    @pyqtSlot(int)
    def update_progress_bar(self, val: int):
        self.progress_bar.setValue(val)

    @pyqtSlot(int)
    def accept_banknote(self, banknote: int):
        for btn in self.buttons[1:]:
            btn.setEnabled(True)
        if banknote:
            oam = self.amount
            self.amount += banknote
            if self.amount > PaymentTransaction.MAX_AMOUNT // 100:
                self.amount = oam
                self.error_label.setStyleSheet('color: red;')
                self.error_label.setText('Max amount: {} rubles'.format(PaymentTransaction.MAX_AMOUNT // 100))
            else:
                self.error_label.setStyleSheet("color: green;")
                self.error_label.setText('OK')
                self.terminal.display.update_amount(self.amount)
        else:
            self.error_label.setStyleSheet("color: red;")
            self.error_label.setText('Sorry, your banknote is corrupted')


class Worker(QtCore.QObject):
    """
    Must derive from QObject in order to emit signals, connect slots to other signals, and operate in a QThread.
    """

    sig_step = pyqtSignal(int, str)  # worker id, step description: emitted every step through work() loop
    sig_done = pyqtSignal(int)  # worker id: emitted at end of work()
    sig_msg = pyqtSignal(str)  # message to be shown to user

    def __init__(self, id: int):
        super().__init__()
        self.__id = id
        self.__abort = False

    @pyqtSlot()
    def work(self):
        """
        Pretend this worker method does work that takes a long time. During this time, the thread's
        event loop is blocked, except if the application's processEvents() is called: this gives every
        thread (incl. main) a chance to process events, which in this sample means processing signals
        received from GUI (such as abort).
        """
        thread_name = QThread.currentThread().objectName()
        thread_id = int(QThread.currentThreadId())  # cast to int() is necessary
        self.sig_msg.emit('Running worker #{} from thread "{}" (#{})'.format(self.__id, thread_name, thread_id))

        for step in range(100):
            time.sleep(0.1)
            self.sig_step.emit(self.__id, 'step ' + str(step))

            # check if we need to abort the loop; need to process events to receive signals;
            # app.processEvents()  # this could cause change to self.__abort
            if self.__abort:
                # note that "step" value will not necessarily be same for every thread
                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                break

        self.sig_done.emit(self.__id)

    def abort(self):
        self.sig_msg.emit('Worker #{} notified to abort'.format(self.__id))
        self.__abort = True


class BanknoteChecker(Worker):

    sig_step = pyqtSignal(int)

    def __init__(self, banknote):
        super().__init__(0)
        self.banknote = banknote

    @pyqtSlot()
    def simulate_banknote_checking(self):
        for step in range(100):
            time.sleep(.01)
            self.sig_step.emit(step+1)
        seed = random.randint(0, 100)
        if seed < 5:
            self.sig_done.emit(0)
        else:
            self.sig_done.emit(self.banknote)


