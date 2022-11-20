# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'launcher_v2.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resource_rc

class Ui_RobustarLauncher(object):
    def setupUi(self, RobustarLauncher):
        if not RobustarLauncher.objectName():
            RobustarLauncher.setObjectName(u"RobustarLauncher")
        RobustarLauncher.resize(1000, 1020)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RobustarLauncher.sizePolicy().hasHeightForWidth())
        RobustarLauncher.setSizePolicy(sizePolicy)
        RobustarLauncher.setMinimumSize(QSize(1000, 1020))
        RobustarLauncher.setMaximumSize(QSize(1000, 1020))
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        RobustarLauncher.setFont(font)
        icon = QIcon()
        icon.addFile(u":/resources/logo_short.png", QSize(), QIcon.Normal, QIcon.Off)
        RobustarLauncher.setWindowIcon(icon)
        RobustarLauncher.setStyleSheet(u"QWidget{font: 8pt \"Arial\"}\n"
"QPushButton{background-color: #E1E1E1; \n"
"			font: 8pt Arial;\n"
"			border: 1px solid #ADADAD;}\n"
"QPushButton:hover {\n"
"   background-color: #E3ECF3;\n"
"   border: 1px solid #3287CA;\n"
"}")
        self.layoutWidget = QWidget(RobustarLauncher)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 1001, 1001))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.headerLayout = QHBoxLayout()
        self.headerLayout.setObjectName(u"headerLayout")
        self.header = QLabel(self.layoutWidget)
        self.header.setObjectName(u"header")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy1)
        self.header.setMinimumSize(QSize(164, 42))
        self.header.setMaximumSize(QSize(164, 42))
        self.header.setTextFormat(Qt.AutoText)
        self.header.setPixmap(QPixmap(u":/resources/logo_long.png"))
        self.header.setScaledContents(True)
        self.header.setIndent(-1)

        self.headerLayout.addWidget(self.header)


        self.verticalLayout.addLayout(self.headerLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(15, -1, 11, -1)
        self.buttonFrame = QFrame(self.layoutWidget)
        self.buttonFrame.setObjectName(u"buttonFrame")
        sizePolicy1.setHeightForWidth(self.buttonFrame.sizePolicy().hasHeightForWidth())
        self.buttonFrame.setSizePolicy(sizePolicy1)
        self.buttonFrame.setMinimumSize(QSize(161, 905))
        self.buttonFrame.setMaximumSize(QSize(161, 905))
        self.buttonFrame.setFont(font)
        self.buttonFrame.setStyleSheet(u"#buttonFrame{background: #F9F9F9}\n"
"")
        self.buttonFrame.setFrameShape(QFrame.StyledPanel)
        self.buttonFrame.setFrameShadow(QFrame.Raised)
        self.layoutWidget1 = QWidget(self.buttonFrame)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(0, 0, 161, 901))
        self.buttonLayout = QVBoxLayout(self.layoutWidget1)
        self.buttonLayout.setSpacing(60)
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.buttonLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.buttonLayout.setContentsMargins(0, 60, 0, 0)
        self.loadButtonLayout = QHBoxLayout()
        self.loadButtonLayout.setObjectName(u"loadButtonLayout")
        self.loadButtonLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.loadButtonLayout.addItem(self.horizontalSpacer_9)

        self.loadProfileButton = QPushButton(self.layoutWidget1)
        self.loadProfileButton.setObjectName(u"loadProfileButton")
        sizePolicy1.setHeightForWidth(self.loadProfileButton.sizePolicy().hasHeightForWidth())
        self.loadProfileButton.setSizePolicy(sizePolicy1)
        self.loadProfileButton.setMinimumSize(QSize(100, 25))
        self.loadProfileButton.setMaximumSize(QSize(100, 25))
        self.loadProfileButton.setFont(font)
        self.loadProfileButton.setStyleSheet(u"")

        self.loadButtonLayout.addWidget(self.loadProfileButton)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.loadButtonLayout.addItem(self.horizontalSpacer_10)


        self.buttonLayout.addLayout(self.loadButtonLayout)

        self.saveButtonLayout = QHBoxLayout()
        self.saveButtonLayout.setObjectName(u"saveButtonLayout")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.saveButtonLayout.addItem(self.horizontalSpacer_7)

        self.saveProfileButton = QPushButton(self.layoutWidget1)
        self.saveProfileButton.setObjectName(u"saveProfileButton")
        sizePolicy1.setHeightForWidth(self.saveProfileButton.sizePolicy().hasHeightForWidth())
        self.saveProfileButton.setSizePolicy(sizePolicy1)
        self.saveProfileButton.setMinimumSize(QSize(100, 25))
        self.saveProfileButton.setMaximumSize(QSize(100, 25))
        self.saveProfileButton.setFont(font)

        self.saveButtonLayout.addWidget(self.saveProfileButton)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.saveButtonLayout.addItem(self.horizontalSpacer_8)


        self.buttonLayout.addLayout(self.saveButtonLayout)

        self.startButtonLayout = QHBoxLayout()
        self.startButtonLayout.setObjectName(u"startButtonLayout")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.startButtonLayout.addItem(self.horizontalSpacer_5)

        self.startServerButton = QPushButton(self.layoutWidget1)
        self.startServerButton.setObjectName(u"startServerButton")
        sizePolicy1.setHeightForWidth(self.startServerButton.sizePolicy().hasHeightForWidth())
        self.startServerButton.setSizePolicy(sizePolicy1)
        self.startServerButton.setMinimumSize(QSize(100, 25))
        self.startServerButton.setMaximumSize(QSize(100, 25))
        self.startServerButton.setFont(font)
        self.startServerButton.setLayoutDirection(Qt.LeftToRight)

        self.startButtonLayout.addWidget(self.startServerButton)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.startButtonLayout.addItem(self.horizontalSpacer_6)


        self.buttonLayout.addLayout(self.startButtonLayout)

        self.stopButtoLayout = QHBoxLayout()
        self.stopButtoLayout.setObjectName(u"stopButtoLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.stopButtoLayout.addItem(self.horizontalSpacer_3)

        self.stopServerButton = QPushButton(self.layoutWidget1)
        self.stopServerButton.setObjectName(u"stopServerButton")
        sizePolicy1.setHeightForWidth(self.stopServerButton.sizePolicy().hasHeightForWidth())
        self.stopServerButton.setSizePolicy(sizePolicy1)
        self.stopServerButton.setMinimumSize(QSize(100, 25))
        self.stopServerButton.setMaximumSize(QSize(100, 25))
        self.stopServerButton.setFont(font)

        self.stopButtoLayout.addWidget(self.stopServerButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.stopButtoLayout.addItem(self.horizontalSpacer_4)


        self.buttonLayout.addLayout(self.stopButtoLayout)

        self.deleteButtonLayout = QHBoxLayout()
        self.deleteButtonLayout.setObjectName(u"deleteButtonLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.deleteButtonLayout.addItem(self.horizontalSpacer)

        self.deleteServerButton = QPushButton(self.layoutWidget1)
        self.deleteServerButton.setObjectName(u"deleteServerButton")
        sizePolicy1.setHeightForWidth(self.deleteServerButton.sizePolicy().hasHeightForWidth())
        self.deleteServerButton.setSizePolicy(sizePolicy1)
        self.deleteServerButton.setMinimumSize(QSize(100, 25))
        self.deleteServerButton.setMaximumSize(QSize(100, 25))
        self.deleteServerButton.setFont(font)

        self.deleteButtonLayout.addWidget(self.deleteServerButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.deleteButtonLayout.addItem(self.horizontalSpacer_2)


        self.buttonLayout.addLayout(self.deleteButtonLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.buttonLayout.addItem(self.verticalSpacer_2)

        self.buttonLayout.setStretch(0, 1)
        self.buttonLayout.setStretch(1, 1)
        self.buttonLayout.setStretch(2, 1)
        self.buttonLayout.setStretch(3, 1)
        self.buttonLayout.setStretch(4, 1)
        self.buttonLayout.setStretch(5, 2)

        self.horizontalLayout_2.addWidget(self.buttonFrame)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.tabWidget = QTabWidget(self.layoutWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy1.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy1)
        self.tabWidget.setMinimumSize(QSize(801, 575))
        self.tabWidget.setMaximumSize(QSize(801, 575))
        self.tabWidget.setFont(font)
        self.createTab = QWidget()
        self.createTab.setObjectName(u"createTab")
        self.horizontalLayoutWidget_7 = QWidget(self.createTab)
        self.horizontalLayoutWidget_7.setObjectName(u"horizontalLayoutWidget_7")
        self.horizontalLayoutWidget_7.setGeometry(QRect(20, 10, 761, 531))
        self.horizontalLayout_6 = QHBoxLayout(self.horizontalLayoutWidget_7)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(9)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.dockerGroupBox = QGroupBox(self.horizontalLayoutWidget_7)
        self.dockerGroupBox.setObjectName(u"dockerGroupBox")
        sizePolicy.setHeightForWidth(self.dockerGroupBox.sizePolicy().hasHeightForWidth())
        self.dockerGroupBox.setSizePolicy(sizePolicy)
        self.dockerGroupBox.setMinimumSize(QSize(0, 169))
        self.dockerGroupBox.setMaximumSize(QSize(16777215, 168))
        self.dockerGroupBox.setFont(font)
        self.layoutWidget2 = QWidget(self.dockerGroupBox)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 20, 362, 143))
        self.verticalLayout_6 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_8 = QLabel(self.layoutWidget2)
        self.label_8.setObjectName(u"label_8")
        sizePolicy1.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy1)
        self.label_8.setMinimumSize(QSize(174, 39))
        self.label_8.setMaximumSize(QSize(174, 39))
        self.label_8.setFont(font)

        self.horizontalLayout_8.addWidget(self.label_8)

        self.nameInput = QLineEdit(self.layoutWidget2)
        self.nameInput.setObjectName(u"nameInput")
        sizePolicy1.setHeightForWidth(self.nameInput.sizePolicy().hasHeightForWidth())
        self.nameInput.setSizePolicy(sizePolicy1)
        self.nameInput.setMinimumSize(QSize(174, 24))
        self.nameInput.setMaximumSize(QSize(174, 24))
        self.nameInput.setFont(font)
        self.nameInput.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.nameInput.setClearButtonEnabled(True)

        self.horizontalLayout_8.addWidget(self.nameInput)


        self.verticalLayout_6.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.layoutWidget2)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setMinimumSize(QSize(174, 39))
        self.label_3.setMaximumSize(QSize(174, 39))
        self.label_3.setFont(font)

        self.horizontalLayout_5.addWidget(self.label_3)

        self.versionComboBox = QComboBox(self.layoutWidget2)
        self.versionComboBox.setObjectName(u"versionComboBox")
        sizePolicy1.setHeightForWidth(self.versionComboBox.sizePolicy().hasHeightForWidth())
        self.versionComboBox.setSizePolicy(sizePolicy1)
        self.versionComboBox.setMinimumSize(QSize(174, 24))
        self.versionComboBox.setMaximumSize(QSize(174, 24))
        self.versionComboBox.setFont(font)

        self.horizontalLayout_5.addWidget(self.versionComboBox)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_7 = QLabel(self.layoutWidget2)
        self.label_7.setObjectName(u"label_7")
        sizePolicy1.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy1)
        self.label_7.setMinimumSize(QSize(174, 39))
        self.label_7.setMaximumSize(QSize(174, 39))
        self.label_7.setFont(font)

        self.horizontalLayout_9.addWidget(self.label_7)

        self.portInput = QLineEdit(self.layoutWidget2)
        self.portInput.setObjectName(u"portInput")
        sizePolicy1.setHeightForWidth(self.portInput.sizePolicy().hasHeightForWidth())
        self.portInput.setSizePolicy(sizePolicy1)
        self.portInput.setMinimumSize(QSize(174, 24))
        self.portInput.setMaximumSize(QSize(174, 24))
        self.portInput.setFont(font)
        self.portInput.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.portInput.setClearButtonEnabled(True)

        self.horizontalLayout_9.addWidget(self.portInput)


        self.verticalLayout_6.addLayout(self.horizontalLayout_9)


        self.verticalLayout_3.addWidget(self.dockerGroupBox)

        self.verticalSpacer = QSpacerItem(20, 132, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.dataGroupBox = QGroupBox(self.horizontalLayoutWidget_7)
        self.dataGroupBox.setObjectName(u"dataGroupBox")
        self.dataGroupBox.setMinimumSize(QSize(0, 0))
        self.dataGroupBox.setMaximumSize(QSize(16777215, 232))
        self.dataGroupBox.setFont(font)
        self.layoutWidget3 = QWidget(self.dataGroupBox)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(10, 20, 361, 193))
        self.verticalLayout_7 = QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_7.setSpacing(9)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, -1, -1, -1)
        self.label_6 = QLabel(self.layoutWidget3)
        self.label_6.setObjectName(u"label_6")
        sizePolicy1.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy1)
        self.label_6.setMinimumSize(QSize(174, 39))
        self.label_6.setMaximumSize(QSize(174, 39))
        self.label_6.setFont(font)

        self.horizontalLayout_16.addWidget(self.label_6)

        self.trainPathDisplay = QLineEdit(self.layoutWidget3)
        self.trainPathDisplay.setObjectName(u"trainPathDisplay")
        sizePolicy1.setHeightForWidth(self.trainPathDisplay.sizePolicy().hasHeightForWidth())
        self.trainPathDisplay.setSizePolicy(sizePolicy1)
        self.trainPathDisplay.setMinimumSize(QSize(137, 24))
        self.trainPathDisplay.setMaximumSize(QSize(137, 24))
        self.trainPathDisplay.setFont(font)
        self.trainPathDisplay.setMouseTracking(True)
        self.trainPathDisplay.setReadOnly(False)

        self.horizontalLayout_16.addWidget(self.trainPathDisplay)

        self.trainPathButton = QPushButton(self.layoutWidget3)
        self.trainPathButton.setObjectName(u"trainPathButton")
        sizePolicy1.setHeightForWidth(self.trainPathButton.sizePolicy().hasHeightForWidth())
        self.trainPathButton.setSizePolicy(sizePolicy1)
        self.trainPathButton.setMinimumSize(QSize(28, 20))
        self.trainPathButton.setMaximumSize(QSize(28, 20))
        self.trainPathButton.setFont(font)

        self.horizontalLayout_16.addWidget(self.trainPathButton)


        self.verticalLayout_7.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(-1, -1, 0, -1)
        self.label_13 = QLabel(self.layoutWidget3)
        self.label_13.setObjectName(u"label_13")
        sizePolicy1.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy1)
        self.label_13.setMinimumSize(QSize(174, 39))
        self.label_13.setMaximumSize(QSize(174, 39))
        self.label_13.setFont(font)

        self.horizontalLayout_17.addWidget(self.label_13)

        self.testPathDisplay = QLineEdit(self.layoutWidget3)
        self.testPathDisplay.setObjectName(u"testPathDisplay")
        sizePolicy1.setHeightForWidth(self.testPathDisplay.sizePolicy().hasHeightForWidth())
        self.testPathDisplay.setSizePolicy(sizePolicy1)
        self.testPathDisplay.setMinimumSize(QSize(137, 24))
        self.testPathDisplay.setMaximumSize(QSize(137, 24))
        self.testPathDisplay.setFont(font)

        self.horizontalLayout_17.addWidget(self.testPathDisplay)

        self.testPathButton = QPushButton(self.layoutWidget3)
        self.testPathButton.setObjectName(u"testPathButton")
        sizePolicy1.setHeightForWidth(self.testPathButton.sizePolicy().hasHeightForWidth())
        self.testPathButton.setSizePolicy(sizePolicy1)
        self.testPathButton.setMinimumSize(QSize(28, 20))
        self.testPathButton.setMaximumSize(QSize(28, 20))
        self.testPathButton.setFont(font)

        self.horizontalLayout_17.addWidget(self.testPathButton)


        self.verticalLayout_7.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_14 = QLabel(self.layoutWidget3)
        self.label_14.setObjectName(u"label_14")
        sizePolicy1.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy1)
        self.label_14.setMinimumSize(QSize(174, 39))
        self.label_14.setMaximumSize(QSize(174, 39))
        self.label_14.setFont(font)

        self.horizontalLayout_18.addWidget(self.label_14)

        self.checkPointPathDisplay = QLineEdit(self.layoutWidget3)
        self.checkPointPathDisplay.setObjectName(u"checkPointPathDisplay")
        sizePolicy1.setHeightForWidth(self.checkPointPathDisplay.sizePolicy().hasHeightForWidth())
        self.checkPointPathDisplay.setSizePolicy(sizePolicy1)
        self.checkPointPathDisplay.setMinimumSize(QSize(137, 24))
        self.checkPointPathDisplay.setMaximumSize(QSize(137, 24))
        self.checkPointPathDisplay.setFont(font)

        self.horizontalLayout_18.addWidget(self.checkPointPathDisplay)

        self.checkPointPathButton = QPushButton(self.layoutWidget3)
        self.checkPointPathButton.setObjectName(u"checkPointPathButton")
        sizePolicy1.setHeightForWidth(self.checkPointPathButton.sizePolicy().hasHeightForWidth())
        self.checkPointPathButton.setSizePolicy(sizePolicy1)
        self.checkPointPathButton.setMinimumSize(QSize(28, 20))
        self.checkPointPathButton.setMaximumSize(QSize(28, 20))
        self.checkPointPathButton.setFont(font)

        self.horizontalLayout_18.addWidget(self.checkPointPathButton)


        self.verticalLayout_7.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_15 = QLabel(self.layoutWidget3)
        self.label_15.setObjectName(u"label_15")
        sizePolicy1.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy1)
        self.label_15.setMinimumSize(QSize(174, 39))
        self.label_15.setMaximumSize(QSize(174, 39))
        self.label_15.setFont(font)

        self.horizontalLayout_19.addWidget(self.label_15)

        self.influencePathDisplay = QLineEdit(self.layoutWidget3)
        self.influencePathDisplay.setObjectName(u"influencePathDisplay")
        sizePolicy1.setHeightForWidth(self.influencePathDisplay.sizePolicy().hasHeightForWidth())
        self.influencePathDisplay.setSizePolicy(sizePolicy1)
        self.influencePathDisplay.setMinimumSize(QSize(137, 24))
        self.influencePathDisplay.setMaximumSize(QSize(137, 24))
        self.influencePathDisplay.setFont(font)

        self.horizontalLayout_19.addWidget(self.influencePathDisplay)

        self.influencePathButton = QPushButton(self.layoutWidget3)
        self.influencePathButton.setObjectName(u"influencePathButton")
        sizePolicy1.setHeightForWidth(self.influencePathButton.sizePolicy().hasHeightForWidth())
        self.influencePathButton.setSizePolicy(sizePolicy1)
        self.influencePathButton.setMinimumSize(QSize(28, 20))
        self.influencePathButton.setMaximumSize(QSize(28, 20))
        self.influencePathButton.setFont(font)

        self.horizontalLayout_19.addWidget(self.influencePathButton)


        self.verticalLayout_7.addLayout(self.horizontalLayout_19)


        self.verticalLayout_3.addWidget(self.dataGroupBox)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.dockerGroupBox_2 = QGroupBox(self.horizontalLayoutWidget_7)
        self.dockerGroupBox_2.setObjectName(u"dockerGroupBox_2")
        sizePolicy1.setHeightForWidth(self.dockerGroupBox_2.sizePolicy().hasHeightForWidth())
        self.dockerGroupBox_2.setSizePolicy(sizePolicy1)
        self.dockerGroupBox_2.setMinimumSize(QSize(372, 525))
        self.dockerGroupBox_2.setMaximumSize(QSize(372, 525))
        self.dockerGroupBox_2.setFont(font)
        self.layoutWidget_2 = QWidget(self.dockerGroupBox_2)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(10, 20, 362, 493))
        self.verticalLayout_9 = QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_4 = QLabel(self.layoutWidget_2)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setMinimumSize(QSize(174, 39))
        self.label_4.setMaximumSize(QSize(174, 39))
        self.label_4.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_4)

        self.archComboBox = QComboBox(self.layoutWidget_2)
        self.archComboBox.addItem("")
        self.archComboBox.addItem("")
        self.archComboBox.addItem("")
        self.archComboBox.addItem("")
        self.archComboBox.addItem("")
        self.archComboBox.addItem("")
        self.archComboBox.addItem("")
        self.archComboBox.addItem("")
        self.archComboBox.setObjectName(u"archComboBox")
        sizePolicy1.setHeightForWidth(self.archComboBox.sizePolicy().hasHeightForWidth())
        self.archComboBox.setSizePolicy(sizePolicy1)
        self.archComboBox.setMinimumSize(QSize(174, 24))
        self.archComboBox.setMaximumSize(QSize(174, 24))
        self.archComboBox.setFont(font)

        self.horizontalLayout_7.addWidget(self.archComboBox)


        self.verticalLayout_9.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_9 = QLabel(self.layoutWidget_2)
        self.label_9.setObjectName(u"label_9")
        sizePolicy1.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy1)
        self.label_9.setMinimumSize(QSize(174, 39))
        self.label_9.setMaximumSize(QSize(174, 39))
        self.label_9.setFont(font)

        self.horizontalLayout_4.addWidget(self.label_9)

        self.pretrainedCheckBox = QCheckBox(self.layoutWidget_2)
        self.pretrainedCheckBox.setObjectName(u"pretrainedCheckBox")
        sizePolicy1.setHeightForWidth(self.pretrainedCheckBox.sizePolicy().hasHeightForWidth())
        self.pretrainedCheckBox.setSizePolicy(sizePolicy1)
        self.pretrainedCheckBox.setMinimumSize(QSize(174, 24))
        self.pretrainedCheckBox.setMaximumSize(QSize(174, 24))

        self.horizontalLayout_4.addWidget(self.pretrainedCheckBox)


        self.verticalLayout_9.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_16 = QLabel(self.layoutWidget_2)
        self.label_16.setObjectName(u"label_16")
        sizePolicy1.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy1)
        self.label_16.setMinimumSize(QSize(174, 39))
        self.label_16.setMaximumSize(QSize(174, 39))
        self.label_16.setFont(font)

        self.horizontalLayout_14.addWidget(self.label_16)

        self.weightFileComboBox = QComboBox(self.layoutWidget_2)
        self.weightFileComboBox.addItem("")
        self.weightFileComboBox.setObjectName(u"weightFileComboBox")
        sizePolicy1.setHeightForWidth(self.weightFileComboBox.sizePolicy().hasHeightForWidth())
        self.weightFileComboBox.setSizePolicy(sizePolicy1)
        self.weightFileComboBox.setMinimumSize(QSize(174, 24))
        self.weightFileComboBox.setMaximumSize(QSize(174, 24))
        self.weightFileComboBox.setFont(font)

        self.horizontalLayout_14.addWidget(self.weightFileComboBox)


        self.verticalLayout_9.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.label_19 = QLabel(self.layoutWidget_2)
        self.label_19.setObjectName(u"label_19")
        sizePolicy1.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy1)
        self.label_19.setMinimumSize(QSize(174, 39))
        self.label_19.setMaximumSize(QSize(174, 39))
        self.label_19.setFont(font)

        self.horizontalLayout_21.addWidget(self.label_19)

        self.deviceInput = QLineEdit(self.layoutWidget_2)
        self.deviceInput.setObjectName(u"deviceInput")
        sizePolicy1.setHeightForWidth(self.deviceInput.sizePolicy().hasHeightForWidth())
        self.deviceInput.setSizePolicy(sizePolicy1)
        self.deviceInput.setMinimumSize(QSize(174, 24))
        self.deviceInput.setMaximumSize(QSize(174, 24))
        self.deviceInput.setFont(font)
        self.deviceInput.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.deviceInput.setClearButtonEnabled(True)

        self.horizontalLayout_21.addWidget(self.deviceInput)


        self.verticalLayout_9.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.label_20 = QLabel(self.layoutWidget_2)
        self.label_20.setObjectName(u"label_20")
        sizePolicy1.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy1)
        self.label_20.setMinimumSize(QSize(174, 39))
        self.label_20.setMaximumSize(QSize(174, 39))
        self.label_20.setFont(font)

        self.horizontalLayout_23.addWidget(self.label_20)

        self.shuffleCheckBox = QCheckBox(self.layoutWidget_2)
        self.shuffleCheckBox.setObjectName(u"shuffleCheckBox")
        sizePolicy1.setHeightForWidth(self.shuffleCheckBox.sizePolicy().hasHeightForWidth())
        self.shuffleCheckBox.setSizePolicy(sizePolicy1)
        self.shuffleCheckBox.setMinimumSize(QSize(174, 24))
        self.shuffleCheckBox.setMaximumSize(QSize(174, 24))

        self.horizontalLayout_23.addWidget(self.shuffleCheckBox)


        self.verticalLayout_9.addLayout(self.horizontalLayout_23)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_21 = QLabel(self.layoutWidget_2)
        self.label_21.setObjectName(u"label_21")
        sizePolicy1.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy1)
        self.label_21.setMinimumSize(QSize(174, 39))
        self.label_21.setMaximumSize(QSize(174, 39))
        self.label_21.setFont(font)

        self.horizontalLayout_24.addWidget(self.label_21)

        self.batchSizeInput = QLineEdit(self.layoutWidget_2)
        self.batchSizeInput.setObjectName(u"batchSizeInput")
        sizePolicy1.setHeightForWidth(self.batchSizeInput.sizePolicy().hasHeightForWidth())
        self.batchSizeInput.setSizePolicy(sizePolicy1)
        self.batchSizeInput.setMinimumSize(QSize(174, 24))
        self.batchSizeInput.setMaximumSize(QSize(174, 24))
        self.batchSizeInput.setFont(font)
        self.batchSizeInput.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.batchSizeInput.setClearButtonEnabled(True)

        self.horizontalLayout_24.addWidget(self.batchSizeInput)


        self.verticalLayout_9.addLayout(self.horizontalLayout_24)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.label_22 = QLabel(self.layoutWidget_2)
        self.label_22.setObjectName(u"label_22")
        sizePolicy1.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy1)
        self.label_22.setMinimumSize(QSize(174, 39))
        self.label_22.setMaximumSize(QSize(174, 39))
        self.label_22.setFont(font)

        self.horizontalLayout_25.addWidget(self.label_22)

        self.workerNumberInput = QLineEdit(self.layoutWidget_2)
        self.workerNumberInput.setObjectName(u"workerNumberInput")
        sizePolicy1.setHeightForWidth(self.workerNumberInput.sizePolicy().hasHeightForWidth())
        self.workerNumberInput.setSizePolicy(sizePolicy1)
        self.workerNumberInput.setMinimumSize(QSize(174, 24))
        self.workerNumberInput.setMaximumSize(QSize(174, 24))
        self.workerNumberInput.setFont(font)
        self.workerNumberInput.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.workerNumberInput.setClearButtonEnabled(True)

        self.horizontalLayout_25.addWidget(self.workerNumberInput)


        self.verticalLayout_9.addLayout(self.horizontalLayout_25)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.label_25 = QLabel(self.layoutWidget_2)
        self.label_25.setObjectName(u"label_25")
        sizePolicy1.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy1)
        self.label_25.setMinimumSize(QSize(174, 39))
        self.label_25.setMaximumSize(QSize(174, 39))
        self.label_25.setFont(font)

        self.horizontalLayout_28.addWidget(self.label_25)

        self.classNumberInput = QLineEdit(self.layoutWidget_2)
        self.classNumberInput.setObjectName(u"classNumberInput")
        sizePolicy1.setHeightForWidth(self.classNumberInput.sizePolicy().hasHeightForWidth())
        self.classNumberInput.setSizePolicy(sizePolicy1)
        self.classNumberInput.setMinimumSize(QSize(174, 24))
        self.classNumberInput.setMaximumSize(QSize(174, 24))
        self.classNumberInput.setFont(font)
        self.classNumberInput.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.classNumberInput.setClearButtonEnabled(True)

        self.horizontalLayout_28.addWidget(self.classNumberInput)


        self.verticalLayout_9.addLayout(self.horizontalLayout_28)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.label_23 = QLabel(self.layoutWidget_2)
        self.label_23.setObjectName(u"label_23")
        sizePolicy1.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy1)
        self.label_23.setMinimumSize(QSize(174, 39))
        self.label_23.setMaximumSize(QSize(174, 39))
        self.label_23.setFont(font)

        self.horizontalLayout_26.addWidget(self.label_23)

        self.imgSizeInput = QLineEdit(self.layoutWidget_2)
        self.imgSizeInput.setObjectName(u"imgSizeInput")
        sizePolicy1.setHeightForWidth(self.imgSizeInput.sizePolicy().hasHeightForWidth())
        self.imgSizeInput.setSizePolicy(sizePolicy1)
        self.imgSizeInput.setMinimumSize(QSize(174, 24))
        self.imgSizeInput.setMaximumSize(QSize(174, 24))
        self.imgSizeInput.setFont(font)
        self.imgSizeInput.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.imgSizeInput.setClearButtonEnabled(True)

        self.horizontalLayout_26.addWidget(self.imgSizeInput)


        self.verticalLayout_9.addLayout(self.horizontalLayout_26)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.label_24 = QLabel(self.layoutWidget_2)
        self.label_24.setObjectName(u"label_24")
        sizePolicy1.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy1)
        self.label_24.setMinimumSize(QSize(174, 39))
        self.label_24.setMaximumSize(QSize(174, 39))
        self.label_24.setFont(font)

        self.horizontalLayout_27.addWidget(self.label_24)

        self.paddingComboBox = QComboBox(self.layoutWidget_2)
        self.paddingComboBox.addItem("")
        self.paddingComboBox.addItem("")
        self.paddingComboBox.setObjectName(u"paddingComboBox")
        sizePolicy1.setHeightForWidth(self.paddingComboBox.sizePolicy().hasHeightForWidth())
        self.paddingComboBox.setSizePolicy(sizePolicy1)
        self.paddingComboBox.setMinimumSize(QSize(174, 24))
        self.paddingComboBox.setMaximumSize(QSize(174, 24))
        self.paddingComboBox.setFont(font)

        self.horizontalLayout_27.addWidget(self.paddingComboBox)


        self.verticalLayout_9.addLayout(self.horizontalLayout_27)


        self.verticalLayout_4.addWidget(self.dockerGroupBox_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_3)

        self.tabWidget.addTab(self.createTab, "")
        self.manageTab = QWidget()
        self.manageTab.setObjectName(u"manageTab")
        self.layoutWidget4 = QWidget(self.manageTab)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(20, 10, 771, 401))
        self.horizontalLayout_20 = QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.groupBox_2 = QGroupBox(self.layoutWidget4)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font)
        self.exitedListWidget = QListWidget(self.groupBox_2)
        self.exitedListWidget.setObjectName(u"exitedListWidget")
        self.exitedListWidget.setGeometry(QRect(10, 30, 361, 161))
        sizePolicy1.setHeightForWidth(self.exitedListWidget.sizePolicy().hasHeightForWidth())
        self.exitedListWidget.setSizePolicy(sizePolicy1)
        self.exitedListWidget.setMinimumSize(QSize(361, 161))
        self.exitedListWidget.setMaximumSize(QSize(361, 161))

        self.verticalLayout_8.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.layoutWidget4)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font)
        self.createdListWidget = QListWidget(self.groupBox_3)
        self.createdListWidget.setObjectName(u"createdListWidget")
        self.createdListWidget.setGeometry(QRect(10, 20, 361, 171))
        sizePolicy1.setHeightForWidth(self.createdListWidget.sizePolicy().hasHeightForWidth())
        self.createdListWidget.setSizePolicy(sizePolicy1)
        self.createdListWidget.setMinimumSize(QSize(361, 171))
        self.createdListWidget.setMaximumSize(QSize(361, 171))

        self.verticalLayout_8.addWidget(self.groupBox_3)

        self.verticalLayout_8.setStretch(0, 1)
        self.verticalLayout_8.setStretch(1, 1)

        self.horizontalLayout_20.addLayout(self.verticalLayout_8)

        self.groupBox = QGroupBox(self.layoutWidget4)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font)
        self.runningListWidget = QListWidget(self.groupBox)
        self.runningListWidget.setObjectName(u"runningListWidget")
        self.runningListWidget.setGeometry(QRect(10, 30, 361, 361))
        sizePolicy1.setHeightForWidth(self.runningListWidget.sizePolicy().hasHeightForWidth())
        self.runningListWidget.setSizePolicy(sizePolicy1)
        self.runningListWidget.setMinimumSize(QSize(361, 361))
        self.runningListWidget.setMaximumSize(QSize(361, 361))

        self.horizontalLayout_20.addWidget(self.groupBox)

        self.refreshListWidgetsButton = QPushButton(self.manageTab)
        self.refreshListWidgetsButton.setObjectName(u"refreshListWidgetsButton")
        self.refreshListWidgetsButton.setGeometry(QRect(717, 416, 75, 25))
        sizePolicy1.setHeightForWidth(self.refreshListWidgetsButton.sizePolicy().hasHeightForWidth())
        self.refreshListWidgetsButton.setSizePolicy(sizePolicy1)
        self.refreshListWidgetsButton.setMinimumSize(QSize(75, 25))
        self.refreshListWidgetsButton.setMaximumSize(QSize(75, 25))
        self.tabWidget.addTab(self.manageTab, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        self.tabWidget_2 = QTabWidget(self.layoutWidget)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        sizePolicy1.setHeightForWidth(self.tabWidget_2.sizePolicy().hasHeightForWidth())
        self.tabWidget_2.setSizePolicy(sizePolicy1)
        self.tabWidget_2.setMinimumSize(QSize(801, 319))
        self.tabWidget_2.setMaximumSize(QSize(801, 319))
        self.tabWidget_2.setFont(font)
        self.tabWidget_2.setStyleSheet(u"")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.promptBrowser = QTextBrowser(self.tab)
        self.promptBrowser.setObjectName(u"promptBrowser")
        self.promptBrowser.setGeometry(QRect(0, 0, 801, 311))
        sizePolicy1.setHeightForWidth(self.promptBrowser.sizePolicy().hasHeightForWidth())
        self.promptBrowser.setSizePolicy(sizePolicy1)
        self.promptBrowser.setMinimumSize(QSize(801, 311))
        self.promptBrowser.setMaximumSize(QSize(801, 311))
        self.promptBrowser.setStyleSheet(u"")
        self.tabWidget_2.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.detailBrowser = QTextBrowser(self.tab_2)
        self.detailBrowser.setObjectName(u"detailBrowser")
        self.detailBrowser.setGeometry(QRect(0, 0, 801, 311))
        sizePolicy1.setHeightForWidth(self.detailBrowser.sizePolicy().hasHeightForWidth())
        self.detailBrowser.setSizePolicy(sizePolicy1)
        self.detailBrowser.setMinimumSize(QSize(801, 311))
        self.detailBrowser.setMaximumSize(QSize(801, 311))
        self.tabWidget_2.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.logBrowser = QTextBrowser(self.tab_3)
        self.logBrowser.setObjectName(u"logBrowser")
        self.logBrowser.setGeometry(QRect(0, 0, 801, 311))
        sizePolicy1.setHeightForWidth(self.logBrowser.sizePolicy().hasHeightForWidth())
        self.logBrowser.setSizePolicy(sizePolicy1)
        self.logBrowser.setMinimumSize(QSize(801, 311))
        self.logBrowser.setMaximumSize(QSize(801, 311))
        self.tabWidget_2.addTab(self.tab_3, "")

        self.verticalLayout_2.addWidget(self.tabWidget_2)

        self.verticalLayout_2.setStretch(0, 9)
        self.verticalLayout_2.setStretch(1, 5)

        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 10)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 11)

        self.retranslateUi(RobustarLauncher)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(RobustarLauncher)
    # setupUi

    def retranslateUi(self, RobustarLauncher):
        RobustarLauncher.setWindowTitle(QCoreApplication.translate("RobustarLauncher", u"Robustar Launcher", None))
        self.header.setText("")
        self.loadProfileButton.setText(QCoreApplication.translate("RobustarLauncher", u"Load Profile", None))
        self.saveProfileButton.setText(QCoreApplication.translate("RobustarLauncher", u"Save Profile", None))
        self.startServerButton.setText(QCoreApplication.translate("RobustarLauncher", u"Start Server", None))
        self.stopServerButton.setText(QCoreApplication.translate("RobustarLauncher", u"Stop Server", None))
        self.deleteServerButton.setText(QCoreApplication.translate("RobustarLauncher", u"Delete Server", None))
        self.dockerGroupBox.setTitle(QCoreApplication.translate("RobustarLauncher", u"Docker", None))
