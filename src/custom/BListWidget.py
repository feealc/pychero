from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class BListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def b_clear_content(self):
        self.clear()

    def b_has_item(self):
        return self.count() > 0

    def b_get_index_to_insert(self):
        if self.b_has_item():
            return self.count()
        else:
            return 0

    def b_add_row(self, value):
        index = self.b_get_index_to_insert()
        self.insertItem(index, value)
