from PyQt5 import QtCore
from PyQt5.QtSql import QSqlTableModel


class BreathingModel(QtCore.QAbstractListModel):
    """
    This is a model that is not coupled with a db but that has the data injected
    """
    def __init__(self, phrases=["one", "two", "three", "four", "five"], parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__phrases = phrases

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__phrases)

    def data(self, index, role=None):
        """ This method runs for every role """

        if role == QtCore.Qt.EditRole:
            return self.__phrases[index.row()]

        if role == QtCore.Qt.ToolTipRole:
            return "Select a breathing phrase"

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            value = self.__phrases[row]
            return value

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role=None):

        if role == QtCore.Qt.EditRole:
            row = index.row()
            self.__phrases[row] = value
            self.dataChanged.emit(index, index)
            return True

        return False

    def insertRows(self, position, rows, parent=QtCore.QModelIndex(), *args, **kwargs):
        self.beginInsertRows(parent, position, position + rows - 1)

        for i in range(rows):
            self.__phrases.insert(position, '')

        self.endInsertRows()

        return True

    def removeRows(self, position, rows, parent=QtCore.QModelIndex(), *args, **kwargs):
        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            value = self.__phrases[position]
            self.__phrases.remove(value)

        self.endRemoveRows()

        return True


class RestModel(QSqlTableModel):
    """
    This model is coupled with a db
    """
    def __init__(self):
        QSqlTableModel.__init__(self)
        self.setTable('phrases')
        self.select()
