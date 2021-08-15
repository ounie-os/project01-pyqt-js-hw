from PyQt5.QtCore import QThread
from ExcelTEST003_DBWrite002 import DB_Write
from ExcelTEST001 import func_filling_table


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
