from PyQt5 import QtWidgets, QtGui


class Panel2(QtWidgets.QVBoxLayout):
    def __init__(self, model, list_view, active_phrase_view, parent=None):
        super(Panel2, self).__init__(parent)

        self.breathing_model = model
        self.breathing_phrases_qlv = list_view
        self.active_breathing_phrase_qlv = active_phrase_view
        self.edit_breathing_phrase = EditBreathingPhrase(self.breathing_model)
        self._init_ui()

    def _init_ui(self):
        edit_breathing_phrase_qpb = QtWidgets.QPushButton('edit')
        edit_breathing_phrase_qpb.clicked.connect(self.on_edit_breathing_phrase_clicked)

        add_breathing_phrase_qpb = QtWidgets.QPushButton('add')
        add_breathing_phrase_qpb.clicked.connect(self.on_add_phrase_clicked)

        remove_breathing_phrase_qpb = QtWidgets.QPushButton('remove')
        remove_breathing_phrase_qpb.clicked.connect(self.on_remove_phrase_clicked)

        button_box_breathing_phrases = QtWidgets.QHBoxLayout()
        button_box_breathing_phrases.addWidget(edit_breathing_phrase_qpb)
        button_box_breathing_phrases.addWidget(add_breathing_phrase_qpb)
        button_box_breathing_phrases.addWidget(remove_breathing_phrase_qpb)

        self.addWidget(self.breathing_phrases_qlv)
        self.addLayout(button_box_breathing_phrases)
        self.addStretch(1)

        self.breathing_phrases_qlv.setModel(self.breathing_model)
        self.breathing_phrases_qlv.setModelColumn(2)
        self.breathing_phrases_qlv.doubleClicked.connect(self.on_edit_breathing_phrase_clicked)
        self.breathing_phrases_qlv.clicked.connect(self.on_breathing_phrase_clicked)

    def on_edit_breathing_phrase_clicked(self):
        self.edit_breathing_phrase.show()

        if self.breathing_phrases_qlv.selectedIndexes():
            self.edit_breathing_phrase.mapper.setCurrentIndex(self.breathing_phrases_qlv.selectedIndexes()[0].row())
        else:
            self.on_add_phrase_clicked()

    def on_add_phrase_clicked(self):
        row_nr = self.breathing_model.rowCount()
        self.breathing_model.insertRow(row_nr)
        self.edit_breathing_phrase.mapper.toLast()
        self.edit_breathing_phrase.show()

    def on_remove_phrase_clicked(self):
        if self.breathing_phrases_qlv.selectedIndexes():
            self.breathing_model.removeRow(self.breathing_phrases_qlv.selectedIndexes()[0].row())
            self.breathing_model.select()
            self.active_breathing_phrase_qlv.mapper.toFirst()

    def on_breathing_phrase_clicked(self):
        if self.breathing_phrases_qlv.selectedIndexes():
            self.active_breathing_phrase_qlv.set_active_phrase(self.breathing_phrases_qlv.selectedIndexes())


class EditBreathingPhrase(QtWidgets.QWidget):
    """
    An example of an edit form using a QDataWidgetMapper and a QSqlQueryModel
    """
    def __init__(self, model, parent=None):
        super(EditBreathingPhrase, self).__init__(parent)

        self.model = model
        self.mapper = QtWidgets.QDataWidgetMapper(self)
        self._init_ui()

    def _init_ui(self):
        vertical_order_label = QtWidgets.QLabel("Vertical order:")
        vertical_order_edit = QtWidgets.QLineEdit()
        vertical_order_edit.setValidator(QtGui.QIntValidator())

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
        self.mapper.addMapping(vertical_order_edit, 1)
        self.mapper.addMapping(title_edit, 2)
        self.mapper.addMapping(ib_phrase_edit, 3)
        self.mapper.addMapping(ob_phrase_edit, 4)
        self.mapper.addMapping(ib_short_phrase_edit, 5)
        self.mapper.addMapping(ob_short_phrase_edit, 6)
        self.mapper.setSubmitPolicy(QtWidgets.QDataWidgetMapper.ManualSubmit)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(vertical_order_label, 0, 0, 1, 1)
        layout.addWidget(vertical_order_edit, 0, 1, 1, 1)
        layout.addWidget(title_label, 1, 0, 1, 1)
        layout.addWidget(title_edit, 1, 1, 1, 1)
        layout.addWidget(ib_phrase_label, 2, 0, 1, 1)
        layout.addWidget(ib_phrase_edit, 2, 1, 1, 1)
        layout.addWidget(ob_phrase_label, 3, 0, 1, 1)
        layout.addWidget(ob_phrase_edit, 3, 1, 1, 1)
        layout.addWidget(ib_short_phrase_label, 4, 0, 1, 1)
        layout.addWidget(ib_short_phrase_edit, 4, 1, 1, 1)
        layout.addWidget(ob_short_phrase_label, 5, 0, 1, 1)
        layout.addWidget(ob_short_phrase_edit, 5, 1, 1, 1)
        layout.addWidget(cancel_button, 6, 0, 1, 1)
        layout.addWidget(submit_button, 6, 1, 1, 1)
        self.setLayout(layout)

        self.mapper.toFirst()

    def _submit_form(self):
        self.mapper.submit()
        self.close()
