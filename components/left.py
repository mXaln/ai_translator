from PyQt5 import QtWidgets


class LeftLayout(QtWidgets.QVBoxLayout):
    def __init__(self, lang_model, parent=None):
        super(LeftLayout, self).__init__(parent)

        self.combo = QtWidgets.QComboBox()
        self.text_edit = QtWidgets.QTextEdit()

        self.combo.setModel(lang_model)
        self.combo.setPlaceholderText("Select Source Language")
        self.combo.setView(QtWidgets.QListView())
        self.combo.setStyleSheet("combobox-popup: 0;")
        self.combo.setMaxVisibleItems(20)
        self.combo.setCurrentIndex(-1)

        self.addWidget(self.combo)
        self.addWidget(self.text_edit)

    def set_text(self, text):
        self.text_edit.setText(text)

    def get_text(self):
        return self.text_edit.toPlainText()

    def get_lang(self):
        return str(self.combo.currentText())
