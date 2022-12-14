import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen

from src.furlanis_data_class import get_true_filename
from src.gui.userinterface import ui_window


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
