from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class BLabel(QLabel):
    def __init__(self, parent=None, font_size=None, align_center=False, text=None):
        super().__init__(parent=parent)

        if font_size is not None:
            self.b_set_font_size(size=font_size)

        if align_center:
            self.b_set_alignment_center()

        if text is not None:
            self.setText(text)

    def b_set_font_size(self, size):
        self.setFont(QFont('Arial', size))

    def b_set_alignment_center(self):
        self.setAlignment(Qt.AlignCenter)
