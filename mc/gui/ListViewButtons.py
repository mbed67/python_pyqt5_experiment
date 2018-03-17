from PyQt5.QtWidgets import QHBoxLayout, QPushButton

from mc.mc_global import MoveDirectionEnum


class ListViewButtons(QHBoxLayout):
    def __init__(self, model, view, form, active_phrase=None, parent=None):
        super(ListViewButtons, self).__init__(parent)
        self.model = model
        self.view = view
        self.form = form
        self.active_phrase = active_phrase
        self._init_ui()

    def _init_ui(self):
        edit_qpb = QPushButton('edit')
        edit_qpb.clicked.connect(self.on_edit_clicked)

        add_qpb = QPushButton('add')
        add_qpb.clicked.connect(self.on_add_clicked)

        remove_qpb = QPushButton('remove')
        remove_qpb.clicked.connect(self.on_remove_clicked)

        move_up_qpb = QPushButton('up')
        move_up_qpb.clicked.connect(self.on_move_up_clicked)

        move_down_qpb = QPushButton('down')
        move_down_qpb.clicked.connect(self.on_move_down_clicked)

        self.view.doubleClicked.connect(self.on_edit_clicked)

        self.addWidget(edit_qpb)
        self.addWidget(add_qpb)
        self.addWidget(remove_qpb)
        self.addWidget(move_up_qpb)
        self.addWidget(move_down_qpb)

    def on_edit_clicked(self):
        self.form.show()

        if self.view.selectedIndexes():
            self.form.mapper.setCurrentIndex(self.view.selectedIndexes()[0].row())
        else:
            self.on_add_phrase_clicked()

    def on_add_clicked(self):
        row_nr = self.model.rowCount()
        vertical_order = row_nr + 1
        self.model.insertRow(row_nr)
        self.form.vertical_order.setText(str(vertical_order))
        self.form.mapper.toLast()
        self.form.show()

    def on_remove_clicked(self):
        if self.view.selectedIndexes():
            self.model.removeRow(self.view.selectedIndexes()[0].row())
            self.model.select()
            if self.active_phrase:
                self.active_phrase.mapper.toFirst()

    def on_move_up_clicked(self):
        current_index = self.view.currentIndex()
        if current_index != -1:
            self._move_up_or_down(current_index, MoveDirectionEnum.up)
            self.view.setCurrentIndex(
                current_index.sibling(current_index.row() - 1, current_index.column())
                if current_index.row() != 0
                else current_index
            )

    def on_move_down_clicked(self):
        current_index = self.view.currentIndex()
        if current_index != -1:
            self._move_up_or_down(current_index, MoveDirectionEnum.down)
            self.view.setCurrentIndex(
                current_index.sibling(current_index.row() + 1, current_index.column())
                if current_index.row() != current_index.model().rowCount() - 1
                else current_index
            )

    def _move_up_or_down(self, current_index, direction):
        old_vertical_order = current_index.sibling(current_index.row(), 1).data()
        new_vertical_order = old_vertical_order + direction.value
        row_to_swap = current_index.row() + direction.value
        self.model.setData(current_index.sibling(current_index.row(), 1), new_vertical_order)
        self.model.submitAll()
        self.model.setData(current_index.sibling(row_to_swap, 1), old_vertical_order)
        self.model.submitAll()
        self.model.select()

