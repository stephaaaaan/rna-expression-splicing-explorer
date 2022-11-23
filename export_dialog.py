import os
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QVBoxLayout,
                             QFileDialog, QFrame, QGridLayout, QHBoxLayout,
                             QLabel, QLineEdit, QListWidget, QMessageBox,
                             QPushButton, QComboBox, QWidget)

class export_dialog(QWidget):
    def __init__(self):
        super().__init__()
        export_layout = QGridLayout()
        filepath_label = QLabel('Filepath')
        export_layout.addWidget(filepath_label,0,0)
        self.filepath_input = QLineEdit()
        if sys.platform == 'linux':
            desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        else:
            desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.filepath_input.setText(desktop_path)
        self.filepath_input.setMinimumSize(300,20)
        export_layout.addWidget(self.filepath_input,0,1)
        filepath_change_btn = QPushButton('change')
        filepath_change_btn.clicked.connect(self.change_filepath)
        export_layout.addWidget(filepath_change_btn,0,2)
        filename_label = QLabel('Filename')
        export_layout.addWidget(filename_label,1,0)
        filename_input = QLineEdit()
        export_layout.addWidget(filename_input,1,1)
        fileformat = QComboBox()
        fileformat.addItems(['csv','xlsx'])
        fileformat.setCurrentIndex(0)
        export_layout.addWidget(fileformat,1,2)
        self.setLayout(export_layout)

    

    def change_filepath(self):
        filepath = QFileDialog.getExistingDirectory()
        self.filepath_input.setText(filepath)

app = QApplication(sys.argv)
main = export_dialog()
main.show()
sys.exit(app.exec_())