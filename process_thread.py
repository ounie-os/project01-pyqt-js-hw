from PyQt5.QtCore import QThread

from ExcelTEST001_02 import func_filling_table
from ExcelTEST003_DBWrite003 import DB_Write


class generateTableThread(QThread):
    def __init__(self):
        super(generateTableThread, self).__init__()

    def run(self):
        func_filling_table()


class dbWriteThread(QThread):
    def __init__(self):
        super(dbWriteThread, self).__init__()

    def run(self):
        DB_Write()
