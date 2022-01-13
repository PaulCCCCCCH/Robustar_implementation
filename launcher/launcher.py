from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog, QWidget
import os

class Launcher(QWidget):
    def __init__(self):
        super(Launcher, self).__init__()

        self.cwd = os.getcwd()

        self.ui = QUiLoader().load('launcher.ui')


        self.ui.trainPathButton.clicked.connect(self.chooseDirectory)
        self.ui.loadConfigButton.clicked.connect(self.chooseFile)
        self.ui.saveConfigButton.clicked.connect(self.saveFile)

    def chooseDirectory(self):
        directory = QFileDialog.getExistingDirectory(self, "Choose Directory", self.cwd)

    def chooseFile(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self, "Choose File", self.cwd, "JSON Files (*.json)")

    def saveFile(self):
        fileName_choose, filetype = QFileDialog.getSaveFileName(self, "Save File", self.cwd, "JSON Files (*.json)")


app = QApplication([])
launcher = Launcher()

launcher.ui.setFixedSize(800, 680)
launcher.ui.show()
app.exec_()