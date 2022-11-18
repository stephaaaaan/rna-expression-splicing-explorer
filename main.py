import sys

from PyQt5.QtWidgets import QApplication

from userinterface import ui_window


def main():
    app = QApplication(sys.argv)
    main = ui_window()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()