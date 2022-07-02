from PySide2.QtWidgets import QWidget
from views.main_view_ui import Ui_RobustarLauncher


class MainView(QWidget):
    def __init__(self, ctrl):
        super().__init__()

        self.ctrl = ctrl
        self.ui = Ui_RobustarLauncher()
        self.ui.setupUi(self)

        # Match the corresponding signals to slots in controllers
        self.ui.nameInput.textEdited.connect(self.ctrl.setMContainerName)
        self.ui.versionComboBox.currentIndexChanged.connect(self.ctrl.setMImageVersion)
        self.ui.websitePortInput.textEdited.connect(self.ctrl.setMWebsitePort)
        self.ui.backendPortInput.textEdited.connect(self.ctrl.setMBackendPort)
        self.ui.tensorboardPortInput.textEdited.connect(self.ctrl.setMTensorboardPort)
        self.ui.trainPathButton.clicked.connect(self.ctrl.setMTrainPath)
        self.ui.testPathButton.clicked.connect(self.ctrl.setMTestPath)
        self.ui.checkPointPathButton.clicked.connect(self.ctrl.setMCheckPointPath)
        self.ui.influencePathButton.clicked.connect(self.ctrl.setMInfluencePath)
        self.ui.configFileButton.clicked.connect(self.ctrl.setMConfigFile)
        self.ui.loadProfileButton.clicked.connect(self.ctrl.loadProfile)
        self.ui.saveProfileButton.clicked.connect(self.ctrl.saveProfile)
        # self.ui.startServerButton.clicked.connect(self.ctrl.startServer)
        # self.ui.stopServerButton.clicked.connect(self.ctrl.stopServer)
        # self.ui.deleteServerButton.clicked.connect(self.ctrl.deleteServer)
        # self.ui.refreshListWidgetsButton.clicked.connect(self.ctrl.initExistContainer)

        # Set the listWidgets so that only one entry in them can be selected at a time
        self.listWidgets = [self.ui.runningListWidget, self.ui.exitedListWidget, self.ui.createdListWidget]
        self.ui.runningListWidget.selectionModel().selectionChanged.connect(
            lambda sel, unsel: self.singleSelect(self.ui.runningListWidget, self.listWidgets))
        self.ui.exitedListWidget.selectionModel().selectionChanged.connect(
            lambda sel, unsel: self.singleSelect(self.ui.exitedListWidget, self.listWidgets))
        self.ui.createdListWidget.selectionModel().selectionChanged.connect(
            lambda sel, unsel: self.singleSelect(self.ui.createdListWidget, self.listWidgets))


    # Function to ensure only one entry in the three listWidgets can be selected at a time
    def singleSelect(self, listWidget, listWidgets):

        for widget in listWidgets:
            # Only check the other listWidgets
            if widget == listWidget:
                continue

            # If the newly selected item is not in the same listWidget as the previous selected one
            # Remove the previous one from its listWidget
            if widget.selectionModel().hasSelection():
                widget.selectionModel().clearSelection()