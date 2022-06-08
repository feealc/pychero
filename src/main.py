import sys
import argparse
from PyQt5.QtWidgets import *
from views.window_main import MainWindow
from views.window_egg_main import WindowEggMain
from test import test_main

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--eggs', action='store_true', help='Mostrar a tela de eggs')
    parser.add_argument('-m', '--maximized', action='store_true', help='Mostrar a tela secundaria maximizada')
    parser.add_argument('-t', '--test', action='store_true', help='Executar funcao de teste')
    args = parser.parse_args()

    if args.test:
        test_main()
        sys.exit()

    app = QApplication([])

    win = None
    if args.eggs:
        win = WindowEggMain()
    else:
        win = MainWindow(parser=parser, args=args)

    win.show()
    win.b_center_window()

    sys.exit(app.exec())
