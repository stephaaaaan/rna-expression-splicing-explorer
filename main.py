import sys
import time

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen

from gene_table import gene_count_table, get_true_filename
from userinterface import ui_window


def main():
    app = QApplication(sys.argv)
    w,h=app.primaryScreen().size().width(),app.primaryScreen().size().height()
    splash = QSplashScreen()
    splash.setPixmap(QPixmap(get_true_filename("icon.ico")))
    splash.show()
    main = ui_window(w,h)
    splash.finish(main)
    main.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
