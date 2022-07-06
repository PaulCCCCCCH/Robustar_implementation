import json
import time
import docker
import os

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog, QWidget, QListWidget, QTextBrowser
from PySide2.QtCore import Signal, QObject, Qt
from threading import Thread

# Change path input by the user to system path
def getSystemPath(userPath: str):
    return str(os.path.normpath(userPath))


# Custom signals
class CustomSignals(QObject):
    # Custom signal for printing message in promptBrowser or detailBrowser
    printMessageSignal = Signal(QTextBrowser, str)

    # Custom signal for adding items in running or exited container list widget
    addItemSignal = Signal(QListWidget, str)

    # Custom signal for removing item from running or exited container list widget
    removeItemSignal = Signal(QListWidget, str)

    # Custom signal for enabling server control buttons
    enableControlSignal = Signal()

    # Custom signal for disabling server control buttons
    disableControlSignal = Signal()


# Robustar launcher GUI
class Launcher(QWidget):
    def __init__(self):
        # Initialize the UI
        super(Launcher, self).__init__()
        self.ui = QUiLoader().load('launcher_v2.ui')

        # Initialize the signal source object
        self.customSignals = CustomSignals()

        # Initialize the client to communicate with the Docker daemon
        self.client = docker.from_env()

        # Set the default path of the path choosing window
        self.cwd = '/'

        # String to temporarily store container name
        self.tempName = ''

        # Boolean to record if the container is chosen in createTab
        self.fromCreateTab = True

        # Set the default configuration
        self.configs = {
                        'containerName': 'robustar',
                        'imageVersion': 'cuda11.1-0.1.0-beta',
                        'websitePort': '8000',
                        'backendPort': '6848',
                        'tensorboardPort': '6006',
                        'trainPath': '',
                        'testPath': '',
                        'checkPointPath': '',
                        'influencePath': '',
                        'configFile': ''
                        }
        self.loadPath = ''
        self.savePath = ''

        # Match the corresponding signals and slots
        self.ui.nameInput.textEdited.connect(self.changeContainerName)
        self.ui.versionComboBox.currentIndexChanged.connect(self.changeImageVersion)
        self.ui.websitePortInput.textEdited.connect(self.changeWebsitePort)
        self.ui.backendPortInput.textEdited.connect(self.changeBackendPort)
        self.ui.tensorboardPortInput.textEdited.connect(self.changeTensorboardPort)
        self.ui.trainPathButton.clicked.connect(self.chooseTrainPath)
        self.ui.testPathButton.clicked.connect(self.chooseTestPath)
        self.ui.checkPointPathButton.clicked.connect(self.chooseCheckPointPath)
        self.ui.influencePathButton.clicked.connect(self.chooseInfluencePath)
        self.ui.configFileButton.clicked.connect(self.chooseConfigFile)

        self.ui.loadProfileButton.clicked.connect(self.loadProfile)
        self.ui.saveProfileButton.clicked.connect(self.saveProfile)
        self.ui.startServerButton.clicked.connect(self.startServer)
        self.ui.stopServerButton.clicked.connect(self.stopServer)
        self.ui.deleteServerButton.clicked.connect(self.deleteServer)
        self.ui.refreshListWidgetsButton.clicked.connect(self.initContainerList)

        self.customSignals.printMessageSignal.connect(self.printMessage)
        self.customSignals.addItemSignal.connect(self.addItem)
        self.customSignals.removeItemSignal.connect(self.removeItem)
        self.customSignals.enableControlSignal.connect(self.enableControl)
        self.customSignals.disableControlSignal.connect(self.disableControl)

        # Set the listWidgets so that only one entry in them can be selected at a time
        self.listWidgets = [self.ui.runningListWidget, self.ui.exitedListWidget, self.ui.createdListWidget]
        self.ui.runningListWidget.selectionModel().selectionChanged.connect(lambda sel, unsel: self.singleSelect(self.ui.runningListWidget, self.listWidgets))
        self.ui.exitedListWidget.selectionModel().selectionChanged.connect(lambda sel, unsel: self.singleSelect(self.ui.exitedListWidget, self.listWidgets))
        self.ui.createdListWidget.selectionModel().selectionChanged.connect(lambda sel, unsel: self.singleSelect(self.ui.createdListWidget, self.listWidgets))

    def changeContainerName(self):
        self.configs['containerName'] = self.ui.nameInput.text()

    def changeImageVersion(self):
        self.configs['imageVersion'] = self.ui.versionComboBox.currentText()

    def changeWebsitePort(self):
        self.configs['websitePort'] = self.ui.websitePortInput.text()

    def changeBackendPort(self):
        self.configs['backendPort'] = self.ui.backendPortInput.text()

    def changeTensorboardPort(self):
        self.configs['tensorboardPort'] = self.ui.tensorboardPortInput.text()

    def chooseTrainPath(self):
        userPath = QFileDialog.getExistingDirectory(self, "Choose Train Set Path", self.cwd)
        if userPath:
            self.configs['trainPath'] = userPath
            self.ui.trainPathDisplay.setText(userPath)

    def chooseTestPath(self):
        userPath = QFileDialog.getExistingDirectory(self, "Choose Test Set Path", self.cwd)
        if userPath:
            self.configs['testPath'] = userPath
            self.ui.testPathDisplay.setText(userPath)

    def chooseCheckPointPath(self):
        userPath = QFileDialog.getExistingDirectory(self, "Choose Checkpoints Path", self.cwd)
        if userPath:
            self.configs['checkPointPath'] = userPath
            self.ui.checkPointPathDisplay.setText(userPath)

    def chooseInfluencePath(self):
        userPath = QFileDialog.getExistingDirectory(self, "Choose Influence Result Path", self.cwd)
        if userPath:
            self.configs['influencePath'] = userPath
            self.ui.influencePathDisplay.setText(userPath)

    def chooseConfigFile(self):
        userPath, _ = QFileDialog.getOpenFileName(self, "Choose Config File", self.cwd, "JSON Files (*.json);;All Files (*)")
        if userPath:
            self.configs['configFile'] = userPath
            self.ui.configFileDisplay.setText(userPath)

    def loadProfile(self):
        self.loadPath, _ = QFileDialog.getOpenFileName(self, "Load Configs", self.cwd, "JSON Files (*.json);;All Files (*)")
        try:
            with open(self.loadPath, 'r') as f:
                self.configs = json.load(f)

                # Update the UI according to the loaded file
                self.ui.nameInput.setText(self.configs['containerName'])
                self.ui.versionComboBox.setCurrentText(self.configs['imageVersion'])
                self.ui.websitePortInput.setText(self.configs['websitePort'])
                self.ui.backendPortInput.setText(self.configs['backendPort'])
                self.ui.tensorboardPortInput.setText(self.configs['tensorboardPort'])
                self.ui.trainPathDisplay.setText(self.configs['trainPath'])
                self.ui.testPathDisplay.setText(self.configs['testPath'])
                self.ui.checkPointPathDisplay.setText(self.configs['checkPointPath'])
                self.ui.influencePathDisplay.setText(self.configs['influencePath'])
                self.ui.configFileDisplay.setText(self.configs['configFile'])


        except FileNotFoundError:
            print('Load path not found')

    def saveProfile(self):
        self.savePath, _ = QFileDialog.getOpenFileName(self, "Save Configs", self.cwd, "JSON Files (*.json);;All Files (*)")
        try:
            with open(self.savePath, 'w') as f:
                json.dump(self.configs, f)
        except FileNotFoundError:
            print('The dialog is closed')


    def getMissingConfig(self):
        for configName in ['trainPath', 'testPath', 'influencePath', 'checkPointPath', 'configFile']:
            if not self.configs[configName].strip():
                return configName
        return ""


    def startServer(self):
        image = 'paulcccccch/robustar:' + self.configs['imageVersion']
        tmp_file_path = "/Robustar2/launcher/tmp.json"

        missingConfig = self.getMissingConfig()
        if missingConfig:
            self.customSignals.printMessageSignal.emit(self.ui.promptBrowser, "Please provide {}".format(missingConfig))
            return

        def startServerInThread():
            try:
                # Emit signal to disable the server control buttons
                self.customSignals.disableControlSignal.emit()

                self.getSelectedContainer()

                startExistingContainer()

            # If the container with the input name has not been created yet
            # Create a new container and run it
            except docker.errors.NotFound:

                if(self.fromCreateTab == True):
                    try:
                        # If the version uses cuda
                        if 'cuda' in image:
                            createCudaContainer()
                        # If the version only uses cpu
                        else:
                            createCpuContainer()

                        self.customSignals.printMessageSignal.emit(self.ui.promptBrowser, "Running " + self.configs['imageVersion'])
                        self.customSignals.printMessageSignal.emit(self.ui.promptBrowser,
                                                                    self.container.name + ' is available at http://localhost:' +
                                                                    self.configs['websitePort'])
                        self.customSignals.addItemSignal.emit(self.ui.runningListWidget, self.container.name)


                    except docker.errors.APIError as apiError:

                        # If the exception is raised by the port issues
                        # Add the new container to the createdListWidget
                        if ('port is already allocated' in str(apiError)):

                            # Because of the exception
                            # self.container has not been changed to the created one
                            # Thus use self.configs['containerName'] instead of self.container.name
                            self.customSignals.addItemSignal.emit(self.ui.createdListWidget,
                                                                  self.configs['containerName'])

                            self.customSignals.printMessageSignal.emit(self.ui.promptBrowser, self.configs[
                                'containerName'] + ' is created but fails to run because port is already allocated. See more in <i>Details</i> page')
                            self.customSignals.printMessageSignal.emit(self.ui.detailBrowser, str(apiError))

                        else:
                            self.customSignals.printMessageSignal.emit(self.ui.promptBrowser,
                                                                       'Unexpected error encountered. See more in <i>Details</i> page')
                            self.customSignals.printMessageSignal.emit(self.ui.detailBrowser, str(apiError))

                else:
                    self.customSignals.printMessageSignal.emit(self.ui.promptBrowser,
                                                               'Can not find ' + self.tempName + '. Refresh the <i>Manage</i> page to check the latest information')



            except docker.errors.APIError as apiError:

                # If the exception is raised by the port issues
                # Add the new container to the createdListWidget
                if ('port is already allocated' in str(apiError)):

                    self.customSignals.printMessageSignal.emit(self.ui.promptBrowser, self.tempName + ' fails to run because port is already allocated. See more in <i>Details</i> page')
                    self.customSignals.printMessageSignal.emit(self.ui.detailBrowser, str(apiError))

                else:
                    self.customSignals.printMessageSignal.emit(self.ui.promptBrowser,
                                                               'Unexpected error encountered. See more in <i>Details</i> page')
                    self.customSignals.printMessageSignal.emit(self.ui.detailBrowser, str(apiError))


            finally:
                self.customSignals.enableControlSignal.emit()


        # Function to start container that has been created
        # Could raise docker.errors.APIError
        def startExistingContainer():

            # If user selects a container, start it
            # Else, do nothing
            if(self.container != None):

                # If the container has exited
                # Restart the container
                # Update both runningListWidget and exitedListWidget
                if self.container.status == 'exited':
                    self.container.restart()
                    self.customSignals.printMessageSignal.emit(self.ui.promptBrowser,
                        self.container.name + ' is available at http://localhost:' + self.configs['websitePort'])
                    self.customSignals.addItemSignal.emit(self.ui.runningListWidget, self.container.name)
                    self.customSignals.removeItemSignal.emit(self.ui.exitedListWidget, self.container.name)

                # If the container has been created
                # Start the container
                elif self.container.status == 'created':
                    self.container.start()
                    self.customSignals.printMessageSignal.emit(self.ui.promptBrowser,
                        self.container.name + ' is available at http://localhost:' + self.configs['websitePort'])
                    self.customSignals.addItemSignal.emit(self.ui.runningListWidget, self.container.name)
                    self.customSignals.removeItemSignal.emit(self.ui.createdListWidget, self.container.name)

                # If the container is running
                elif self.container.status == 'running':
                    self.customSignals.printMessageSignal.emit(self.ui.promptBrowser, self.container.name + ' is running')

                # If the container is in other status
                else:
                    self.customSignals.printMessageSignal.emit(self.ui.promptBrowser, 'Illegal container status encountered')

        def writeTmpFile():
            content = '''{
    "websitePort": ''' + self.configs['websitePort'] + ''',
    "backendPort": ''' + self.configs['backendPort'] + ''',
    "tensorboardPort": ''' + self.configs['tensorboardPort'] + '''
}'''
            with open(os.path.abspath(tmp_file_path), 'w') as f:
                f.write(content)

        def createCpuContainer():
            writeTmpFile()
            self.container = self.client.containers.run(
                image,
                detach=True,
                name=self.configs['containerName'],
                ports={
                    '80/tcp': (
                        '127.0.0.1', int(self.configs['websitePort'])),
                    '8000/tcp': ('127.0.0.1', self.configs['backendPort']),
                    '6006/tcp': ('127.0.0.1', self.configs['tensorboardPort']),
                },
                environment={
                    'websitePort': self.configs['websitePort'],
                    'backendPort': self.configs['backendPort'],
                    'tensorboardPort': self.configs['tensorboardPort'],
                    'VUE_APP_BASE_URL': f"http://localhost:{self.configs['backendPort']}",
                },
                mounts=[
                    docker.types.Mount(target='/Robustar2/dataset/train',
                                       source=getSystemPath(self.configs['trainPath']),
                                       type='bind'),
                    docker.types.Mount(target='/Robustar2/dataset/test',
                                       source=getSystemPath(self.configs['testPath']),
                                       type='bind'),
                    docker.types.Mount(target='/Robustar2/influence_images',
                                       source=getSystemPath(self.configs['influencePath']),
                                       type='bind'),
                    docker.types.Mount(
                        target='/Robustar2/checkpoints',
                        source=getSystemPath(self.configs['checkPointPath']),
                        type='bind'),
                ],
                volumes=[
                    getSystemPath(self.configs['configFile']) + ':/Robustar2/configs.json',
                    os.path.abspath(tmp_file_path) + ':/var/www/html/serverUrls.json']
            )

        def createCudaContainer():
            writeTmpFile()
            self.container = self.client.containers.run(
                image,
                detach=True,
                name=self.configs['containerName'],
                ports={
                    '80/tcp': (
                        '127.0.0.1', int(self.configs['websitePort'])),
                    '8000/tcp': ('127.0.0.1', self.configs['backendPort']),
                    '6006/tcp': ('127.0.0.1', self.configs['tensorboardPort']),
                },
                environment={
                    'websitePort': self.configs['websitePort'],
                    'backendPort': self.configs['backendPort'],
                    'tensorboardPort': self.configs['tensorboardPort'],
                    'VUE_APP_BASE_URL': f"http://localhost:{self.configs['backendPort']}",
                },
                mounts=[
                    docker.types.Mount(target='/Robustar2/dataset/train',
                                       source=getSystemPath(self.configs['trainPath']),
                                       type='bind'),
                    docker.types.Mount(target='/Robustar2/dataset/test',
                                       source=getSystemPath(self.configs['testPath']),
                                       type='bind'),
                    docker.types.Mount(target='/Robustar2/influence_images',
                                       source=getSystemPath(self.configs['influencePath']),
                                       type='bind'),
                    docker.types.Mount(
                        target='/Robustar2/checkpoints',
                        source=getSystemPath(self.configs['checkPointPath']),
                        type='bind'),
                ],
                volumes=[
                    self.configs['configFile'] + ':/Robustar2/configs.json',
                    os.path.abspath(tmp_file_path) + ':/var/www/html/serverUrls.json'],

                # Set the device_requests parm
                device_requests=[
                    docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])
                ]
            )

            # hard core for now
            cont_flag = True
            while cont_flag:
                try:
                    sleep(10)
                    containerPostSteps()
                    cont_flag = False
                except:
                    pass

        startServerThread = Thread(target=startServerInThread)
        startServerThread.start()


    def stopServer(self):

        def stopServerInThread():

            try:
                self.customSignals.disableControlSignal.emit()

                self.getSelectedContainer()

                if(self.container != None):
                    # If the container has been stopped
                    if self.container.status == 'exited':
                        self.customSignals.printMessageSignal.emit(self.ui.promptBrowser, self.container.name + ' has already stopped')

                    # If the container has been created but not run
                    elif self.container.status == 'created':
                        self.customSignals.printMessageSignal.emit(self.ui.promptBrowser, self.container.name + ' is not running')

                    # If the container is running
                    # Stop the container
                    # Update both runningListWidget and exitedListWidget
                    elif self.container.status == 'running':
                        self.container.stop()
                        self.customSignals.printMessageSignal.emit(self.ui.promptBrowser, self.container.name + ' is now stopped')
                        self.customSignals.addItemSignal.emit(self.ui.exitedListWidget, self.container.name)
                        self.customSignals.removeItemSignal.emit(self.ui.runningListWidget, self.container.name)

                    # If the container is in other status
                    else:
                        self.customSignals.printMessageSignal.emit(self.ui.promptBrowser, 'Illegal container status encountered')

            except docker.errors.NotFound:

                self.customSignals.printMessageSignal.emit(self.ui.promptBrowser,
                                                               'Can not find ' + self.tempName + '. Refresh <i>Manage</i> page to check the latest information')

            except docker.errors.APIError as apiError:
                self.customSignals.printMessageSignal.emit(self.ui.promptBrowser, 'Unexpected error encountered. See more in <i>Details</i> page')
                self.customSignals.printMessageSignal.emit(self.ui.detailBrowser, str(apiError))

            finally:
                self.customSignals.enableControlSignal.emit()

        stopServerThread = Thread(target=stopServerInThread)
        stopServerThread.start()


    def deleteServer(self):
        try:
            self.customSignals.disableControlSignal.emit()

            self.getSelectedContainer()

            if(self.container != None):
                if (self.container.status == 'exited' or self.container.status == 'created'):
                    self.container.remove()
                    self.customSignals.printMessageSignal.emit(self.ui.promptBrowser, self.container.name + ' removed')

                    if (self.container.status == 'exited'):
                        self.customSignals.removeItemSignal.emit(self.ui.exitedListWidget, self.container.name)

                    else:
                        self.customSignals.removeItemSignal.emit(self.ui.createdListWidget, self.container.name)

                elif self.container.status == 'running':
                    self.customSignals.printMessageSignal.emit(self.ui.promptBrowser,
                        self.container.name + ' is still running. Stop ' + self.container.name + ' before deletion')

                # If the container is in other status
                else:
                    self.customSignals.printMessageSignal.emit(self.ui.promptBrowser, 'Illegal container status encountered')

        except docker.errors.NotFound:

            self.customSignals.printMessageSignal.emit(self.ui.promptBrowser,
                                                       'Can not find ' + self.tempName + '. Refresh <i>Manage</i> page to check the latest information')

        except docker.errors.APIError as apiError:
            self.customSignals.printMessageSignal.emit(self.ui.promptBrowser, 'Unexpected error encountered. See more in <i>Details</i> page')
            self.customSignals.printMessageSignal.emit(self.ui.detailBrowser, str(apiError))

        finally:
            self.customSignals.enableControlSignal.emit()


    def initContainerList(self):

        def initContainerInThread():
            # Clear all content in the listWidgets
            for listWidget in self.listWidgets:
                listWidget.clear()

            # Get all containers
            containerList = self.client.containers.list(all=True)

            for container in containerList:
                # Classify the containers using different versions of robustar as their images according to status
                if ('paulcccccch/robustar:' in str(container.image)):
                    if (container.status == 'running'):
                        self.customSignals.addItemSignal.emit(self.ui.runningListWidget, container.name)
                    elif (container.status == 'exited'):
                        self.customSignals.addItemSignal.emit(self.ui.exitedListWidget, container.name)
                    elif (container.status == 'created'):
                        self.customSignals.addItemSignal.emit(self.ui.createdListWidget, container.name)
                    else:
                        self.customSignals.printMessageSignal.emit(self.ui.promptBrowser, 'Illegal container status encountered')


        listContainerThread = Thread(target=initContainerInThread())
        listContainerThread.start()

    def printMessage(self, textBrowser, message):
        currentTime = time.strftime("%H:%M:%S", time.localtime())
        textBrowser.append(currentTime + ' -- ' + message + '\n')
        textBrowser.ensureCursorVisible()

    def addItem(self, listWidget, name):
        listWidget.addItem(name)

    def removeItem(self, listWidget, name):
        items = listWidget.findItems(name, Qt.MatchExactly)
        item = items[0]
        row = listWidget.row(item)
        listWidget.takeItem(row)

    def enableControl(self):
        self.ui.startServerButton.setEnabled(True)
        self.ui.stopServerButton.setEnabled(True)
        self.ui.deleteServerButton.setEnabled(True)

    def disableControl(self):
        self.ui.startServerButton.setEnabled(False)
        self.ui.stopServerButton.setEnabled(False)
        self.ui.deleteServerButton.setEnabled(False)


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


    # Function to get the container by its name
    # Could raise docker.errors.NotFound and docker.errors.APIError
    def getSelectedContainer(self):

        # If it's in createTab
        # Get the container with the input name
        if (self.ui.tabWidget.currentIndex() == 0):
            self.fromCreateTab = True
            self.tempName = self.configs['containerName']
            self.container = self.client.containers.get(self.configs['containerName'])

        # If it's in manageTab
        # Get the selected container
        else:
            self.fromCreateTab = False
            items = self.getItemsFromListWidgets()
            if (len(items) == 0):
                self.container = None
                self.customSignals.printMessageSignal.emit(self.ui.promptBrowser, 'Please select a container you want to stop')
            else:
                item = items[0]
                containerName = item.text()
                self.tempName = containerName
                self.container = self.client.containers.get(containerName)


    # Function to get the selected item list(actually only one item in the list) from listWidgets
    def getItemsFromListWidgets(self):
        return self.ui.runningListWidget.selectedItems() if len(
            self.ui.runningListWidget.selectedItems()) > 0 else self.ui.exitedListWidget.selectedItems() if len(
            self.ui.exitedListWidget.selectedItems()) > 0 else self.ui.createdListWidget.selectedItems() if len(
            self.ui.createdListWidget.selectedItems()) > 0 else []

app = QApplication([])
launcher = Launcher()

launcher.ui.setFixedSize(1000, 850)
launcher.ui.show()
launcher.initContainerList()
app.exec_()