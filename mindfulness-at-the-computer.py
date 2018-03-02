#!/usr/bin/env python3
import logging
import os
import sys
from PyQt5 import Qt, QtWidgets
from mc.model.Model import *
from mc.gui.main_win import MainWin
from mc import mc_global
import mc.db


class App(Qt.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.breathing_model = BreathingModel(["one", "two", "three", "four", "five"])
        self.rest_model = RestModel()

        self.main_view = MainWin(self.breathing_model, self.rest_model)
        self.main_view.show()


if __name__ == '__main__':
    mc_global.db_file_exists_at_application_startup_bl = os.path.isfile(mc_global.get_database_filename())
    # -settings this variable before the file has been created

    logging.basicConfig(level=logging.DEBUG)  # -by default only warnings and higher are shown

    # Application information

    mc.mc_global.sys_info_telist.append(("Application name", mc.mc_global.APPLICATION_VERSION_STR))
    mc.mc_global.sys_info_telist.append(("Application version", mc.mc_global.APPLICATION_VERSION_STR))

    # get db connection
    db_conn = mc.db.get_db_connection()
    # mc.mc_global.sys_info_telist.append(("Application database schema version", mc.db.get_schema_version(db_conn)))
    # mc.mc_global.sys_info_telist.append(("Python version", sys.version))
    # mc.mc_global.sys_info_telist.append(("SQLite version", sqlite3.sqlite_version))
    # mc.mc_global.sys_info_telist.append(("PySQLite (Python module) version", sqlite3.version))
    # mc.mc_global.sys_info_telist.append(("Qt version", QtCore.qVersion()))
    # noinspection PyUnresolvedReferences
    mc.mc_global.sys_info_telist.append(("PyQt (Python module) version", Qt.PYQT_VERSION_STR))

    matc_qapplication = App(sys.argv)
    desktop_widget = matc_qapplication.desktop()
    mc.mc_global.sys_info_telist.append(("Virtual desktop", str(desktop_widget.isVirtualDesktop())))
    mc.mc_global.sys_info_telist.append(("Screen count", str(desktop_widget.screenCount())))
    mc.mc_global.sys_info_telist.append(("Primary screen", str(desktop_widget.primaryScreen())))
    translator = QtCore.QTranslator()

    # Warning While removing debug keep the loading call intact
    system_locale = QtCore.QLocale.system().name()
    logging.info('System Localization: ' + system_locale)
    logging.info(
        'Localization Load Status: ' + str(translator.load(system_locale + '.qm', 'translate/' + system_locale))
    )  # -name, dir
    matc_qapplication.installTranslator(translator)

    matc_qapplication.setQuitOnLastWindowClosed(False)

    if mc.mc_global.db_upgrade_message_str:
        # noinspection PyCallByClass
        QtWidgets.QMessageBox.warning(matc_main_window, "title", mc.mc_global.db_upgrade_message_str)

    sys.exit(matc_qapplication.exec_())
