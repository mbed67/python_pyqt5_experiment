from PyQt5 import QtCore
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel


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


class RestModel(QSqlQueryModel):
    """
    This model is coupled with a db
    """
    def flags(self, index):
        flags = super(RestModel, self).flags(index)

        if index.column() in (0, 2, 3, 4, 5):
            flags |= QtCore.Qt.ItemIsEditable

        return flags

    def setData(self, index, value, role):
        if index.column() not in (0, 2, 3, 4, 5):
            return False

        primaryKeyIndex = self.index(index.row(), 1)
        id = self.data(primaryKeyIndex)

        self.clear()

        column = {
            '0': 'title',
            '2': 'ib_phrase',
            '3': 'ob_phrase',
            '4': 'ib_short_phrase',
            '5': 'ob_short_phrase',
        }

        print(column.get(str(index.column())))
        print(value)

        ok = self.update_table(id, column.get(str(index.column())), value)

        self.refresh()

        return ok

    def refresh(self):
        self.setQuery('select title, id, ib_phrase, ob_phrase, ib_short_phrase, ob_short_phrase from phrases')
        self.setHeaderData(0, QtCore.Qt.Horizontal, "Title")
        self.setHeaderData(1, QtCore.Qt.Horizontal, "Id")
        self.setHeaderData(2, QtCore.Qt.Horizontal, "In breath")
        self.setHeaderData(3, QtCore.Qt.Horizontal, "Out breath")
        self.setHeaderData(4, QtCore.Qt.Horizontal, "In short")
        self.setHeaderData(5, QtCore.Qt.Horizontal, "Out short")
        return True

    def update_table(self, id, column, value):
        query = QSqlQuery()
        query.prepare('update phrases set ' + column + ' = ? where id = ?')
        query.addBindValue(value)
        query.addBindValue(id)
        return query.exec_()
