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


class Ui_main_dialog(object):
    def setupUi(self, main_dialog):
        if not main_dialog.objectName():
            main_dialog.setObjectName(u"main_dialog")
        main_dialog.resize(806, 400)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_dialog.sizePolicy().hasHeightForWidth())
        main_dialog.setSizePolicy(sizePolicy)
        main_dialog.setMinimumSize(QSize(308, 123))
        main_dialog.setMaximumSize(QSize(1000, 1000))
        self.gridLayout = QGridLayout(main_dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.main_v_layout = QVBoxLayout()
        self.main_v_layout.setObjectName(u"main_v_layout")
        self.main_v_layout.setContentsMargins(-1, 0, -1, 0)
        self.info_v_layout = QVBoxLayout()
        self.info_v_layout.setObjectName(u"info_v_layout")
        self.warning_label = QLabel(main_dialog)
        self.warning_label.setObjectName(u"warning_label")
        sizePolicy.setHeightForWidth(self.warning_label.sizePolicy().hasHeightForWidth())
        self.warning_label.setSizePolicy(sizePolicy)
        self.warning_label.setMinimumSize(QSize(776, 144))
        self.warning_label.setMaximumSize(QSize(776, 144))
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(16)
        self.warning_label.setFont(font)
        self.warning_label.setAlignment(Qt.AlignCenter)
        self.warning_label.setWordWrap(True)

        self.info_v_layout.addWidget(self.warning_label)

        self.exception_label = QLabel(main_dialog)
        self.exception_label.setObjectName(u"exception_label")
        sizePolicy.setHeightForWidth(self.exception_label.sizePolicy().hasHeightForWidth())
        self.exception_label.setSizePolicy(sizePolicy)
        self.exception_label.setMinimumSize(QSize(776, 96))
        self.exception_label.setMaximumSize(QSize(776, 96))
        font1 = QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setWeight(50)
        self.exception_label.setFont(font1)
        self.exception_label.setAlignment(Qt.AlignCenter)
        self.exception_label.setWordWrap(True)

        self.info_v_layout.addWidget(self.exception_label)


        self.main_v_layout.addLayout(self.info_v_layout)

        self.ok_h_layout = QHBoxLayout()
        self.ok_h_layout.setObjectName(u"ok_h_layout")
        self.ok_left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.ok_h_layout.addItem(self.ok_left_spacer)

        self.ok_push_button = QPushButton(main_dialog)
        self.ok_push_button.setObjectName(u"ok_push_button")
        sizePolicy.setHeightForWidth(self.ok_push_button.sizePolicy().hasHeightForWidth())
        self.ok_push_button.setSizePolicy(sizePolicy)
        self.ok_push_button.setMinimumSize(QSize(120, 40))
        self.ok_push_button.setMaximumSize(QSize(120, 40))

        self.ok_h_layout.addWidget(self.ok_push_button)

        self.ok_right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.ok_h_layout.addItem(self.ok_right_spacer)

        self.ok_h_layout.setStretch(0, 1)
        self.ok_h_layout.setStretch(1, 1)
        self.ok_h_layout.setStretch(2, 1)

        self.main_v_layout.addLayout(self.ok_h_layout)

        self.main_v_layout.setStretch(1, 1)

        self.gridLayout.addLayout(self.main_v_layout, 1, 0, 1, 1)


        self.retranslateUi(main_dialog)

        QMetaObject.connectSlotsByName(main_dialog)
    # setupUi

    def retranslateUi(self, main_dialog):
        main_dialog.setWindowTitle(QCoreApplication.translate("main_dialog", u"Warning", None))
        self.warning_label.setText("")
        self.exception_label.setText("")
        self.ok_push_button.setText(QCoreApplication.translate("main_dialog", u"OK", None))
    # retranslateUi

