from PyQt5 import QtWidgets


class Panel1(QtWidgets.QVBoxLayout):
    def __init__(self, model, source, parent=None):
        super(Panel1, self).__init__(parent)

        self.model = model
        self.source = source
        self.active_breathing_phrase_qlv = ActiveBreathingPhrase(self.model)
        self.active_breathing_phrase_qlv.set_active_phrase(self.source.selectedIndexes())
        self.addWidget(self.active_breathing_phrase_qlv)
        self.addStretch(1)


class ActiveBreathingPhrase(QtWidgets.QGroupBox):
    def __init__(self, model, parent=None):
        super(ActiveBreathingPhrase, self).__init__(parent)

        self.model = model
        self.mapper = QtWidgets.QDataWidgetMapper(self)
        self._init_ui()

    def _init_ui(self):
        self.setTitle('Active breathing phrase')

        title = QtWidgets.QLineEdit()
        title.setStyleSheet("background: transparent; border: none")
        title.setReadOnly(True)

        ib_phrase = QtWidgets.QLineEdit()
        ib_phrase.setStyleSheet("background: transparent; border: none")
        ib_phrase.setReadOnly(True)

        ob_phrase = QtWidgets.QLineEdit()
        ob_phrase.setStyleSheet("background: transparent; border: none")
        ob_phrase.setReadOnly(True)

        self.mapper.setModel(self.model)
        self.mapper.addMapping(title, 2)
        self.mapper.addMapping(ib_phrase, 3)
        self.mapper.addMapping(ob_phrase, 4)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(title, 0, 1, 1, 1)
        layout.addWidget(ib_phrase, 1, 1, 1, 1)
        layout.addWidget(ob_phrase, 2, 1, 1, 1)
        self.setLayout(layout)

    def set_active_phrase(self, selected_indexes):
        if selected_indexes:
            self.mapper.setCurrentModelIndex(selected_indexes[0])
        else:
            self.mapper.toFirst()
