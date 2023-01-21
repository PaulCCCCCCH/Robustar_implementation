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
        main_widget.setStyleSheet(u"QWidget{font: 8pt \"Arial\"}\n"
"QPushButton{background-color: #E1E1E1; \n"
"			font: 8pt Arial;\n"
"			border: 1px solid #ADADAD;}\n"
"QPushButton:hover {\n"
"   background-color: #E3ECF3;\n"
"   border: 1px solid #3287CA;\n"
"}")
        self.layoutWidget = QWidget(main_widget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 1001, 1001))
        self.ui_v_layout = QVBoxLayout(self.layoutWidget)
        self.ui_v_layout.setObjectName(u"ui_v_layout")
        self.ui_v_layout.setContentsMargins(0, 0, 0, 0)
        self.header_h_layout = QHBoxLayout()
        self.header_h_layout.setObjectName(u"header_h_layout")
        self.header_label = QLabel(self.layoutWidget)
        self.header_label.setObjectName(u"header_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.header_label.sizePolicy().hasHeightForWidth())
        self.header_label.setSizePolicy(sizePolicy1)
        self.header_label.setMinimumSize(QSize(164, 42))
        self.header_label.setMaximumSize(QSize(164, 42))
        self.header_label.setTextFormat(Qt.AutoText)
        self.header_label.setPixmap(QPixmap(u":/resources/logo_long.png"))
        self.header_label.setScaledContents(True)
        self.header_label.setIndent(-1)

        self.header_h_layout.addWidget(self.header_label)


        self.ui_v_layout.addLayout(self.header_h_layout)

        self.op_h_layout = QHBoxLayout()
        self.op_h_layout.setObjectName(u"op_h_layout")
        self.op_h_layout.setContentsMargins(15, -1, 11, -1)
        self.op_button_frame = QFrame(self.layoutWidget)
        self.op_button_frame.setObjectName(u"op_button_frame")
        sizePolicy1.setHeightForWidth(self.op_button_frame.sizePolicy().hasHeightForWidth())
        self.op_button_frame.setSizePolicy(sizePolicy1)
        self.op_button_frame.setMinimumSize(QSize(161, 905))
        self.op_button_frame.setMaximumSize(QSize(161, 905))
        self.op_button_frame.setFont(font)
        self.op_button_frame.setStyleSheet(u"#buttonFrame{background: #F9F9F9}\n"
"")
        self.op_button_frame.setFrameShape(QFrame.StyledPanel)
        self.op_button_frame.setFrameShadow(QFrame.Raised)
        self.layoutWidget1 = QWidget(self.op_button_frame)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(0, 0, 161, 901))
        self.op_button_v_layout = QVBoxLayout(self.layoutWidget1)
        self.op_button_v_layout.setSpacing(60)
        self.op_button_v_layout.setObjectName(u"op_button_v_layout")
        self.op_button_v_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.op_button_v_layout.setContentsMargins(0, 60, 0, 0)
        self.load_h_layout = QHBoxLayout()
        self.load_h_layout.setObjectName(u"load_h_layout")
        self.load_h_layout.setContentsMargins(-1, 0, -1, -1)
        self.load_left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.load_h_layout.addItem(self.load_left_spacer)

        self.load_push_button = QPushButton(self.layoutWidget1)
        self.load_push_button.setObjectName(u"load_push_button")
        sizePolicy1.setHeightForWidth(self.load_push_button.sizePolicy().hasHeightForWidth())
        self.load_push_button.setSizePolicy(sizePolicy1)
        self.load_push_button.setMinimumSize(QSize(100, 25))
        self.load_push_button.setMaximumSize(QSize(100, 25))
        self.load_push_button.setFont(font)
        self.load_push_button.setStyleSheet(u"")

        self.load_h_layout.addWidget(self.load_push_button)

        self.load_right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.load_h_layout.addItem(self.load_right_spacer)


        self.op_button_v_layout.addLayout(self.load_h_layout)

        self.save_h_layout = QHBoxLayout()
        self.save_h_layout.setObjectName(u"save_h_layout")
        self.save_left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.save_h_layout.addItem(self.save_left_spacer)

        self.save_push_button = QPushButton(self.layoutWidget1)
        self.save_push_button.setObjectName(u"save_push_button")
        sizePolicy1.setHeightForWidth(self.save_push_button.sizePolicy().hasHeightForWidth())
        self.save_push_button.setSizePolicy(sizePolicy1)
        self.save_push_button.setMinimumSize(QSize(100, 25))
        self.save_push_button.setMaximumSize(QSize(100, 25))
        self.save_push_button.setFont(font)

        self.save_h_layout.addWidget(self.save_push_button)

        self.save_right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.save_h_layout.addItem(self.save_right_spacer)


        self.op_button_v_layout.addLayout(self.save_h_layout)

        self.start_h_layout = QHBoxLayout()
        self.start_h_layout.setObjectName(u"start_h_layout")
        self.start_left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.start_h_layout.addItem(self.start_left_spacer)

        self.start_push_button = QPushButton(self.layoutWidget1)
        self.start_push_button.setObjectName(u"start_push_button")
        sizePolicy1.setHeightForWidth(self.start_push_button.sizePolicy().hasHeightForWidth())
        self.start_push_button.setSizePolicy(sizePolicy1)
        self.start_push_button.setMinimumSize(QSize(100, 25))
        self.start_push_button.setMaximumSize(QSize(100, 25))
        self.start_push_button.setFont(font)
        self.start_push_button.setLayoutDirection(Qt.LeftToRight)

        self.start_h_layout.addWidget(self.start_push_button)

        self.start_right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.start_h_layout.addItem(self.start_right_spacer)


        self.op_button_v_layout.addLayout(self.start_h_layout)

        self.stop_h_layout = QHBoxLayout()
        self.stop_h_layout.setObjectName(u"stop_h_layout")
        self.stop_left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.stop_h_layout.addItem(self.stop_left_spacer)

        self.stop_push_button = QPushButton(self.layoutWidget1)
        self.stop_push_button.setObjectName(u"stop_push_button")
        sizePolicy1.setHeightForWidth(self.stop_push_button.sizePolicy().hasHeightForWidth())
        self.stop_push_button.setSizePolicy(sizePolicy1)
        self.stop_push_button.setMinimumSize(QSize(100, 25))
        self.stop_push_button.setMaximumSize(QSize(100, 25))
        self.stop_push_button.setFont(font)

        self.stop_h_layout.addWidget(self.stop_push_button)

        self.stop_right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.stop_h_layout.addItem(self.stop_right_spacer)


        self.op_button_v_layout.addLayout(self.stop_h_layout)

        self.delete_h_layout = QHBoxLayout()
        self.delete_h_layout.setObjectName(u"delete_h_layout")
        self.delete_left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.delete_h_layout.addItem(self.delete_left_spacer)

        self.delete_push_button = QPushButton(self.layoutWidget1)
        self.delete_push_button.setObjectName(u"delete_push_button")
        sizePolicy1.setHeightForWidth(self.delete_push_button.sizePolicy().hasHeightForWidth())
        self.delete_push_button.setSizePolicy(sizePolicy1)
        self.delete_push_button.setMinimumSize(QSize(100, 25))
        self.delete_push_button.setMaximumSize(QSize(100, 25))
        self.delete_push_button.setFont(font)

        self.delete_h_layout.addWidget(self.delete_push_button)

        self.delete_right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.delete_h_layout.addItem(self.delete_right_spacer)


        self.op_button_v_layout.addLayout(self.delete_h_layout)

        self.button_v_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.op_button_v_layout.addItem(self.button_v_spacer)

        self.op_button_v_layout.setStretch(0, 1)
        self.op_button_v_layout.setStretch(1, 1)
        self.op_button_v_layout.setStretch(2, 1)
        self.op_button_v_layout.setStretch(3, 1)
        self.op_button_v_layout.setStretch(4, 1)
        self.op_button_v_layout.setStretch(5, 2)

        self.op_h_layout.addWidget(self.op_button_frame)

        self.op_main_v_layout = QVBoxLayout()
        self.op_main_v_layout.setObjectName(u"op_main_v_layout")
        self.op_main_v_layout.setContentsMargins(-1, 0, -1, 0)
        self.cm_tab_widget = QTabWidget(self.layoutWidget)
        self.cm_tab_widget.setObjectName(u"cm_tab_widget")
        sizePolicy1.setHeightForWidth(self.cm_tab_widget.sizePolicy().hasHeightForWidth())
        self.cm_tab_widget.setSizePolicy(sizePolicy1)
        self.cm_tab_widget.setMinimumSize(QSize(801, 575))
        self.cm_tab_widget.setMaximumSize(QSize(801, 575))
        self.cm_tab_widget.setFont(font)
        self.create_widget = QWidget()
        self.create_widget.setObjectName(u"create_widget")
        self.layoutWidget2 = QWidget(self.create_widget)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(21, 11, 761, 529))
        self.create_h_layout = QHBoxLayout(self.layoutWidget2)
        self.create_h_layout.setSpacing(9)
        self.create_h_layout.setObjectName(u"create_h_layout")
        self.create_h_layout.setContentsMargins(0, 0, 0, 0)
        self.docker_data_v_layout = QVBoxLayout()
        self.docker_data_v_layout.setSpacing(0)
        self.docker_data_v_layout.setObjectName(u"docker_data_v_layout")
        self.docker_data_v_layout.setContentsMargins(-1, 0, -1, -1)
        self.docker_group_box = QGroupBox(self.layoutWidget2)
        self.docker_group_box.setObjectName(u"docker_group_box")
        sizePolicy.setHeightForWidth(self.docker_group_box.sizePolicy().hasHeightForWidth())
        self.docker_group_box.setSizePolicy(sizePolicy)
        self.docker_group_box.setMinimumSize(QSize(0, 169))
        self.docker_group_box.setMaximumSize(QSize(16777215, 168))
        self.docker_group_box.setFont(font)
        self.layoutWidget3 = QWidget(self.docker_group_box)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(10, 20, 362, 143))
        self.docker_v_layout = QVBoxLayout(self.layoutWidget3)
        self.docker_v_layout.setObjectName(u"docker_v_layout")
        self.docker_v_layout.setContentsMargins(0, 0, 0, 0)
        self.name_h_layout = QHBoxLayout()
        self.name_h_layout.setObjectName(u"name_h_layout")
        self.name_label = QLabel(self.layoutWidget3)
        self.name_label.setObjectName(u"name_label")
        sizePolicy1.setHeightForWidth(self.name_label.sizePolicy().hasHeightForWidth())
        self.name_label.setSizePolicy(sizePolicy1)
        self.name_label.setMinimumSize(QSize(174, 39))
        self.name_label.setMaximumSize(QSize(174, 39))
        self.name_label.setFont(font)

        self.name_h_layout.addWidget(self.name_label)

        self.name_line_edit = QLineEdit(self.layoutWidget3)
        self.name_line_edit.setObjectName(u"name_line_edit")
        sizePolicy1.setHeightForWidth(self.name_line_edit.sizePolicy().hasHeightForWidth())
        self.name_line_edit.setSizePolicy(sizePolicy1)
        self.name_line_edit.setMinimumSize(QSize(174, 24))
        self.name_line_edit.setMaximumSize(QSize(174, 24))
        self.name_line_edit.setFont(font)
        self.name_line_edit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.name_line_edit.setClearButtonEnabled(True)

        self.name_h_layout.addWidget(self.name_line_edit)


        self.docker_v_layout.addLayout(self.name_h_layout)

        self.image_h_layout = QHBoxLayout()
        self.image_h_layout.setObjectName(u"image_h_layout")
        self.image_label = QLabel(self.layoutWidget3)
        self.image_label.setObjectName(u"image_label")
        sizePolicy1.setHeightForWidth(self.image_label.sizePolicy().hasHeightForWidth())
        self.image_label.setSizePolicy(sizePolicy1)
        self.image_label.setMinimumSize(QSize(174, 39))
        self.image_label.setMaximumSize(QSize(174, 39))
        self.image_label.setFont(font)

        self.image_h_layout.addWidget(self.image_label)

        self.image_combo_box = QComboBox(self.layoutWidget3)
        self.image_combo_box.setObjectName(u"image_combo_box")
        sizePolicy1.setHeightForWidth(self.image_combo_box.sizePolicy().hasHeightForWidth())
        self.image_combo_box.setSizePolicy(sizePolicy1)
        self.image_combo_box.setMinimumSize(QSize(174, 24))
        self.image_combo_box.setMaximumSize(QSize(174, 24))
        self.image_combo_box.setFont(font)

        self.image_h_layout.addWidget(self.image_combo_box)


        self.docker_v_layout.addLayout(self.image_h_layout)

        self.port_h_layout = QHBoxLayout()
        self.port_h_layout.setObjectName(u"port_h_layout")
        self.port_label = QLabel(self.layoutWidget3)
        self.port_label.setObjectName(u"port_label")
        sizePolicy1.setHeightForWidth(self.port_label.sizePolicy().hasHeightForWidth())
        self.port_label.setSizePolicy(sizePolicy1)
        self.port_label.setMinimumSize(QSize(174, 39))
        self.port_label.setMaximumSize(QSize(174, 39))
        self.port_label.setFont(font)

        self.port_h_layout.addWidget(self.port_label)

        self.port_line_edit = QLineEdit(self.layoutWidget3)
        self.port_line_edit.setObjectName(u"port_line_edit")
        sizePolicy1.setHeightForWidth(self.port_line_edit.sizePolicy().hasHeightForWidth())
        self.port_line_edit.setSizePolicy(sizePolicy1)
        self.port_line_edit.setMinimumSize(QSize(174, 24))
        self.port_line_edit.setMaximumSize(QSize(174, 24))
        self.port_line_edit.setFont(font)
        self.port_line_edit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.port_line_edit.setClearButtonEnabled(True)

        self.port_h_layout.addWidget(self.port_line_edit)


        self.docker_v_layout.addLayout(self.port_h_layout)


        self.docker_data_v_layout.addWidget(self.docker_group_box)

        self.docker_data_v_spacer = QSpacerItem(20, 132, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.docker_data_v_layout.addItem(self.docker_data_v_spacer)

        self.data_group_box = QGroupBox(self.layoutWidget2)
        self.data_group_box.setObjectName(u"data_group_box")
        self.data_group_box.setMinimumSize(QSize(0, 0))
        self.data_group_box.setMaximumSize(QSize(16777215, 232))
        self.data_group_box.setFont(font)
        self.layoutWidget4 = QWidget(self.data_group_box)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(10, 20, 361, 201))
        self.data_v_layout = QVBoxLayout(self.layoutWidget4)
        self.data_v_layout.setSpacing(9)
        self.data_v_layout.setObjectName(u"data_v_layout")
        self.data_v_layout.setContentsMargins(0, 0, 0, 0)
        self.train_h_layout = QHBoxLayout()
        self.train_h_layout.setObjectName(u"train_h_layout")
        self.train_h_layout.setContentsMargins(0, -1, -1, -1)
        self.train_label = QLabel(self.layoutWidget4)
        self.train_label.setObjectName(u"train_label")
        sizePolicy1.setHeightForWidth(self.train_label.sizePolicy().hasHeightForWidth())
        self.train_label.setSizePolicy(sizePolicy1)
        self.train_label.setMinimumSize(QSize(174, 39))
        self.train_label.setMaximumSize(QSize(174, 39))
        self.train_label.setFont(font)

        self.train_h_layout.addWidget(self.train_label)

        self.train_line_edit = QLineEdit(self.layoutWidget4)
        self.train_line_edit.setObjectName(u"train_line_edit")
        sizePolicy1.setHeightForWidth(self.train_line_edit.sizePolicy().hasHeightForWidth())
        self.train_line_edit.setSizePolicy(sizePolicy1)
        self.train_line_edit.setMinimumSize(QSize(137, 24))
        self.train_line_edit.setMaximumSize(QSize(137, 24))
        self.train_line_edit.setFont(font)
        self.train_line_edit.setMouseTracking(True)
        self.train_line_edit.setReadOnly(False)

        self.train_h_layout.addWidget(self.train_line_edit)

        self.train_push_button = QPushButton(self.layoutWidget4)
        self.train_push_button.setObjectName(u"train_push_button")
        sizePolicy1.setHeightForWidth(self.train_push_button.sizePolicy().hasHeightForWidth())
        self.train_push_button.setSizePolicy(sizePolicy1)
        self.train_push_button.setMinimumSize(QSize(28, 20))
        self.train_push_button.setMaximumSize(QSize(28, 20))
        self.train_push_button.setFont(font)

        self.train_h_layout.addWidget(self.train_push_button)


        self.data_v_layout.addLayout(self.train_h_layout)

        self.val_h_layout = QHBoxLayout()
        self.val_h_layout.setObjectName(u"val_h_layout")
        self.val_h_layout.setContentsMargins(-1, -1, 0, -1)
        self.val_label = QLabel(self.layoutWidget4)
        self.val_label.setObjectName(u"val_label")
        sizePolicy1.setHeightForWidth(self.val_label.sizePolicy().hasHeightForWidth())
        self.val_label.setSizePolicy(sizePolicy1)
        self.val_label.setMinimumSize(QSize(174, 39))
        self.val_label.setMaximumSize(QSize(174, 39))
        self.val_label.setFont(font)

        self.val_h_layout.addWidget(self.val_label)

        self.val_line_edit = QLineEdit(self.layoutWidget4)
        self.val_line_edit.setObjectName(u"val_line_edit")
        sizePolicy1.setHeightForWidth(self.val_line_edit.sizePolicy().hasHeightForWidth())
        self.val_line_edit.setSizePolicy(sizePolicy1)
        self.val_line_edit.setMinimumSize(QSize(137, 24))
        self.val_line_edit.setMaximumSize(QSize(137, 24))
        self.val_line_edit.setFont(font)

        self.val_h_layout.addWidget(self.val_line_edit)

        self.val_push_button = QPushButton(self.layoutWidget4)
        self.val_push_button.setObjectName(u"val_push_button")
        sizePolicy1.setHeightForWidth(self.val_push_button.sizePolicy().hasHeightForWidth())
        self.val_push_button.setSizePolicy(sizePolicy1)
        self.val_push_button.setMinimumSize(QSize(28, 20))
        self.val_push_button.setMaximumSize(QSize(28, 20))
        self.val_push_button.setFont(font)

        self.val_h_layout.addWidget(self.val_push_button)


        self.data_v_layout.addLayout(self.val_h_layout)

        self.test_h_layout = QHBoxLayout()
        self.test_h_layout.setObjectName(u"test_h_layout")
        self.test_h_layout.setContentsMargins(-1, -1, 0, -1)
        self.test_label = QLabel(self.layoutWidget4)
        self.test_label.setObjectName(u"test_label")
        sizePolicy1.setHeightForWidth(self.test_label.sizePolicy().hasHeightForWidth())
        self.test_label.setSizePolicy(sizePolicy1)
        self.test_label.setMinimumSize(QSize(174, 39))
        self.test_label.setMaximumSize(QSize(174, 39))
        self.test_label.setFont(font)

        self.test_h_layout.addWidget(self.test_label)

        self.test_line_edit = QLineEdit(self.layoutWidget4)
        self.test_line_edit.setObjectName(u"test_line_edit")
        sizePolicy1.setHeightForWidth(self.test_line_edit.sizePolicy().hasHeightForWidth())
        self.test_line_edit.setSizePolicy(sizePolicy1)
        self.test_line_edit.setMinimumSize(QSize(137, 24))
        self.test_line_edit.setMaximumSize(QSize(137, 24))
        self.test_line_edit.setFont(font)

        self.test_h_layout.addWidget(self.test_line_edit)

        self.test_push_button = QPushButton(self.layoutWidget4)
        self.test_push_button.setObjectName(u"test_push_button")
        sizePolicy1.setHeightForWidth(self.test_push_button.sizePolicy().hasHeightForWidth())
        self.test_push_button.setSizePolicy(sizePolicy1)
        self.test_push_button.setMinimumSize(QSize(28, 20))
        self.test_push_button.setMaximumSize(QSize(28, 20))
        self.test_push_button.setFont(font)

        self.test_h_layout.addWidget(self.test_push_button)
        

        self.data_v_layout.addLayout(self.test_h_layout)

        self.paired_h_layout = QHBoxLayout()
        self.paired_h_layout.setObjectName(u"paired_h_layout")
        self.paired_h_layout.setContentsMargins(-1, -1, 0, -1)
        self.paired_label = QLabel(self.layoutWidget4)
        self.paired_label.setObjectName(u"paired_label")
        sizePolicy1.setHeightForWidth(self.paired_label.sizePolicy().hasHeightForWidth())
        self.paired_label.setSizePolicy(sizePolicy1)
        self.paired_label.setMinimumSize(QSize(174, 39))
        self.paired_label.setMaximumSize(QSize(174, 39))
        self.paired_label.setFont(font)

        self.paired_h_layout.addWidget(self.paired_label)

        self.paired_line_edit = QLineEdit(self.layoutWidget4)
        self.paired_line_edit.setObjectName(u"paired_line_edit")
        sizePolicy1.setHeightForWidth(self.paired_line_edit.sizePolicy().hasHeightForWidth())
        self.paired_line_edit.setSizePolicy(sizePolicy1)
        self.paired_line_edit.setMinimumSize(QSize(137, 24))
        self.paired_line_edit.setMaximumSize(QSize(137, 24))
        self.paired_line_edit.setFont(font)

        self.paired_h_layout.addWidget(self.paired_line_edit)

        self.paired_push_button = QPushButton(self.layoutWidget4)
        self.paired_push_button.setObjectName(u"paired_push_button")
        sizePolicy1.setHeightForWidth(self.paired_push_button.sizePolicy().hasHeightForWidth())
        self.paired_push_button.setSizePolicy(sizePolicy1)
        self.paired_push_button.setMinimumSize(QSize(28, 20))
        self.paired_push_button.setMaximumSize(QSize(28, 20))
        self.paired_push_button.setFont(font)

        self.paired_h_layout.addWidget(self.paired_push_button)


        self.data_v_layout.addLayout(self.paired_h_layout)

        self.gen_h_layout = QHBoxLayout()
        self.gen_h_layout.setObjectName(u"gen_h_layout")
        self.gen_h_layout.setContentsMargins(-1, -1, 0, -1)
        self.gen_label = QLabel(self.layoutWidget4)
        self.gen_label.setObjectName(u"gen_label")
        sizePolicy1.setHeightForWidth(self.gen_label.sizePolicy().hasHeightForWidth())
        self.gen_label.setSizePolicy(sizePolicy1)
        self.gen_label.setMinimumSize(QSize(174, 39))
        self.gen_label.setMaximumSize(QSize(174, 39))
        self.gen_label.setFont(font)

        self.gen_h_layout.addWidget(self.gen_label)

        self.gen_line_edit = QLineEdit(self.layoutWidget4)
        self.gen_line_edit.setObjectName(u"gen_line_edit")
        sizePolicy1.setHeightForWidth(self.gen_line_edit.sizePolicy().hasHeightForWidth())
        self.gen_line_edit.setSizePolicy(sizePolicy1)
        self.gen_line_edit.setMinimumSize(QSize(137, 24))
        self.gen_line_edit.setMaximumSize(QSize(137, 24))
        self.gen_line_edit.setFont(font)

        self.gen_h_layout.addWidget(self.gen_line_edit)

        self.gen_push_button = QPushButton(self.layoutWidget4)
        self.gen_push_button.setObjectName(u"gen_push_button")
        sizePolicy1.setHeightForWidth(self.gen_push_button.sizePolicy().hasHeightForWidth())
        self.gen_push_button.setSizePolicy(sizePolicy1)
        self.gen_push_button.setMinimumSize(QSize(28, 20))
        self.gen_push_button.setMaximumSize(QSize(28, 20))
        self.gen_push_button.setFont(font)

        self.gen_h_layout.addWidget(self.gen_push_button)


        self.data_v_layout.addLayout(self.gen_h_layout)

        self.ckpt_h_layout = QHBoxLayout()
        self.ckpt_h_layout.setObjectName(u"ckpt_h_layout")
        self.ckpt_label = QLabel(self.layoutWidget4)
        self.ckpt_label.setObjectName(u"ckpt_label")
        sizePolicy1.setHeightForWidth(self.ckpt_label.sizePolicy().hasHeightForWidth())
        self.ckpt_label.setSizePolicy(sizePolicy1)
        self.ckpt_label.setMinimumSize(QSize(174, 39))
        self.ckpt_label.setMaximumSize(QSize(174, 39))
        self.ckpt_label.setFont(font)

        self.ckpt_h_layout.addWidget(self.ckpt_label)

        self.ckpt_line_edit = QLineEdit(self.layoutWidget4)
        self.ckpt_line_edit.setObjectName(u"ckpt_line_edit")
        sizePolicy1.setHeightForWidth(self.ckpt_line_edit.sizePolicy().hasHeightForWidth())
        self.ckpt_line_edit.setSizePolicy(sizePolicy1)
        self.ckpt_line_edit.setMinimumSize(QSize(137, 24))
        self.ckpt_line_edit.setMaximumSize(QSize(137, 24))
        self.ckpt_line_edit.setFont(font)

        self.ckpt_h_layout.addWidget(self.ckpt_line_edit)

        self.ckpt_push_button = QPushButton(self.layoutWidget4)
        self.ckpt_push_button.setObjectName(u"ckpt_push_button")
        sizePolicy1.setHeightForWidth(self.ckpt_push_button.sizePolicy().hasHeightForWidth())
        self.ckpt_push_button.setSizePolicy(sizePolicy1)
        self.ckpt_push_button.setMinimumSize(QSize(28, 20))
        self.ckpt_push_button.setMaximumSize(QSize(28, 20))
        self.ckpt_push_button.setFont(font)

        self.ckpt_h_layout.addWidget(self.ckpt_push_button)


        self.data_v_layout.addLayout(self.ckpt_h_layout)

        self.inf_h_layout = QHBoxLayout()
        self.inf_h_layout.setObjectName(u"inf_h_layout")
        self.inf_label = QLabel(self.layoutWidget4)
        self.inf_label.setObjectName(u"inf_label")
        sizePolicy1.setHeightForWidth(self.inf_label.sizePolicy().hasHeightForWidth())
        self.inf_label.setSizePolicy(sizePolicy1)
        self.inf_label.setMinimumSize(QSize(174, 39))
        self.inf_label.setMaximumSize(QSize(174, 39))
        self.inf_label.setFont(font)

        self.inf_h_layout.addWidget(self.inf_label)

        self.inf_line_edit = QLineEdit(self.layoutWidget4)
        self.inf_line_edit.setObjectName(u"inf_line_edit")
        sizePolicy1.setHeightForWidth(self.inf_line_edit.sizePolicy().hasHeightForWidth())
        self.inf_line_edit.setSizePolicy(sizePolicy1)
        self.inf_line_edit.setMinimumSize(QSize(137, 24))
        self.inf_line_edit.setMaximumSize(QSize(137, 24))
        self.inf_line_edit.setFont(font)

        self.inf_h_layout.addWidget(self.inf_line_edit)

        self.inf_push_button = QPushButton(self.layoutWidget4)
        self.inf_push_button.setObjectName(u"inf_push_button")
        sizePolicy1.setHeightForWidth(self.inf_push_button.sizePolicy().hasHeightForWidth())
        self.inf_push_button.setSizePolicy(sizePolicy1)
        self.inf_push_button.setMinimumSize(QSize(28, 20))
        self.inf_push_button.setMaximumSize(QSize(28, 20))
        self.inf_push_button.setFont(font)

        self.inf_h_layout.addWidget(self.inf_push_button)


        self.data_v_layout.addLayout(self.inf_h_layout)


        self.docker_data_v_layout.addWidget(self.data_group_box)


        self.create_h_layout.addLayout(self.docker_data_v_layout)

        self.model_v_layout_2 = QVBoxLayout()
        self.model_v_layout_2.setObjectName(u"model_v_layout_2")
        self.model_group_box = QGroupBox(self.layoutWidget2)
        self.model_group_box.setObjectName(u"model_group_box")
        sizePolicy1.setHeightForWidth(self.model_group_box.sizePolicy().hasHeightForWidth())
        self.model_group_box.setSizePolicy(sizePolicy1)
        self.model_group_box.setMinimumSize(QSize(372, 525))
        self.model_group_box.setMaximumSize(QSize(372, 525))
        self.model_group_box.setFont(font)
        self.layoutWidget_2 = QWidget(self.model_group_box)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(10, 20, 362, 493))
        self.model_v_layout = QVBoxLayout(self.layoutWidget_2)
        self.model_v_layout.setObjectName(u"model_v_layout")
        self.model_v_layout.setContentsMargins(0, 0, 0, 0)
        self.arch_h_layout = QHBoxLayout()
        self.arch_h_layout.setObjectName(u"arch_h_layout")
        self.arch_label = QLabel(self.layoutWidget_2)
        self.arch_label.setObjectName(u"arch_label")
        sizePolicy1.setHeightForWidth(self.arch_label.sizePolicy().hasHeightForWidth())
        self.arch_label.setSizePolicy(sizePolicy1)
        self.arch_label.setMinimumSize(QSize(174, 39))
        self.arch_label.setMaximumSize(QSize(174, 39))
        self.arch_label.setFont(font)

        self.arch_h_layout.addWidget(self.arch_label)

        self.arch_combo_box = QComboBox(self.layoutWidget_2)
        self.arch_combo_box.addItem("")
        self.arch_combo_box.addItem("")
        self.arch_combo_box.addItem("")
        self.arch_combo_box.addItem("")
        self.arch_combo_box.addItem("")
        self.arch_combo_box.addItem("")
        self.arch_combo_box.addItem("")
        self.arch_combo_box.addItem("")
        self.arch_combo_box.setObjectName(u"arch_combo_box")
        sizePolicy1.setHeightForWidth(self.arch_combo_box.sizePolicy().hasHeightForWidth())
        self.arch_combo_box.setSizePolicy(sizePolicy1)
        self.arch_combo_box.setMinimumSize(QSize(174, 24))
        self.arch_combo_box.setMaximumSize(QSize(174, 24))
        self.arch_combo_box.setFont(font)

        self.arch_h_layout.addWidget(self.arch_combo_box)


        self.model_v_layout.addLayout(self.arch_h_layout)

        self.pretrain_h_layout = QHBoxLayout()
        self.pretrain_h_layout.setObjectName(u"pretrain_h_layout")
        self.pretrain_label = QLabel(self.layoutWidget_2)
        self.pretrain_label.setObjectName(u"pretrain_label")
        sizePolicy1.setHeightForWidth(self.pretrain_label.sizePolicy().hasHeightForWidth())
        self.pretrain_label.setSizePolicy(sizePolicy1)
        self.pretrain_label.setMinimumSize(QSize(174, 39))
        self.pretrain_label.setMaximumSize(QSize(174, 39))
        self.pretrain_label.setFont(font)

        self.pretrain_h_layout.addWidget(self.pretrain_label)

        self.pretrain_check_box = QCheckBox(self.layoutWidget_2)
        self.pretrain_check_box.setObjectName(u"pretrain_check_box")
        sizePolicy1.setHeightForWidth(self.pretrain_check_box.sizePolicy().hasHeightForWidth())
        self.pretrain_check_box.setSizePolicy(sizePolicy1)
        self.pretrain_check_box.setMinimumSize(QSize(174, 24))
        self.pretrain_check_box.setMaximumSize(QSize(174, 24))

        self.pretrain_h_layout.addWidget(self.pretrain_check_box)


        self.model_v_layout.addLayout(self.pretrain_h_layout)

        self.weight_h_layout = QHBoxLayout()
        self.weight_h_layout.setObjectName(u"weight_h_layout")
        self.weight_label = QLabel(self.layoutWidget_2)
        self.weight_label.setObjectName(u"weight_label")
        sizePolicy1.setHeightForWidth(self.weight_label.sizePolicy().hasHeightForWidth())
        self.weight_label.setSizePolicy(sizePolicy1)
        self.weight_label.setMinimumSize(QSize(174, 39))
        self.weight_label.setMaximumSize(QSize(174, 39))
        self.weight_label.setFont(font)

        self.weight_h_layout.addWidget(self.weight_label)

        self.weight_combo_box = QComboBox(self.layoutWidget_2)
        self.weight_combo_box.addItem("")
        self.weight_combo_box.setObjectName(u"weight_combo_box")
        sizePolicy1.setHeightForWidth(self.weight_combo_box.sizePolicy().hasHeightForWidth())
        self.weight_combo_box.setSizePolicy(sizePolicy1)
        self.weight_combo_box.setMinimumSize(QSize(174, 24))
        self.weight_combo_box.setMaximumSize(QSize(174, 24))
        self.weight_combo_box.setFont(font)

        self.weight_h_layout.addWidget(self.weight_combo_box)


        self.model_v_layout.addLayout(self.weight_h_layout)

        self.device_h_layout = QHBoxLayout()
        self.device_h_layout.setObjectName(u"device_h_layout")
        self.device_label = QLabel(self.layoutWidget_2)
        self.device_label.setObjectName(u"device_label")
        sizePolicy1.setHeightForWidth(self.device_label.sizePolicy().hasHeightForWidth())
        self.device_label.setSizePolicy(sizePolicy1)
        self.device_label.setMinimumSize(QSize(174, 39))
        self.device_label.setMaximumSize(QSize(174, 39))
        self.device_label.setFont(font)

        self.device_h_layout.addWidget(self.device_label)

        self.device_line_edit = QLineEdit(self.layoutWidget_2)
        self.device_line_edit.setObjectName(u"device_line_edit")
        sizePolicy1.setHeightForWidth(self.device_line_edit.sizePolicy().hasHeightForWidth())
        self.device_line_edit.setSizePolicy(sizePolicy1)
        self.device_line_edit.setMinimumSize(QSize(174, 24))
        self.device_line_edit.setMaximumSize(QSize(174, 24))
        self.device_line_edit.setFont(font)
        self.device_line_edit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.device_line_edit.setClearButtonEnabled(True)

        self.device_h_layout.addWidget(self.device_line_edit)


        self.model_v_layout.addLayout(self.device_h_layout)

        self.shuffle_h_layout = QHBoxLayout()
        self.shuffle_h_layout.setObjectName(u"shuffle_h_layout")
        self.shuffle_label = QLabel(self.layoutWidget_2)
        self.shuffle_label.setObjectName(u"shuffle_label")
        sizePolicy1.setHeightForWidth(self.shuffle_label.sizePolicy().hasHeightForWidth())
        self.shuffle_label.setSizePolicy(sizePolicy1)
        self.shuffle_label.setMinimumSize(QSize(174, 39))
        self.shuffle_label.setMaximumSize(QSize(174, 39))
        self.shuffle_label.setFont(font)

        self.shuffle_h_layout.addWidget(self.shuffle_label)

        self.shuffle_check_box = QCheckBox(self.layoutWidget_2)
        self.shuffle_check_box.setObjectName(u"shuffle_check_box")
        sizePolicy1.setHeightForWidth(self.shuffle_check_box.sizePolicy().hasHeightForWidth())
        self.shuffle_check_box.setSizePolicy(sizePolicy1)
        self.shuffle_check_box.setMinimumSize(QSize(174, 24))
        self.shuffle_check_box.setMaximumSize(QSize(174, 24))

        self.shuffle_h_layout.addWidget(self.shuffle_check_box)


        self.model_v_layout.addLayout(self.shuffle_h_layout)

        self.batch_h_layout = QHBoxLayout()
        self.batch_h_layout.setObjectName(u"batch_h_layout")
        self.batch_lable = QLabel(self.layoutWidget_2)
        self.batch_lable.setObjectName(u"batch_lable")
        sizePolicy1.setHeightForWidth(self.batch_lable.sizePolicy().hasHeightForWidth())
        self.batch_lable.setSizePolicy(sizePolicy1)
        self.batch_lable.setMinimumSize(QSize(174, 39))
        self.batch_lable.setMaximumSize(QSize(174, 39))
        self.batch_lable.setFont(font)

        self.batch_h_layout.addWidget(self.batch_lable)

        self.batch_line_edit = QLineEdit(self.layoutWidget_2)
        self.batch_line_edit.setObjectName(u"batch_line_edit")
        sizePolicy1.setHeightForWidth(self.batch_line_edit.sizePolicy().hasHeightForWidth())
        self.batch_line_edit.setSizePolicy(sizePolicy1)
        self.batch_line_edit.setMinimumSize(QSize(174, 24))
        self.batch_line_edit.setMaximumSize(QSize(174, 24))
        self.batch_line_edit.setFont(font)
        self.batch_line_edit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.batch_line_edit.setClearButtonEnabled(True)

        self.batch_h_layout.addWidget(self.batch_line_edit)


        self.model_v_layout.addLayout(self.batch_h_layout)

        self.worker_h_layout = QHBoxLayout()
        self.worker_h_layout.setObjectName(u"worker_h_layout")
        self.worker_h_layout_2 = QLabel(self.layoutWidget_2)
        self.worker_h_layout_2.setObjectName(u"worker_h_layout_2")
        sizePolicy1.setHeightForWidth(self.worker_h_layout_2.sizePolicy().hasHeightForWidth())
        self.worker_h_layout_2.setSizePolicy(sizePolicy1)
        self.worker_h_layout_2.setMinimumSize(QSize(174, 39))
        self.worker_h_layout_2.setMaximumSize(QSize(174, 39))
        self.worker_h_layout_2.setFont(font)

        self.worker_h_layout.addWidget(self.worker_h_layout_2)

        self.worker_line_edit = QLineEdit(self.layoutWidget_2)
        self.worker_line_edit.setObjectName(u"worker_line_edit")
        sizePolicy1.setHeightForWidth(self.worker_line_edit.sizePolicy().hasHeightForWidth())
        self.worker_line_edit.setSizePolicy(sizePolicy1)
        self.worker_line_edit.setMinimumSize(QSize(174, 24))
        self.worker_line_edit.setMaximumSize(QSize(174, 24))
        self.worker_line_edit.setFont(font)
        self.worker_line_edit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.worker_line_edit.setClearButtonEnabled(True)

        self.worker_h_layout.addWidget(self.worker_line_edit)


        self.model_v_layout.addLayout(self.worker_h_layout)

        self.cls_h_layout = QHBoxLayout()
        self.cls_h_layout.setObjectName(u"cls_h_layout")
        self.cls_label = QLabel(self.layoutWidget_2)
        self.cls_label.setObjectName(u"cls_label")
        sizePolicy1.setHeightForWidth(self.cls_label.sizePolicy().hasHeightForWidth())
        self.cls_label.setSizePolicy(sizePolicy1)
        self.cls_label.setMinimumSize(QSize(174, 39))
        self.cls_label.setMaximumSize(QSize(174, 39))
        self.cls_label.setFont(font)

        self.cls_h_layout.addWidget(self.cls_label)

        self.cls_line_edit = QLineEdit(self.layoutWidget_2)
        self.cls_line_edit.setObjectName(u"cls_line_edit")
        sizePolicy1.setHeightForWidth(self.cls_line_edit.sizePolicy().hasHeightForWidth())
        self.cls_line_edit.setSizePolicy(sizePolicy1)
        self.cls_line_edit.setMinimumSize(QSize(174, 24))
        self.cls_line_edit.setMaximumSize(QSize(174, 24))
        self.cls_line_edit.setFont(font)
        self.cls_line_edit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.cls_line_edit.setClearButtonEnabled(True)

        self.cls_h_layout.addWidget(self.cls_line_edit)


        self.model_v_layout.addLayout(self.cls_h_layout)

        self.size_h_layout = QHBoxLayout()
        self.size_h_layout.setObjectName(u"size_h_layout")
        self.size_label = QLabel(self.layoutWidget_2)
        self.size_label.setObjectName(u"size_label")
        sizePolicy1.setHeightForWidth(self.size_label.sizePolicy().hasHeightForWidth())
        self.size_label.setSizePolicy(sizePolicy1)
        self.size_label.setMinimumSize(QSize(174, 39))
        self.size_label.setMaximumSize(QSize(174, 39))
        self.size_label.setFont(font)

        self.size_h_layout.addWidget(self.size_label)

        self.size_line_edit = QLineEdit(self.layoutWidget_2)
        self.size_line_edit.setObjectName(u"size_line_edit")
        sizePolicy1.setHeightForWidth(self.size_line_edit.sizePolicy().hasHeightForWidth())
        self.size_line_edit.setSizePolicy(sizePolicy1)
        self.size_line_edit.setMinimumSize(QSize(174, 24))
        self.size_line_edit.setMaximumSize(QSize(174, 24))
        self.size_line_edit.setFont(font)
        self.size_line_edit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.size_line_edit.setClearButtonEnabled(True)

        self.size_h_layout.addWidget(self.size_line_edit)


        self.model_v_layout.addLayout(self.size_h_layout)

        self.pad_h_layout = QHBoxLayout()
        self.pad_h_layout.setObjectName(u"pad_h_layout")
        self.pad_label = QLabel(self.layoutWidget_2)
        self.pad_label.setObjectName(u"pad_label")
        sizePolicy1.setHeightForWidth(self.pad_label.sizePolicy().hasHeightForWidth())
        self.pad_label.setSizePolicy(sizePolicy1)
        self.pad_label.setMinimumSize(QSize(174, 39))
        self.pad_label.setMaximumSize(QSize(174, 39))
        self.pad_label.setFont(font)

        self.pad_h_layout.addWidget(self.pad_label)

        self.pad_combo_box = QComboBox(self.layoutWidget_2)
        self.pad_combo_box.addItem("")
        self.pad_combo_box.addItem("")
        self.pad_combo_box.setObjectName(u"pad_combo_box")
        sizePolicy1.setHeightForWidth(self.pad_combo_box.sizePolicy().hasHeightForWidth())
        self.pad_combo_box.setSizePolicy(sizePolicy1)
        self.pad_combo_box.setMinimumSize(QSize(174, 24))
        self.pad_combo_box.setMaximumSize(QSize(174, 24))
        self.pad_combo_box.setFont(font)

        self.pad_h_layout.addWidget(self.pad_combo_box)


        self.model_v_layout.addLayout(self.pad_h_layout)


        self.model_v_layout_2.addWidget(self.model_group_box)


        self.create_h_layout.addLayout(self.model_v_layout_2)

        self.cm_tab_widget.addTab(self.create_widget, "")
        self.manage_widget = QWidget()
        self.manage_widget.setObjectName(u"manage_widget")
        self.layoutWidget5 = QWidget(self.manage_widget)
        self.layoutWidget5.setObjectName(u"layoutWidget5")
        self.layoutWidget5.setGeometry(QRect(20, 10, 771, 401))
        self.manage_h_layout = QHBoxLayout(self.layoutWidget5)
        self.manage_h_layout.setObjectName(u"manage_h_layout")
        self.manage_h_layout.setContentsMargins(0, 0, 0, 0)
        self.exit_create_v_layout = QVBoxLayout()
        self.exit_create_v_layout.setObjectName(u"exit_create_v_layout")
        self.exit_group_box = QGroupBox(self.layoutWidget5)
        self.exit_group_box.setObjectName(u"exit_group_box")
        self.exit_group_box.setFont(font)
        self.exit_list_widget = QListWidget(self.exit_group_box)
        self.exit_list_widget.setObjectName(u"exit_list_widget")
        self.exit_list_widget.setGeometry(QRect(10, 30, 361, 161))
        sizePolicy1.setHeightForWidth(self.exit_list_widget.sizePolicy().hasHeightForWidth())
        self.exit_list_widget.setSizePolicy(sizePolicy1)
        self.exit_list_widget.setMinimumSize(QSize(361, 161))
        self.exit_list_widget.setMaximumSize(QSize(361, 161))

        self.exit_create_v_layout.addWidget(self.exit_group_box)

        self.create_group_box = QGroupBox(self.layoutWidget5)
        self.create_group_box.setObjectName(u"create_group_box")
        self.create_group_box.setFont(font)
        self.create_list_widget = QListWidget(self.create_group_box)
        self.create_list_widget.setObjectName(u"create_list_widget")
        self.create_list_widget.setGeometry(QRect(10, 20, 361, 171))
        sizePolicy1.setHeightForWidth(self.create_list_widget.sizePolicy().hasHeightForWidth())
        self.create_list_widget.setSizePolicy(sizePolicy1)
        self.create_list_widget.setMinimumSize(QSize(361, 171))
        self.create_list_widget.setMaximumSize(QSize(361, 171))

        self.exit_create_v_layout.addWidget(self.create_group_box)

        self.exit_create_v_layout.setStretch(0, 1)
        self.exit_create_v_layout.setStretch(1, 1)

        self.manage_h_layout.addLayout(self.exit_create_v_layout)

        self.run_group_box = QGroupBox(self.layoutWidget5)
        self.run_group_box.setObjectName(u"run_group_box")
        self.run_group_box.setFont(font)
        self.run_list_widget = QListWidget(self.run_group_box)
        self.run_list_widget.setObjectName(u"run_list_widget")
        self.run_list_widget.setGeometry(QRect(10, 30, 361, 361))
        sizePolicy1.setHeightForWidth(self.run_list_widget.sizePolicy().hasHeightForWidth())
        self.run_list_widget.setSizePolicy(sizePolicy1)
        self.run_list_widget.setMinimumSize(QSize(361, 361))
        self.run_list_widget.setMaximumSize(QSize(361, 361))

        self.manage_h_layout.addWidget(self.run_group_box)

        self.refresh_push_button = QPushButton(self.manage_widget)
        self.refresh_push_button.setObjectName(u"refresh_push_button")
        self.refresh_push_button.setGeometry(QRect(717, 416, 75, 25))
        sizePolicy1.setHeightForWidth(self.refresh_push_button.sizePolicy().hasHeightForWidth())
        self.refresh_push_button.setSizePolicy(sizePolicy1)
        self.refresh_push_button.setMinimumSize(QSize(75, 25))
        self.refresh_push_button.setMaximumSize(QSize(75, 25))
        self.cm_tab_widget.addTab(self.manage_widget, "")

        self.op_main_v_layout.addWidget(self.cm_tab_widget)

        self.pdl_tab_widget = QTabWidget(self.layoutWidget)
        self.pdl_tab_widget.setObjectName(u"pdl_tab_widget")
        sizePolicy1.setHeightForWidth(self.pdl_tab_widget.sizePolicy().hasHeightForWidth())
        self.pdl_tab_widget.setSizePolicy(sizePolicy1)
        self.pdl_tab_widget.setMinimumSize(QSize(801, 319))
        self.pdl_tab_widget.setMaximumSize(QSize(801, 319))
        self.pdl_tab_widget.setFont(font)
        self.pdl_tab_widget.setStyleSheet(u"")
        self.prompt_widget = QWidget()
        self.prompt_widget.setObjectName(u"prompt_widget")
        self.prompt_text_browser = QTextBrowser(self.prompt_widget)
        self.prompt_text_browser.setObjectName(u"prompt_text_browser")
        self.prompt_text_browser.setGeometry(QRect(0, 0, 801, 311))
        sizePolicy1.setHeightForWidth(self.prompt_text_browser.sizePolicy().hasHeightForWidth())
        self.prompt_text_browser.setSizePolicy(sizePolicy1)
        self.prompt_text_browser.setMinimumSize(QSize(801, 311))
        self.prompt_text_browser.setMaximumSize(QSize(801, 311))
        self.prompt_text_browser.setStyleSheet(u"")
        self.pdl_tab_widget.addTab(self.prompt_widget, "")
        self.detail_widget = QWidget()
        self.detail_widget.setObjectName(u"detail_widget")
        self.detail_text_browser = QTextBrowser(self.detail_widget)
        self.detail_text_browser.setObjectName(u"detail_text_browser")
        self.detail_text_browser.setGeometry(QRect(0, 0, 801, 311))
        sizePolicy1.setHeightForWidth(self.detail_text_browser.sizePolicy().hasHeightForWidth())
        self.detail_text_browser.setSizePolicy(sizePolicy1)
        self.detail_text_browser.setMinimumSize(QSize(801, 311))
        self.detail_text_browser.setMaximumSize(QSize(801, 311))
        self.pdl_tab_widget.addTab(self.detail_widget, "")
        self.log_widget = QWidget()
        self.log_widget.setObjectName(u"log_widget")
        self.log_text_browser = QTextBrowser(self.log_widget)
        self.log_text_browser.setObjectName(u"log_text_browser")
        self.log_text_browser.setGeometry(QRect(0, 0, 801, 311))
        sizePolicy1.setHeightForWidth(self.log_text_browser.sizePolicy().hasHeightForWidth())
        self.log_text_browser.setSizePolicy(sizePolicy1)
        self.log_text_browser.setMinimumSize(QSize(801, 311))
        self.log_text_browser.setMaximumSize(QSize(801, 311))
        self.pdl_tab_widget.addTab(self.log_widget, "")

        self.op_main_v_layout.addWidget(self.pdl_tab_widget)

        self.op_main_v_layout.setStretch(0, 9)
        self.op_main_v_layout.setStretch(1, 5)

        self.op_h_layout.addLayout(self.op_main_v_layout)

        self.op_h_layout.setStretch(0, 2)
        self.op_h_layout.setStretch(1, 10)

        self.ui_v_layout.addLayout(self.op_h_layout)

        self.ui_v_layout.setStretch(0, 1)
        self.ui_v_layout.setStretch(1, 11)

        self.retranslateUi(main_widget)

        self.cm_tab_widget.setCurrentIndex(0)
        self.pdl_tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(main_widget)
    # setupUi

    def retranslateUi(self, main_widget):
        main_widget.setWindowTitle(QCoreApplication.translate("main_widget", u"Robustar Launcher", None))
        self.header_label.setText("")
        self.load_push_button.setText(QCoreApplication.translate("main_widget", u"Load Profile", None))
        self.save_push_button.setText(QCoreApplication.translate("main_widget", u"Save Profile", None))
        self.start_push_button.setText(QCoreApplication.translate("main_widget", u"Start Server", None))
        self.stop_push_button.setText(QCoreApplication.translate("main_widget", u"Stop Server", None))
        self.delete_push_button.setText(QCoreApplication.translate("main_widget", u"Delete Server", None))
        self.docker_group_box.setTitle(QCoreApplication.translate("main_widget", u"Docker", None))
