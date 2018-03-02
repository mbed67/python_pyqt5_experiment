from PyQt5 import QtWidgets


class CentralWidget(QtWidgets.QWidget):
    """
    The central widget holding all layouts
    """
    def __init__(self, breathing_model, rest_model, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        # Initialize the models
        self.breathing_model = breathing_model
        self.rest_model = rest_model
        self.rest_model.refresh()

        self.breathing_phrases_qlv = QtWidgets.QListView()
        self.breathing_phrases_qlv.setModel(self.breathing_model)

        # now two views that share the same model. As you edit a cell in one of them, the others are updated.
        self.test_qlv = QtWidgets.QListView()
        self.test_qlv.setModel(self.rest_model)
        self.rest_phrases_qlv = QtWidgets.QTableView()
        self.rest_phrases_qlv.setModel(self.rest_model)

        # this one also uses the rest_model but is used as a form. It still has issues saving all the fields
        # currently only the first field is saved
        self.active_breathing_phrase_qgb = EditBreathingPhrase(self.rest_model)

        self.panel_1 = QtWidgets.QVBoxLayout()
        self.panel_1.addWidget(self.active_breathing_phrase_qgb)
        self.panel_1.addWidget(self.test_qlv)
        self.panel_1.addStretch(1)
        self.panel_2 = QtWidgets.QVBoxLayout()
        self.panel_2.addWidget(self.breathing_phrases_qlv)
        self.panel_1.addStretch(1)
        self.panel_3 = QtWidgets.QVBoxLayout()
        self.panel_3.addWidget(self.rest_phrases_qlv)
        self.panel_1.addStretch(1)

        self.main_container_hbox_l3 = QtWidgets.QHBoxLayout()
        self.main_container_hbox_l3.addLayout(self.panel_1)
        self.main_container_hbox_l3.addLayout(self.panel_2)
        self.main_container_hbox_l3.addLayout(self.panel_3)
        self.setLayout(self.main_container_hbox_l3)


class EditBreathingPhrase(QtWidgets.QWidget):
    """
    An example of an edit form using a QDataWidgetMapper and a QSqlQueryModel
    """
    def __init__(self, model, parent=None):
        super(EditBreathingPhrase, self).__init__(parent)

        self.model = model

        # Set up the widgets.
        self.title_label = QtWidgets.QLabel("Title:")
        self.title_edit = QtWidgets.QLineEdit()

        self.ib_phrase_label = QtWidgets.QLabel("In breath phrase:")
        self.ib_phrase_edit = QtWidgets.QLineEdit()

        self.ob_phrase_label = QtWidgets.QLabel("Out breath phrase:")
        self.ob_phrase_edit = QtWidgets.QLineEdit()

        self.ib_short_phrase_label = QtWidgets.QLabel("In breath short:")
        self.ib_short_phrase_edit = QtWidgets.QLineEdit()

        self.ob_short_phrase_label = QtWidgets.QLabel("Out breath short:")
        self.ob_short_phrase_edit = QtWidgets.QLineEdit()

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.submit_button = QtWidgets.QPushButton("Submit")

        # Set up the mapper.
        self.mapper = QtWidgets.QDataWidgetMapper(self)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.title_edit, 0)
        self.mapper.addMapping(self.ib_phrase_edit, 2)
        self.mapper.addMapping(self.ob_phrase_edit, 3)
        self.mapper.addMapping(self.ib_short_phrase_edit, 4)
        self.mapper.addMapping(self.ob_short_phrase_edit, 5)
        self.mapper.setSubmitPolicy(QtWidgets.QDataWidgetMapper.ManualSubmit)
        self.cancel_button.clicked.connect(self.close)
        self.submit_button.clicked.connect(self._submit_form)

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.title_label, 0, 0, 1, 1)
        self.layout.addWidget(self.title_edit, 0, 1, 1, 1)
        self.layout.addWidget(self.ib_phrase_label, 1, 0, 1, 1)
        self.layout.addWidget(self.ib_phrase_edit, 1, 1, 1, 1)
        self.layout.addWidget(self.ob_phrase_label, 2, 0, 1, 1)
        self.layout.addWidget(self.ob_phrase_edit, 2, 1, 1, 1)
        self.layout.addWidget(self.ib_short_phrase_label, 3, 0, 1, 1)
        self.layout.addWidget(self.ib_short_phrase_edit, 3, 1, 1, 1)
        self.layout.addWidget(self.ob_short_phrase_label, 4, 0, 1, 1)
        self.layout.addWidget(self.ob_short_phrase_edit, 4, 1, 1, 1)
        self.layout.addWidget(self.cancel_button, 5, 0, 1, 1)
        self.layout.addWidget(self.submit_button, 5, 1, 1, 1)
        self.setLayout(self.layout)

        self.mapper.toFirst()

    def _submit_form(self):
        # This seems to save only the first item... strange...
        # The documentation says the following:
        # For every mapped section, the item delegate reads the current value from the widget and sets it in the model.
        # Finally, the model's submit() method is invoked.
        # http://doc.qt.io/archives/qt-4.8/qdatawidgetmapper.html
        self.mapper.submit()
        self.close()
