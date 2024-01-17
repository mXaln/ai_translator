from PyQt5 import QtWidgets, QtCore, QtGui


class OverlayWidget(QtWidgets.QLabel):
    def __init__(self, message, parent=None):
        super(OverlayWidget, self).__init__(parent)
        self.setAutoFillBackground(True)

        self.setText(message)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(22, 22, 22, 200))
        palette.setColor(QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white)
        self.setPalette(palette)

        self.setVisible(False)