#if QT_CONFIG(tooltip)
        self.label_8.setToolTip(QCoreApplication.translate("RobustarLauncher", u"The name of the docker container", None))
#endif // QT_CONFIG(tooltip)
        self.label_8.setText(QCoreApplication.translate("RobustarLauncher", u"Container Name", None))
        self.nameInput.setText(QCoreApplication.translate("RobustarLauncher", u"robustar", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("RobustarLauncher", u"The version of the docker image of the container", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("RobustarLauncher", u"Image Version", None))
        self.versionComboBox.setProperty("placeholderText", "")
#if QT_CONFIG(tooltip)
        self.label_7.setToolTip(QCoreApplication.translate("RobustarLauncher", u"The port the docker container forwards to", None))
#endif // QT_CONFIG(tooltip)
        self.label_7.setText(QCoreApplication.translate("RobustarLauncher", u"Port", None))
        self.portInput.setText(QCoreApplication.translate("RobustarLauncher", u"8000", None))
        self.dataGroupBox.setTitle(QCoreApplication.translate("RobustarLauncher", u"Data", None))
#if QT_CONFIG(tooltip)
        self.label_6.setToolTip(QCoreApplication.translate("RobustarLauncher", u"The root path of the train set", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("RobustarLauncher", u"Train Set", None))
        self.trainPathDisplay.setText("")
        self.trainPathButton.setText(QCoreApplication.translate("RobustarLauncher", u"...", None))
#if QT_CONFIG(tooltip)
        self.label_13.setToolTip(QCoreApplication.translate("RobustarLauncher", u"The root path of the test set", None))
#endif // QT_CONFIG(tooltip)
        self.label_13.setText(QCoreApplication.translate("RobustarLauncher", u"Test Set", None))
        self.testPathDisplay.setText("")
        self.testPathButton.setText(QCoreApplication.translate("RobustarLauncher", u"...", None))
#if QT_CONFIG(tooltip)
        self.label_14.setToolTip(QCoreApplication.translate("RobustarLauncher", u"The root path for all checkpoint files saved by Robustar", None))
#endif // QT_CONFIG(tooltip)
        self.label_14.setText(QCoreApplication.translate("RobustarLauncher", u"Checkpoint", None))
        self.checkPointPathDisplay.setText("")
        self.checkPointPathButton.setText(QCoreApplication.translate("RobustarLauncher", u"...", None))
#if QT_CONFIG(tooltip)
        self.label_15.setToolTip(QCoreApplication.translate("RobustarLauncher", u"The root path for all influence result calculated by Robustar", None))
#endif // QT_CONFIG(tooltip)
        self.label_15.setText(QCoreApplication.translate("RobustarLauncher", u"Influence Result", None))
        self.influencePathDisplay.setText("")
        self.influencePathButton.setText(QCoreApplication.translate("RobustarLauncher", u"...", None))
        self.dockerGroupBox_2.setTitle(QCoreApplication.translate("RobustarLauncher", u"Model", None))
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("RobustarLauncher", u"The architecture of the model", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("RobustarLauncher", u"Architecture", None))
        self.archComboBox.setItemText(0, QCoreApplication.translate("RobustarLauncher", u"resnet-18", None))
        self.archComboBox.setItemText(1, QCoreApplication.translate("RobustarLauncher", u"resnet-34", None))
        self.archComboBox.setItemText(2, QCoreApplication.translate("RobustarLauncher", u"resnet-50", None))
        self.archComboBox.setItemText(3, QCoreApplication.translate("RobustarLauncher", u"resnet-101", None))
        self.archComboBox.setItemText(4, QCoreApplication.translate("RobustarLauncher", u"resnet-152", None))
        self.archComboBox.setItemText(5, QCoreApplication.translate("RobustarLauncher", u"resnet-18-32x32", None))
        self.archComboBox.setItemText(6, QCoreApplication.translate("RobustarLauncher", u"mobilenet-v2", None))
        self.archComboBox.setItemText(7, QCoreApplication.translate("RobustarLauncher", u"alexnet", None))

        self.archComboBox.setCurrentText(QCoreApplication.translate("RobustarLauncher", u"resnet-18", None))
        self.archComboBox.setProperty("placeholderText", "")
#if QT_CONFIG(tooltip)
        self.label_9.setToolTip(QCoreApplication.translate("RobustarLauncher", u"Check the box if you want a model with pretrained weights", None))
#endif // QT_CONFIG(tooltip)
        self.label_9.setText(QCoreApplication.translate("RobustarLauncher", u"Pretrained", None))
        self.pretrainedCheckBox.setText("")
#if QT_CONFIG(tooltip)
        self.label_16.setToolTip(QCoreApplication.translate("RobustarLauncher", u"The weight file used to initialize the model. Optional weight files are under the root path of the checkpoint you set", None))
#endif // QT_CONFIG(tooltip)
        self.label_16.setText(QCoreApplication.translate("RobustarLauncher", u"Weight File", None))
        self.weightFileComboBox.setItemText(0, QCoreApplication.translate("RobustarLauncher", u"None", None))

        self.weightFileComboBox.setProperty("placeholderText", "")
#if QT_CONFIG(tooltip)
        self.label_19.setToolTip(QCoreApplication.translate("RobustarLauncher", u"The device on which the model will be created", None))
#endif // QT_CONFIG(tooltip)
        self.label_19.setText(QCoreApplication.translate("RobustarLauncher", u"Device", None))
        self.deviceInput.setText(QCoreApplication.translate("RobustarLauncher", u"cpu", None))
#if QT_CONFIG(tooltip)
        self.label_20.setToolTip(QCoreApplication.translate("RobustarLauncher", u"Check the box if you want the train data to be shuffled", None))
#endif // QT_CONFIG(tooltip)
        self.label_20.setText(QCoreApplication.translate("RobustarLauncher", u"Shuffle", None))
        self.shuffleCheckBox.setText("")
#if QT_CONFIG(tooltip)
        self.label_21.setToolTip(QCoreApplication.translate("RobustarLauncher", u"The batch size of the data", None))
#endif // QT_CONFIG(tooltip)
        self.label_21.setText(QCoreApplication.translate("RobustarLauncher", u"Batch Size", None))
        self.batchSizeInput.setText("")
#if QT_CONFIG(tooltip)
        self.label_22.setToolTip(QCoreApplication.translate("RobustarLauncher", u"The number of workers for the data loader", None))
#endif // QT_CONFIG(tooltip)
        self.label_22.setText(QCoreApplication.translate("RobustarLauncher", u"Worker Number", None))
        self.workerNumberInput.setText("")
#if QT_CONFIG(tooltip)
        self.label_25.setToolTip(QCoreApplication.translate("RobustarLauncher", u"The number of classes of the data", None))
#endif // QT_CONFIG(tooltip)
        self.label_25.setText(QCoreApplication.translate("RobustarLauncher", u"Class Number", None))
        self.classNumberInput.setText("")
#if QT_CONFIG(tooltip)
        self.label_23.setToolTip(QCoreApplication.translate("RobustarLauncher", u"The length of side of the input image of the model", None))
#endif // QT_CONFIG(tooltip)
        self.label_23.setText(QCoreApplication.translate("RobustarLauncher", u"Image Size", None))
        self.imgSizeInput.setText("")
#if QT_CONFIG(tooltip)
        self.label_24.setToolTip(QCoreApplication.translate("RobustarLauncher", u"The mode of padding", None))
#endif // QT_CONFIG(tooltip)
        self.label_24.setText(QCoreApplication.translate("RobustarLauncher", u"Image Padding", None))
        self.paddingComboBox.setItemText(0, QCoreApplication.translate("RobustarLauncher", u"short side", None))
        self.paddingComboBox.setItemText(1, QCoreApplication.translate("RobustarLauncher", u"none", None))

        self.paddingComboBox.setCurrentText(QCoreApplication.translate("RobustarLauncher", u"short side", None))
        self.paddingComboBox.setProperty("placeholderText", "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.createTab), QCoreApplication.translate("RobustarLauncher", u"Create", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("RobustarLauncher", u"Exited", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("RobustarLauncher", u"Created", None))
        self.groupBox.setTitle(QCoreApplication.translate("RobustarLauncher", u"Running", None))
        self.refreshListWidgetsButton.setText(QCoreApplication.translate("RobustarLauncher", u"Refresh", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.manageTab), QCoreApplication.translate("RobustarLauncher", u"Manage", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab), QCoreApplication.translate("RobustarLauncher", u"Prompts", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), QCoreApplication.translate("RobustarLauncher", u"Details", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("RobustarLauncher", u"Logs", None))
    # retranslateUi

