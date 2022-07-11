from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from custom.BTableWidget import BTableWidget
from custom.BLabel import BLabel
from custom.BMainWindow import BMainWindow
from database.archero_db import ArcheroDb
from classes.egg import Egg
from views.window_egg_main import WindowEggMain
from views.window_egg_add import WindowEggAdd
from views.window_egg_edit import WindowEggEdit
import define as df


class MainWindow(BMainWindow):
    def __init__(self, parent=None, parser=None, args=None):
        super().__init__(parent)
        self.parser = parser
        self.args = args

        self.__init_interface()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def __init_interface(self):
        self.setWindowTitle('Pychero')
        self.resize(400, 400)

        # eggs
        self.bt_eggs = QPushButton('Eggs')
        self.bt_eggs.clicked.connect(self.__action_bt_eggs)

        self.main_layout.addWidget(self.bt_eggs)

    def __close_window_event(self, event: QCloseEvent):
        event.accept()
        self.show()

    #

    def __action_bt_eggs(self):
        self.win_eggs = WindowEggMain()
        self.win_eggs.closeEvent = lambda event: self.__close_window_event(event=event)
        self.hide()
        if self.args.maximized:
            self.win_eggs.showMaximized()
        else:
            self.win_eggs.show()
