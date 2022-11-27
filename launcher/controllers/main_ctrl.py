import requests
import docker
import os
import json
import time

from PySide2.QtCore import QObject, Qt
from PySide2 import QtGui
from PySide2.QtWidgets import QFileDialog
from threading import Thread


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
        from controllers.docker_ctrl import DockerController

        try:
            self.initImageVersions()
            self.dockerCtrl = DockerController(self.model, self.mainView, self)
            self.dockerCtrl.refreshServers()
            self.mainView.show()
        except requests.RequestException:
            self.popupView.ui.warningLabel.setText(f'Failed to fetch image versions online!\nPlease check your network!')
            self.popupView.show()
        except docker.errors.DockerException:
            self.popupView.ui.warningLabel.setText('Docker is not running!\nPlease start Docker first!')
            self.popupView.show()


    # Slot functions to change the model
    def setMContainerName(self):
        self.model.containerName = self.mainView.ui.nameInput.text()

    def setMImageVersion(self):
        self.model.imageVersion = self.mainView.ui.versionComboBox.currentText()

    def setMPort(self):
        self.model.port = self.mainView.ui.portInput.text()

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

        self.initWeightFiles()

    def setMInfluencePath(self):
        path = QFileDialog.getExistingDirectory(self.mainView, "Choose Influence Result Path", self.model.cwd)
        self.model.cwd = os.path.dirname(path)
        if path:
            self.model.influencePath = path

    def setMArch(self):
        self.model.modelArch = self.mainView.ui.archComboBox.currentText()

    def setMPretrained(self):
        if self.mainView.ui.pretrainedCheckBox.isChecked():
            self.model.pretrained = 'True'
        else:
            self.model.pretrained = 'False'

    def setMWeightFile(self):
        self.model.weightFile = self.mainView.ui.weightFileComboBox.currentText()

    def setMDevice(self):
        self.model.device = self.mainView.ui.deviceInput.text()

    def setMShuffle(self):
        if self.mainView.ui.shuffleCheckBox.isChecked():
            self.model.shuffle = 'True'
        else:
            self.model.shuffle = 'False'

    def setMBatchSize(self):
        self.model.batchSize = self.mainView.ui.batchSizeInput.text()

    def setMWorkerNumber(self):
        self.model.workerNumber = self.mainView.ui.workerNumberInput.text()

    def setMImgSize(self):
        self.model.imgSize = self.mainView.ui.imgSizeInput.text()

    def setMPadding(self):
        self.model.padding = self.mainView.ui.paddingComboBox.currentText()

    def setMClassNumber(self):
        self.model.classNumber = self.mainView.ui.classNumberInput.text()

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
        if(self.mainView.ui.tabWidget.currentIndex() == 0 and self.checkProfile()):
            return
        else:
            t = ServerOperationThread(target=self.dockerCtrl.startServer, ctrl=self)
            t.start()

    def stopServer(self):
        t = ServerOperationThread(target=self.dockerCtrl.stopServer, ctrl=self)
        t.start()

    def deleteServer(self):
        t = ServerOperationThread(target=self.dockerCtrl.deleteServer, ctrl=self)
        t.start()

    def refreshServers(self):
        t = Thread(target=self.dockerCtrl.refreshServers)
        t.start()


    # Slot functions to change the view
    def setVContainerName(self, val):
        self.mainView.ui.nameInput.setText(val)

    def setVImageVersion(self, val):
        self.mainView.ui.versionComboBox.setCurrentText(val)

    def setVPort(self, val):
        self.mainView.ui.portInput.setText(val)

    def setVTrainPath(self, val):
        self.mainView.ui.trainPathDisplay.setText(val)

    def setVTestPath(self, val):
        self.mainView.ui.testPathDisplay.setText(val)

    def setVCheckPointPath(self, val):
        self.mainView.ui.checkPointPathDisplay.setText(val)
        self.initWeightFiles()

    def setVInfluencePath(self, val):
        self.mainView.ui.influencePathDisplay.setText(val)

    def setVModelArch(self, val):
        self.mainView.ui.archComboBox.setCurrentText(val)

    def setVPretrained(self, val):
        if val == 'True':
            self.mainView.ui.pretrainedCheckBox.setChecked(True)
        else:
            self.mainView.ui.pretrainedCheckBox.setChecked(False)

    def setVWeightFile(self, val):
        self.mainView.ui.weightFileComboBox.setCurrentText(val)

    def setVDevice(self, val):
        self.mainView.ui.deviceInput.setText(val)

    def setVShuffle(self, val):
        if val == 'True':
            self.mainView.ui.shuffleCheckBox.setChecked(True)
        else:
            self.mainView.ui.shuffleCheckBox.setChecked(False)

    def setVBatchSize(self, val):
        self.mainView.ui.batchSizeInput.setText(val)

    def setVWorkerNumber(self, val):
        self.mainView.ui.workerNumberInput.setText(val)

    def setVImgSize(self, val):
        self.mainView.ui.imgSizeInput.setText(val)

    def setVPadding(self, val):
        self.mainView.ui.paddingComboBox.setCurrentText(val)

    def setVClassNumber(self, val):
        self.mainView.ui.classNumberInput.setText(val)


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
                           'batch_size': 'batch size', 'num_workers': 'worker number',
                           'num_classes': 'class number', 'image_size': 'image size'}
        missProfilePrompt = []

        for profileName in ['trainPath', 'testPath', 'influencePath', 'checkPointPath', 'batch_size', 'num_workers', 'num_classes', 'image_size']:
            if not self.model.profile[profileName].strip():
                missProfilePrompt.append(missProfileDict[profileName])

        if len(missProfilePrompt) != 0:
            self.printMessage(self.mainView.ui.promptBrowser,
                              "Please provide {}".format(', '.join(missProfilePrompt)))
            return 1
        return 0
    
    def getItemsFromListWidgets(self):
        return self.mainView.ui.runningListWidget.selectedItems() if len(
            self.mainView.ui.runningListWidget.selectedItems()) > 0 else self.mainView.ui.exitedListWidget.selectedItems() if len(
            self.mainView.ui.exitedListWidget.selectedItems()) > 0 else self.mainView.ui.createdListWidget.selectedItems() if len(
            self.mainView.ui.createdListWidget.selectedItems()) > 0 else []


    def updateSucView(self):
        self.printMessage(self.mainView.ui.promptBrowser,
                                    '{} is available at http://localhost:{}'.format(self.model.tempName,
                                                                                    self.model.tempPort))
        self.addItem(self.mainView.ui.runningListWidget, self.model.tempName)

    # Fetch the docker image versions to add to the image version combobox and initiate model's image version
    def initImageVersions(self):
        res = requests.get(
            'https://registry.hub.docker.com/v2/repositories/paulcccccch/robustar/tags?page_size=1024', timeout=3)

        for item in res.json()['results']:
            self.mainView.ui.versionComboBox.addItem(item['name'])
        self.model.imageVersion = self.mainView.ui.versionComboBox.currentText()

    # Scan the checkpoint directory to add checkpoint files to the weight file combobox and initiates model's weight file
    def initWeightFiles(self):
        self.mainView.ui.weightFileComboBox.clear()
        self.mainView.ui.weightFileComboBox.addItem('None')

        for file in os.listdir(self.model.checkPointPath):
            if file.endswith('.pth') or file.endswith('.pt'):
                self.mainView.ui.weightFileComboBox.addItem(file)

        self.model.weightFile = self.mainView.ui.weightFileComboBox.currentText()

class ServerOperationThread(Thread):
    def __init__(self, target, ctrl):
        Thread.__init__(self, daemon=True)
        self.func = target
        self.ctrl = ctrl

    def run(self):
        self.ctrl.disableControl()
        self.func()
        self.ctrl.enableControl()