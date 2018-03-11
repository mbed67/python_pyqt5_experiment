from PyQt5.QtSql import QSqlTableModel


class BreathingModel(QSqlTableModel):
    """
    This model is coupled with a db
    """
    def __init__(self):
        QSqlTableModel.__init__(self)
        self.setTable('phrases')
        self.select()


class RestModel(QSqlTableModel):
    """
    This model is coupled with a db
    """
    def __init__(self):
        QSqlTableModel.__init__(self)
        self.setTable('rest_actions')
        self.select()