#if QT_CONFIG(tooltip)
        self.name_label.setToolTip(QCoreApplication.translate("main_widget", u"The name of the docker container", None))
#endif // QT_CONFIG(tooltip)
        self.name_label.setText(QCoreApplication.translate("main_widget", u"Container Name", None))
        self.name_line_edit.setText(QCoreApplication.translate("main_widget", u"robustar", None))
#if QT_CONFIG(tooltip)
        self.image_label.setToolTip(QCoreApplication.translate("main_widget", u"The version of the docker image of the container", None))
#endif // QT_CONFIG(tooltip)
        self.image_label.setText(QCoreApplication.translate("main_widget", u"Image Version", None))
        self.image_combo_box.setProperty("placeholderText", "")
#if QT_CONFIG(tooltip)
        self.port_label.setToolTip(QCoreApplication.translate("main_widget", u"The port the docker container forwards to", None))
#endif // QT_CONFIG(tooltip)
        self.port_label.setText(QCoreApplication.translate("main_widget", u"Port", None))
        self.port_line_edit.setText(QCoreApplication.translate("main_widget", u"8000", None))
        self.data_group_box.setTitle(QCoreApplication.translate("main_widget", u"Data", None))
#if QT_CONFIG(tooltip)
        self.train_label.setToolTip(QCoreApplication.translate("main_widget", u"The root path of the train set", None))
