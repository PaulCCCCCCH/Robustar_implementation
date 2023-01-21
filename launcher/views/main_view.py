from PySide2.QtWidgets import QWidget
from views.main_view_ui import Ui_main_widget


class MainView(QWidget):
    def __init__(self, ctrl):
        super().__init__()

        self.ctrl = ctrl
        self.ui = Ui_main_widget()
        self.ui.setupUi(self)

        # Match the corresponding signals to slots in controllers
        self.ui.name_line_edit.textEdited.connect(self.ctrl.set_m_name)
        self.ui.image_combo_box.currentIndexChanged.connect(self.ctrl.set_m_image)
        self.ui.port_line_edit.textEdited.connect(self.ctrl.set_m_port)
        self.ui.train_push_button.clicked.connect(self.ctrl.set_m_train_path)
        self.ui.val_push_button.clicked.connect(self.ctrl.set_m_val_path)
        self.ui.test_push_button.clicked.connect(self.ctrl.set_m_test_path)
        self.ui.paired_push_button.clicked.connect(self.ctrl.setMPairedPath)
        self.ui.gen_push_button.clicked.connect(self.ctrl.setMGeneratedPath)
        self.ui.ckpt_push_button.clicked.connect(self.ctrl.set_m_ckpt_path)
        self.ui.inf_push_button.clicked.connect(self.ctrl.set_m_inf_path)

        self.ui.arch_combo_box.currentIndexChanged.connect(self.ctrl.set_m_arch)
        self.ui.pretrain_check_box.stateChanged.connect(self.ctrl.set_m_pretrain)
        self.ui.weight_combo_box.currentIndexChanged.connect(self.ctrl.set_m_weight)
        self.ui.device_line_edit.textEdited.connect(self.ctrl.set_m_device)
        self.ui.shuffle_check_box.stateChanged.connect(self.ctrl.set_m_shuffle)
        self.ui.batch_line_edit.textEdited.connect(self.ctrl.set_m_batch)
        self.ui.worker_line_edit.textEdited.connect(self.ctrl.set_m_worker)
        self.ui.size_line_edit.textEdited.connect(self.ctrl.set_m_size)
        self.ui.pad_combo_box.currentIndexChanged.connect(self.ctrl.set_m_pad)
        self.ui.cls_line_edit.textEdited.connect(self.ctrl.set_m_cls)

        self.ui.load_push_button.clicked.connect(self.ctrl.load_profile)
        self.ui.save_push_button.clicked.connect(self.ctrl.save_profile)
        self.ui.start_push_button.clicked.connect(self.ctrl.start_server)
        self.ui.stop_push_button.clicked.connect(self.ctrl.stop_server)
        self.ui.delete_push_button.clicked.connect(self.ctrl.delete_server)
        self.ui.refresh_push_button.clicked.connect(self.ctrl.refresh_server)

        # Set the listWidgets so that only one entry in them can be selected at a time
        self.list_widget_lst = [
            self.ui.run_list_widget,
            self.ui.exit_list_widget,
            self.ui.create_list_widget,
        ]
        self.ui.run_list_widget.selectionModel().selectionChanged.connect(
            lambda sel, unsel: self.single_select(
                self.ui.run_list_widget, self.list_widget_lst
            )
        )
        self.ui.exit_list_widget.selectionModel().selectionChanged.connect(
            lambda sel, unsel: self.single_select(
                self.ui.exit_list_widget, self.list_widget_lst
            )
        )
        self.ui.create_list_widget.selectionModel().selectionChanged.connect(
            lambda sel, unsel: self.single_select(
                self.ui.create_list_widget, self.list_widget_lst
            )
        )

    # Function to ensure only one entry in the three listWidgets can be selected at a time
    def single_select(self, list_widget, list_widget_lst):

        for widget in list_widget_lst:
            # Only check the other listWidgets
            if widget == list_widget:
                continue

            # If the newly selected item is not in the same listWidget as the previous selected one
            # Remove the previous one from its listWidget
            if widget.selectionModel().hasSelection():
                widget.selectionModel().clearSelection()
