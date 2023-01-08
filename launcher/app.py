import sys
from PySide2.QtWidgets import QApplication
from model.model import Model
from controllers.main_ctrl import MainController
from views.main_view import MainView
from views.popup_view import PopupView


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        self.mainCtrl = MainController()

        self.model = Model(self.mainCtrl)

        self.mainView = MainView(self.mainCtrl)
        self.popupView = PopupView()

        self.mainCtrl.set_model(self.model)
        self.mainCtrl.set_main_view(self.mainView)
        self.mainCtrl.set_popup_view(self.popupView)

        self.mainCtrl.init()

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())