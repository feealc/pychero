from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class BTableWidget(QTableWidget):
    def __init__(self, parent=None):
        # super(BTableWidget, self).__init__()
        super().__init__(parent=parent)
        # print('BTableWidget init')
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.__center_content = False
        self.__header_labels = []

    # def contextMenuEvent(self, event):
    #     contextMenu = QMenu(self)
    #     newAct = contextMenu.addAction("New")
    #     openAct = contextMenu.addAction("Open")
    #     quitAct = contextMenu.addAction("Quit")
    #     action = contextMenu.exec_(self.mapToGlobal(event.pos()))
    #     if action == quitAct:
    #         self.close()

    def b_clear_content(self):
        self.clearContents()
        self.setRowCount(0)

    def b_add_row(self, from_tuple=None):
        row = self.rowCount()
        self.setRowCount(row + 1)
        col = 0
        for item in from_tuple:
            cell = QTableWidgetItem(str(item))
            # cell.setFlags(QtCore.Qt.ItemIsEditable)
            # cell.setFlags(QtCore.Qt.ItemIsEnabled)
            # cell.setFlags(QtCore.Qt.ItemIsEditable)
            # cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # disable cell editing
            if self.__center_content:
                cell.setTextAlignment(Qt.AlignCenter)  # align cell content center
            self.setItem(row, col, cell)
            col += 1

    def b_set_column_header(self, header_labels, ajust_columns=False):
        self.__header_labels = header_labels
        self.setColumnCount(len(self.__header_labels))
        self.setHorizontalHeaderLabels(self.__header_labels)
        if ajust_columns:
            self.b_ajust_header_columns()

    def b_set_center_content(self, value=True):
        self.__center_content = value

    def b_hide_vertical_headers(self):
        self.verticalHeader().setVisible(False)

    def b_show_vertical_headers(self):
        self.verticalHeader().setVisible(True)

    def b_set_select_row(self):
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

    def b_ajust_header_columns(self):
        header = self.horizontalHeader()
        for index, hl in enumerate(self.__header_labels):
            header.setSectionResizeMode(index, QHeaderView.ResizeMode.ResizeToContents)

    def b_ajust_header_columns_headerview(self, header_view_list):
        if len(header_view_list) != len(self.__header_labels):
            return
        header = self.horizontalHeader()
        for index, header_view in enumerate(header_view_list):
            header.setSectionResizeMode(index, header_view)
