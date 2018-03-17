import enum

from PyQt5 import Qt, QtCore

from PyQt5.QtSql import QSqlTableModel, QSqlQuery


class BreathingModel(QSqlTableModel):
    def __init__(self):
        QSqlTableModel.__init__(self)
        self.setTable('phrases')
        self.setSort(1, QtCore.Qt.AscendingOrder)
        self.select()


class RestModel(QSqlTableModel):
    def __init__(self):
        QSqlTableModel.__init__(self)
        self.setTable('rest_actions')
        self.setSort(1, QtCore.Qt.AscendingOrder)
        self.select()
