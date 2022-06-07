from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from custom.BTableWidget import BTableWidget
from custom.BLabel import BLabel
from custom.BMainWindow import BMainWindow
from database.archero_db import ArcheroDb
from classes.egg import Egg
from views.window_egg_add import WindowEggAdd
from views.window_egg_edit import WindowEggEdit
import define as df


class MainWindow(BMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.main_layout = QVBoxLayout()
        self.centralWidget.setLayout(self.main_layout)

        self.__db = ArcheroDb()
        self.tab_eggs_eggs_list = []
        self.tab_eggs_eggs_list_filter = []

        self.__init_interface()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def __init_interface(self):
        self.setWindowTitle(df.kMAIN_TITLE)
        self.resize(1200, 800)

        # tabs
        self.tabbar = QTabWidget()
        self.__create_tabbar()

        #

        self.main_layout.addWidget(self.tabbar)

    def __create_tabbar(self):
        self.__create_tab_eggs()
        self.tabbar.addTab(self.tab_eggs, df.kTAB_EGGS_NAME)
        # self.tabbar.setCurrentIndex(1)

    def __create_tab_eggs(self):
        self.tab_eggs = QWidget()
        self.tab_eggs_layout = QVBoxLayout()
        self.tab_eggs_layout.setAlignment(Qt.AlignTop)

        # shortcut
        self.__tab_eggs_create_shortcuts()

        # buttons
        self.tab_eggs_bt_add = QPushButton(df.kBT_ADD_TEXT)
        self.tab_eggs_bt_add.clicked.connect(self.__tab_eggs_action_add_egg)

        # labels
        self.tab_eggs_lbl_layout = QHBoxLayout()
        self.tab_eggs_lbl_total_eggs = BLabel(font_size=14, align_center=True)
        self.tab_eggs_lbl_total_eggs_mob = BLabel(font_size=14, align_center=True)
        self.tab_eggs_lbl_total_eggs_boss = BLabel(font_size=14, align_center=True)
        self.tab_eggs_lbl_layout.addWidget(self.tab_eggs_lbl_total_eggs)
        self.tab_eggs_lbl_layout.addWidget(self.tab_eggs_lbl_total_eggs_mob)
        self.tab_eggs_lbl_layout.addWidget(self.tab_eggs_lbl_total_eggs_boss)

        # filter
        self.tab_eggs_gb_filter = QGroupBox(df.kGB_FILTER_TEXT)
        self.tab_eggs_gb_filter_layout = QVBoxLayout()
        #
        self.tab_eggs_bt_clear_filter = QPushButton(df.kBT_CLEAN_TEXT)
        self.tab_eggs_bt_clear_filter.clicked.connect(self.__tab_eggs_action_clear_filter)
        self.tab_eggs_gb_filter_layout.addWidget(self.tab_eggs_bt_clear_filter)
        #
        self.tab_eggs_gb_filter_rb_layout = QHBoxLayout()
        self.tab_eggs_rb_all = QRadioButton("Todos")
        self.tab_eggs_rb_all.setChecked(True)
        self.tab_eggs_rb_all.toggled.connect(self.__tab_eggs_action_rb_all)
        self.tab_eggs_rb_mob = QRadioButton("Mob")
        self.tab_eggs_rb_mob.toggled.connect(self.__tab_eggs_action_rb_mob)
        self.tab_eggs_rb_boss = QRadioButton("Boss")
        self.tab_eggs_rb_boss.toggled.connect(self.__tab_eggs_action_rb_boss)
        self.tab_eggs_gb_filter_rb_layout.setAlignment(Qt.AlignCenter)
        self.tab_eggs_gb_filter_rb_layout.addWidget(self.tab_eggs_rb_all)
        self.tab_eggs_gb_filter_rb_layout.addSpacing(30)
        self.tab_eggs_gb_filter_rb_layout.addWidget(self.tab_eggs_rb_mob)
        self.tab_eggs_gb_filter_rb_layout.addSpacing(30)
        self.tab_eggs_gb_filter_rb_layout.addWidget(self.tab_eggs_rb_boss)
        self.tab_eggs_gb_filter_layout.addLayout(self.tab_eggs_gb_filter_rb_layout)
        #
        self.tab_eggs_gb_filter_name_en_layout = QHBoxLayout()
        self.tab_eggs_lbl_name_en_filter = BLabel()
        self.tab_eggs_lbl_name_en_filter.setText('Nome EN: ')
        self.tab_eggs_txt_search_name_en_filter = QLineEdit()
        self.tab_eggs_txt_search_name_en_filter.textChanged.connect(self.__tab_eggs_action_txt_search_name_en_changed)
        self.tab_eggs_gb_filter_name_en_layout.addWidget(self.tab_eggs_lbl_name_en_filter)
        self.tab_eggs_gb_filter_name_en_layout.addSpacing(10)
        self.tab_eggs_gb_filter_name_en_layout.addWidget(self.tab_eggs_txt_search_name_en_filter)
        self.tab_eggs_gb_filter_layout.addLayout(self.tab_eggs_gb_filter_name_en_layout)
        #
        self.tab_eggs_gb_filter.setLayout(self.tab_eggs_gb_filter_layout)

        # table
        self.tab_eggs_table = BTableWidget()
        self.tab_eggs_table.b_hide_vertical_headers()
        self.tab_eggs_table.b_set_select_row()
        header_labels = ['Name', 'Type', 'Star']
        self.tab_eggs_table.b_set_column_header(header_labels=header_labels)
        self.tab_eggs_table.b_ajust_header_columns_headerview(header_view_list=[QHeaderView.Stretch,
                                                                                QHeaderView.ResizeToContents,
                                                                                QHeaderView.ResizeToContents])
        self.tab_eggs_table.doubleClicked.connect(self.__tab_eggs_action_edit_egg)

        # all
        self.tab_eggs_layout.addWidget(self.tab_eggs_bt_add)
        self.tab_eggs_layout.addSpacing(10)
        self.tab_eggs_layout.addLayout(self.tab_eggs_lbl_layout)
        self.tab_eggs_layout.addWidget(self.tab_eggs_gb_filter)
        self.tab_eggs_layout.addSpacing(10)
        self.tab_eggs_layout.addWidget(self.tab_eggs_table)
        self.tab_eggs.setLayout(self.tab_eggs_layout)

        self.__tab_eggs_load_eggs()

    def __tab_eggs_create_shortcuts(self):
        sc = QShortcut(QKeySequence('Ctrl+N'), self)
        sc.activated.connect(self.__tab_eggs_action_add_egg)

        sc = QShortcut(QKeySequence('Ctrl+F'), self)
        sc.activated.connect(self.__tab_eggs_search)

        sc = QShortcut(QKeySequence('Ctrl+Shift+F'), self)
        sc.activated.connect(self.__tab_eggs_search_clear)

        sc = QShortcut(QKeySequence('Ctrl+L'), self)
        sc.activated.connect(self.__tab_eggs_action_clear_filter)

        sc = QShortcut(QKeySequence('A'), self)
        sc.activated.connect(self._tab_eggs_shorcut_all)
        sc = QShortcut(QKeySequence('M'), self)
        sc.activated.connect(self._tab_eggs_shorcut_mob)
        sc = QShortcut(QKeySequence('B'), self)
        sc.activated.connect(self._tab_eggs_shorcut_boss)

    def __tab_eggs_load_eggs(self):
        # print('__tab_eggs_load_eggs()')
        self.tab_eggs_table.b_clear_content()

        lines = self.__db.select_all_eggs()
        self.tab_eggs_eggs_list = []
        for line in lines:
            tvs = Egg(tuple_from_db=line)
            self.tab_eggs_eggs_list.append(tvs)

        self.tab_eggs_eggs_list_filter = []
        for egg in self.tab_eggs_eggs_list:
            if self.tab_eggs_rb_mob.isChecked():
                if egg.type_mob:
                    self.tab_eggs_eggs_list_filter.append(egg)
            elif self.tab_eggs_rb_boss.isChecked():
                if egg.type_boss:
                    self.tab_eggs_eggs_list_filter.append(egg)
            else:
                self.tab_eggs_eggs_list_filter.append(egg)

        aux_list = self.tab_eggs_eggs_list_filter
        self.tab_eggs_eggs_list_filter = []
        name_en_txt = self.tab_eggs_txt_search_name_en_filter.text()
        if name_en_txt != '':
            for index, egg in enumerate(aux_list):
                if egg.name_en.lower().find(name_en_txt.lower()) != -1:
                    self.tab_eggs_eggs_list_filter.append(egg)
        else:
            self.tab_eggs_eggs_list_filter = aux_list

        for egg in self.tab_eggs_eggs_list_filter:
            self.tab_eggs_table.b_add_row(from_tuple=egg.to_tuple_table())
            # egg.dump()

        self.__tab_eggs_update_label_title()

    def __tab_eggs_update_label_title(self):
        total_eggs = len(self.tab_eggs_eggs_list)
        total_eggs_mob = 0
        total_eggs_boss = 0

        for egg in self.tab_eggs_eggs_list:
            if egg.type_mob:
                total_eggs_mob += 1
            elif egg.type_boss:
                total_eggs_boss += 1

        self.tab_eggs_lbl_total_eggs.setText(f'Total: {total_eggs}')
        self.tab_eggs_lbl_total_eggs_mob.setText(f'Mob: {total_eggs_mob}')
        self.tab_eggs_lbl_total_eggs_boss.setText(f'Boss: {total_eggs_boss}')

    def __tab_eggs_close_event(self):
        self.__tab_eggs_load_eggs()

    def __tab_eggs_action_clear_filter(self):
        self.tab_eggs_rb_all.setChecked(True)
        self.tab_eggs_txt_search_name_en_filter.setText('')
        self.__tab_eggs_load_eggs()

    def __tab_eggs_action_add_egg(self):
        self.add_egg_win = WindowEggAdd()
        self.add_egg_win.window_closed.connect(self.__tab_eggs_close_event)
        self.add_egg_win.show()
        self.add_egg_win.b_center_window()

    def __tab_eggs_action_rb_all(self):
        self.__tab_eggs_load_eggs()

    def __tab_eggs_action_rb_mob(self):
        self.__tab_eggs_load_eggs()

    def __tab_eggs_action_rb_boss(self):
        self.__tab_eggs_load_eggs()

    def __tab_eggs_action_edit_egg(self, mi):
        index = mi.row()
        if index >= 0:
            egg = self.tab_eggs_eggs_list_filter[index]
            # print(egg)
            self.edit_egg_win = WindowEggEdit(egg=egg)
            self.edit_egg_win.window_closed.connect(self.__tab_eggs_close_event)
            self.edit_egg_win.show()
            self.edit_egg_win.b_center_window()

    def __tab_eggs_action_txt_search_name_en_changed(self):
        self.__tab_eggs_load_eggs()

    def __tab_eggs_search(self):
        self.tab_eggs_txt_search_name_en_filter.setFocus()

    def __tab_eggs_search_clear(self):
        self.tab_eggs_txt_search_name_en_filter.setText('')
        self.tab_eggs_txt_search_name_en_filter.setFocus()

    def _tab_eggs_shorcut_all(self):
        self.tab_eggs_rb_all.setChecked(True)
        self.__tab_eggs_action_rb_all()

    def _tab_eggs_shorcut_mob(self):
        self.tab_eggs_rb_mob.setChecked(True)
        self.__tab_eggs_action_rb_mob()

    def _tab_eggs_shorcut_boss(self):
        self.tab_eggs_rb_boss.setChecked(True)
        self.__tab_eggs_action_rb_boss()
