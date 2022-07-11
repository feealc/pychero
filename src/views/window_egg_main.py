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


class WindowEggMain(BMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__db = ArcheroDb()
        self.eggs_list = []
        self.eggs_list_filter = []
        self.shortcuts_list = []

        self.__init_interface()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def __init_interface(self):
        self.setWindowTitle(df.kMAIN_TITLE)
        self.resize(1200, 800)

        # shortcut
        self.__create_shortcuts()

        # buttons
        self.bt_add = QPushButton(df.kBT_ADD_TEXT)
        self.bt_add.setToolTip('teste tooltip')
        self.bt_add.clicked.connect(self.__action_add_egg)
        self.main_layout.addWidget(self.bt_add)

        # labels
        self.lbl_layout = QHBoxLayout()
        self.lbl_total_eggs = BLabel(font_size=14, align_center=True)
        self.lbl_total_eggs_mob = BLabel(font_size=14, align_center=True)
        self.lbl_total_eggs_boss = BLabel(font_size=14, align_center=True)
        self.lbl_layout.addWidget(self.lbl_total_eggs)
        self.lbl_layout.addWidget(self.lbl_total_eggs_mob)
        self.lbl_layout.addWidget(self.lbl_total_eggs_boss)
        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(self.lbl_layout)
        self.__update_label_title()

        # filter
        self.gb_filter = QGroupBox(df.kGB_FILTER_TEXT)
        self.gb_filter_layout = QVBoxLayout()
        #
        self.bt_clear_filter = QPushButton(df.kBT_CLEAN_TEXT)
        self.bt_clear_filter.clicked.connect(self.__action_clear_filter)
        self.gb_filter_layout.addWidget(self.bt_clear_filter)
        #
        self.gb_filter_rb_layout = QHBoxLayout()
        self.rb_all = QRadioButton("Todos")
        self.rb_all.setChecked(True)
        self.rb_all.toggled.connect(self.__action_rb_all)
        self.rb_mob = QRadioButton("Mob")
        self.rb_mob.toggled.connect(self.__action_rb_mob)
        self.rb_boss = QRadioButton("Boss")
        self.rb_boss.toggled.connect(self.__action_rb_boss)
        self.gb_filter_rb_layout.setAlignment(Qt.AlignCenter)
        self.gb_filter_rb_layout.addWidget(self.rb_all)
        self.gb_filter_rb_layout.addSpacing(30)
        self.gb_filter_rb_layout.addWidget(self.rb_mob)
        self.gb_filter_rb_layout.addSpacing(30)
        self.gb_filter_rb_layout.addWidget(self.rb_boss)
        self.gb_filter_layout.addLayout(self.gb_filter_rb_layout)
        #
        self.gb_filter_name_en_layout = QHBoxLayout()
        self.lbl_name_en_filter = BLabel()
        self.lbl_name_en_filter.setText('Nome EN: ')
        self.txt_search_name_en_filter = QLineEdit()
        self.txt_search_name_en_filter.textChanged.connect(self.__action_txt_search_name_en_changed)
        self.gb_filter_name_en_layout.addWidget(self.lbl_name_en_filter)
        self.gb_filter_name_en_layout.addSpacing(10)
        self.gb_filter_name_en_layout.addWidget(self.txt_search_name_en_filter)
        self.gb_filter_layout.addLayout(self.gb_filter_name_en_layout)
        #
        self.gb_filter.setLayout(self.gb_filter_layout)
        self.main_layout.addWidget(self.gb_filter)

        # table
        self.table = BTableWidget()
        self.table.b_hide_vertical_headers()
        self.table.b_set_select_row()
        header_labels = ['Name', 'Type', 'Star']
        self.table.b_set_column_header(header_labels=header_labels)
        self.table.b_ajust_header_columns_headerview(header_view_list=[QHeaderView.Stretch,
                                                                       QHeaderView.ResizeToContents,
                                                                       QHeaderView.ResizeToContents])
        self.table.doubleClicked.connect(self.__action_edit_egg)
        self.main_layout.addWidget(self.table)

        self.__load_eggs()

    def __create_shortcuts(self):
        sc = QShortcut(QKeySequence('F1'), self)
        sc.activated.connect(self.__show_shortcuts)

        self.shortcuts_list = []

        sc = QShortcut(QKeySequence('Ctrl+N'), self)
        sc.setObjectName('Adicionar egg')
        sc.activated.connect(self.__action_add_egg)
        self.shortcuts_list.append(sc)

        sc = QShortcut(QKeySequence('Ctrl+F'), self)
        sc.setObjectName('Buscar nome egg')
        sc.activated.connect(self.__action_search)
        self.shortcuts_list.append(sc)

        sc = QShortcut(QKeySequence('Ctrl+Shift+F'), self)
        sc.setObjectName('Buscar nome egg e limpar pesquisa corrente')
        sc.activated.connect(self.__action_search_clear)
        self.shortcuts_list.append(sc)

        sc = QShortcut(QKeySequence('Ctrl+L'), self)
        sc.setObjectName('Limpar filtro')
        sc.activated.connect(self.__action_clear_filter)
        self.shortcuts_list.append(sc)

        sc = QShortcut(QKeySequence('A'), self)
        sc.setObjectName('Eggs - todos')
        sc.activated.connect(self.__shortcut_all)
        self.shortcuts_list.append(sc)

        sc = QShortcut(QKeySequence('M'), self)
        sc.setObjectName('Eggs - mobs')
        sc.activated.connect(self.__shortcut_mob)
        self.shortcuts_list.append(sc)

        sc = QShortcut(QKeySequence('B'), self)
        sc.setObjectName('Eggs - boss')
        sc.activated.connect(self.__shortcut_boss)
        self.shortcuts_list.append(sc)

    def __show_shortcuts(self):
        msg = ''
        for index, sc in enumerate(self.shortcuts_list):
            msg += f'{sc.key().toString()}' + '\n' + f'{sc.objectName()}' + '\n'
            if index < len(self.shortcuts_list) - 1:
                msg += '\n'
        QMessageBox.information(self, 'Atalhos', msg, QMessageBox.Ok)

    def __load_eggs(self):
        self.table.b_clear_content()

        lines = self.__db.select_all_eggs()
        self.eggs_list = []
        for line in lines:
            tvs = Egg(tuple_from_db=line)
            self.eggs_list.append(tvs)

        self.eggs_list_filter = []
        for egg in self.eggs_list:
            if self.rb_mob.isChecked():
                if egg.type_mob:
                    self.eggs_list_filter.append(egg)
            elif self.rb_boss.isChecked():
                if egg.type_boss:
                    self.eggs_list_filter.append(egg)
            else:
                self.eggs_list_filter.append(egg)

        aux_list = self.eggs_list_filter
        self.eggs_list_filter = []
        name_en_txt = self.txt_search_name_en_filter.text()
        if name_en_txt != '':
            for index, egg in enumerate(aux_list):
                if egg.name_en.lower().find(name_en_txt.lower()) != -1:
                    self.eggs_list_filter.append(egg)
        else:
            self.eggs_list_filter = aux_list

        for egg in self.eggs_list_filter:
            self.table.b_add_row(from_tuple=egg.to_tuple_table())
            # egg.dump()

        self.__update_label_title()

    def __update_label_title(self):
        total_eggs = len(self.eggs_list)
        total_eggs_mob = 0
        total_eggs_boss = 0

        for egg in self.eggs_list:
            if egg.type_mob:
                total_eggs_mob += 1
            elif egg.type_boss:
                total_eggs_boss += 1

        self.lbl_total_eggs.setText(f'Total: {total_eggs}')
        self.lbl_total_eggs_mob.setText(f'Mob: {total_eggs_mob}')
        self.lbl_total_eggs_boss.setText(f'Boss: {total_eggs_boss}')

    def __close_event(self):
        self.__load_eggs()

    def __action_clear_filter(self):
        self.rb_all.setChecked(True)
        self.txt_search_name_en_filter.setText('')
        self.__load_eggs()

    def __action_add_egg(self):
        self.add_egg_win = WindowEggAdd()
        self.add_egg_win.window_closed.connect(self.__close_event)
        self.add_egg_win.show()
        self.add_egg_win.b_center_window()

    def __action_rb_all(self):
        self.__load_eggs()

    def __action_rb_mob(self):
        self.__load_eggs()

    def __action_rb_boss(self):
        self.__load_eggs()

    def __action_edit_egg(self, mi):
        index = mi.row()
        if index >= 0:
            egg = self.eggs_list_filter[index]
            # print(egg)
            self.edit_egg_win = WindowEggEdit(egg=egg)
            self.edit_egg_win.window_closed.connect(self.__close_event)
            self.edit_egg_win.show()
            self.edit_egg_win.b_center_window()

    def __action_txt_search_name_en_changed(self):
        self.__load_eggs()

    def __action_search(self):
        self.txt_search_name_en_filter.setFocus()

    def __action_search_clear(self):
        self.txt_search_name_en_filter.setText('')
        self.txt_search_name_en_filter.setFocus()

    def __shortcut_all(self):
        self.rb_all.setChecked(True)
        self.__action_rb_all()

    def __shortcut_mob(self):
        self.rb_mob.setChecked(True)
        self.__action_rb_mob()

    def __shortcut_boss(self):
        self.rb_boss.setChecked(True)
        self.__action_rb_boss()