#endif // QT_CONFIG(tooltip)
        self.train_label.setText(QCoreApplication.translate("main_widget", u"Train Set", None))
        self.train_line_edit.setText("")
        self.train_push_button.setText(QCoreApplication.translate("main_widget", u"...", None))
#if QT_CONFIG(tooltip)
        self.val_label.setToolTip(QCoreApplication.translate("main_widget", u"The root path of the validation set", None))
#endif // QT_CONFIG(tooltip)
        self.val_label.setText(QCoreApplication.translate("main_widget", u"Validation Set", None))
        self.val_line_edit.setText("")
        self.val_push_button.setText(QCoreApplication.translate("main_widget", u"...", None))
#if QT_CONFIG(tooltip)
        self.test_label.setToolTip(QCoreApplication.translate("main_widget", u"The root path of the test set", None))
#endif // QT_CONFIG(tooltip)
        self.test_label.setText(QCoreApplication.translate("main_widget", u"Test Set", None))
        self.test_line_edit.setText("")
        self.test_push_button.setText(QCoreApplication.translate("main_widget", u"...", None))
#if QT_CONFIG(tooltip)
        self.paired_label.setToolTip(QCoreApplication.translate("main_widget", u"The root path of the paired set", None))
#endif // QT_CONFIG(tooltip)
        self.paired_label.setText(QCoreApplication.translate("main_widget", u"Paired Set", None))
        self.paired_line_edit.setText("")
        self.paired_push_button.setText(QCoreApplication.translate("main_widget", u"...", None))
