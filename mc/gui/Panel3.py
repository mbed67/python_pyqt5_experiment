from PyQt5 import QtWidgets, QtGui


class Panel3(QtWidgets.QVBoxLayout):
    def __init__(self, model, list_view, parent=None):
        super(Panel3, self).__init__(parent)

        self.rest_model = model
        self.rest_phrases_qlv = list_view
        self.edit_rest_phrase = EditRestPhrase(self.rest_model)
        self._init_ui()

    def _init_ui(self):
        self.rest_phrases_qlv.setModel(self.rest_model)
        self.rest_phrases_qlv.setModelColumn(2)
        self.rest_phrases_qlv.doubleClicked.connect(self.on_edit_rest_phrase_clicked)

        edit_rest_phrase_qpb = QtWidgets.QPushButton('edit')
        edit_rest_phrase_qpb.clicked.connect(self.on_edit_rest_phrase_clicked)

        add_rest_phrase_qpb = QtWidgets.QPushButton('add')
        add_rest_phrase_qpb.clicked.connect(self.on_add_phrase_clicked)

        remove_rest_phrase_qpb = QtWidgets.QPushButton('remove')
        remove_rest_phrase_qpb.clicked.connect(self.on_remove_phrase_clicked)

        button_box_rest_phrases = QtWidgets.QHBoxLayout()
        button_box_rest_phrases.addWidget(edit_rest_phrase_qpb)
        button_box_rest_phrases.addWidget(add_rest_phrase_qpb)
        button_box_rest_phrases.addWidget(remove_rest_phrase_qpb)

        self.addWidget(self.rest_phrases_qlv)
        self.addLayout(button_box_rest_phrases)
        self.addStretch(1)

        self.rest_phrases_qlv.setModel(self.rest_model)
        self.rest_phrases_qlv.setModelColumn(2)
        self.rest_phrases_qlv.doubleClicked.connect(self.on_edit_rest_phrase_clicked)

    def on_edit_rest_phrase_clicked(self):
        self.edit_rest_phrase.show()

        if self.rest_phrases_qlv.selectedIndexes():
            self.edit_rest_phrase.mapper.setCurrentIndex(self.rest_phrases_qlv.selectedIndexes()[0].row())
        else:
            self.on_add_phrase_clicked()

    def on_add_phrase_clicked(self):
        row_nr = self.rest_model.rowCount()
        vertical_order = self.rest_model.max_vertical_order_breathing_phrases() + 1
        self.rest_model.insertRow(row_nr)
        self.edit_rest_phrase.vertical_order.setText(str(vertical_order))
        self.edit_rest_phrase.mapper.toLast()
        self.edit_rest_phrase.show()

    def on_remove_phrase_clicked(self):
        if self.rest_phrases_qlv.selectedIndexes():
            self.rest_model.removeRow(self.rest_phrases_qlv.selectedIndexes()[0].row())
            self.rest_model.select()


class EditRestPhrase(QtWidgets.QWidget):
    """
    An example of an edit form using a QDataWidgetMapper and a QSqlQueryModel
    """
    def __init__(self, model, parent=None):
        super(EditRestPhrase, self).__init__(parent)

        self.model = model
        self.mapper = QtWidgets.QDataWidgetMapper(self)
        self.vertical_order = QtWidgets.QLineEdit()
        self._init_ui()

    def _init_ui(self):
        title_label = QtWidgets.QLabel("Title:")
        title_edit = QtWidgets.QLineEdit()

        image_path_label = QtWidgets.QLabel("Image path:")
        image_path_edit = QtWidgets.QLineEdit()

        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)

        submit_button = QtWidgets.QPushButton("Submit")
        submit_button.clicked.connect(self._submit_form)

        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.vertical_order, 1)
        self.mapper.addMapping(title_edit, 2)
        self.mapper.addMapping(image_path_edit, 3)
        self.mapper.setSubmitPolicy(QtWidgets.QDataWidgetMapper.ManualSubmit)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(title_label, 0, 0, 1, 1)
        layout.addWidget(title_edit, 0, 1, 1, 1)
        layout.addWidget(image_path_label, 1, 0, 1, 1)
        layout.addWidget(image_path_edit, 1, 1, 1, 1)
        layout.addWidget(cancel_button, 2, 0, 1, 1)
        layout.addWidget(submit_button, 2, 1, 1, 1)
        self.setLayout(layout)

        self.mapper.toFirst()

    def _submit_form(self):
        self.mapper.submit()
        self.close()
