import sys

from PyQt5.QtWidgets import QApplication, QSplashScreen

from userinterface import ui_window
from PyQt5.QtGui import QPixmap
from gene_table import gene_count_table, get_true_filename
import time


def main():
    app = QApplication(sys.argv)
    splash = QSplashScreen()
    splash.setPixmap(QPixmap(get_true_filename("icon.ico")))
    splash.show()
    # s = gene_count_table()
    main = ui_window()
    splash.finish(main)
    main.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