#if QT_CONFIG(tooltip)
        self.gen_label.setToolTip(QCoreApplication.translate("main_widget", u"The root path of the generated files", None))
#endif // QT_CONFIG(tooltip)
        self.gen_label.setText(QCoreApplication.translate("main_widget", u"Generated Files", None))
        self.gen_line_edit.setText("")
        self.gen_push_button.setText(QCoreApplication.translate("main_widget", u"...", None))
#if QT_CONFIG(tooltip)
        self.ckpt_label.setToolTip(QCoreApplication.translate("main_widget", u"The root path for all checkpoint files saved by Robustar", None))
#endif // QT_CONFIG(tooltip)
        self.ckpt_label.setText(QCoreApplication.translate("main_widget", u"Checkpoint", None))
        self.ckpt_line_edit.setText("")
        self.ckpt_push_button.setText(QCoreApplication.translate("main_widget", u"...", None))
#if QT_CONFIG(tooltip)
        self.inf_label.setToolTip(QCoreApplication.translate("main_widget", u"The root path for all influence result calculated by Robustar", None))
#endif // QT_CONFIG(tooltip)
        self.inf_label.setText(QCoreApplication.translate("main_widget", u"Influence Result", None))
        self.inf_line_edit.setText("")
        self.inf_push_button.setText(QCoreApplication.translate("main_widget", u"...", None))
        self.model_group_box.setTitle(QCoreApplication.translate("main_widget", u"Model", None))
