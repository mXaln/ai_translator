from PyQt5 import QtWidgets, QtCore, QtGui
from components.center import CenterLayout


class WorkspaceWidget(QtWidgets.QWidget):
    translate = QtCore.pyqtSignal()

    def __init__(self, lang_model, parent=None):
        super(WorkspaceWidget, self).__init__(parent)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.center = CenterLayout(lang_model)
        self.layout.addLayout(self.center)

        translate_btn = QtWidgets.QPushButton("Translate")
        translate_btn.clicked.connect(self.on_translate)
        translate_btn.setMinimumHeight(30)
        translate_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        translate_btn.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: rgb(0, 64, 184);
                border-radius : 4px;
                border: 1px solid rgb(0, 25, 71);
            }
            QPushButton:hover {
                background-color: rgb(0, 44, 122);
            }
            QPushButton:pressed {
                background-color: rgb(0, 25, 71);
            }
        """)

        self.layout.addWidget(translate_btn)

    def on_translate(self):
        self.translate.emit()

    def set_source_text(self, text):
        self.center.set_source_text(text)

    def get_source_text(self):
        return self.center.get_source_text()

    def get_source_lang(self):
        return self.center.get_source_lang()

    def set_target_text(self, text):
        self.center.set_target_text(text)

    def get_target_text(self):
        return self.center.get_target_text()

    def get_target_lang(self):
        return self.center.get_target_lang()
