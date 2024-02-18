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


class Ui_main_widget(object):
    def setupUi(self, main_widget):
        if not main_widget.objectName():
            main_widget.setObjectName(u"main_widget")
        main_widget.resize(1000, 1020)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_widget.sizePolicy().hasHeightForWidth())
        main_widget.setSizePolicy(sizePolicy)
        main_widget.setMinimumSize(QSize(1000, 1020))
        main_widget.setMaximumSize(QSize(1000, 1020))
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        main_widget.setFont(font)
        icon = QIcon()
        icon.addFile(u":/resources/logo_short.png", QSize(), QIcon.Normal, QIcon.Off)
        main_widget.setWindowIcon(icon)
        main_widget.setStyleSheet(
            u'QWidget{font: 8pt "Arial"}\n'
            "QPushButton{background-color: #E1E1E1; \n"
            "			font: 8pt Arial;\n"
            "			border: 1px solid #ADADAD;}\n"
            "QPushButton:hover {\n"
            "   background-color: #E3ECF3;\n"
            "   border: 1px solid #3287CA;\n"
            "}"
        )
        self.layoutWidget = QWidget(main_widget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(35, 0, 931, 44))
        self.header_h_layout = QHBoxLayout(self.layoutWidget)
        self.header_h_layout.setObjectName(u"header_h_layout")
        self.header_h_layout.setContentsMargins(0, 0, 0, 0)
        self.header_label = QLabel(self.layoutWidget)
        self.header_label.setObjectName(u"header_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.header_label.sizePolicy().hasHeightForWidth()
        )
        self.header_label.setSizePolicy(sizePolicy1)
        self.header_label.setMinimumSize(QSize(164, 42))
        self.header_label.setMaximumSize(QSize(164, 42))
        self.header_label.setTextFormat(Qt.AutoText)
        self.header_label.setPixmap(QPixmap(u":/resources/logo_long.png"))
        self.header_label.setScaledContents(True)
        self.header_label.setIndent(-1)

        self.header_h_layout.addWidget(self.header_label)

        self.layoutWidget1 = QWidget(main_widget)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(28, 55, 942, 941))
        self.op_main_v_layout = QVBoxLayout(self.layoutWidget1)
        self.op_main_v_layout.setObjectName(u"op_main_v_layout")
        self.op_main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.cm_tab_widget = QTabWidget(self.layoutWidget1)
        self.cm_tab_widget.setObjectName(u"cm_tab_widget")
        sizePolicy1.setHeightForWidth(
            self.cm_tab_widget.sizePolicy().hasHeightForWidth()
        )
        self.cm_tab_widget.setSizePolicy(sizePolicy1)
        self.cm_tab_widget.setMinimumSize(QSize(940, 610))
        self.cm_tab_widget.setMaximumSize(QSize(940, 610))
        self.cm_tab_widget.setFont(font)
        self.create_widget = QWidget()
        self.create_widget.setObjectName(u"create_widget")
        self.layoutWidget2 = QWidget(self.create_widget)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(4, 9, 931, 606))
        self.create_h_layout = QHBoxLayout(self.layoutWidget2)
        self.create_h_layout.setSpacing(9)
        self.create_h_layout.setObjectName(u"create_h_layout")
        self.create_h_layout.setContentsMargins(0, 0, 0, 0)
        self.server_v_layout = QVBoxLayout()
        self.server_v_layout.setObjectName(u"server_v_layout")
        self.server_group_box = QGroupBox(self.layoutWidget2)
        self.server_group_box.setObjectName(u"server_group_box")
        sizePolicy1.setHeightForWidth(
            self.server_group_box.sizePolicy().hasHeightForWidth()
        )
        self.server_group_box.setSizePolicy(sizePolicy1)
        self.server_group_box.setMinimumSize(QSize(458, 400))
        self.server_group_box.setMaximumSize(QSize(458, 400))
        self.server_group_box.setFont(font)
        self.layoutWidget_5 = QWidget(self.server_group_box)
        self.layoutWidget_5.setObjectName(u"layoutWidget_5")
        self.layoutWidget_5.setGeometry(QRect(10, 20, 441, 343))
        self.server_v_layout_2 = QVBoxLayout(self.layoutWidget_5)
        self.server_v_layout_2.setObjectName(u"server_v_layout_2")
        self.server_v_layout_2.setContentsMargins(0, 0, 0, 0)
        self.name_h_layout = QHBoxLayout()
        self.name_h_layout.setObjectName(u"name_h_layout")
        self.name_label = QLabel(self.layoutWidget_5)
        self.name_label.setObjectName(u"name_label")
        sizePolicy1.setHeightForWidth(self.name_label.sizePolicy().hasHeightForWidth())
        self.name_label.setSizePolicy(sizePolicy1)
        self.name_label.setMinimumSize(QSize(200, 39))
        self.name_label.setMaximumSize(QSize(200, 39))
        self.name_label.setFont(font)

        self.name_h_layout.addWidget(self.name_label)

        self.name_line_edit = QLineEdit(self.layoutWidget_5)
        self.name_line_edit.setObjectName(u"name_line_edit")
        sizePolicy1.setHeightForWidth(
            self.name_line_edit.sizePolicy().hasHeightForWidth()
        )
        self.name_line_edit.setSizePolicy(sizePolicy1)
        self.name_line_edit.setMinimumSize(QSize(200, 24))
        self.name_line_edit.setMaximumSize(QSize(200, 24))
        self.name_line_edit.setFont(font)
        self.name_line_edit.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )
        self.name_line_edit.setClearButtonEnabled(True)

        self.name_h_layout.addWidget(self.name_line_edit)

        self.server_v_layout_2.addLayout(self.name_h_layout)

        self.image_h_layout = QHBoxLayout()
        self.image_h_layout.setObjectName(u"image_h_layout")
        self.image_label = QLabel(self.layoutWidget_5)
        self.image_label.setObjectName(u"image_label")
        sizePolicy1.setHeightForWidth(self.image_label.sizePolicy().hasHeightForWidth())
        self.image_label.setSizePolicy(sizePolicy1)
        self.image_label.setMinimumSize(QSize(200, 39))
        self.image_label.setMaximumSize(QSize(200, 39))
        self.image_label.setFont(font)

        self.image_h_layout.addWidget(self.image_label)

        self.image_combo_box = QComboBox(self.layoutWidget_5)
        self.image_combo_box.setObjectName(u"image_combo_box")
        sizePolicy1.setHeightForWidth(
            self.image_combo_box.sizePolicy().hasHeightForWidth()
        )
        self.image_combo_box.setSizePolicy(sizePolicy1)
        self.image_combo_box.setMinimumSize(QSize(200, 24))
        self.image_combo_box.setMaximumSize(QSize(200, 24))
        self.image_combo_box.setFont(font)

        self.image_h_layout.addWidget(self.image_combo_box)

        self.server_v_layout_2.addLayout(self.image_h_layout)

        self.port_h_layout = QHBoxLayout()
        self.port_h_layout.setObjectName(u"port_h_layout")
        self.port_label = QLabel(self.layoutWidget_5)
        self.port_label.setObjectName(u"port_label")
        sizePolicy1.setHeightForWidth(self.port_label.sizePolicy().hasHeightForWidth())
        self.port_label.setSizePolicy(sizePolicy1)
        self.port_label.setMinimumSize(QSize(200, 39))
        self.port_label.setMaximumSize(QSize(200, 39))
        self.port_label.setFont(font)

        self.port_h_layout.addWidget(self.port_label)

        self.port_line_edit = QLineEdit(self.layoutWidget_5)
        self.port_line_edit.setObjectName(u"port_line_edit")
        sizePolicy1.setHeightForWidth(
            self.port_line_edit.sizePolicy().hasHeightForWidth()
        )
        self.port_line_edit.setSizePolicy(sizePolicy1)
        self.port_line_edit.setMinimumSize(QSize(200, 24))
        self.port_line_edit.setMaximumSize(QSize(200, 24))
        self.port_line_edit.setFont(font)
        self.port_line_edit.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )
        self.port_line_edit.setClearButtonEnabled(True)

        self.port_h_layout.addWidget(self.port_line_edit)

        self.server_v_layout_2.addLayout(self.port_h_layout)

        self.device_h_layout = QHBoxLayout()
        self.device_h_layout.setObjectName(u"device_h_layout")
        self.device_label = QLabel(self.layoutWidget_5)
        self.device_label.setObjectName(u"device_label")
        sizePolicy1.setHeightForWidth(
            self.device_label.sizePolicy().hasHeightForWidth()
        )
        self.device_label.setSizePolicy(sizePolicy1)
        self.device_label.setMinimumSize(QSize(200, 39))
        self.device_label.setMaximumSize(QSize(200, 39))
        self.device_label.setFont(font)

        self.device_h_layout.addWidget(self.device_label)

        self.device_combo_box = QComboBox(self.layoutWidget_5)
        self.device_combo_box.addItem("")
        self.device_combo_box.setObjectName(u"device_combo_box")
        sizePolicy1.setHeightForWidth(
            self.device_combo_box.sizePolicy().hasHeightForWidth()
        )
        self.device_combo_box.setSizePolicy(sizePolicy1)
        self.device_combo_box.setMinimumSize(QSize(200, 24))
        self.device_combo_box.setMaximumSize(QSize(200, 24))
        self.device_combo_box.setFont(font)

        self.device_h_layout.addWidget(self.device_combo_box)

        self.server_v_layout_2.addLayout(self.device_h_layout)

        self.cls_h_layout = QHBoxLayout()
        self.cls_h_layout.setObjectName(u"cls_h_layout")
        self.cls_label = QLabel(self.layoutWidget_5)
        self.cls_label.setObjectName(u"cls_label")
        sizePolicy1.setHeightForWidth(self.cls_label.sizePolicy().hasHeightForWidth())
        self.cls_label.setSizePolicy(sizePolicy1)
        self.cls_label.setMinimumSize(QSize(200, 39))
        self.cls_label.setMaximumSize(QSize(200, 39))
        self.cls_label.setFont(font)

        self.cls_h_layout.addWidget(self.cls_label)

        self.cls_line_edit = QLineEdit(self.layoutWidget_5)
        self.cls_line_edit.setObjectName(u"cls_line_edit")
        sizePolicy1.setHeightForWidth(
            self.cls_line_edit.sizePolicy().hasHeightForWidth()
        )
        self.cls_line_edit.setSizePolicy(sizePolicy1)
        self.cls_line_edit.setMinimumSize(QSize(200, 24))
        self.cls_line_edit.setMaximumSize(QSize(200, 24))
        self.cls_line_edit.setFont(font)
        self.cls_line_edit.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )
        self.cls_line_edit.setClearButtonEnabled(True)

        self.cls_h_layout.addWidget(self.cls_line_edit)

        self.server_v_layout_2.addLayout(self.cls_h_layout)

        self.size_h_layout = QHBoxLayout()
        self.size_h_layout.setObjectName(u"size_h_layout")
        self.size_label = QLabel(self.layoutWidget_5)
        self.size_label.setObjectName(u"size_label")
        sizePolicy1.setHeightForWidth(self.size_label.sizePolicy().hasHeightForWidth())
        self.size_label.setSizePolicy(sizePolicy1)
        self.size_label.setMinimumSize(QSize(200, 39))
        self.size_label.setMaximumSize(QSize(200, 39))
        self.size_label.setFont(font)

        self.size_h_layout.addWidget(self.size_label)

        self.size_line_edit = QLineEdit(self.layoutWidget_5)
        self.size_line_edit.setObjectName(u"size_line_edit")
        sizePolicy1.setHeightForWidth(
            self.size_line_edit.sizePolicy().hasHeightForWidth()
        )
        self.size_line_edit.setSizePolicy(sizePolicy1)
        self.size_line_edit.setMinimumSize(QSize(200, 24))
        self.size_line_edit.setMaximumSize(QSize(200, 24))
        self.size_line_edit.setFont(font)
        self.size_line_edit.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )
        self.size_line_edit.setClearButtonEnabled(True)

        self.size_h_layout.addWidget(self.size_line_edit)

        self.server_v_layout_2.addLayout(self.size_h_layout)

        self.pad_h_layout = QHBoxLayout()
        self.pad_h_layout.setObjectName(u"pad_h_layout")
        self.pad_label = QLabel(self.layoutWidget_5)
        self.pad_label.setObjectName(u"pad_label")
        sizePolicy1.setHeightForWidth(self.pad_label.sizePolicy().hasHeightForWidth())
        self.pad_label.setSizePolicy(sizePolicy1)
        self.pad_label.setMinimumSize(QSize(200, 39))
        self.pad_label.setMaximumSize(QSize(200, 39))
        self.pad_label.setFont(font)

        self.pad_h_layout.addWidget(self.pad_label)

        self.pad_combo_box = QComboBox(self.layoutWidget_5)
        self.pad_combo_box.addItem("")
        self.pad_combo_box.addItem("")
        self.pad_combo_box.setObjectName(u"pad_combo_box")
        sizePolicy1.setHeightForWidth(
            self.pad_combo_box.sizePolicy().hasHeightForWidth()
        )
        self.pad_combo_box.setSizePolicy(sizePolicy1)
        self.pad_combo_box.setMinimumSize(QSize(200, 24))
        self.pad_combo_box.setMaximumSize(QSize(200, 24))
        self.pad_combo_box.setFont(font)

        self.pad_h_layout.addWidget(self.pad_combo_box)

        self.server_v_layout_2.addLayout(self.pad_h_layout)

        self.server_v_layout.addWidget(self.server_group_box)

        self.create_h_layout.addLayout(self.server_v_layout)

        self.dir_v_layout = QVBoxLayout()
        self.dir_v_layout.setObjectName(u"dir_v_layout")
        self.dir_group_box = QGroupBox(self.layoutWidget2)
        self.dir_group_box.setObjectName(u"dir_group_box")
        sizePolicy1.setHeightForWidth(
            self.dir_group_box.sizePolicy().hasHeightForWidth()
        )
        self.dir_group_box.setSizePolicy(sizePolicy1)
        self.dir_group_box.setMinimumSize(QSize(458, 400))
        self.dir_group_box.setMaximumSize(QSize(458, 400))
        self.dir_group_box.setFont(font)
        self.layoutWidget_6 = QWidget(self.dir_group_box)
        self.layoutWidget_6.setObjectName(u"layoutWidget_6")
        self.layoutWidget_6.setGeometry(QRect(10, 20, 441, 343))
        self.dir_v_layout_2 = QVBoxLayout(self.layoutWidget_6)
        self.dir_v_layout_2.setSpacing(9)
        self.dir_v_layout_2.setObjectName(u"dir_v_layout_2")
        self.dir_v_layout_2.setContentsMargins(0, 0, 0, 0)
        self.train_h_layout = QHBoxLayout()
        self.train_h_layout.setSpacing(9)
        self.train_h_layout.setObjectName(u"train_h_layout")
        self.train_h_layout.setContentsMargins(0, -1, -1, -1)
        self.train_label = QLabel(self.layoutWidget_6)
        self.train_label.setObjectName(u"train_label")
        sizePolicy1.setHeightForWidth(self.train_label.sizePolicy().hasHeightForWidth())
        self.train_label.setSizePolicy(sizePolicy1)
        self.train_label.setMinimumSize(QSize(100, 39))
        self.train_label.setMaximumSize(QSize(200, 39))
        self.train_label.setFont(font)

        self.train_h_layout.addWidget(self.train_label)

        self.train_line_edit = QLineEdit(self.layoutWidget_6)
        self.train_line_edit.setObjectName(u"train_line_edit")
        self.train_line_edit.setEnabled(True)
        sizePolicy1.setHeightForWidth(
            self.train_line_edit.sizePolicy().hasHeightForWidth()
        )
        self.train_line_edit.setSizePolicy(sizePolicy1)
        self.train_line_edit.setMinimumSize(QSize(154, 24))
        self.train_line_edit.setMaximumSize(QSize(154, 24))
        self.train_line_edit.setFont(font)
        self.train_line_edit.setMouseTracking(True)
        self.train_line_edit.setReadOnly(True)

        self.train_h_layout.addWidget(self.train_line_edit)

        self.train_push_button = QPushButton(self.layoutWidget_6)
        self.train_push_button.setObjectName(u"train_push_button")
        sizePolicy1.setHeightForWidth(
            self.train_push_button.sizePolicy().hasHeightForWidth()
        )
        self.train_push_button.setSizePolicy(sizePolicy1)
        self.train_push_button.setMinimumSize(QSize(25, 20))
        self.train_push_button.setMaximumSize(QSize(25, 20))
        self.train_push_button.setFont(font)

        self.train_h_layout.addWidget(self.train_push_button)

        self.dir_v_layout_2.addLayout(self.train_h_layout)

        self.val_h_layout = QHBoxLayout()
        self.val_h_layout.setObjectName(u"val_h_layout")
        self.val_h_layout.setContentsMargins(-1, -1, 0, -1)
        self.val_label = QLabel(self.layoutWidget_6)
        self.val_label.setObjectName(u"val_label")
        sizePolicy1.setHeightForWidth(self.val_label.sizePolicy().hasHeightForWidth())
        self.val_label.setSizePolicy(sizePolicy1)
        self.val_label.setMinimumSize(QSize(200, 39))
        self.val_label.setMaximumSize(QSize(200, 39))
        self.val_label.setFont(font)

        self.val_h_layout.addWidget(self.val_label)

        self.val_line_edit = QLineEdit(self.layoutWidget_6)
        self.val_line_edit.setObjectName(u"val_line_edit")
        sizePolicy1.setHeightForWidth(
            self.val_line_edit.sizePolicy().hasHeightForWidth()
        )
        self.val_line_edit.setSizePolicy(sizePolicy1)
        self.val_line_edit.setMinimumSize(QSize(154, 24))
        self.val_line_edit.setMaximumSize(QSize(154, 24))
        self.val_line_edit.setFont(font)
        self.val_line_edit.setReadOnly(True)

        self.val_h_layout.addWidget(self.val_line_edit)

        self.val_push_button = QPushButton(self.layoutWidget_6)
        self.val_push_button.setObjectName(u"val_push_button")
        sizePolicy1.setHeightForWidth(
            self.val_push_button.sizePolicy().hasHeightForWidth()
        )
        self.val_push_button.setSizePolicy(sizePolicy1)
        self.val_push_button.setMinimumSize(QSize(25, 20))
        self.val_push_button.setMaximumSize(QSize(25, 20))
        self.val_push_button.setFont(font)

        self.val_h_layout.addWidget(self.val_push_button)

        self.dir_v_layout_2.addLayout(self.val_h_layout)

        self.test_h_layout = QHBoxLayout()
        self.test_h_layout.setObjectName(u"test_h_layout")
        self.test_h_layout.setContentsMargins(-1, -1, 0, -1)
        self.test_label = QLabel(self.layoutWidget_6)
        self.test_label.setObjectName(u"test_label")
        sizePolicy1.setHeightForWidth(self.test_label.sizePolicy().hasHeightForWidth())
        self.test_label.setSizePolicy(sizePolicy1)
        self.test_label.setMinimumSize(QSize(200, 39))
        self.test_label.setMaximumSize(QSize(200, 39))
        self.test_label.setFont(font)

        self.test_h_layout.addWidget(self.test_label)

        self.test_line_edit = QLineEdit(self.layoutWidget_6)
        self.test_line_edit.setObjectName(u"test_line_edit")
        sizePolicy1.setHeightForWidth(
            self.test_line_edit.sizePolicy().hasHeightForWidth()
        )
        self.test_line_edit.setSizePolicy(sizePolicy1)
        self.test_line_edit.setMinimumSize(QSize(154, 24))
        self.test_line_edit.setMaximumSize(QSize(154, 24))
        self.test_line_edit.setFont(font)
        self.test_line_edit.setReadOnly(True)

        self.test_h_layout.addWidget(self.test_line_edit)

        self.test_push_button = QPushButton(self.layoutWidget_6)
        self.test_push_button.setObjectName(u"test_push_button")
        sizePolicy1.setHeightForWidth(
            self.test_push_button.sizePolicy().hasHeightForWidth()
        )
        self.test_push_button.setSizePolicy(sizePolicy1)
        self.test_push_button.setMinimumSize(QSize(25, 20))
        self.test_push_button.setMaximumSize(QSize(25, 20))
        self.test_push_button.setFont(font)

        self.test_h_layout.addWidget(self.test_push_button)

        self.dir_v_layout_2.addLayout(self.test_h_layout)

        self.paired_h_layout = QHBoxLayout()
        self.paired_h_layout.setObjectName(u"paired_h_layout")
        self.paired_h_layout.setContentsMargins(-1, -1, 0, -1)
        self.paired_label = QLabel(self.layoutWidget_6)
        self.paired_label.setObjectName(u"paired_label")
        sizePolicy1.setHeightForWidth(
            self.paired_label.sizePolicy().hasHeightForWidth()
        )
        self.paired_label.setSizePolicy(sizePolicy1)
        self.paired_label.setMinimumSize(QSize(200, 39))
        self.paired_label.setMaximumSize(QSize(200, 39))
        self.paired_label.setFont(font)

        self.paired_h_layout.addWidget(self.paired_label)

        self.paired_line_edit = QLineEdit(self.layoutWidget_6)
        self.paired_line_edit.setObjectName(u"paired_line_edit")
        sizePolicy1.setHeightForWidth(
            self.paired_line_edit.sizePolicy().hasHeightForWidth()
        )
        self.paired_line_edit.setSizePolicy(sizePolicy1)
        self.paired_line_edit.setMinimumSize(QSize(154, 24))
        self.paired_line_edit.setMaximumSize(QSize(154, 24))
        self.paired_line_edit.setFont(font)
        self.paired_line_edit.setReadOnly(True)

        self.paired_h_layout.addWidget(self.paired_line_edit)

        self.paired_push_button = QPushButton(self.layoutWidget_6)
        self.paired_push_button.setObjectName(u"paired_push_button")
        sizePolicy1.setHeightForWidth(
            self.paired_push_button.sizePolicy().hasHeightForWidth()
        )
        self.paired_push_button.setSizePolicy(sizePolicy1)
        self.paired_push_button.setMinimumSize(QSize(25, 20))
        self.paired_push_button.setMaximumSize(QSize(25, 20))
        self.paired_push_button.setFont(font)

        self.paired_h_layout.addWidget(self.paired_push_button)

        self.dir_v_layout_2.addLayout(self.paired_h_layout)

        self.inf_h_layout = QHBoxLayout()
        self.inf_h_layout.setObjectName(u"inf_h_layout")
        self.inf_label = QLabel(self.layoutWidget_6)
        self.inf_label.setObjectName(u"inf_label")
        sizePolicy1.setHeightForWidth(self.inf_label.sizePolicy().hasHeightForWidth())
        self.inf_label.setSizePolicy(sizePolicy1)
        self.inf_label.setMinimumSize(QSize(200, 39))
        self.inf_label.setMaximumSize(QSize(200, 39))
        self.inf_label.setFont(font)

        self.inf_h_layout.addWidget(self.inf_label)

        self.inf_line_edit = QLineEdit(self.layoutWidget_6)
        self.inf_line_edit.setObjectName(u"inf_line_edit")
        sizePolicy1.setHeightForWidth(
            self.inf_line_edit.sizePolicy().hasHeightForWidth()
        )
        self.inf_line_edit.setSizePolicy(sizePolicy1)
        self.inf_line_edit.setMinimumSize(QSize(154, 24))
        self.inf_line_edit.setMaximumSize(QSize(154, 24))
        self.inf_line_edit.setFont(font)
        self.inf_line_edit.setReadOnly(True)

        self.inf_h_layout.addWidget(self.inf_line_edit)

        self.inf_push_button = QPushButton(self.layoutWidget_6)
        self.inf_push_button.setObjectName(u"inf_push_button")
        sizePolicy1.setHeightForWidth(
            self.inf_push_button.sizePolicy().hasHeightForWidth()
        )
        self.inf_push_button.setSizePolicy(sizePolicy1)
        self.inf_push_button.setMinimumSize(QSize(25, 20))
        self.inf_push_button.setMaximumSize(QSize(25, 20))
        self.inf_push_button.setFont(font)

        self.inf_h_layout.addWidget(self.inf_push_button)

        self.dir_v_layout_2.addLayout(self.inf_h_layout)

        self.out_h_layout = QHBoxLayout()
        self.out_h_layout.setObjectName(u"out_h_layout")
        self.out_h_layout.setContentsMargins(-1, -1, 0, -1)
        self.out_label = QLabel(self.layoutWidget_6)
        self.out_label.setObjectName(u"out_label")
        sizePolicy1.setHeightForWidth(self.out_label.sizePolicy().hasHeightForWidth())
        self.out_label.setSizePolicy(sizePolicy1)
        self.out_label.setMinimumSize(QSize(200, 39))
        self.out_label.setMaximumSize(QSize(200, 39))
        self.out_label.setFont(font)

        self.out_h_layout.addWidget(self.out_label)

        self.out_line_edit = QLineEdit(self.layoutWidget_6)
        self.out_line_edit.setObjectName(u"out_line_edit")
        sizePolicy1.setHeightForWidth(
            self.out_line_edit.sizePolicy().hasHeightForWidth()
        )
        self.out_line_edit.setSizePolicy(sizePolicy1)
        self.out_line_edit.setMinimumSize(QSize(154, 24))
        self.out_line_edit.setMaximumSize(QSize(154, 24))
        self.out_line_edit.setFont(font)
        self.out_line_edit.setReadOnly(True)

        self.out_h_layout.addWidget(self.out_line_edit)

        self.out_push_button = QPushButton(self.layoutWidget_6)
        self.out_push_button.setObjectName(u"out_push_button")
        sizePolicy1.setHeightForWidth(
            self.out_push_button.sizePolicy().hasHeightForWidth()
        )
        self.out_push_button.setSizePolicy(sizePolicy1)
        self.out_push_button.setMinimumSize(QSize(25, 20))
        self.out_push_button.setMaximumSize(QSize(25, 20))
        self.out_push_button.setFont(font)

        self.out_h_layout.addWidget(self.out_push_button)

        self.dir_v_layout_2.addLayout(self.out_h_layout)

        self.dir_v_layout.addWidget(self.dir_group_box)

        self.create_h_layout.addLayout(self.dir_v_layout)

        self.create_button_frame = QFrame(self.create_widget)
        self.create_button_frame.setObjectName(u"create_button_frame")
        self.create_button_frame.setGeometry(QRect(9, 539, 921, 41))
        self.create_button_frame.setFrameShape(QFrame.StyledPanel)
        self.create_button_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayoutWidget = QWidget(self.create_button_frame)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 921, 41))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(
            526, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.create_push_button = QPushButton(self.horizontalLayoutWidget)
        self.create_push_button.setObjectName(u"create_push_button")
        sizePolicy1.setHeightForWidth(
            self.create_push_button.sizePolicy().hasHeightForWidth()
        )
        self.create_push_button.setSizePolicy(sizePolicy1)
        self.create_push_button.setMinimumSize(QSize(100, 25))
        self.create_push_button.setMaximumSize(QSize(100, 25))
        self.create_push_button.setFont(font)
        self.create_push_button.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout.addWidget(self.create_push_button)

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.load_push_button = QPushButton(self.horizontalLayoutWidget)
        self.load_push_button.setObjectName(u"load_push_button")
        sizePolicy1.setHeightForWidth(
            self.load_push_button.sizePolicy().hasHeightForWidth()
        )
        self.load_push_button.setSizePolicy(sizePolicy1)
        self.load_push_button.setMinimumSize(QSize(100, 25))
        self.load_push_button.setMaximumSize(QSize(100, 25))
        self.load_push_button.setFont(font)
        self.load_push_button.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.load_push_button)

        self.horizontalSpacer_3 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.save_push_button = QPushButton(self.horizontalLayoutWidget)
        self.save_push_button.setObjectName(u"save_push_button")
        sizePolicy1.setHeightForWidth(
            self.save_push_button.sizePolicy().hasHeightForWidth()
        )
        self.save_push_button.setSizePolicy(sizePolicy1)
        self.save_push_button.setMinimumSize(QSize(100, 25))
        self.save_push_button.setMaximumSize(QSize(100, 25))
        self.save_push_button.setFont(font)

        self.horizontalLayout.addWidget(self.save_push_button)

        self.cm_tab_widget.addTab(self.create_widget, "")
        self.manage_widget = QWidget()
        self.manage_widget.setObjectName(u"manage_widget")
        self.layoutWidget3 = QWidget(self.manage_widget)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(0, 10, 931, 531))
        self.manage_h_layout = QHBoxLayout(self.layoutWidget3)
        self.manage_h_layout.setObjectName(u"manage_h_layout")
        self.manage_h_layout.setContentsMargins(0, 0, 0, 0)
        self.exit_create_v_layout = QVBoxLayout()
        self.exit_create_v_layout.setSpacing(0)
        self.exit_create_v_layout.setObjectName(u"exit_create_v_layout")
        self.exit_create_v_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.exit_group_box = QGroupBox(self.layoutWidget3)
        self.exit_group_box.setObjectName(u"exit_group_box")
        sizePolicy1.setHeightForWidth(
            self.exit_group_box.sizePolicy().hasHeightForWidth()
        )
        self.exit_group_box.setSizePolicy(sizePolicy1)
        self.exit_group_box.setMinimumSize(QSize(455, 325))
        self.exit_group_box.setMaximumSize(QSize(455, 325))
        self.exit_group_box.setFont(font)
        self.exit_list_widget = QListWidget(self.exit_group_box)
        self.exit_list_widget.setObjectName(u"exit_list_widget")
        self.exit_list_widget.setGeometry(QRect(10, 20, 438, 290))
        sizePolicy1.setHeightForWidth(
            self.exit_list_widget.sizePolicy().hasHeightForWidth()
        )
        self.exit_list_widget.setSizePolicy(sizePolicy1)
        self.exit_list_widget.setMinimumSize(QSize(438, 290))
        self.exit_list_widget.setMaximumSize(QSize(438, 290))

        self.exit_create_v_layout.addWidget(self.exit_group_box)

        self.create_group_box = QGroupBox(self.layoutWidget3)
        self.create_group_box.setObjectName(u"create_group_box")
        sizePolicy1.setHeightForWidth(
            self.create_group_box.sizePolicy().hasHeightForWidth()
        )
        self.create_group_box.setSizePolicy(sizePolicy1)
        self.create_group_box.setMinimumSize(QSize(455, 200))
        self.create_group_box.setMaximumSize(QSize(455, 200))
        self.create_group_box.setFont(font)
        self.create_list_widget = QListWidget(self.create_group_box)
        self.create_list_widget.setObjectName(u"create_list_widget")
        self.create_list_widget.setGeometry(QRect(10, 20, 438, 162))
        sizePolicy1.setHeightForWidth(
            self.create_list_widget.sizePolicy().hasHeightForWidth()
        )
        self.create_list_widget.setSizePolicy(sizePolicy1)
        self.create_list_widget.setMinimumSize(QSize(438, 162))
        self.create_list_widget.setMaximumSize(QSize(438, 160))

        self.exit_create_v_layout.addWidget(self.create_group_box)

        self.manage_h_layout.addLayout(self.exit_create_v_layout)

        self.run_group_box = QGroupBox(self.layoutWidget3)
        self.run_group_box.setObjectName(u"run_group_box")
        sizePolicy1.setHeightForWidth(
            self.run_group_box.sizePolicy().hasHeightForWidth()
        )
        self.run_group_box.setSizePolicy(sizePolicy1)
        self.run_group_box.setMinimumSize(QSize(458, 525))
        self.run_group_box.setMaximumSize(QSize(458, 525))
        self.run_group_box.setFont(font)
        self.run_list_widget = QListWidget(self.run_group_box)
        self.run_list_widget.setObjectName(u"run_list_widget")
        self.run_list_widget.setGeometry(QRect(10, 20, 438, 490))
        sizePolicy1.setHeightForWidth(
            self.run_list_widget.sizePolicy().hasHeightForWidth()
        )
        self.run_list_widget.setSizePolicy(sizePolicy1)
        self.run_list_widget.setMinimumSize(QSize(438, 490))
        self.run_list_widget.setMaximumSize(QSize(438, 490))

        self.manage_h_layout.addWidget(self.run_group_box)

        self.create_button_frame_2 = QFrame(self.manage_widget)
        self.create_button_frame_2.setObjectName(u"create_button_frame_2")
        self.create_button_frame_2.setGeometry(QRect(9, 539, 921, 41))
        self.create_button_frame_2.setFrameShape(QFrame.StyledPanel)
        self.create_button_frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayoutWidget_2 = QWidget(self.create_button_frame_2)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(0, 0, 921, 41))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_4 = QSpacerItem(
            386, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.start_push_button = QPushButton(self.horizontalLayoutWidget_2)
        self.start_push_button.setObjectName(u"start_push_button")
        sizePolicy1.setHeightForWidth(
            self.start_push_button.sizePolicy().hasHeightForWidth()
        )
        self.start_push_button.setSizePolicy(sizePolicy1)
        self.start_push_button.setMinimumSize(QSize(100, 25))
        self.start_push_button.setMaximumSize(QSize(100, 25))
        self.start_push_button.setFont(font)
        self.start_push_button.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_2.addWidget(self.start_push_button)

        self.horizontalSpacer_5 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.stop_push_button = QPushButton(self.horizontalLayoutWidget_2)
        self.stop_push_button.setObjectName(u"stop_push_button")
        sizePolicy1.setHeightForWidth(
            self.stop_push_button.sizePolicy().hasHeightForWidth()
        )
        self.stop_push_button.setSizePolicy(sizePolicy1)
        self.stop_push_button.setMinimumSize(QSize(100, 25))
        self.stop_push_button.setMaximumSize(QSize(100, 25))
        self.stop_push_button.setFont(font)

        self.horizontalLayout_2.addWidget(self.stop_push_button)

        self.horizontalSpacer_6 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

        self.delete_push_button = QPushButton(self.horizontalLayoutWidget_2)
        self.delete_push_button.setObjectName(u"delete_push_button")
        sizePolicy1.setHeightForWidth(
            self.delete_push_button.sizePolicy().hasHeightForWidth()
        )
        self.delete_push_button.setSizePolicy(sizePolicy1)
        self.delete_push_button.setMinimumSize(QSize(100, 25))
        self.delete_push_button.setMaximumSize(QSize(100, 25))
        self.delete_push_button.setFont(font)

        self.horizontalLayout_2.addWidget(self.delete_push_button)

        self.horizontalSpacer_7 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer_7)

        self.refresh_push_button = QPushButton(self.horizontalLayoutWidget_2)
        self.refresh_push_button.setObjectName(u"refresh_push_button")
        sizePolicy1.setHeightForWidth(
            self.refresh_push_button.sizePolicy().hasHeightForWidth()
        )
        self.refresh_push_button.setSizePolicy(sizePolicy1)
        self.refresh_push_button.setMinimumSize(QSize(100, 25))
        self.refresh_push_button.setMaximumSize(QSize(100, 25))

        self.horizontalLayout_2.addWidget(self.refresh_push_button)

        self.cm_tab_widget.addTab(self.manage_widget, "")

        self.op_main_v_layout.addWidget(self.cm_tab_widget)

        self.pdl_tab_widget = QTabWidget(self.layoutWidget1)
        self.pdl_tab_widget.setObjectName(u"pdl_tab_widget")
        sizePolicy1.setHeightForWidth(
            self.pdl_tab_widget.sizePolicy().hasHeightForWidth()
        )
        self.pdl_tab_widget.setSizePolicy(sizePolicy1)
        self.pdl_tab_widget.setMinimumSize(QSize(940, 319))
        self.pdl_tab_widget.setMaximumSize(QSize(940, 319))
        self.pdl_tab_widget.setFont(font)
        self.pdl_tab_widget.setStyleSheet(u"")
        self.prompt_widget = QWidget()
        self.prompt_widget.setObjectName(u"prompt_widget")
        self.prompt_text_browser = QTextBrowser(self.prompt_widget)
        self.prompt_text_browser.setObjectName(u"prompt_text_browser")
        self.prompt_text_browser.setGeometry(QRect(0, 0, 940, 297))
        sizePolicy1.setHeightForWidth(
            self.prompt_text_browser.sizePolicy().hasHeightForWidth()
        )
        self.prompt_text_browser.setSizePolicy(sizePolicy1)
        self.prompt_text_browser.setMinimumSize(QSize(940, 297))
        self.prompt_text_browser.setMaximumSize(QSize(940, 297))
        self.prompt_text_browser.setStyleSheet(u"")
        self.pdl_tab_widget.addTab(self.prompt_widget, "")
        self.detail_widget = QWidget()
        self.detail_widget.setObjectName(u"detail_widget")
        self.detail_text_browser = QTextBrowser(self.detail_widget)
        self.detail_text_browser.setObjectName(u"detail_text_browser")
        self.detail_text_browser.setGeometry(QRect(0, 0, 940, 297))
        sizePolicy1.setHeightForWidth(
            self.detail_text_browser.sizePolicy().hasHeightForWidth()
        )
        self.detail_text_browser.setSizePolicy(sizePolicy1)
        self.detail_text_browser.setMinimumSize(QSize(940, 297))
        self.detail_text_browser.setMaximumSize(QSize(940, 297))
        self.pdl_tab_widget.addTab(self.detail_widget, "")
        self.log_widget = QWidget()
        self.log_widget.setObjectName(u"log_widget")
        self.log_text_browser = QTextBrowser(self.log_widget)
        self.log_text_browser.setObjectName(u"log_text_browser")
        self.log_text_browser.setGeometry(QRect(0, 0, 940, 297))
        sizePolicy1.setHeightForWidth(
            self.log_text_browser.sizePolicy().hasHeightForWidth()
        )
        self.log_text_browser.setSizePolicy(sizePolicy1)
        self.log_text_browser.setMinimumSize(QSize(940, 297))
        self.log_text_browser.setMaximumSize(QSize(940, 297))
        self.pdl_tab_widget.addTab(self.log_widget, "")

        self.op_main_v_layout.addWidget(self.pdl_tab_widget)

        self.op_main_v_layout.setStretch(1, 5)

        self.retranslateUi(main_widget)

        self.cm_tab_widget.setCurrentIndex(0)
        self.pdl_tab_widget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(main_widget)

    # setupUi

    def retranslateUi(self, main_widget):
        main_widget.setWindowTitle(
            QCoreApplication.translate("main_widget", u"Robustar Launcher", None)
        )
        self.header_label.setText("")
        self.server_group_box.setTitle(
            QCoreApplication.translate("main_widget", u"Server", None)
        )
        # if QT_CONFIG(tooltip)
        self.name_label.setToolTip(
            QCoreApplication.translate(
                "main_widget", u"The name of the docker container", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.name_label.setText(
            QCoreApplication.translate("main_widget", u"Server Name", None)
        )
        self.name_line_edit.setText(
            QCoreApplication.translate("main_widget", u"robustar", None)
        )
        # if QT_CONFIG(tooltip)
        self.image_label.setToolTip(
            QCoreApplication.translate(
                "main_widget", u"The version of the docker image of the container", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.image_label.setText(
            QCoreApplication.translate("main_widget", u"Image Version", None)
        )
        self.image_combo_box.setProperty("placeholderText", "")
        # if QT_CONFIG(tooltip)
        self.port_label.setToolTip(
            QCoreApplication.translate(
                "main_widget", u"The port the docker container forwards to", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.port_label.setText(
            QCoreApplication.translate("main_widget", u"Port", None)
        )
        self.port_line_edit.setText(
            QCoreApplication.translate("main_widget", u"8000", None)
        )
        # if QT_CONFIG(tooltip)
        self.device_label.setToolTip(
            QCoreApplication.translate(
                "main_widget", u"The device on which the model will be created", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.device_label.setText(
            QCoreApplication.translate("main_widget", u"Device", None)
        )
        self.device_combo_box.setItemText(
            0, QCoreApplication.translate("main_widget", u"cpu", None)
        )

        self.device_combo_box.setCurrentText(
            QCoreApplication.translate("main_widget", u"cpu", None)
        )
        self.device_combo_box.setProperty("placeholderText", "")
        # if QT_CONFIG(tooltip)
        self.cls_label.setToolTip(
            QCoreApplication.translate(
                "main_widget", u"The number of classes of the data", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cls_label.setText(
            QCoreApplication.translate("main_widget", u"Class Number", None)
        )
        self.cls_line_edit.setText("")
        # if QT_CONFIG(tooltip)
        self.size_label.setToolTip(
            QCoreApplication.translate(
                "main_widget",
                u"The length of side of the input image of the model",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.size_label.setText(
            QCoreApplication.translate("main_widget", u"Image Size", None)
        )
        self.size_line_edit.setText("")
        # if QT_CONFIG(tooltip)
        self.pad_label.setToolTip(
            QCoreApplication.translate("main_widget", u"The mode of padding", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.pad_label.setText(
            QCoreApplication.translate("main_widget", u"Image Padding", None)
        )
        self.pad_combo_box.setItemText(
            0, QCoreApplication.translate("main_widget", u"short side", None)
        )
        self.pad_combo_box.setItemText(
            1, QCoreApplication.translate("main_widget", u"none", None)
        )

        self.pad_combo_box.setCurrentText(
            QCoreApplication.translate("main_widget", u"short side", None)
        )
        self.pad_combo_box.setProperty("placeholderText", "")
        self.dir_group_box.setTitle(
            QCoreApplication.translate("main_widget", u"Directory", None)
        )
        # if QT_CONFIG(tooltip)
        self.train_label.setToolTip(
            QCoreApplication.translate(
                "main_widget", u"The root path of the train set", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.train_label.setText(
            QCoreApplication.translate("main_widget", u"Train Set", None)
        )
        self.train_line_edit.setText("")
        self.train_push_button.setText(
            QCoreApplication.translate("main_widget", u"...", None)
        )
        # if QT_CONFIG(tooltip)
        self.val_label.setToolTip(
            QCoreApplication.translate(
                "main_widget", u"The root path of the validation set", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.val_label.setText(
            QCoreApplication.translate("main_widget", u"Validation Set", None)
        )
        self.val_line_edit.setText("")
        self.val_push_button.setText(
            QCoreApplication.translate("main_widget", u"...", None)
        )
        # if QT_CONFIG(tooltip)
        self.test_label.setToolTip(
            QCoreApplication.translate(
                "main_widget", u"The root path of the test set", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.test_label.setText(
            QCoreApplication.translate("main_widget", u"Test Set", None)
        )
        self.test_line_edit.setText("")
        self.test_push_button.setText(
            QCoreApplication.translate("main_widget", u"...", None)
        )
        # if QT_CONFIG(tooltip)
        self.paired_label.setToolTip(
            QCoreApplication.translate(
                "main_widget", u"The root path of the paired set", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.paired_label.setText(
            QCoreApplication.translate("main_widget", u"Paired Set", None)
        )
        self.paired_line_edit.setText("")
        self.paired_push_button.setText(
            QCoreApplication.translate("main_widget", u"...", None)
        )
        # if QT_CONFIG(tooltip)
        self.inf_label.setToolTip(
            QCoreApplication.translate(
                "main_widget",
                u"The root path for all influence result calculated by Robustar",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.inf_label.setText(
            QCoreApplication.translate("main_widget", u"Influence Result", None)
        )
        self.inf_line_edit.setText("")
        self.inf_push_button.setText(
            QCoreApplication.translate("main_widget", u"...", None)
        )
        # if QT_CONFIG(tooltip)
        self.out_label.setToolTip(
            QCoreApplication.translate(
                "main_widget", u"The root path of the generated files", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.out_label.setText(
            QCoreApplication.translate("main_widget", u"Output", None)
        )
        self.out_line_edit.setText("")
        self.out_push_button.setText(
            QCoreApplication.translate("main_widget", u"...", None)
        )
        self.create_push_button.setText(
            QCoreApplication.translate("main_widget", u"Create Server", None)
        )
        self.load_push_button.setText(
            QCoreApplication.translate("main_widget", u"Load Profile", None)
        )
        self.save_push_button.setText(
            QCoreApplication.translate("main_widget", u"Save Profile", None)
        )
        self.cm_tab_widget.setTabText(
            self.cm_tab_widget.indexOf(self.create_widget),
            QCoreApplication.translate("main_widget", u"Create", None),
        )
        self.exit_group_box.setTitle(
            QCoreApplication.translate("main_widget", u"Exited", None)
        )
        self.create_group_box.setTitle(
            QCoreApplication.translate("main_widget", u"Created", None)
        )
        self.run_group_box.setTitle(
            QCoreApplication.translate("main_widget", u"Running", None)
        )
        self.start_push_button.setText(
            QCoreApplication.translate("main_widget", u"Start Server", None)
        )
        self.stop_push_button.setText(
            QCoreApplication.translate("main_widget", u"Stop Server", None)
        )
        self.delete_push_button.setText(
            QCoreApplication.translate("main_widget", u"Delete Server", None)
        )
        self.refresh_push_button.setText(
            QCoreApplication.translate("main_widget", u"Refresh", None)
        )
        self.cm_tab_widget.setTabText(
            self.cm_tab_widget.indexOf(self.manage_widget),
            QCoreApplication.translate("main_widget", u"Manage", None),
        )
        self.pdl_tab_widget.setTabText(
            self.pdl_tab_widget.indexOf(self.prompt_widget),
            QCoreApplication.translate("main_widget", u"Prompts", None),
        )
        self.pdl_tab_widget.setTabText(
            self.pdl_tab_widget.indexOf(self.detail_widget),
            QCoreApplication.translate("main_widget", u"Details", None),
        )
        self.pdl_tab_widget.setTabText(
            self.pdl_tab_widget.indexOf(self.log_widget),
            QCoreApplication.translate("main_widget", u"Logs", None),
        )

    # retranslateUi