#if QT_CONFIG(tooltip)
        self.arch_label.setToolTip(QCoreApplication.translate("main_widget", u"The architecture of the model", None))
#endif // QT_CONFIG(tooltip)
        self.arch_label.setText(QCoreApplication.translate("main_widget", u"Architecture", None))
        self.arch_combo_box.setItemText(0, QCoreApplication.translate("main_widget", u"resnet-18", None))
        self.arch_combo_box.setItemText(1, QCoreApplication.translate("main_widget", u"resnet-34", None))
        self.arch_combo_box.setItemText(2, QCoreApplication.translate("main_widget", u"resnet-50", None))
        self.arch_combo_box.setItemText(3, QCoreApplication.translate("main_widget", u"resnet-101", None))
        self.arch_combo_box.setItemText(4, QCoreApplication.translate("main_widget", u"resnet-152", None))
        self.arch_combo_box.setItemText(5, QCoreApplication.translate("main_widget", u"resnet-18-32x32", None))
        self.arch_combo_box.setItemText(6, QCoreApplication.translate("main_widget", u"mobilenet-v2", None))
        self.arch_combo_box.setItemText(7, QCoreApplication.translate("main_widget", u"alexnet", None))

        self.arch_combo_box.setCurrentText(QCoreApplication.translate("main_widget", u"resnet-18", None))
        self.arch_combo_box.setProperty("placeholderText", "")
