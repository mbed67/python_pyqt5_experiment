import enum

from PyQt5 import Qt, QtCore

from PyQt5.QtSql import QSqlTableModel, QSqlQuery


class BreathingModel(QSqlTableModel):
    """
    This model is coupled with a db
    """
    def __init__(self):
        QSqlTableModel.__init__(self)
        self.setTable('phrases')
        self.setSort(1, QtCore.Qt.AscendingOrder)
        self.select()

    @staticmethod
    def max_vertical_order_breathing_phrases():
        query = QSqlQuery("select max(vertical_order) from phrases")
        query.next()
        return query.value(0)


class RestModel(QSqlTableModel):
    """
    This model is coupled with a db
    """
    def __init__(self):
        QSqlTableModel.__init__(self)
        self.setTable('rest_actions')
        self.select()

    @staticmethod
    def max_vertical_order_rest_phrases():
        query = QSqlQuery("select max(vertical_order) from rest_actions")
        query.next()
        return query.value(0)
