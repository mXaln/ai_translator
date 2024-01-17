from PyQt5 import QtCore


class LanguagesModel(QtCore.QAbstractListModel):
    def __init__(self, languages=None):
        super(LanguagesModel, self).__init__()
        self.languages = languages or {}
        self.keys = list(self.languages.keys())

    def data(self, index, role=...):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            row = index.row()
            text = self.keys[row]
            return text

    def rowCount(self, index=...):
        return len(self.languages)