#if QT_CONFIG(tooltip)
        self.pretrain_label.setToolTip(QCoreApplication.translate("main_widget", u"Check the box if you want a model with pretrained weights", None))
#endif // QT_CONFIG(tooltip)
        self.pretrain_label.setText(QCoreApplication.translate("main_widget", u"Pretrained", None))
        self.pretrain_check_box.setText("")
#if QT_CONFIG(tooltip)
        self.weight_label.setToolTip(QCoreApplication.translate("main_widget", u"The weight file used to initialize the model. Optional weight files are under the root path of the checkpoint you set", None))
#endif // QT_CONFIG(tooltip)
        self.weight_label.setText(QCoreApplication.translate("main_widget", u"Weight File", None))
        self.weight_combo_box.setItemText(0, QCoreApplication.translate("main_widget", u"None", None))

        self.weight_combo_box.setProperty("placeholderText", "")
#if QT_CONFIG(tooltip)
        self.device_label.setToolTip(QCoreApplication.translate("main_widget", u"The device on which the model will be created", None))
#endif // QT_CONFIG(tooltip)
        self.device_label.setText(QCoreApplication.translate("main_widget", u"Device", None))
        self.device_line_edit.setText(QCoreApplication.translate("main_widget", u"cpu", None))
#if QT_CONFIG(tooltip)
        self.shuffle_label.setToolTip(QCoreApplication.translate("main_widget", u"Check the box if you want the train data to be shuffled", None))
