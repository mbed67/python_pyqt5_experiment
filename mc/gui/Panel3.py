from PyQt5 import QtWidgets, QtGui
from mc.gui.ListViewButtons import ListViewButtons


class Panel3(QtWidgets.QVBoxLayout):
    def __init__(self, model, list_view, parent=None):
        super(Panel3, self).__init__(parent)

        self.rest_model = model
        self.rest_phrases_qlv = list_view
        self.edit_rest_phrase = EditRestPhrase(self.rest_model)
        self.button_box = ListViewButtons(self.rest_model, self.rest_phrases_qlv, self.edit_rest_phrase)
        self._init_ui()

    def _init_ui(self):
        self.rest_phrases_qlv.setModel(self.rest_model)
        self.rest_phrases_qlv.setModelColumn(2)

        self.addWidget(self.rest_phrases_qlv)
        self.addLayout(self.button_box)
        self.addStretch(1)


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
