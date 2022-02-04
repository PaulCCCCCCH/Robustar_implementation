import json
import subprocess

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog, QWidget

class Launcher(QWidget):
    def __init__(self):
        # Initialize the UI
        super(Launcher, self).__init__()
        self.ui = QUiLoader().load('launcher.ui')

        # Set the default path of the path choosing window
        self.cwd = '/'

        # Set the starting state of the server
        self.runningState = False

        # Set the default configuration
        self.configs = {
                        'containerName': 'robustar',
                        'imageVersion': 'cuda11.1-0.0.1-beta',
                        'portNumber': '8000',
                        'trainPath': '/Robustar2/dataset/train',
                        'validationPath': '/Robustar2/dataset/validation',
                        'testPath': '/Robustar2/dataset/test',
                        'checkPointPath': '/Robustar2/checkpoint_images',
                        'influencePath': '/Robustar2/influence_images',
                        'configFile': 'configs.json'
                        }
        self.loadPath = ''
        self.savePath = ''

        # Match the corresponding signals and slots
        self.ui.nameInput.textEdited.connect(self.changeContainerName)
        self.ui.versionComboBox.currentIndexChanged.connect(self.changeImageVersion)
        self.ui.trainPathButton.clicked.connect(self.chooseTrainPath)
        self.ui.validationPathButton.clicked.connect(self.chooseValidationPath)
        self.ui.testPathButton.clicked.connect(self.chooseTestPath)
        self.ui.checkPointPathButton.clicked.connect(self.chooseCheckPointPath)
        self.ui.influencePathButton.clicked.connect(self.chooseInfluencePath)
        self.ui.loadConfigButton.clicked.connect(self.loadConfig)
        self.ui.saveConfigButton.clicked.connect(self.saveConfig)
        self.ui.serverControlButton.clicked.connect(self.controlServer)

        # Set the default command to execute in shell
        self.command = ''


    def changeContainerName(self):
        self.configs['containerName'] = self.ui.nameInput.text()

    def changeImageVersion(self):
        self.configs['imageVersion'] = self.ui.versionComboBox.currentText()

    def changePortNumber(self):
        self.configs['portNumber'] = self.ui.portInput.text()

    def chooseTrainPath(self):
        self.configs['trainPath'] = QFileDialog.getExistingDirectory(self, "Choose Train Set Path", self.cwd)
        self.ui.trainPathDisplay.setText(self.configs['trainPath'])
        
    def chooseValidationPath(self):
        self.configs['validationPath'] = QFileDialog.getExistingDirectory(self, "Choose Validation Set Path", self.cwd)
        self.ui.validationPathDisplay.setText(self.configs['validationPath'])

    def chooseTestPath(self):
        self.configs['testPath'] = QFileDialog.getExistingDirectory(self, "Choose Test Set Path", self.cwd)
        self.ui.testPathDisplay.setText(self.configs['testPath'])

    def chooseCheckPointPath(self):
        self.configs['checkPointPath'] = QFileDialog.getExistingDirectory(self, "Choose Check Points Path", self.cwd)
        self.ui.checkPointPathDisplay.setText(self.configs['checkPointPath'])

    def chooseInfluencePath(self):
        self.configs['influencePath'] = QFileDialog.getExistingDirectory(self, "Choose Influence Result Path", self.cwd)
        self.ui.influencePathDisplay.setText(self.configs['influencePath'])

    def loadConfig(self):
        self.loadPath, _ = QFileDialog.getOpenFileName(self, "Load Configs", self.cwd, "JSON Files (*.json);;All Files (*)")
        try:
            with open(self.loadPath, 'r') as f:
                self.configs = json.load(f)

                # Update the UI according to the loaded file
                self.ui.nameInput.setText(self.configs['containerName'])
                self.ui.versionComboBox.setCurrentText(self.configs['imageVersion'])
                self.ui.portInput.setText(self.configs['portNumber'])
                self.ui.trainPathDisplay.setText(self.configs['trainPath'])
                self.ui.validationPathDisplay.setText(self.configs['validationPath'])
                self.ui.testPathDisplay.setText(self.configs['testPath'])
                self.ui.checkPointPathDisplay.setText(self.configs['checkPointPath'])
                self.ui.influencePathDisplay.setText(self.configs['influencePath'])

        except FileNotFoundError:
            print('Load path not found')

    def saveConfig(self):
        self.savePath, _ = QFileDialog.getOpenFileName(self, "Save Configs", self.cwd, "JSON Files (*.json);;All Files (*)")
        try:
            with open(self.savePath, 'w') as f:
                json.dump(self.configs, f)
        except FileNotFoundError:
            print('Save path not found')

    def controlServer(self):
        # setupCommand = 'docker pull paulcccccch/robustar:' + self.configs['imageVersion']
        # self.runShellCommand(setupCommand)

        if self.runningState == False:
            runCommand = self.getRunCommand()
            runReturnCode = self.runShellCommand(runCommand)
            if runReturnCode == 0:
                self.runningState = True
                self.ui.serverControlButton.setText('Stop Server')
                self.ui.messageBrowser.append('Robustar is available at http://localhost:' + self.configs['portNumber'])
                self.ui.messageBrowser.moveCursor(self.ui.messageBrowser.textCursor().End)
                QApplication.processEvents()
        else:
            stopCommand = 'docker stop ' + self.configs['containerName']
            self.runShellCommand(stopCommand)
            self.runningState = False
            self.ui.serverControlButton.setText('Start Server')


    # Concatenate the command to be executed
    def getRunCommand(self):
        runCommand = 'docker run --name ' + self.configs['containerName'] + ' -it -d ' +\
                       '-p 127.0.0.1:' + self.configs['portNumber'] + ':80 ' +\
                       '-p 127.0.0.1:6848:8000 ' +\
                       '-p 127.0.0.1:6006:6006 ' +\
                       '--mount type=bind,source=' + self.configs['trainPath'] + ',target=/Robustar2/dataset/train ' +\
                       '--mount type=bind,source=' + self.configs['testPath'] + ',target=/Robustar2/dataset/test ' +\
                       '--mount type=bind,source=' + self.configs['influencePath'] + ',target=/Robustar2/influence_images ' +\
                       '--mount type=bind,source=' + self.configs['checkPointPath'] + ',target=/Robustar2/checkpoint_images ' +\
                       '-v ' + self.configs['configFile'] + ':/Robustar2/configs.json ' +\
                       'paulcccccch/robustar:' + self.configs['imageVersion']

        return runCommand

    # Run a shell command and update UI according to it
    def runShellCommand(self, command):
        process = subprocess.Popen([r'C:/Program Files/Git/bin/bash.exe', "-c", command],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)

        while True:
            output = process.stdout.readline()
            error = process.stderr.readline()
            if (len(output) != 0):
                print(output.strip())
                self.ui.messageBrowser.append(output.strip())
                self.ui.messageBrowser.moveCursor(self.ui.messageBrowser.textCursor().End)
                QApplication.processEvents()
            if (len(error) != 0):
                print(error.strip())
                self.ui.messageBrowser.append(error.strip())
                self.ui.messageBrowser.moveCursor(self.ui.messageBrowser.textCursor().End)
                QApplication.processEvents()

            # Check if the process has finished
            return_code = process.poll()
            if return_code is not None:
                # print('RETURN CODE', return_code)
                # self.ui.messageBrowser.append('RETURN CODE ' + str(return_code))
                # self.ui.messageBrowser.moveCursor(self.ui.messageBrowser.textCursor().End)
                # QApplication.processEvents()

                # Process has finished, read rest of the output
                for output in process.stdout.readlines():
                    if (len(output) != 0):
                        print(output.strip())
                        self.ui.messageBrowser.append(output.strip())
                        self.ui.messageBrowser.moveCursor(self.ui.messageBrowser.textCursor().End)
                        QApplication.processEvents()
                break

        self.ui.messageBrowser.append('\n')
        self.ui.messageBrowser.moveCursor(self.ui.messageBrowser.textCursor().End)
        QApplication.processEvents()

        return return_code


app = QApplication([])
launcher = Launcher()

launcher.ui.setFixedSize(800, 680)
launcher.ui.show()
app.exec_()