#endif // QT_CONFIG(tooltip)
        self.shuffle_label.setText(QCoreApplication.translate("main_widget", u"Shuffle", None))
        self.shuffle_check_box.setText("")
#if QT_CONFIG(tooltip)
        self.batch_lable.setToolTip(QCoreApplication.translate("main_widget", u"The batch size of the data", None))
#endif // QT_CONFIG(tooltip)
        self.batch_lable.setText(QCoreApplication.translate("main_widget", u"Batch Size", None))
        self.batch_line_edit.setText("")
#if QT_CONFIG(tooltip)
        self.worker_h_layout_2.setToolTip(QCoreApplication.translate("main_widget", u"The number of workers for the data loader", None))
#endif // QT_CONFIG(tooltip)
        self.worker_h_layout_2.setText(QCoreApplication.translate("main_widget", u"Worker Number", None))
        self.worker_line_edit.setText("")
#if QT_CONFIG(tooltip)
        self.cls_label.setToolTip(QCoreApplication.translate("main_widget", u"The number of classes of the data", None))
#endif // QT_CONFIG(tooltip)
        self.cls_label.setText(QCoreApplication.translate("main_widget", u"Class Number", None))
        self.cls_line_edit.setText("")
#if QT_CONFIG(tooltip)
        self.size_label.setToolTip(QCoreApplication.translate("main_widget", u"The length of side of the input image of the model", None))
