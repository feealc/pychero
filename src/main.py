import sys
import argparse
from PyQt5.QtWidgets import *
from views.window_main import MainWindow
from test import test_main

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--maximized', action='store_true', help='Mostrar a tela principal maximizada')
    parser.add_argument('-t', '--test', action='store_true', help='Executar funcao de teste')
    args = parser.parse_args()

    if args.test:
        test_main()
        sys.exit()

    app = QApplication([])
    win = MainWindow()

    if args.maximized:
        win.showMaximized()
    else:
        win.show()
    win.b_center_window()

    sys.exit(app.exec())
