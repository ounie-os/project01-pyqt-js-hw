import os.path
import time

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTabWidget

from skeleton import Ui_skeleton


class FileOperation(QMainWindow, Ui_skeleton):
    def __init__(self, parent=None):
        super(FileOperation, self).__init__(parent)

    def set_up_ui(self):
        self.setupUi(self)
        self.show_label_date_now()
        self.set_up_signal_slot()
        self.tabWidget.setTabPosition(QTabWidget.West)

    def show_label_date_now(self):
        # 显示当前日期
        self.label_46.setText(time.strftime("%Y-%m-%d", time.localtime()))

    def set_up_signal_slot(self):
        pass
        # 上传原表1按钮
        # self.pushButton.clicked.connect(self.upload_origin_table_1_file)

        # self.pushButton_2.clicked.connect(self.upload_origin_table_2_file)
        #
        # self.pushButton_3.clicked.connect(self.upload_origin_table_3_file)
        #
        # self.pushButton_4.clicked.connect(self.upload_new_table_1_file)
        #
        # self.pushButton_4.clicked.connect(self.upload_new_table_1_file)

    @pyqtSlot()
    def on_pushButton_16_clicked(self):
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', '/', 'Excel文件(*.xls *.xlsx)')
        file_name_with_extension = os.path.basename(fname)
        file_name = os.path.splitext(file_name_with_extension)[0]
        self.label_40.setText(file_name)
        # excel_file = pd.read_excel((fname))
        # print(excel_file)

    @pyqtSlot()
    def on_pushButton_17_clicked(self):
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', '/', 'Excel文件(*.xls *.xlsx)')
        file_name_with_extension = os.path.basename(fname)
        file_name = os.path.splitext(file_name_with_extension)[0]
        self.label_41.setText(file_name)

    @pyqtSlot()
    def on_pushButton_21_clicked(self):
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', '/', 'Excel文件(*.xls *.xlsx)')
        file_name_with_extension = os.path.basename(fname)
        file_name = os.path.splitext(file_name_with_extension)[0]
        self.label_48.setText(file_name)

    @pyqtSlot()
    def on_pushButton_18_clicked(self):
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', '/', 'Excel文件(*.xls *.xlsx)')
        file_name_with_extension = os.path.basename(fname)
        file_name = os.path.splitext(file_name_with_extension)[0]
        self.label_43.setText(file_name)

    @pyqtSlot()
    def on_pushButton_19_clicked(self):
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', '/', 'Excel文件(*.xls *.xlsx)')
        file_name_with_extension = os.path.basename(fname)
        file_name = os.path.splitext(file_name_with_extension)[0]
        self.label_45.setText(file_name)