#endif // QT_CONFIG(tooltip)
        self.size_label.setText(QCoreApplication.translate("main_widget", u"Image Size", None))
        self.size_line_edit.setText("")
#if QT_CONFIG(tooltip)
        self.pad_label.setToolTip(QCoreApplication.translate("main_widget", u"The mode of padding", None))
#endif // QT_CONFIG(tooltip)
        self.pad_label.setText(QCoreApplication.translate("main_widget", u"Image Padding", None))
        self.pad_combo_box.setItemText(0, QCoreApplication.translate("main_widget", u"short side", None))
        self.pad_combo_box.setItemText(1, QCoreApplication.translate("main_widget", u"none", None))

        self.pad_combo_box.setCurrentText(QCoreApplication.translate("main_widget", u"short side", None))
        self.pad_combo_box.setProperty("placeholderText", "")
        self.cm_tab_widget.setTabText(self.cm_tab_widget.indexOf(self.create_widget), QCoreApplication.translate("main_widget", u"Create", None))
        self.exit_group_box.setTitle(QCoreApplication.translate("main_widget", u"Exited", None))
        self.create_group_box.setTitle(QCoreApplication.translate("main_widget", u"Created", None))
        self.run_group_box.setTitle(QCoreApplication.translate("main_widget", u"Running", None))
        self.refresh_push_button.setText(QCoreApplication.translate("main_widget", u"Refresh", None))
        self.cm_tab_widget.setTabText(self.cm_tab_widget.indexOf(self.manage_widget), QCoreApplication.translate("main_widget", u"Manage", None))
        self.pdl_tab_widget.setTabText(self.pdl_tab_widget.indexOf(self.prompt_widget), QCoreApplication.translate("main_widget", u"Prompts", None))
        self.pdl_tab_widget.setTabText(self.pdl_tab_widget.indexOf(self.detail_widget), QCoreApplication.translate("main_widget", u"Details", None))
        self.pdl_tab_widget.setTabText(self.pdl_tab_widget.indexOf(self.log_widget), QCoreApplication.translate("main_widget", u"Logs", None))
    # retranslateUi

