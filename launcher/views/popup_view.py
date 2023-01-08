import sys

from PySide2.QtWidgets import QDialog
from PySide2.QtCore import Qt
from views.popup_view_ui import Ui_Dialog


class PopupView(QDialog):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.okButton.clicked.connect(sys.exit)

        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)