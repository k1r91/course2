from terminal_template import Ui_TerminalMainWindow
from PyQt5 import QtWidgets, QtCore, QtGui


class Display:

    def __init__(self, parent):
        self.parent = parent
        self.ui = parent.ui
        self.grid_top = self.ui.grid_top
        self.grid_bottom = self.ui.grid_bottom
        self.config_error_page()
        self.current_page = 0
        # print(self.current_list)

    def load_main_screen(self):
        self.parent.refresh_org_db()
        for i, page in enumerate(self.parent.types):
            btn = DisplayButton('', 100, 30, text=page[1])
            self.grid_top.addWidget(btn, 0, i, 1, 1, QtCore.Qt.AlignLeft)
        for i in range(5):
            btn = DisplayButton('', 200, 130, text='Test')
            self.grid_bottom.addWidget(btn, 0, i, 1, 1)
        for i in range(5):
            btn = DisplayButton('', 200, 130, text='Test')
            self.grid_bottom.addWidget(btn, 1, i, 1, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

    def config_error_page(self):
        self.error_label = QtWidgets.QLabel('Sorry, current terminal is under maintenance.')
        self.error_label.setStyleSheet("font-weight: bold; color: red; border-image: none; font-size: 36px;")

    def load_error_screen(self):
        self.grid.addWidget(self.error_label, 0, 0, 1, 1, QtCore.Qt.AlignCenter)


class DisplayButton(QtWidgets.QPushButton):
    def __init__(self, icon_path, w, h, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedWidth(w)
        self.setFixedHeight(h)
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(self.icon)
        self.setStyleSheet('border-image: none;')