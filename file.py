# cython: language_level=3


import json
import os.path
import time

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, QDate
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QLineEdit

import ExcelTEST004_save_Func
import ExcelTEST005_DB_test
from ExcelTEST002_judge02 import judge02
from ExcelTEST002_judge03 import judge03
from ExcelTEST004_save_Func_02 import save2
from process_thread import generateTableThread, dbWriteThread
from skeleton import Ui_MainWindow


class FileOperation(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(FileOperation, self).__init__(parent)
        # 初始化配置文件
        self.config_obj = MyConfig('./config.json')
        self.permit_next = set()
        self.permit_db = set()
        self.generate_table_thread = generateTableThread()
        self.db_write_thread = dbWriteThread()
        self.cur_dir = '.'

    def set_up_ui(self):
        self.setupUi(self)
        self.calendarWidget.setHidden(True)
        self.label_47.setHidden(True)
        self.label_48.setHidden(True)
        self.widget_15.setHidden(True)

        # 实现去掉最小化窗口的按钮
        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

        self.show_label_date_now()
        self.set_up_signal_slot()
        self.init_placeholder_text()
        self.init_data_screen_text()

        self.checkBox.stateChanged[int].connect(self.checkbox_change)

        self.generate_table_thread.started.connect(self.started_generate_table_thread)
        self.generate_table_thread.finished.connect(self.finished_generate_table_thread)

        self.db_write_thread.started.connect(self.started_db_write_thread)
        self.db_write_thread.finished.connect(self.finished_db_write_thread)

        self.tabWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.checkBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.tabWidget.currentChanged.connect(self.on_tabWidget_currentChanged)

    def started_generate_table_thread(self):
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.pushButton_9.setEnabled(False)
        self.pushButton_9.setText("生成基表中...")

    def finished_generate_table_thread(self):
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(True)
        self.pushButton_9.setText("生成基表并保存")
        self.pushButton_9.setEnabled(True)

        self.pushButton_11.setEnabled(True)
        # 可以进行筛选
        self.pushButton_12.setEnabled(True)
        # 可以将筛选结果保存到文件
        self.pushButton_13.setEnabled(True)
        # 完成按钮可以点击
        self.pushButton_17.setEnabled(True)

        q = QMessageBox()
        q.information(self, "提示", "完成")

    def started_db_write_thread(self):
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.pushButton_9.setEnabled(False)
        self.pushButton_16.setEnabled(False)
        self.pushButton_16.setText("请稍等...")

    def finished_db_write_thread(self):
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(True)
        self.pushButton_9.setEnabled(True)
        self.pushButton_16.setEnabled(True)
        self.pushButton_16.setText("写入数据库")
        q = QMessageBox()
        q.information(self, "提示", "完成")

    def checkbox_change(self, index):
        if self.checkBox.isChecked():
            self.lineEdit_45.setEchoMode(QLineEdit.Normal)
        else:
            self.lineEdit_45.setEchoMode(QLineEdit.Password)

    def show_label_date_now(self):
        # 显示当前日期
        time_str_now = time.strftime("%Y-%m-%d", time.localtime())
        self.label_16.setText(time_str_now)
        # 改变config.json里面的时间。暂时还未写入实际文件，待生成基表之前写入
        self.config_obj.modify_raw_table_items('table_data', v=time_str_now)

    def set_up_signal_slot(self):
        pass

    def init_data_screen_text(self):
        judge_label_list = [
            self.label,
            self.label_24
        ]
        judge_parameters_dict = self.config_obj.extract_raw_table_items('judge_parameters')

        index = 0
        for v in judge_parameters_dict.values():
            if len(v) > 0:
                judge_label_list[index].setText(v)
                index += 1
            if index > len(judge_label_list):
                break

    def fill_lineedit_placeholdertext(self, input_list, param1_str, param2_str):
        dict_items = self.config_obj.extract_raw_table_items(param1_str, param2_str)
        # 设置提示文字
        i = 0
        for k, v in dict_items.items():
            if i < len(input_list) and isinstance(v, (str,)) and len(v):
                input_list[i].setPlaceholderText(v)
                i += 1

    def init_placeholder_text(self):
        """
        设置用户输入框的默认值
        :return:
        """
        table_nengyuan_input_list = [
            self.lineEdit_17,
            self.lineEdit_18,
            self.lineEdit_19,
            self.lineEdit_20,
            self.lineEdit_21,
            self.lineEdit_22,
            self.lineEdit_23,
            self.lineEdit_24,
            self.lineEdit_25,
            self.lineEdit_26,
            self.lineEdit_27,
            self.lineEdit_28,
            self.lineEdit_32,
            self.lineEdit_30,
            self.lineEdit_31,
            self.lineEdit_29
        ]
        self.fill_lineedit_placeholdertext(table_nengyuan_input_list, 'raw_parameters', 'table_nengyuan')

        table_jianzhu_input_list = [
            self.lineEdit_33,
            self.lineEdit_34,
            self.lineEdit_35,
            self.lineEdit_36,
            self.lineEdit_37,
            self.lineEdit_38,
            self.lineEdit_39,
            self.lineEdit_40,
            self.lineEdit_44,
            self.lineEdit_42,
            self.lineEdit_43,
            self.lineEdit_41
        ]
        self.fill_lineedit_placeholdertext(table_jianzhu_input_list, 'raw_parameters', 'table_jianzhu')

        table_shebei_input_list = [
            self.lineEdit_133,
            self.lineEdit_130,
            self.lineEdit_131,
            self.lineEdit_132
        ]

        self.fill_lineedit_placeholdertext(table_shebei_input_list, 'raw_parameters', 'table_shebei')

        self.lineEdit_46.setPlaceholderText(self.config_obj.extract_raw_table_items('Xishu_dian'))

        self.lineEdit_47.setPlaceholderText(self.config_obj.extract_raw_table_items('Xishu_tianranqi'))


    def fill_lineedit_text(self, input_list, param1_str, param2_str):
        dict_items = self.config_obj.extract_raw_table_items(param1_str, param2_str)
        # 填充实际文字
        i = 0
        for k, v in dict_items.items():
            if i < len(input_list) and isinstance(v, (str,)) and len(v):
                input_list[i].setText(v)
                i += 1

    def permit_next_judge(self):
        """
        判断是否5个文件都上传完毕。完毕后下一步按钮才能被点击
        :return:
        """
        if len(self.permit_next) == 5:
            self.pushButton_8.setEnabled(True)
            self.pushButton_9.setEnabled(True)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        # 打开原表1
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', self.cur_dir, 'Excel文件(*.xls *.xlsx)')
        file_name_with_extension = os.path.basename(fname)
        file_dir = os.path.dirname(fname)
        self.cur_dir = file_dir
        self.config_obj.modify_raw_table_items('filepath', v=file_dir + '/')
        self.config_obj.modify_raw_table_items('raw_tables', 'nengyuanziyuan', v=file_name_with_extension)
        self.label_6.setText(file_name_with_extension)
        self.permit_next.add(1)
        self.permit_next_judge()

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        # 打开原表2
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', self.cur_dir, 'Excel文件(*.xls *.xlsx)')
        file_name_with_extension = os.path.basename(fname)
        file_dir = os.path.dirname(fname)
        self.cur_dir = file_dir
        self.config_obj.modify_raw_table_items('filepath', v=file_dir + '/')
        self.config_obj.modify_raw_table_items('raw_tables', 'jianzhuxinxi', v=file_name_with_extension)
        self.label_8.setText(file_name_with_extension)
        self.permit_next.add(2)
        self.permit_next_judge()

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        # 打开原表3
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', self.cur_dir, 'Excel文件(*.xls *.xlsx)')
        file_name_with_extension = os.path.basename(fname)
        file_dir = os.path.dirname(fname)
        self.cur_dir = file_dir
        self.config_obj.modify_raw_table_items('filepath', v=file_dir + '/')
        self.config_obj.modify_raw_table_items('raw_tables', 'shebeixinxi', v=file_name_with_extension)
        self.label_10.setText(file_name_with_extension)
        self.permit_next.add(3)
        self.permit_next_judge()

    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        # 基表1
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', self.cur_dir, 'Excel文件(*.xls *.xlsx)')
        file_name_with_extension = os.path.basename(fname)
        file_dir = os.path.dirname(fname)
        self.cur_dir = file_dir
        self.config_obj.modify_raw_table_items('filepath', v=file_dir + '/')
        self.config_obj.modify_raw_table_items('target_table', 'Jibiao1', v=file_name_with_extension)
        self.label_12.setText(file_name_with_extension)
        self.permit_next.add(4)
        self.permit_next_judge()

    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        # 基表2
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', self.cur_dir, 'Excel文件(*.xls *.xlsx)')
        file_name_with_extension = os.path.basename(fname)
        file_dir = os.path.dirname(fname)
        self.cur_dir = file_dir
        self.config_obj.modify_raw_table_items('filepath', v=file_dir + '/')
        self.config_obj.modify_raw_table_items('target_table', 'Jibiao2', v=file_name_with_extension)
        self.label_14.setText(file_name_with_extension)
        self.permit_next.add(5)
        self.permit_next_judge()

    @pyqtSlot()
    def on_pushButton_6_clicked(self):
        self.calendarWidget.setHidden(False)
        self.calendarWidget.clicked[QDate].connect(self.show_date)

    def show_date(self, date):
        date_str_today = date.toString("yyyy-MM-dd")
        self.label_16.setText(date_str_today)
        # 改变config.json里面的时间。暂时还未写入实际文件，待生成基表之前写入
        self.config_obj.modify_raw_table_items('table_data', v=date_str_today)
        self.calendarWidget.setHidden(True)
        # 日期设置完毕后，焦点设置回到日历按钮
        self.pushButton_6.setFocus()


    @pyqtSlot()
    def on_pushButton_8_clicked(self):
        """
        表格上传完毕后，点击下一步
        :return:
        """
        self.tabWidget.setCurrentIndex(2)

    @pyqtSlot()
    def on_pushButton_10_clicked(self):
        self.tabWidget.setCurrentIndex(1)

    @pyqtSlot()
    def on_pushButton_11_clicked(self):
        self.tabWidget.setCurrentIndex(3)

    @pyqtSlot()
    def on_pushButton_9_clicked(self):
        """
        生成基表并保存
        :return:
        """

        # 更新config.json文件中的raw_parameters
        def update_raw_parameters(target_dict, params_dict):
            for x in list(params_dict):
                target_dict[x[0]] = x[1].text() if len(x[1].text()) else target_dict[x[0]]

        # 用户选择文件路径并保存到config.json文件中
        save_dir = QFileDialog.getExistingDirectory(self, '请选择文件保存路径', '.')
        if len(save_dir) == 0:
            q = QMessageBox()
            q.information(self, "提示", "请选择基表保存路径")
            return
        save_filename01_name = self.config_obj.extract_raw_table_items('save_filename01_name')
        save_filename02_name = self.config_obj.extract_raw_table_items('save_filename02_name')
        save_filename011_name = self.config_obj.extract_raw_table_items('save_filename011_name')
        save_filename022_name = self.config_obj.extract_raw_table_items('save_filename011_name')
        self.config_obj.modify_raw_table_items('save_filename01', v=save_dir + '/' + save_filename01_name)
        self.config_obj.modify_raw_table_items('save_filename02', v=save_dir + '/' + save_filename02_name)
        self.config_obj.modify_raw_table_items('judge_filename01', v=save_dir + '/' + save_filename01_name)
        self.config_obj.modify_raw_table_items('judge_filename02', v=save_dir + '/' + save_filename02_name)
        self.config_obj.modify_raw_table_items('save_filename011', v=save_dir + '/' + save_filename011_name)
        self.config_obj.modify_raw_table_items('save_filename022', v=save_dir + '/' + save_filename022_name)

        # 原表1
        table_nengyuan_input_list = [
            self.lineEdit_17,
            self.lineEdit_18,
            self.lineEdit_19,
            self.lineEdit_20,
            self.lineEdit_21,
            self.lineEdit_22,
            self.lineEdit_23,
            self.lineEdit_24,
            self.lineEdit_25,
            self.lineEdit_26,
            self.lineEdit_27,
            self.lineEdit_28,
            self.lineEdit_32,
            self.lineEdit_30,
            self.lineEdit_31,
            self.lineEdit_29
        ]

        table_nengyuan_key_list = [
            "raw_para01",
            "raw_para02",
            "raw_para05_1",
            "raw_para07_1",
            "raw_para12",
            "raw_para13",
            "raw_para14",
            "raw_para15",
            "raw_para16",
            "raw_para22",
            "raw_para24",
            "raw_para25",
            "raw_para26"
        ]

        table_nengyuan_dict = self.config_obj.extract_raw_table_items("raw_parameters", "table_nengyuan")
        update_raw_parameters(table_nengyuan_dict, zip(table_nengyuan_key_list, table_nengyuan_input_list))

        # 原表2
        table_jianzhu_input_list = [
            self.lineEdit_33,
            self.lineEdit_34,
            self.lineEdit_35,
            self.lineEdit_36,
            self.lineEdit_37,
            self.lineEdit_38,
            self.lineEdit_39,
            self.lineEdit_40,
            self.lineEdit_44,
            self.lineEdit_42,
            self.lineEdit_43,
            self.lineEdit_41
        ]

        table_jianzhu_key_list = [
            "raw_para03",
            "raw_para04",
            "raw_para05",
            "raw_para06",
            "raw_para07_2",
            "raw_para07_3",
            "raw_para10",
            "raw_para19",
            "raw_para20",
        ]

        table_jianzhu_dict = self.config_obj.extract_raw_table_items("raw_parameters", "table_jianzhu")
        update_raw_parameters(table_jianzhu_dict, zip(table_jianzhu_key_list, table_jianzhu_input_list))

        # 原表3
        table_shebei_input_list = [
            self.lineEdit_133,
            self.lineEdit_130
        ]

        table_shebei_key_list = [
            "raw_para08(09)",
            "raw_para21"
        ]

        table_shebei_dict = self.config_obj.extract_raw_table_items("raw_parameters", "table_shebei")
        update_raw_parameters(table_shebei_dict, zip(table_shebei_key_list, table_shebei_input_list))

        f = open(self.config_obj.file_path, mode='w')
        json.dump(self.config_obj.file_py_obj, f, ensure_ascii=False, indent=4)
        f.flush()
        f.close()

        # 开启填充基表的线程
        self.generate_table_thread.start()

    @pyqtSlot()
    def on_pushButton_13_clicked(self):
        # 第一个筛选按钮对应的保存

        ret, info = ExcelTEST004_save_Func.save()
        q = QMessageBox()
        if ret == 0:
            q.about(self, "提示", "成功")
        else:
            q.about(self, "提示", info)

    @pyqtSlot()
    def on_pushButton_12_clicked(self):
        # 第一个筛选按钮

        # 更新config.json文件中的judge_parameters_range
        max_screen1 = self.lineEdit.text()
        self.config_obj.modify_raw_table_items('judge_parameters_range', 'judge_range01', 'max',
                                               v=max_screen1 if len(max_screen1) else '')
        min_screen1 = self.lineEdit_2.text()
        self.config_obj.modify_raw_table_items('judge_parameters_range', 'judge_range01', 'min',
                                               v=min_screen1 if len(min_screen1) else '')
        max_screen2 = self.lineEdit_3.text()
        self.config_obj.modify_raw_table_items('judge_parameters_range', 'judge_range02', 'max',
                                               v=max_screen2 if len(max_screen2) else '')
        min_screen2 = self.lineEdit_4.text()
        self.config_obj.modify_raw_table_items('judge_parameters_range', 'judge_range02', 'min',
                                               v=min_screen2 if len(min_screen2) else '')

        f = open(self.config_obj.file_path, mode='w')
        json.dump(self.config_obj.file_py_obj, f, ensure_ascii=False, indent=4)
        f.flush()
        f.close()

        judge02()

        with open('result.json') as f:
            result = json.load(f)
            rate = round(result['NumPer'], 2)
            self.label_29.setText(str(result['raw_dataNum']))
            self.label_46.setText(str(result['new_dataNum']))
            self.label_51.setText(str(rate))

    @pyqtSlot()
    def on_pushButton_16_clicked(self):
        # 保存数据库操作
        self.pushButton_7.setFocus()
        self.db_write_thread.start()

    @pyqtSlot()
    def on_pushButton_17_clicked(self):
        q = QMessageBox()
        q.information(self, "提示", "完成")

    @pyqtSlot()
    def on_pushButton_7_clicked(self):
        self.set_db_config()

        error_reason = ExcelTEST005_DB_test.DB_Write_test()
        f = open('result02.json')
        result_obj = json.load(f)
        result = result_obj['connection_result']
        q = QMessageBox()
        if result == 0:
            q.information(self, "提示", "数据库连接成功")
            self.pushButton_16.setEnabled(True)
        else:
            q.information(self, "提示", error_reason)

    @pyqtSlot()
    def on_pushButton_14_clicked(self):
        # 第二个筛选按钮
        judge03()

    @pyqtSlot()
    def on_pushButton_15_clicked(self):
        # 第二个保存按钮
        save2()

    @pyqtSlot()
    def on_pushButton_18_clicked(self):
        # 前进到数据库界面
        self.tabWidget.setCurrentIndex(4)

    @pyqtSlot()
    def on_lineEdit_13_editingFinished(self):
        pass

    @pyqtSlot()
    def on_lineEdit_14_editingFinished(self):
        pass

    @pyqtSlot()
    def on_lineEdit_15_editingFinished(self):
        pass

    @pyqtSlot()
    def on_lineEdit_16_editingFinished(self):
        pass

    @pyqtSlot()
    def on_lineEdit_45_editingFinished(self):
        pass

    def set_db_config(self):
        host = self.lineEdit_13.text()
        port = self.lineEdit_14.text()
        database = self.lineEdit_15.text()
        username = self.lineEdit_16.text()
        password = self.lineEdit_45.text()
        self.config_obj.modify_raw_table_items('DB_connect', 'host', v=host)
        self.config_obj.modify_raw_table_items('DB_connect', 'port', v=port)
        self.config_obj.modify_raw_table_items('DB_connect', 'database', v=database)
        self.config_obj.modify_raw_table_items('DB_connect', 'username', v=username)
        self.config_obj.modify_raw_table_items('DB_connect', 'password', v=password)
        f = open(self.config_obj.file_path, mode='w')
        json.dump(self.config_obj.file_py_obj, f, ensure_ascii=False, indent=4)
        f.flush()
        f.close()

    @pyqtSlot()
    def on_lineEdit_17_editingFinished(self):
        """
        原表1 第1个编辑框编辑完毕
        :return:
        """
        # print(self.lineEdit_17.text())
        pass

    @pyqtSlot()
    def on_lineEdit_18_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_19_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_20_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_21_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_22_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_23_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_24_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_25_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_26_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_27_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_28_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_29_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_30_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_31_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_32_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_33_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_34_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_35_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_36_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_37_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_38_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_39_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_40_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_41_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_42_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_43_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_lineEdit_44_editingFinished(self):
        """

        :return:
        """
        pass

    @pyqtSlot()
    def on_tabWidget_currentChanged(self):
        index = self.tabWidget.currentIndex()
        if index == 0:
            self.label_47.setHidden(True)
            self.label_48.setHidden(True)
            self.widget_15.setHidden(True)
        else:
            self.label_47.setHidden(False)
            self.label_48.setHidden(False)
            self.widget_15.setHidden(False)


class MyConfig:
    def __init__(self, file_path):
        try:
            file_fp = open(file_path)
            self.file_py_obj = json.load(file_fp)
            self.file_path = file_path
            file_fp.close()
        except FileNotFoundError as e:
            print(e)

    def extract_raw_table_items(self, *params):
        result = None
        if len(params) == 1:
            result = self.file_py_obj[params[0]]
        elif len(params) == 2:
            result = self.file_py_obj[params[0]][params[1]]
        else:
            raise Exception
        return result

    def modify_raw_table_items(self, *k, v):
        if len(k) == 1:
            self.file_py_obj[k[0]] = v
        elif len(k) == 2:
            self.file_py_obj[k[0]][k[1]] = v
        elif len(k) == 3:
            self.file_py_obj[k[0]][k[1]][k[2]] = v
        else:
            raise Exception
