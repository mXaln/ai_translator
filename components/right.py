from PyQt5 import QtWidgets


class RightLayout(QtWidgets.QVBoxLayout):
    def __init__(self, lang_model, parent=None):
        super(RightLayout, self).__init__(parent)

        self.combo = QtWidgets.QComboBox()
        self.text_edit = QtWidgets.QTextEdit()

        self.combo.setModel(lang_model)
        self.combo.setPlaceholderText("Select Target Language")
        self.combo.setView(QtWidgets.QListView())
        self.combo.setStyleSheet("combobox-popup: 0;")
        self.combo.setMaxVisibleItems(20)
        self.combo.setCurrentIndex(-1)

        self.text_edit.setReadOnly(True)
        self.text_edit.setObjectName("target_text")

        self.addWidget(self.combo)
        self.addWidget(self.text_edit)

    def set_text(self, text):
        self.text_edit.setText(text)

    def get_text(self):
        return self.text_edit.toPlainText()

    def get_lang(self):
        return str(self.combo.currentText())
