import docker
import os
import json
import time

from PySide2.QtCore import QObject, Qt
from PySide2.QtWidgets import QFileDialog
from threading import Thread

from controllers.docker_ctrl import DockerController


class MainController(QObject):
    def __init__(self):
        super().__init__()

    def setModel(self, model):
        self.model = model

    def setMainView(self, view):
        self.mainView = view

    def setPopupView(self, view):
        self.popupView = view

    def init(self):
        try:
            self.dockerCtrl = DockerController(self.model, self.mainView)

            self.mainView.show()
        except docker.errors.DockerException:
            self.popupView.show()
            
            
    # Slot functions to change the model
    def setMContainerName(self):
        self.model.containerName = self.mainView.ui.nameInput.text()

    def setMImageVersion(self):
        self.model.imageVersion = self.mainView.ui.versionComboBox.currentText()

    def setMWebsitePort(self):
        self.model.websitePort = self.mainView.ui.websitePortInput.text()

    def setMBackendPort(self):
        self.model.backendPort = self.mainView.ui.backendPortInput.text()

    def setMTensorboardPort(self):
        self.model.tensorboardPort = self.mainView.ui.tensorboardPortInput.text()

    def setMTrainPath(self):
        path = QFileDialog.getExistingDirectory(self.mainView, "Choose Train Set Path", self.model.cwd)
        self.model.cwd = os.path.dirname(path)
        if path:
            self.model.trainPath = path

    def setMTestPath(self):
        path = QFileDialog.getExistingDirectory(self.mainView, "Choose Test Set Path", self.model.cwd)
        self.model.cwd = os.path.dirname(path)
        if path:
            self.model.testPath = path

    def setMCheckPointPath(self):
        path = QFileDialog.getExistingDirectory(self.mainView, "Choose Checkpoints Path", self.model.cwd)
        self.model.cwd = os.path.dirname(path)
        if path:
            self.model.checkPointPath = path

    def setMInfluencePath(self):
        path = QFileDialog.getExistingDirectory(self.mainView, "Choose Influence Result Path", self.model.cwd)
        self.model.cwd = os.path.dirname(path)
        if path:
            self.model.influencePath = path

    def setMConfigFile(self):
        path, _ = QFileDialog.getOpenFileName(self.mainView, "Choose Config File", self.model.cwd, "JSON Files (*.json);;All Files (*)")
        self.model.cwd = os.path.dirname(path)
        if path:
            self.model.configFile = path

    def loadProfile(self):
        path, _ = QFileDialog.getOpenFileName(self.mainView, "Load Profile", self.model.cwd, "JSON Files (*.json);;All Files (*)")
        self.model.cwd = os.path.dirname(path)
        try:
            with open(path, 'r') as f:
                self.model.profile = json.load(f)
        except FileNotFoundError:
            print('Load path not found')

    def saveProfile(self):
        path, _ = QFileDialog.getSaveFileName(self.mainView, "Save Profile", self.model.cwd, "JSON Files (*.json);;All Files (*)")
        self.model.cwd = os.path.dirname(path)
        try:
            with open(path, 'w') as f:
                json.dump(self.model.profile, f)
        except FileNotFoundError:
            print('The dialog is closed')

    def startServer(self):
        if(self.checkProfile()):
            return
        else:
            t = ServerOperationThread(target=self.dockerCtrl.startServer)










    # Slot functions to change the view
    def setVContainerName(self, val):
        self.mainView.ui.nameInput.setText(val)

    def setVImageVersion(self, val):
        self.mainView.ui.versionComboBox.setCurrentText(val)

    def setVWebsitePort(self, val):
        self.mainView.ui.websitePortInput.setText(val)

    def setVBackendPort(self, val):
        self.mainView.ui.backendPortInput.setText(val)

    def setVTensorboardPort(self, val):
        self.mainView.ui.tensorboardPortInput.setText(val)

    def setVTrainPath(self, val):
        self.mainView.ui.trainPathDisplay.setText(val)

    def setVTestPath(self, val):
        self.mainView.ui.testPathDisplay.setText(val)

    def setVCheckPointPath(self, val):
        self.mainView.ui.checkPointPathDisplay.setText(val)

    def setVInfluencePath(self, val):
        self.mainView.ui.influencePathDisplay.setText(val)

    def setVConfigFile(self, val):
        self.mainView.ui.configFileDisplay.setText(val)


    # Other control functions
    def printMessage(self, textBrowser, message, timestamp=True):
        if(timestamp == True):
            currentTime = time.strftime("%H:%M:%S", time.localtime())
            message = currentTime + ' - - ' + message + '\n'
        textBrowser.append(message)
        textBrowser.verticalScrollBar().setValue(textBrowser.verticalScrollBar().maximum())

    def addItem(self, listWidget, name):
        listWidget.addItem(name)

    def removeItem(self, listWidget, name):
        items = listWidget.findItems(name, Qt.MatchExactly)
        item = items[0]
        row = listWidget.row(item)
        listWidget.takeItem(row)

    def enableControl(self):
        self.mainView.ui.startServerButton.setEnabled(True)
        self.mainView.ui.stopServerButton.setEnabled(True)
        self.mainView.ui.deleteServerButton.setEnabled(True)

    def disableControl(self):
        self.mainView.ui.startServerButton.setEnabled(False)
        self.mainView.ui.stopServerButton.setEnabled(False)
        self.mainView.ui.deleteServerButton.setEnabled(False)

    def checkProfile(self):
        missProfileDict = {'trainPath': 'train set path', 'testPath': 'test set path',
                          'influencePath': 'influence result path', 'checkPointPath': 'check point path',
                          'configFile': 'config file path'}

        for profileName in ['trainPath', 'testPath', 'influencePath', 'checkPointPath', 'configFile']:
            if not self.model.profile[profileName].strip():
                self.printMessage(self.mainView.ui.promptBrowser, "Please provide {}".format(missProfileDict[profileName]))
                return 1
        return 0
    
    def getItemsFromListWidgets(self):
        return self.mainView.ui.runningListWidget.selectedItems() if len(
            self.mainView.ui.runningListWidget.selectedItems()) > 0 else self.mainView.ui.exitedListWidget.selectedItems() if len(
            self.mainView.ui.exitedListWidget.selectedItems()) > 0 else self.mainView.ui.createdListWidget.selectedItems() if len(
            self.mainView.ui.createdListWidget.selectedItems()) > 0 else []






class ServerOperationThread(Thread):
    def __init__(self, target):
        Thread.__init__(self, daemon=True)
        self.func = target

    def run(self):
        MainController.disableControl()
        self.func()
        MainController.enableControl()