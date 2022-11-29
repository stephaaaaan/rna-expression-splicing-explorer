import os
import sys

from PyQt5.QtWidgets import (QComboBox, QFileDialog, QGridLayout, QLabel,
                             QLineEdit, QMessageBox, QPushButton, QWidget)


class export_dialog(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        # ---------------------------------------------------------------------------- #
        #                                 export window                                #
        # ---------------------------------------------------------------------------- #
        # ---------------------------------- layout ---------------------------------- #
        export_layout = QGridLayout()
        # --------------------------------- filepath --------------------------------- #
        filepath_label = QLabel("Filepath")
        export_layout.addWidget(filepath_label, 0, 0)
        self.filepath_input = QLineEdit()
        if sys.platform == "linux":
            desktop_path = os.path.join(
                os.path.join(os.path.expanduser("~")), "Desktop"
            )
        elif sys.platform == "darwin":
            desktop_path = os.path.join(os.path.join(os.path.expanduser("~")), "Desktop")
        else:
            desktop_path = os.path.join(
                os.path.join(os.environ["USERPROFILE"]), "Desktop"
            )
        self.filepath_input.setText(desktop_path)
        self.filepath_input.textChanged.connect(self.filepath_check_changed_made)
        self.filepath_input.editingFinished.connect(self.filepath_changed)
        self.filepath_input.setMinimumSize(300, 20)
        export_layout.addWidget(self.filepath_input, 0, 1)
        filepath_change_btn = QPushButton("change")
        filepath_change_btn.clicked.connect(self.change_filepath)
        export_layout.addWidget(filepath_change_btn, 0, 2)
        # ---------------------------- filename and format --------------------------- #
        filename_label = QLabel("Filename")
        export_layout.addWidget(filename_label, 1, 0)
        self.filename_input = QLineEdit()
        export_type = (
            "alternative_splicing"
            if self.parent.alternative_splicing.isChecked()
            else "gene_expression"
        )
        self.filename_input.setText(f"{export_type}_data")
        self.filename_input.textChanged.connect(self.filename_changed)
        export_layout.addWidget(self.filename_input, 1, 1)
        self.fileformat = QComboBox()
        self.fileformat.addItems(["csv", "xlsx"])
        self.fileformat.setCurrentIndex(0)
        export_layout.addWidget(self.fileformat, 1, 2)
        # ------------------------------- export button ------------------------------ #
        export_btn = QPushButton("export")
        export_btn.clicked.connect(self.export)
        export_layout.addWidget(export_btn)
        self.setLayout(export_layout)

    # ---------------------------------------------------------------------------- #
    #                                   functions                                  #
    # ---------------------------------------------------------------------------- #
    def change_filepath(self):
        filepath = QFileDialog.getExistingDirectory()
        self.filepath_input.setText(filepath)

    def filepath_check_changed_made(self) -> None:
        if os.path.exists(self.filepath_input.text()):
            self.filepath_input.setStyleSheet(
                "QLineEdit"
                "{"
                "background : #9cffa9;"
                "border-width : 2px;"
                "border-color : darkgreen;"
                "}"
            )
        else:
            self.filepath_input.setStyleSheet(
                "QLineEdit"
                "{"
                "background : white;"
                "border-width : 2px;"
                "border-color : black;"
                "}"
            )

    def filepath_changed(self) -> None:
        if os.path.exists(self.filepath_input.text()):
            self.filepath_input.setStyleSheet(
                "QLineEdit"
                "{"
                "background : white;"
                "border-width : 2px;"
                "border-color : black;"
                "}"
            )
        else:
            self.filepath_input.setStyleSheet(
                "QLineEdit"
                "{"
                "background : #eb6767;"
                "border-width : 2px;"
                "border-color : darkred;"
                "}"
            )

    def filename_changed(self) -> None:
        if self.filename_input.text() != "":
            self.filename_input.setStyleSheet(
                "QLineEdit"
                "{"
                "background : white;"
                "border-width : 2px;"
                "border-color : black;"
                "}"
            )
        else:
            self.filename_input.setStyleSheet(
                "QLineEdit"
                "{"
                "background : #eb6767;"
                "border-width : 2px;"
                "border-color : darkred;"
                "}"
            )

    def export(self):
        if self.filepath_input == "" or not os.path.exists(self.filepath_input.text()):
            msg = QMessageBox()
            msg.setWindowTitle("Filepath error")
            msg.setText("Please set a valid path for export.")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            return
        if self.filename_input == "":
            msg = QMessageBox()
            msg.setWindowTitle("Filename error")
            msg.setText("Filename cannot be empty.")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            return
        if os.path.exists(
            os.path.join(
                self.filepath_input.text(),
                f"{self.filename_input.text()}.{self.fileformat.currentText()}",
            )
        ):
            answer = QMessageBox.question(
                self,
                "File exists",
                f"The file {self.filename_input.text()}.{self.fileformat.currentText()} already exists. Do you want to overwrite it?",
                QMessageBox.Yes,
                QMessageBox.No,
            )
            if answer == QMessageBox.No:
                return

        self.parent.save(
            self.filepath_input.text(),
            self.filename_input.text(),
            self.fileformat.currentText(),
        )
