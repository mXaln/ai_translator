from PyQt5 import QtWidgets
from components.left import LeftLayout
from components.right import RightLayout


class CenterLayout(QtWidgets.QHBoxLayout):
    def __init__(self, lang_model, parent=None):
        super(CenterLayout, self).__init__(parent)

        self.left = LeftLayout(lang_model)
        self.right = RightLayout(lang_model)

        self.addLayout(self.left)
        self.addLayout(self.right)

    def set_source_text(self, text):
        self.left.set_text(text)

    def get_source_text(self):
        return self.left.get_text()

    def get_source_lang(self):
        return self.left.get_lang()

    def set_target_text(self, text):
        self.right.set_text(text)

    def get_target_text(self):
        return self.right.get_text()

    def get_target_lang(self):
        return self.right.get_lang()
