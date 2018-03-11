from PyQt5 import QtWidgets
from mc.gui.Panel1 import Panel1
from mc.gui.Panel2 import Panel2
from mc.gui.Panel3 import Panel3


class CentralWidget(QtWidgets.QWidget):
    """
    The central widget holding all layouts
    """
    def __init__(self, breathing_model, rest_model, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        # Initialize the models
        self.breathing_model = breathing_model
        self.rest_model = rest_model

        # Initialize the panels
        self.breathing_phrases_qlv = QtWidgets.QListView()
        self.rest_phrases_qlv = QtWidgets.QListView()
        self.panel_1 = Panel1(breathing_model, self.breathing_phrases_qlv)
        self.panel_2 = Panel2(breathing_model, self.breathing_phrases_qlv, self.panel_1.active_breathing_phrase_qlv)
        self.panel_3 = Panel3(rest_model, self.rest_phrases_qlv)

        self._init_ui()

    def _init_ui(self):
        self.main_container_hbox_l3 = QtWidgets.QHBoxLayout()
        self.main_container_hbox_l3.addLayout(self.panel_1)
        self.main_container_hbox_l3.addLayout(self.panel_2)
        self.main_container_hbox_l3.addLayout(self.panel_3)
        self.setLayout(self.main_container_hbox_l3)
