import datetime
import traceback
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from custom.BLabel import BLabel
from custom.BTableWidget import BTableWidget
from custom.BListWidget import BListWidget
from custom.BMainWindow import BMainWindow
from database.archero_db import ArcheroDb
from classes.handle_json import HandleJson
from classes.exceptions import *
from classes.egg import ChapterData
from classes.egg import TrainStatData
from classes.egg import TrainStatStarsData
from classes.egg import CompetitionData
import define as df


class WindowEggEdit(BMainWindow):
    window_closed = pyqtSignal()

    def __init__(self, egg, parent=None):
        super().__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.centralWidget.setLayout(self.main_layout)

        """
        - quando fizer alguma mudanca, setar como True
        - se fechar a tela e estiver True, mostrar mensagem perguntando se quer descartar as alteracoes
        """
        self.__flag_changed = False
        self.egg = egg
        self.__db = ArcheroDb()
        self.__json = HandleJson(file_name='project.json')
        # self.__json.dump_json()

        self.__flag_chapter_event_update = False

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
        self.setWindowTitle(f'Egg - {self.egg.name_en} (Id {self.egg.id})')
        # self.resize(1000, 800)

        # =========================================================================================
        # name
        gb_name = QGroupBox('Nome')
        gb_name_layout = QHBoxLayout()
        self.lbl_name_en = BLabel(text='EN:')
        self.txt_name_en = QLineEdit()
        self.txt_name_en.setText(self.egg.name_en)
        self.lbl_name_pt = BLabel(text='PT:')
        self.txt_name_pt = QLineEdit()
        self.txt_name_pt.setText(self.egg.name_pt)
        gb_name_layout.addWidget(self.lbl_name_en)
        gb_name_layout.addWidget(self.txt_name_en)
        gb_name_layout.addSpacing(20)
        gb_name_layout.addWidget(self.lbl_name_pt)
        gb_name_layout.addWidget(self.txt_name_pt)
        gb_name.setLayout(gb_name_layout)
        self.main_layout.addWidget(gb_name)

        # =========================================================================================
        row_type_collected_stars = QHBoxLayout()
        # type
        gb_type = QGroupBox('Tipo')
        gb_type_layout = QHBoxLayout()
        self.rb_mob = QRadioButton('Mob')
        self.rb_mob.setChecked(self.egg.type_mob)
        self.rb_boss = QRadioButton('Boss')
        self.rb_boss.setChecked(self.egg.type_boss)
        gb_type_layout.addWidget(self.rb_mob)
        gb_type_layout.addSpacing(20)
        gb_type_layout.addWidget(self.rb_boss)
        gb_type_layout.setAlignment(Qt.AlignCenter)
        gb_type.setLayout(gb_type_layout)
        row_type_collected_stars.addWidget(gb_type)
        # collected
        gb_collected = QGroupBox('Pego')
        gb_collected_layout = QHBoxLayout()
        self.cb_collected = QCheckBox('Pego')
        self.cb_collected.setChecked(self.egg.collected)
        gb_collected_layout.addWidget(self.cb_collected)
        gb_collected_layout.setAlignment(Qt.AlignCenter)
        gb_collected.setLayout(gb_collected_layout)
        row_type_collected_stars.addWidget(gb_collected)
        # stars
        gb_stars = QGroupBox('Estrelas')
        gb_stars_layout = QHBoxLayout()
        self.spin_stars = QSpinBox()
        self.spin_stars.setMinimumWidth(100)
        self.spin_stars.setMinimum(self.__json.get_stars_min())
        self.spin_stars.setMaximum(self.__json.get_stars_max())
        self.spin_stars.setValue(self.egg.stars)
        gb_stars_layout.addWidget(self.spin_stars)
        gb_stars_layout.setAlignment(Qt.AlignCenter)
        gb_stars.setLayout(gb_stars_layout)
        row_type_collected_stars.addWidget(gb_stars)
        #
        self.main_layout.addLayout(row_type_collected_stars)

        # =========================================================================================
        # find
        row_find = QHBoxLayout()
        # normal chapter
        self.gb_normal_ch = QGroupBox(df.kNORMAL_CHAPTER)
        self.cb_rec_normal_ch = QCheckBox(df.kRECOMMENDED)
        self.table_normal_ch = BTableWidget()
        self.table_normal_ch.doubleClicked.connect(self.__action_edit_chapter_normal)
        self.cbox_normal_ch = QComboBox()
        self.cb_rec_add_normal_ch = QCheckBox(df.kRECOMMENDED)
        self.bt_add_normal_ch = QPushButton(df.kBT_ADD_TEXT)
        self.bt_delete_normal_ch = QPushButton(df.kBT_DELETE_TEXT)
        self.bt_cancel_normal_ch = QPushButton(df.kBT_CANCEL_TEXT)
        self.__build_find_chapter(gb=self.gb_normal_ch,
                                  cb_filter_rec=self.cb_rec_normal_ch,
                                  table=self.table_normal_ch,
                                  cbox=self.cbox_normal_ch,
                                  cb_add_rec=self.cb_rec_add_normal_ch,
                                  bt_add=self.bt_add_normal_ch,
                                  bt_delete=self.bt_delete_normal_ch,
                                  bt_cancel=self.bt_cancel_normal_ch)
        # hero chapter
        self.gb_hero_ch = QGroupBox(df.kHERO_CHAPTER)
        self.cb_rec_hero_ch = QCheckBox(df.kRECOMMENDED)
        self.table_hero_ch = BTableWidget()
        self.table_hero_ch.doubleClicked.connect(self.__action_edit_chapter_hero)
        self.cbox_hero_ch = QComboBox()
        self.cb_rec_add_hero_ch = QCheckBox(df.kRECOMMENDED)
        self.bt_add_hero_ch = QPushButton(df.kBT_ADD_TEXT)
        self.bt_delete_hero_ch = QPushButton(df.kBT_DELETE_TEXT)
        self.bt_cancel_hero_ch = QPushButton(df.kBT_CANCEL_TEXT)
        self.__build_find_chapter(gb=self.gb_hero_ch,
                                  cb_filter_rec=self.cb_rec_hero_ch,
                                  table=self.table_hero_ch,
                                  cbox=self.cbox_hero_ch,
                                  cb_add_rec=self.cb_rec_add_hero_ch,
                                  bt_add=self.bt_add_hero_ch,
                                  bt_delete=self.bt_delete_hero_ch,
                                  bt_cancel=self.bt_cancel_hero_ch)
        # event
        self.gb_event_ch = QGroupBox(df.kEVENT)
        self.cb_rec_event_ch = QCheckBox(df.kRECOMMENDED)
        self.table_event_ch = BTableWidget()
        self.table_event_ch.doubleClicked.connect(self.__action_edit_event)
        self.cbox_event_ch = QComboBox()
        self.cb_rec_add_event_ch = QCheckBox(df.kRECOMMENDED)
        self.bt_add_event_ch = QPushButton(df.kBT_ADD_TEXT)
        self.bt_delete_event_ch = QPushButton(df.kBT_DELETE_TEXT)
        self.bt_cancel_event_ch = QPushButton(df.kBT_CANCEL_TEXT)
        self.__build_find_chapter(gb=self.gb_event_ch,
                                  cb_filter_rec=self.cb_rec_event_ch,
                                  table=self.table_event_ch,
                                  cbox=self.cbox_event_ch,
                                  cb_add_rec=self.cb_rec_add_event_ch,
                                  bt_add=self.bt_add_event_ch,
                                  bt_delete=self.bt_delete_event_ch,
                                  bt_cancel=self.bt_cancel_event_ch)
        row_find.addWidget(self.gb_normal_ch)
        row_find.addWidget(self.gb_hero_ch)
        row_find.addWidget(self.gb_event_ch)
        self.main_layout.addLayout(row_find)

        # =========================================================================================
        row_hatch = QHBoxLayout()
        # to hatch
        gb_to_hatch = QGroupBox('To Hatch')
        gb_to_hatch_layout = QHBoxLayout()
        self.txt_to_hatch = QLineEdit()
        self.txt_to_hatch.setText(self.egg.to_hatch_str)
        gb_to_hatch_layout.addWidget(self.txt_to_hatch)
        gb_to_hatch_layout.setAlignment(Qt.AlignCenter)
        gb_to_hatch.setLayout(gb_to_hatch_layout)
        row_hatch.addWidget(gb_to_hatch)
        # natural hatch
        gb_natural_hatch = QGroupBox('Natural Hatch (min)')
        gb_natural_hatch_layout = QHBoxLayout()
        self.txt_natural_hatch = QLineEdit()
        self.txt_natural_hatch.setText(self.egg.natural_hatch_str)
        gb_natural_hatch_layout.addWidget(self.txt_natural_hatch)
        gb_natural_hatch_layout.setAlignment(Qt.AlignCenter)
        gb_natural_hatch.setLayout(gb_natural_hatch_layout)
        row_hatch.addWidget(gb_natural_hatch)
        # quest 1
        gb_quest1 = QGroupBox('Quest 1')
        gb_quest1_layout = QHBoxLayout()
        self.txt_quest1 = QLineEdit()
        self.txt_quest1.setText(self.egg.quest1_str)
        gb_quest1_layout.addWidget(self.txt_quest1)
        self.cb_quest1 = QCheckBox('Unlocked')
        self.cb_quest1.setChecked(self.egg.quest1_unlocked)
        gb_quest1_layout.addWidget(self.cb_quest1)
        gb_quest1.setLayout(gb_quest1_layout)
        row_hatch.addWidget(gb_quest1)
        # quest 2
        gb_quest2 = QGroupBox('Quest 2')
        gb_quest2_layout = QHBoxLayout()
        self.txt_quest2 = QLineEdit()
        self.txt_quest2.setText(self.egg.quest2_str)
        gb_quest2_layout.addWidget(self.txt_quest2)
        self.cb_quest2 = QCheckBox('Unlocked')
        self.cb_quest2.setChecked(self.egg.quest2_unlocked)
        gb_quest2_layout.addWidget(self.cb_quest2)
        gb_quest2.setLayout(gb_quest2_layout)
        row_hatch.addWidget(gb_quest2)
        #
        self.main_layout.addLayout(row_hatch)

        # =========================================================================================
        row_train = QHBoxLayout()
        # train cost
        gb_train_cost = QGroupBox('Train Cost')
        gb_train_cost_layout = QVBoxLayout()
        self.list_train_cost = BListWidget()
        self.__load_train_cost()
        row_txt_bt_train_cost = QHBoxLayout()
        self.txt_train_cost = QLineEdit()
        row_txt_bt_train_cost.addWidget(self.txt_train_cost)
        self.bt_train_cost = QPushButton('Adicionar')
        self.bt_train_cost.clicked.connect(self.__action_add_train_cost)
        row_txt_bt_train_cost.addWidget(self.bt_train_cost)
        gb_train_cost_layout.addWidget(self.list_train_cost)
        gb_train_cost_layout.addLayout(row_txt_bt_train_cost)
        gb_train_cost_layout.setAlignment(Qt.AlignCenter)
        gb_train_cost.setLayout(gb_train_cost_layout)
        row_train.addWidget(gb_train_cost)
        # train stats
        gb_train_stats = QGroupBox('Train Stats')
        gb_train_stats_layout = QVBoxLayout()
        self.table_train_stats = BTableWidget()
        self.table_train_stats.b_hide_vertical_headers()
        self.table_train_stats.b_set_column_header(header_labels=['Stat', 'Valor'])
        self.table_train_stats.b_ajust_header_columns_headerview(header_view_list=[QHeaderView.Stretch,
                                                                                   QHeaderView.ResizeToContents])
        self.__load_train_stats()
        gb_train_stats_layout.addWidget(self.table_train_stats)
        row_train_stats_add = QHBoxLayout()
        self.cbox_train_stats = QComboBox()
        self.cbox_train_stats.addItems(self.__json.get_train_stats())
        row_train_stats_add.addWidget(self.cbox_train_stats)
        self.txt_train_stats = QLineEdit()
        row_train_stats_add.addWidget(self.txt_train_stats)
        self.cb_train_stats = QCheckBox('5s')
        row_train_stats_add.addWidget(self.cb_train_stats)
        self.bt_add_train_stats = QPushButton('Adicionar')
        self.bt_add_train_stats.clicked.connect(self.__action_add_train_stats)
        row_train_stats_add.addWidget(self.bt_add_train_stats)
        gb_train_stats_layout.addLayout(row_train_stats_add)
        gb_train_stats.setLayout(gb_train_stats_layout)
        row_train.addWidget(gb_train_stats)
        # train stats stars
        gb_train_stats_stars = QGroupBox('Train Stats Stars')
        """
        COLOCAR A QUANTIDADE DE ESTRELA NECESSARIA PRA LIBERAR A STAT
        QUANDO NAO TIVER ISSO (QUE EH A MAIORIA), COLOCAR 0 (ZERO) 
        """
        gb_train_stats_stars_layout = QVBoxLayout()
        self.table_train_stats_stars = BTableWidget()
        self.table_train_stats_stars.b_hide_vertical_headers()
        self.table_train_stats_stars.b_set_column_header(header_labels=['Star', 'Stat', 'Valor', 'xxx'])
        self.table_train_stats_stars.b_ajust_header_columns_headerview(header_view_list=[QHeaderView.ResizeToContents,
                                                                                         QHeaderView.Stretch,
                                                                                         QHeaderView.ResizeToContents,
                                                                                         QHeaderView.ResizeToContents])
        self.table_train_stats_stars.setMinimumWidth(400)
        self.__load_train_stats_stars()
        gb_train_stats_stars_layout.addWidget(self.table_train_stats_stars)

        row_train_stats_stars_add = QHBoxLayout()
        self.spin_stars_add_train_stats_stars = QSpinBox()
        self.spin_stars_add_train_stats_stars.setMinimum(self.__json.get_stars_min())
        self.spin_stars_add_train_stats_stars.setMaximum(self.__json.get_stars_max())
        row_train_stats_stars_add.addWidget(self.spin_stars_add_train_stats_stars)
        self.txt_train_stats_stars = QLineEdit()
        row_train_stats_stars_add.addWidget(self.txt_train_stats_stars)
        self.txt_train_stats_stars_value = QLineEdit()
        self.txt_train_stats_stars_value.setMaximumWidth(70)
        row_train_stats_stars_add.addWidget(self.txt_train_stats_stars_value)
        self.bt_add_train_stats_stars = QPushButton('Adicionar')
        self.bt_add_train_stats_stars.clicked.connect(self.__action_add_train_stats_stars)
        row_train_stats_stars_add.addWidget(self.bt_add_train_stats_stars)
        gb_train_stats_stars_layout.addLayout(row_train_stats_stars_add)
        gb_train_stats_stars.setLayout(gb_train_stats_stars_layout)
        row_train.addWidget(gb_train_stats_stars)
        # competition
        self.gb_competition = QGroupBox('Competição')
        self.gb_competition.setCheckable(True)
        self.gb_competition.setChecked(self.egg.competition_available)
        gb_competition_layout = QVBoxLayout()
        self.table_competition = BTableWidget()
        self.table_competition.setMinimumWidth(250)
        self.table_competition.b_hide_vertical_headers()
        self.table_competition.b_set_column_header(header_labels=['Stat', 'Valor'])
        self.table_competition.b_ajust_header_columns_headerview(header_view_list=[QHeaderView.Stretch,
                                                                                   QHeaderView.ResizeToContents])
        self.__load_competition()
        gb_competition_layout.addWidget(self.table_competition)
        row_competition_add = QHBoxLayout()
        self.cbox_competition_stat = QComboBox()
        self.cbox_competition_stat.addItems(self.__json.get_train_stats())
        row_competition_add.addWidget(self.cbox_competition_stat)
        self.txt_competition_stat_value = QLineEdit()
        row_competition_add.addWidget(self.txt_competition_stat_value)
        self.bt_competition_add = QPushButton('Adicionar')
        self.bt_competition_add.clicked.connect(self.__action_add_competition)
        row_competition_add.addWidget(self.bt_competition_add)
        gb_competition_layout.addLayout(row_competition_add)
        self.gb_competition.setLayout(gb_competition_layout)
        row_train.addWidget(self.gb_competition)
        #
        self.main_layout.addLayout(row_train)

        # =========================================================================================
        # dates
        gb_dates = QGroupBox()
        gb_dates_layout = QHBoxLayout()

        self.lbl_date_created = BLabel()
        self.lbl_date_updated = BLabel()

        self.__build_dates()

        gb_dates_layout.addWidget(self.lbl_date_created)
        gb_dates_layout.addWidget(self.lbl_date_updated)
        gb_dates.setLayout(gb_dates_layout)
        #
        self.main_layout.addWidget(gb_dates)

        # =========================================================================================
        # button
        row_bt = QHBoxLayout()
        self.bt_save = QPushButton('Salvar')
        self.bt_save.clicked.connect(self.__action_save_egg)
        row_bt.addWidget(self.bt_save)
        self.main_layout.addLayout(row_bt)

    def __build_find_chapter(self, gb, cb_filter_rec, table, cbox, cb_add_rec, bt_add, bt_delete, bt_cancel):
        gb_layout = QVBoxLayout()
        gb_layout.setAlignment(Qt.AlignCenter)

        # checkbox
        # gb_layout.addWidget(cb_filter_rec)

        # table
        table.b_hide_vertical_headers()
        table.b_set_select_row()
        table.b_set_column_header(header_labels=['Capítulo', 'Recomendado'])
        table.b_ajust_header_columns_headerview(header_view_list=[QHeaderView.Stretch, QHeaderView.ResizeToContents])
        table.setMaximumWidth(260)
        table.setMaximumHeight(200)
        self.__load_chapters(title=gb.title())
        gb_layout.addWidget(table)

        # row - cbox / checkbox
        if gb.title() == df.kEVENT:
            list_cbox = self.__json.get_events()
        else:
            ch_min = self.__json.get_chapter_min()
            ch_max = self.__json.get_chapter_max()
            list_cbox = list(range(ch_min, ch_max + 1))
        row_cbox_cb = QHBoxLayout()
        cbox.setMinimumWidth(150)
        cbox.addItems(map(str, list_cbox))
        row_cbox_cb.addWidget(cbox)
        row_cbox_cb.addWidget(cb_add_rec)
        gb_layout.addLayout(row_cbox_cb)

        gb_layout_row_bt = QHBoxLayout()

        # add
        bt_add.clicked.connect(lambda: self.__action_add_chapter_event(title=gb.title()))
        gb_layout_row_bt.addWidget(bt_add)

        # delete
        bt_delete.clicked.connect(lambda: self.__action_delete_chapter_event(title=gb.title()))
        gb_layout_row_bt.addWidget(bt_delete)

        # cancel
        bt_cancel.clicked.connect(lambda: self.__action_cancel_edit_chapter_event(title=gb.title()))
        bt_cancel.hide()
        gb_layout_row_bt.addWidget(bt_cancel)

        #

        gb_layout.addLayout(gb_layout_row_bt)
        gb.setLayout(gb_layout)

    def __build_dates(self):
        self.lbl_date_created.setText('Data criação: ' + self.egg.date_created_formatted)
        self.lbl_date_created.b_set_font_size(size=12)
        self.lbl_date_created.setAlignment(Qt.AlignCenter)

        self.lbl_date_updated.setText('Data atualização: ' + self.egg.date_updated_formatted)
        self.lbl_date_updated.b_set_font_size(size=12)
        self.lbl_date_updated.setAlignment(Qt.AlignCenter)

    def __load_chapters(self, title):
        rows = []
        table = None
        if title == df.kNORMAL_CHAPTER:
            rows = self.egg.find_normal_chapters.chapter_data
            table = self.table_normal_ch
        elif title == df.kHERO_CHAPTER:
            rows = self.egg.find_hero_chapters.chapter_data
            table = self.table_hero_ch
        elif title == df.kEVENT:
            rows = self.egg.find_events.chapter_data
            table = self.table_event_ch

        table.b_clear_content()
        for ch in rows:
            # print(ch)
            table.b_add_row(from_tuple=ch.to_tuple_table())

    def __load_train_cost(self):
        self.list_train_cost.b_clear_content()
        for tc in self.egg.train_cost.lst:
            self.list_train_cost.b_add_row(value=tc)

    def __load_train_stats(self):
        self.table_train_stats.b_clear_content()
        for ts in self.egg.train_stats.train_stats_data:
            self.table_train_stats.b_add_row(ts.to_tuple_table())

    def __load_train_stats_stars(self):
        self.table_train_stats_stars.b_clear_content()
        for ts in self.egg.train_stats_stars.train_stats_stars_data:
            self.table_train_stats_stars.b_add_row(ts.to_tuple_table())

    def __load_competition(self):
        self.table_competition.b_clear_content()
        for comp in self.egg.competition_stats.competition_data:
            self.table_competition.b_add_row(comp.to_tuple_table())

    def __action_add_chapter_event(self, title):
        # print(f'__action_add_chapter_event() - title [{title}]')
        chapter = None
        recommended = False
        cbox = None
        cb_rec = None
        bt_add = None
        bt_cancel = None
        if title == df.kNORMAL_CHAPTER:
            chapter = self.cbox_normal_ch.currentText()
            recommended = self.cb_rec_add_normal_ch.isChecked()
            cbox = self.cbox_normal_ch
            cb_rec = self.cb_rec_add_normal_ch
            bt_add = self.bt_add_normal_ch
            bt_cancel = self.bt_cancel_normal_ch
        elif title == df.kHERO_CHAPTER:
            chapter = self.cbox_hero_ch.currentText()
            recommended = self.cb_rec_add_hero_ch.isChecked()
            cbox = self.cbox_hero_ch
            cb_rec = self.cb_rec_add_hero_ch
            bt_add = self.bt_add_hero_ch
            bt_cancel = self.bt_cancel_hero_ch
        elif title == df.kEVENT:
            chapter = self.cbox_event_ch.currentText()
            recommended = self.cb_rec_add_event_ch.isChecked()
            cbox = self.cbox_event_ch
            cb_rec = self.cb_rec_add_event_ch
            bt_add = self.bt_add_event_ch
            bt_cancel = self.bt_cancel_event_ch

        # print(f'chapter [{chapter}] recommended [{recommended}]')
        ch_data = ChapterData(from_add=(chapter, recommended))
        if self.__flag_chapter_event_update:
            self.egg.update_chapter(title=title, ch_data=ch_data)
            self.__load_chapters(title=title)

            cbox.setCurrentIndex(0)
            cb_rec.setChecked(False)
            bt_add.setText(df.kBT_ADD_TEXT)
            bt_cancel.hide()
        else:
            if not self.egg.add_chapter(title=title, ch_data=ch_data):
                QMessageBox.information(self, title, 'Capítulo já existe.', QMessageBox.Ok)
            else:
                self.__load_chapters(title=title)

    def __action_delete_chapter_event(self, title):
        cbox = None
        if title == df.kNORMAL_CHAPTER:
            cbox = self.cbox_normal_ch
        elif title == df.kHERO_CHAPTER:
            cbox = self.cbox_hero_ch
        elif title == df.kEVENT:
            cbox = self.cbox_event_ch

        ch_event = ''
        if cbox is not None:
            ch_event = cbox.currentText()

        if title == df.kNORMAL_CHAPTER:
            self.egg.find_normal_chapters.delete(ch_event=ch_event)
        elif title == df.kHERO_CHAPTER:
            self.egg.find_hero_chapters.delete(ch_event=ch_event)
        elif title == df.kEVENT:
            self.egg.find_events.delete(ch_event=ch_event)

        self.__load_chapters(title=title)
        self.__action_cancel_edit_chapter_event(title=title)

    def __action_cancel_edit_chapter_event(self, title):
        table = None
        cbox = None
        cb_rec = None
        bt_add = None
        bt_delete = None
        bt_cancel = None
        if title == df.kNORMAL_CHAPTER:
            table = self.table_normal_ch
            cbox = self.cbox_normal_ch
            cb_rec = self.cb_rec_add_normal_ch
            bt_add = self.bt_add_normal_ch
            bt_delete = self.bt_delete_normal_ch
            bt_cancel = self.bt_cancel_normal_ch
        elif title == df.kHERO_CHAPTER:
            table = self.table_hero_ch
            cbox = self.cbox_hero_ch
            cb_rec = self.cb_rec_add_hero_ch
            bt_add = self.bt_add_hero_ch
            bt_delete = self.bt_delete_hero_ch
            bt_cancel = self.bt_cancel_hero_ch
        elif title == df.kEVENT:
            table = self.table_event_ch
            cbox = self.cbox_event_ch
            cb_rec = self.cb_rec_add_event_ch
            bt_add = self.bt_add_event_ch
            bt_delete = self.bt_delete_event_ch
            bt_cancel = self.bt_cancel_event_ch

        if table is not None:
            table.clearSelection()

        if cbox is not None:
            cbox.setCurrentIndex(0)

        if cb_rec is not None:
            cb_rec.setChecked(False)

        if bt_add is not None:
            bt_add.setText(df.kBT_ADD_TEXT)

        if bt_delete is not None:
            bt_delete.hide()

        if bt_cancel is not None:
            bt_cancel.hide()

    def __action_add_train_cost(self):
        cost_str = self.txt_train_cost.text()
        cost_int = 0
        try:
            cost_int = int(cost_str)
        except ValueError:
            QMessageBox.warning(self, 'Train Cost', 'Valor não é numérico.', QMessageBox.Ok)
            self.txt_train_cost.setFocus()

        self.egg.train_cost.add_cost(value=cost_int)
        self.__load_train_cost()

        self.txt_train_cost.setText('')
        self.txt_train_cost.setFocus()

    def __action_add_train_stats(self):
        if self.txt_train_stats.text() == '':
            QMessageBox.warning(self, ' ', 'Precisa preencher o valor da habilidade (stat).', QMessageBox.Ok)
            self.txt_train_stats.setFocus()
            return

        add_tuple = (self.cbox_train_stats.currentText(),
                     self.txt_train_stats.text(),
                     self.cb_train_stats.isChecked())
        ts = TrainStatData(from_add=add_tuple)
        self.egg.train_stats.add(data=ts)
        self.__load_train_stats()

        self.txt_train_stats.setText('')
        self.cbox_train_stats.setFocus()

    def __action_add_train_stats_stars(self):
        if self.txt_train_stats_stars.text() == '':
            QMessageBox.warning(self, ' ', 'Precisa preencher a habilidade (stat).', QMessageBox.Ok)
            self.txt_train_stats_stars.setFocus()
            return
        if self.txt_train_stats_stars_value.text() == '':
            QMessageBox.warning(self, ' ', 'Precisa preencher o valor da habilidade (stat).', QMessageBox.Ok)
            self.txt_train_stats_stars_value.setFocus()
            return

        add_tuple = (self.spin_stars_add_train_stats_stars.value(),
                     self.txt_train_stats_stars.text(),
                     self.txt_train_stats_stars_value.text())
        tss = TrainStatStarsData(egg_stars=self.egg.stars, from_add=add_tuple)
        self.egg.train_stats_stars.add(data=tss)
        self.__load_train_stats_stars()
        #
        self.txt_train_stats_stars.setText('')
        self.txt_train_stats_stars_value.setText('')
        self.txt_train_stats_stars.setFocus()

    def __action_add_competition(self):
        if self.txt_competition_stat_value.text() == '':
            QMessageBox.warning(self, ' ', 'Precisa preencher o valor da habilidade (stat).', QMessageBox.Ok)
            self.txt_competition_stat_value.setFocus()
            return

        add_tuple = (self.cbox_competition_stat.currentText(),
                     self.txt_competition_stat_value.text())
        comp = CompetitionData(from_add=add_tuple)
        self.egg.competition_stats.add(data=comp)
        self.__load_competition()

        self.cbox_competition_stat.setFocus()
        self.txt_competition_stat_value.setText('')

    def __action_edit_chapter_normal(self, mi):
        self.__action_edit_chapter_event(mi=mi, title=df.kNORMAL_CHAPTER)

    def __action_edit_chapter_hero(self, mi):
        self.__action_edit_chapter_event(mi=mi, title=df.kHERO_CHAPTER)

    def __action_edit_event(self, mi):
        self.__action_edit_chapter_event(mi=mi, title=df.kEVENT)

    def __action_edit_chapter_event(self, mi, title):
        cbox = None
        cb_rec = None
        bt_add = None
        bt_delete = None
        bt_cancel = None
        reg = None

        index = mi.row()
        if index >= 0:
            self.__flag_chapter_event_update = True

            if title == df.kNORMAL_CHAPTER:
                reg = self.egg.find_normal_chapters.chapter_data[index]
                cbox = self.cbox_normal_ch
                cb_rec = self.cb_rec_add_normal_ch
                bt_add = self.bt_add_normal_ch
                bt_delete = self.bt_delete_normal_ch
                bt_cancel = self.bt_cancel_normal_ch
            elif title == df.kHERO_CHAPTER:
                reg = self.egg.find_hero_chapters.chapter_data[index]
                cbox = self.cbox_hero_ch
                cb_rec = self.cb_rec_add_hero_ch
                bt_add = self.bt_add_hero_ch
                bt_delete = self.bt_delete_hero_ch
                bt_cancel = self.bt_cancel_hero_ch
            elif title == df.kEVENT:
                reg = self.egg.find_events.chapter_data[index]
                cbox = self.cbox_event_ch
                cb_rec = self.cb_rec_add_event_ch
                bt_add = self.bt_add_event_ch
                bt_delete = self.bt_delete_event_ch
                bt_cancel = self.bt_cancel_event_ch

            # print(f'__action_edit_chapter_event [{title}] [{index}] [{reg}] '
            #       f'flag [{self.__flag_chapter_event_update}]')

            if cbox is not None:
                cbox.setCurrentText(reg.chapter_str)

            if cb_rec is not None:
                cb_rec.setChecked(reg.recommended)

            if bt_add is not None:
                bt_add.setText(df.kBT_UPDATE_TEXT)

            if bt_delete is not None:
                bt_delete.show()

            if bt_cancel is not None:
                bt_cancel.show()

    @staticmethod
    def __get_txt_value(txt, required=False, error_msg='', convert_type=None):
        value = txt.text().strip()
        if value == '':
            if required:
                raise RequiredField(error_msg, txt)
            return None
        else:
            if convert_type == 'int':
                try:
                    return int(value)
                except ValueError:
                    raise RequiredFieldInt(error_msg, txt)
            else:
                return value

    def __action_save_egg(self):
        try:
            self.egg.set_gen(name_en=self.__get_txt_value(txt=self.txt_name_en,
                                                          required=True,
                                                          error_msg='Nome em inglês obrigatório'))
            self.egg.set_gen(name_pt=self.__get_txt_value(txt=self.txt_name_pt))
            self.egg.set_gen(type_mob=self.rb_mob.isChecked())
            self.egg.set_gen(type_boss=self.rb_boss.isChecked())
            self.egg.set_gen(collected=self.cb_collected.isChecked())
            self.egg.set_gen(stars=int(self.spin_stars.value()))
            # find normal chapter
            ret = self.egg.find_normal_chapters.convert_to_db()
            # print(f'normal [{ret}]')
            # print(f'orig   [{self.egg.find_normal_chapters.value_orig}]')
            # print(f'==     [{self.egg.find_normal_chapters.value_orig == ret}]')
            self.egg.set_gen(find_normal_chapters=ret)
            # find hero chapter
            ret = self.egg.find_hero_chapters.convert_to_db()
            # print(f'hero [{ret}]')
            # print(f'orig [{self.egg.find_hero_chapters.value_orig}]')
            # print(f'==   [{self.egg.find_hero_chapters.value_orig == ret}]')
            self.egg.set_gen(find_hero_chapters=ret)
            # find event
            ret = self.egg.find_events.convert_to_db()
            # print(f'events [{ret}]')
            # print(f'orig   [{self.egg.find_events.value_orig}]')
            # print(f'==     [{self.egg.find_events.value_orig == ret}]')
            self.egg.set_gen(find_events=ret)
            self.egg.set_gen(to_hatch=self.__get_txt_value(txt=self.txt_to_hatch,
                                                           convert_type='int',
                                                           error_msg='To Hatch precisa ser um número'))
            self.egg.set_gen(natural_hatch=self.__get_txt_value(txt=self.txt_natural_hatch,
                                                                convert_type='int',
                                                                error_msg='Natural Hatch precisa ser um número'))
            self.egg.set_gen(quest1=self.__get_txt_value(txt=self.txt_quest1,
                                                         convert_type='int',
                                                         error_msg='Quest 1 precisa ser um número'))
            self.egg.set_gen(quest1_unlocked=self.cb_quest1.isChecked())
            self.egg.set_gen(quest2=self.__get_txt_value(txt=self.txt_quest2,
                                                         convert_type='int',
                                                         error_msg='Quest 2 precisa ser um número'))
            self.egg.set_gen(quest2_unlocked=self.cb_quest2.isChecked())

            ret = self.egg.train_cost.convert_to_db()
            # print(f'train cost [{ret}]')
            self.egg.set_gen(train_cost=ret)

            ret = self.egg.train_stats.convert_to_db()
            # print(f'train stats [{ret}]')
            self.egg.set_gen(train_stats=ret)

            ret = self.egg.train_stats_stars.convert_to_db()
            # print(f'train stats stars [{ret}]')
            self.egg.set_gen(train_stats_stars=ret)

            self.egg.set_gen(competition_available=self.gb_competition.isChecked())
            ret = self.egg.competition_stats.convert_to_db()
            # print(f'competition stats [{ret}]')
            self.egg.set_gen(competition_stats=ret)

            self.egg.set_gen(date_updated=datetime.datetime.now())

        except RequiredField as e:
            self.__handle_exception(exception=e)
            return
        except RequiredFieldInt as e:
            self.__handle_exception(exception=e)
            return

        # self.egg.dump()
        try:
            self.__db.update_egg(egg=self.egg)
            QMessageBox.information(self, ' ', 'Egg atualizado com sucesso.', QMessageBox.Ok)

            self.__build_dates()
        except:
            print(traceback.format_exc())
            QMessageBox.critical(self, ' ', 'Erro ao atualizar egg.', QMessageBox.Ok)

    def __handle_exception(self, exception):
        QMessageBox.warning(self, ' ', exception.args[0] + '.', QMessageBox.Ok)
        txt = exception.args[1]
        txt.setFocus()
