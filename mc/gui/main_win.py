from PyQt5 import QtWidgets, QtGui
from mc.gui import Ui
import mc.mc_global


class MainWin(QtWidgets.QMainWindow):

    def __init__(self, breathing_model, rest_model):
        self.breathing_model = breathing_model
        self.rest_model = rest_model
        super(MainWin, self).__init__()

        self._build_ui()

    def _build_ui(self):
        self.setGeometry(100, 64, 900, 670)
        self.setWindowIcon(QtGui.QIcon(mc.mc_global.get_app_icon_path()))
        self._setup_set_window_title()
        self.setStyleSheet(
            "selection-background-color:" + mc.mc_global.MC_LIGHT_GREEN_COLOR_STR + ";"
            "selection-color:#000000;"
        )
        central_widget = Ui.CentralWidget(self.breathing_model, self.rest_model, None)
        self.setCentralWidget(central_widget)

    def _setup_set_window_title(self):
        if mc.mc_global.testing_bool:
            data_storage_str = "{Testing - data stored in memory}"
        else:
            data_storage_str = "{Live - data stored on hard drive}"
        window_title_str = (
            mc.mc_global.APPLICATION_TITLE_STR
            + " [" + mc.mc_global.APPLICATION_VERSION_STR + "] "
            + data_storage_str
        )
        self.setWindowTitle(window_title_str)
