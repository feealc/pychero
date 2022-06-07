from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from custom.BLabel import BLabel
from custom.BMainWindow import BMainWindow
from database.archero_db import ArcheroDb
from classes.egg_insert import EggInsert
import define as df


class WindowEggAdd(BMainWindow):
    window_closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.main_layout = QVBoxLayout()
        self.centralWidget.setLayout(self.main_layout)

        self.__db = ArcheroDb()

        self.__init_interface()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
        # event.ignore() # if you want the window to never be closed

    def __init_interface(self):
        # window
        self.setWindowTitle('Adicionar Egg')
        self.resize(400, 120)

        # name_en
        row_name_en = QHBoxLayout()
        self.lbl_name_en = BLabel(text='Nome EN:')
        self.txt_name_en = QLineEdit()
        row_name_en.addWidget(self.lbl_name_en)
        row_name_en.addWidget(self.txt_name_en)

        # type
        row_type = QHBoxLayout()
        self.rb_mob = QRadioButton('Mob')
        self.rb_mob.setChecked(True)
        self.rb_boss = QRadioButton('Boss')
        row_type.addWidget(self.rb_mob)
        row_type.addSpacing(20)
        row_type.addWidget(self.rb_boss)
        row_type.setAlignment(Qt.AlignCenter)

        # button
        row_bt = QHBoxLayout()
        self.bt_save = QPushButton(df.kBT_SAVE_TEXT)
        self.bt_save.clicked.connect(self.__action_save_egg)
        self.bt_save_and_close = QPushButton(df.kBT_SAVE_AND_CLOSE_TEXT)
        self.bt_save_and_close.clicked.connect(self.__action_save_egg_and_close)
        row_bt.addWidget(self.bt_save)
        row_bt.addWidget(self.bt_save_and_close)

        #

        self.main_layout.addLayout(row_name_en)
        self.main_layout.addLayout(row_type)
        self.main_layout.addLayout(row_bt)

    def __action_save_egg(self):
        self.__save_egg(close_window=False)

    def __action_save_egg_and_close(self):
        self.__save_egg(close_window=True)

    def __save_egg(self, close_window=True):
        name_en = self.txt_name_en.text()
        type_mob = self.rb_mob.isChecked()
        type_boss = self.rb_boss.isChecked()
        # print(f'name_en [{name_en}] type_mob [{type_mob}] type_boss [{type_boss}]')

        egg = EggInsert()
        egg.set_gen(name_en=name_en, type_mob=type_mob, type_boss=type_boss)
        # print(egg)

        self.__db.insert_egg(egg_insert=egg)
        QMessageBox.information(self, '', df.kMESSAGE_EGG_ADDED, QMessageBox.Ok)
        if close_window:
            self.close()
