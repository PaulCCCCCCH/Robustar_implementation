# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'popup.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(806, 400)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(308, 123))
        Dialog.setMaximumSize(QSize(1000, 1000))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.warningLabel = QLabel(Dialog)
        self.warningLabel.setObjectName(u"warningLabel")
        sizePolicy.setHeightForWidth(self.warningLabel.sizePolicy().hasHeightForWidth())
        self.warningLabel.setSizePolicy(sizePolicy)
        self.warningLabel.setMinimumSize(QSize(776, 144))
        self.warningLabel.setMaximumSize(QSize(776, 144))
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(16)
        self.warningLabel.setFont(font)
        self.warningLabel.setAlignment(Qt.AlignCenter)
        self.warningLabel.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.warningLabel)

        self.exceptionLabel = QLabel(Dialog)
        self.exceptionLabel.setObjectName(u"exceptionLabel")
        sizePolicy.setHeightForWidth(self.exceptionLabel.sizePolicy().hasHeightForWidth())
        self.exceptionLabel.setSizePolicy(sizePolicy)
        self.exceptionLabel.setMinimumSize(QSize(776, 96))
        self.exceptionLabel.setMaximumSize(QSize(776, 96))
        font1 = QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setWeight(50)
        self.exceptionLabel.setFont(font1)
        self.exceptionLabel.setAlignment(Qt.AlignCenter)
        self.exceptionLabel.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.exceptionLabel)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.okButton = QPushButton(Dialog)
        self.okButton.setObjectName(u"okButton")
        sizePolicy.setHeightForWidth(self.okButton.sizePolicy().hasHeightForWidth())
        self.okButton.setSizePolicy(sizePolicy)
        self.okButton.setMinimumSize(QSize(120, 40))
        self.okButton.setMaximumSize(QSize(120, 40))

        self.horizontalLayout_2.addWidget(self.okButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayout.setStretch(1, 1)

        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Warning", None))
        self.warningLabel.setText(QCoreApplication.translate("Dialog", u"ff", None))
        self.exceptionLabel.setText(QCoreApplication.translate("Dialog", u"ff", None))
        self.okButton.setText(QCoreApplication.translate("Dialog", u"OK", None))
    # retranslateUi

