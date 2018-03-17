from PyQt5 import QtWidgets

from mc.gui.ListViewButtons import ListViewButtons


class Panel2(QtWidgets.QVBoxLayout):
    def __init__(self, model, list_view, active_phrase_view, parent=None):
        super(Panel2, self).__init__(parent)

        self.breathing_model = model
        self.breathing_phrases_qlv = list_view
        self.active_breathing_phrase_qlv = active_phrase_view
        self.edit_breathing_phrase = EditBreathingPhrase(self.breathing_model)
        self.button_box = ListViewButtons(
            self.breathing_model,
            self.breathing_phrases_qlv,
            self.edit_breathing_phrase,
            self.active_breathing_phrase_qlv
        )
        self._init_ui()

    def _init_ui(self):
        self.addWidget(self.breathing_phrases_qlv)
        self.addLayout(self.button_box)
        self.addStretch(1)

        self.breathing_phrases_qlv.setModel(self.breathing_model)
        self.breathing_phrases_qlv.setModelColumn(2)
        self.breathing_phrases_qlv.clicked.connect(self.on_breathing_phrase_clicked)

    def on_breathing_phrase_clicked(self):
        if self.breathing_phrases_qlv.selectedIndexes():
            self.active_breathing_phrase_qlv.set_active_phrase(self.breathing_phrases_qlv.selectedIndexes())


class EditBreathingPhrase(QtWidgets.QWidget):
    """
    A form using a QDataWidgetMapper and a QSqlTableModel
    """
    def __init__(self, model, parent=None):
        super(EditBreathingPhrase, self).__init__(parent)

        self.model = model
        self.mapper = QtWidgets.QDataWidgetMapper(self)
        self.vertical_order = QtWidgets.QLineEdit()
        self._init_ui()

    def _init_ui(self):
        title_label = QtWidgets.QLabel("Title:")
        title_edit = QtWidgets.QLineEdit()

        ib_phrase_label = QtWidgets.QLabel("In breath phrase:")
        ib_phrase_edit = QtWidgets.QLineEdit()

        ob_phrase_label = QtWidgets.QLabel("Out breath phrase:")
        ob_phrase_edit = QtWidgets.QLineEdit()

        ib_short_phrase_label = QtWidgets.QLabel("In breath short:")
        ib_short_phrase_edit = QtWidgets.QLineEdit()

        ob_short_phrase_label = QtWidgets.QLabel("Out breath short:")
        ob_short_phrase_edit = QtWidgets.QLineEdit()

        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)

        submit_button = QtWidgets.QPushButton("Submit")
        submit_button.clicked.connect(self._submit_form)

        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.vertical_order, 1)
        self.mapper.addMapping(title_edit, 2)
        self.mapper.addMapping(ib_phrase_edit, 3)
        self.mapper.addMapping(ob_phrase_edit, 4)
        self.mapper.addMapping(ib_short_phrase_edit, 5)
        self.mapper.addMapping(ob_short_phrase_edit, 6)
        self.mapper.setSubmitPolicy(QtWidgets.QDataWidgetMapper.ManualSubmit)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(title_label, 0, 0, 1, 1)
        layout.addWidget(title_edit, 0, 1, 1, 1)
        layout.addWidget(ib_phrase_label, 1, 0, 1, 1)
        layout.addWidget(ib_phrase_edit, 1, 1, 1, 1)
        layout.addWidget(ob_phrase_label, 2, 0, 1, 1)
        layout.addWidget(ob_phrase_edit, 2, 1, 1, 1)
        layout.addWidget(ib_short_phrase_label, 3, 0, 1, 1)
        layout.addWidget(ib_short_phrase_edit, 3, 1, 1, 1)
        layout.addWidget(ob_short_phrase_label, 4, 0, 1, 1)
        layout.addWidget(ob_short_phrase_edit, 4, 1, 1, 1)
        layout.addWidget(cancel_button, 5, 0, 1, 1)
        layout.addWidget(submit_button, 5, 1, 1, 1)
        self.setLayout(layout)

        self.mapper.toFirst()

    def _submit_form(self):
        self.mapper.submit()
        print(self.model.lastError().text())
        self.close()
