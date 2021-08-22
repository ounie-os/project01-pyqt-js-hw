import sys

import json
import time  # 导入时间模块
import pandas as pd
import csv
import numpy as np
import pymysql
import datetime
import os.path
import apprcc_rc
import ExcelTEST001
import ExcelTEST002_judge
import ExcelTEST003_DBWrite002
import ExcelTEST004_save_Func
import ExcelTEST005_DB_test
import skeleton
import tab_horizontal_west
import process_thread
import cryptography

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QStyleFactory

from file import FileOperation

os.environ['QT_ENABLE_HIGHDPI_SCALING'] = '1'
QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

app = QtWidgets.QApplication(sys.argv)
app.setStyle(QStyleFactory.create("Fusion"))
print(QStyleFactory.keys())
file_widget = FileOperation()
file_widget.set_up_ui()
file_widget.show()

sys.exit(app.exec_())
