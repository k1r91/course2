import sys
import datetime
import hashlib
from PyQt5 import QtWidgets, QtCore, QtGui

sys.path.append('..')

from transaction import PaymentTransactionException


class Display:
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.ui = parent.ui
        self.layout_top = self.ui.horizontalLayout_top
        self.grid_bottom = self.ui.grid_bottom
        self.parent.refresh_org_db()
        self.current_page = 0
        self.load_status_string()
        self.header_buttons = list()
        self.org_buttons = list()
        self.elems = list()
        self.return_timer = QtCore.QTimer()
        self.return_timer.connected = False
        self.incorrect_code = 0

    def flush_screen(self):
        self.elems = self.elems + self.header_buttons + self.org_buttons
        for elem in self.elems:
            elem.close()

    def settings_auth_page(self):
        '''
        Settings authentication page
        :return:
        '''
        self.flush_screen()
        self.sa_pwd_label = QtWidgets.QLabel('Enter password: ')
        self.sa_pwd_line = QtWidgets.QLineEdit()
        self.sa_pwd_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.sa_ok = QtWidgets.QPushButton('OK')
        self.sa_cancel = QtWidgets.QPushButton('Cancel')
        self.sa_cancel.clicked.connect(self.cancel_pay)
        self.sa_ok.clicked.connect(self.settings_page)
        self.sa_error = QtWidgets.QLabel()
        self.sa_error.setStyleSheet('color: red')
        self.grid_bottom.addWidget(self.sa_pwd_label, 0, 0, 1, 2, QtCore.Qt.AlignCenter)
        self.grid_bottom.addWidget(self.sa_pwd_line, 1, 0, 1, 2, QtCore.Qt.AlignCenter|QtCore.Qt.AlignTop)
        self.grid_bottom.addWidget(self.sa_ok, 2, 0, 1, 1, QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.grid_bottom.addWidget(self.sa_cancel, 2, 1, 1, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.grid_bottom.addWidget(self.sa_error, 3, 0, 1, 2, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        self.elems += [self.sa_pwd_label, self.sa_pwd_line, self.sa_ok, self.sa_cancel, self.sa_error]

    def settings_page(self):
        pwd = hashlib.sha256(self.sa_pwd_line.text().encode('utf-8')).hexdigest()
        if pwd != self.parent.secret:
            self.raise_incorrect_code()
            return
        self.flush_screen()
        self.s_block = QtWidgets.QPushButton('Block')
        self.s_block.clicked.connect(self.block)
        self.s_unblock = QtWidgets.QPushButton('Unblock')
        self.s_unblock.clicked.connect(self.unblock)
        self.s_restart = QtWidgets.QPushButton('Restart')
        self.s_restart.clicked.connect(self.parent.restart)
        self.s_shutdown = QtWidgets.QPushButton('Shutdown')
        self.s_shutdown.clicked.connect(self.parent.shutdown)
        self.s_encash = QtWidgets.QPushButton('Encash')
        self.s_exit = QtWidgets.QPushButton('Exit')
        self.s_exit.clicked.connect(self.cancel_pay)
        self.s_label = QtWidgets.QLabel()
        self.s_label.setStyleSheet('color: green')
        self.grid_bottom.addWidget(self.s_block, 0, 0, 1, 2, QtCore.Qt.AlignCenter)
        self.grid_bottom.addWidget(self.s_unblock, 1, 0, 1, 2, QtCore.Qt.AlignCenter)
        self.grid_bottom.addWidget(self.s_restart, 2, 0, 1, 2, QtCore.Qt.AlignCenter)
        self.grid_bottom.addWidget(self.s_shutdown, 3, 0, 1, 2, QtCore.Qt.AlignCenter)
        self.grid_bottom.addWidget(self.s_encash, 4, 0, 1, 2, QtCore.Qt.AlignCenter)
        self.grid_bottom.addWidget(self.s_exit, 5, 0, 1, 2, QtCore.Qt.AlignCenter)
        self.grid_bottom.addWidget(self.s_label, 6, 0, 1, 2, QtCore.Qt.AlignCenter)
        self.elems += [self.s_block, self.s_unblock, self.s_encash, self.s_restart, self.s_label, self.s_exit,
                       self.s_shutdown]

    def encash_auth_page(self):
        pass

    def block(self):
        self.parent.block()
        self.s_label.setText('Terminal was blocked')

    def unblock(self):
        self.parent.unblock()
        self.s_label.setText('Terminal was unblocked')

    def raise_incorrect_code(self):
        self.incorrect_code += 1
        if self.incorrect_code == 3:
            self.load_error_screen()
            self.ui.pushButton_settings.clicked.disconnect()
            self.parent.state = 0
            return
        self.sa_error.setText('Wrong attempt! Remaining attempts: {}'.format(3 - self.incorrect_code))

    def load_main_screen(self):
        self.flush_screen()
        if not self.parent.is_available:
            self.load_error_screen()
            return
        self.org_buttons = list()
        self.header_buttons = list()
        self.parent.refresh_org_db()
        for i, t in enumerate(self.parent.types):
            btn = DisplayButton(None, 120, 30, text=t[1])
            self.layout_top.insertWidget(i, btn)
            self.header_buttons.append(btn)
            btn.clicked.connect(self.change_main_screen_page(i))
        row = 0
        col = 0
        for org in self.get_current_page_organizations():
            btn = DisplayButton(org, 195, 130)
            self.org_buttons.append(btn)
            self.grid_bottom.addWidget(btn, row, col, 1, 1, QtCore.Qt.AlignTop)
            col += 1
            if col % 5 == 0:
                row += 1
                col = 0
        self.load_organization_info()

    def load_organization_info(self):
        self.make_active_header_buttons()
        for i, org in enumerate(self.get_current_page_organizations()):
            self.org_buttons[i].change_icon(org[4])
            self.org_buttons[i].org = org
            if self.org_buttons[i].connected:
                self.org_buttons[i].clicked.disconnect()
            self.org_buttons[i].clicked.connect(self.display_pay_page(self.org_buttons[i].org))
            self.org_buttons[i].connected = True

    def display_pay_page(self, org):
        def closure():
            self.flush_screen()
            back_btn = QtWidgets.QPushButton('<< To main page')
            back_btn.clicked.connect(self.cancel_pay)
            self.layout_top.insertWidget(0, back_btn)
            top_label = QtWidgets.QLabel('Payment to {}.'.format(org[1]))
            logo_label = QtWidgets.QLabel()
            logo_label.setFixedSize(195, 130)
            logo_label.setStyleSheet('border-image: url({}) 0 0 0 0 stretch stretch;'.format(org[4]))
            self.acc_label = QtWidgets.QLabel('Personal account: ')
            self.acc_value = QtWidgets.QLineEdit()
            self.acc_value.setValidator(QtGui.QDoubleValidator())
            self.amount_value = QtWidgets.QLabel(text="Amount: <font color='green'>0</font>₽.")
            self.push_process_pay = QtWidgets.QPushButton('OK')
            self.push_process_pay.clicked.connect(self.process_pay(org))
            self.push_cancel_pay = QtWidgets.QPushButton('Cancel')
            self.push_cancel_pay.clicked.connect(self.cancel_pay)
            self.pay_error_label = QtWidgets.QLabel()
            self.pay_error_label.setStyleSheet('color: red;')
            self.grid_bottom.addWidget(top_label, 0, 0, 1, 2, QtCore.Qt.AlignCenter)
            self.grid_bottom.addWidget(logo_label, 1, 0, 1, 2, QtCore.Qt.AlignCenter)
            self.grid_bottom.addWidget(self.acc_label, 2, 0, 1, 1, QtCore.Qt.AlignRight)
            self.grid_bottom.addWidget(self.acc_value, 2, 1, 1, 1, QtCore.Qt.AlignLeft)
            self.grid_bottom.addWidget(self.amount_value, 3, 0, 1, 2, QtCore.Qt.AlignCenter)
            self.grid_bottom.addWidget(self.push_process_pay, 4, 0, 1, 1, QtCore.Qt.AlignRight)
            self.grid_bottom.addWidget(self.push_cancel_pay, 4, 1, 1, 1, QtCore.Qt.AlignLeft)
            self.grid_bottom.addWidget(self.pay_error_label, 5, 0, 1, 2, QtCore.Qt.AlignCenter)
            self.elems += [top_label, logo_label, self.acc_label,self.acc_value, self.amount_value,
                           self.push_process_pay, self.push_cancel_pay, back_btn, self.pay_error_label]
            self.parent.activate_bill_acceptor()

        return closure

    def update_amount(self, amount):
        self.amount_value.setText("Amount: <font color='green'>{}</font>₽.".format(amount))

    def cancel_pay(self):
        self.load_main_screen()
        self.parent.deactivate_bill_acceptor()
        self.parent.check_printer.deactivate()
        if self.return_timer.connected:
            self.return_timer.connected = False
            self.return_timer.timeout.disconnect()

    def process_pay(self, org):
        def send_pay():
            self.pay_error_label.setText('')
            self.pay_error_label.setStyleSheet('color: red;')
            self.return_timer.connected = False
            try:
                account = int(self.acc_value.text())
            except ValueError:
                self.pay_error_label.setText('Please input correct account')
                return
            if not 0 < account < 256**8:
                self.pay_error_label.setText('Incorrect account')
                return
            amount = self.parent.bill_acceptor.amount
            if amount == 0:
                self.pay_error_label.setText('Amount must be positive')
                return
            try:
                self.parent.send_payment_transaction(org[0], account, amount)
                self.pay_error_label.setStyleSheet('color: green;')
                self.return_timer_seconds = 10
                self.pay_error_label.setText('Your payment is completed. Return to main page in {} sec.'.format(
                    self.return_timer_seconds
                ))
                self.return_timer.connected = True
                self.return_timer.timeout.connect(self.return_timer_callback)
                self.return_timer.start(1000)
                self.push_process_pay.setEnabled(False)
                self.push_cancel_pay.setEnabled(False)
                self.parent.deactivate_bill_acceptor()
                self.parent.activate_check_printer({'org': org, 'org_type': self.parent.types[self.current_page][1],
                                                    'amount': amount, 'account': account})
            except PaymentTransactionException:
                self.pay_error_label.setText('Sorry, payment server unavailable.')
        return send_pay

    def return_timer_callback(self):
        self.return_timer_seconds -= 1
        if self.return_timer_seconds < 0:
            self.return_timer.connected = False
            self.return_timer.timeout.disconnect()
            self.load_main_screen()
            self.parent.check_printer.deactivate()
        self.pay_error_label.setText('Your payment is completed. Return to main page in {} sec.'.format(
            self.return_timer_seconds
        ))

    def change_main_screen_page(self, page):
        def change_page():
            def single_change():
                self.current_page = page
                self.load_organization_info()
            single_change()
        return change_page

    def make_active_header_buttons(self):
        for btn in self.header_buttons:
            btn.setStyleSheet('color: black;')
        self.header_buttons[self.current_page].setStyleSheet('color: red;')

    def load_status_string(self):
        self.update_status_label()
        self.status_timer = QtCore.QTimer()
        self.status_timer.timeout.connect(self.update_status_label)
        self.status_timer.start(1000)

    def update_status_label(self):
        now = datetime.datetime.now()
        text = 'Payment system inc. All rights reserved.  {}'.format(now.strftime('%H:%M:%S %d.%m.%Y'))
        self.ui.label_status.setText(text)

    def get_current_page_organizations(self):
        result = list()
        for org in self.parent.organizations:
            if org[3] == self.parent.types[self.current_page][0]:
                result.append(org)
        return result

    def load_error_screen(self):
        self.flush_screen()
        self.error_label = QtWidgets.QLabel('Sorry, current terminal is under maintenance.')
        self.error_label.setStyleSheet("font-weight: bold; color: red; border-image: none; font-size: 36px;")
        self.ui.label_status.hide()
        self.grid_bottom.addWidget(self.error_label, 0, 0, 1, 2, QtCore.Qt.AlignCenter)
        self.elems.append(self.error_label)


class DisplayButton(QtWidgets.QPushButton):
    def __init__(self, org, w, h, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = w
        self.height = h
        self.setFixedWidth(w)
        self.setFixedHeight(h)
        self.setStyleSheet('border-image: none; background-color: white;')
        self.org = org
        if org is not None:
            self.icon_path = org[4]
            self.change_icon(self.icon_path)
        self.connected = False

    def change_icon(self, icon_path):
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(self.icon)
        i_size = QtCore.QSize(self.width-5, self.height-5)
        self.setIconSize(i_size)

    def not_implemented(self):
        print(self.id)