import json
import os.path
import time

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTabWidget, QMessageBox

from skeleton import Ui_skeleton

from ExcelTEST001 import func_filling_table
from ExcelTEST002_judge import judge


class FileOperation(QMainWindow, Ui_skeleton):
    def __init__(self, parent=None):
        super(FileOperation, self).__init__(parent)
        # 初始化配置文件
        self.config_obj = MyConfig('./config.json')
        self.permit_next = set()

    def set_up_ui(self):
        self.setupUi(self)
        
        # 实现去掉最小化窗口的按钮
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

        self.show_label_date_now()
        self.set_up_signal_slot()
        self.init_placeholder_text()
        self.init_data_screen_text()

    def show_label_date_now(self):
        # 显示当前日期
        time_str_now = time.strftime("%Y-%m-%d", time.localtime())
        self.label_16.setText(time_str_now)
        # 改变config.json里面的时间。暂时还未写入实际文件，待生成基表之前写入
        self.config_obj.modify_raw_table_items('table_data', v=time_str_now)

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

    def init_data_screen_text(self):
        judge_combox_list = [
            self.comboBox,
            self.comboBox_2,
            self.comboBox_3,
            self.comboBox_4,
            self.comboBox_5,
            self.comboBox_6,
        ]
        judge_parameters_dict = self.config_obj.extract_raw_table_items('judge_parameters_ro')

        valid_count = 0

        # 找出有多少个筛选条件
        for v in judge_parameters_dict.values():
            if len(v) > 0:
                valid_count += 1

        for i in range(len(judge_combox_list)):
            judge_combox_list[i].addItem("无")

        for index in range(valid_count):
            for v in judge_parameters_dict.values():
                if len(v) > 0:
                    judge_combox_list[index].addItem(v)
            judge_combox_list[index].setCurrentIndex(0)

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
            self.lineEdit_28
        ]
        self.fill_lineedit_placeholdertext(table_nengyuan_input_list, 'raw_parameters', 'table_nengyuan')

        table_jianzhu_input_list = [
            self.lineEdit_29,
            self.lineEdit_30,
            self.lineEdit_31,
            self.lineEdit_32,
            self.lineEdit_33,
            self.lineEdit_34,
            self.lineEdit_35,
            self.lineEdit_36,
            self.lineEdit_37,
            self.lineEdit_38,
            self.lineEdit_39,
            self.lineEdit_40
        ]
        self.fill_lineedit_placeholdertext(table_jianzhu_input_list, 'raw_parameters', 'table_jianzhu')

        table_shebei_input_list = [
            self.lineEdit_41,
            self.lineEdit_42,
            self.lineEdit_43,
            self.lineEdit_44
        ]

        self.fill_lineedit_placeholdertext(table_shebei_input_list, 'raw_parameters', 'table_shebei')

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
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', '.', 'Excel文件(*.xls *.xlsx)')
        file_name_with_extension = os.path.basename(fname)
        file_dir = os.path.dirname(fname)
        self.config_obj.modify_raw_table_items('filepath', v=file_dir + '/')
        self.config_obj.modify_raw_table_items('raw_tables', 'nengyuanziyuan', v=file_name_with_extension)
        self.label_6.setText(file_name_with_extension)
        self.permit_next.add(1)
        self.permit_next_judge()

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        # 打开原表2
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', '.', 'Excel文件(*.xls *.xlsx)')
        file_name_with_extension = os.path.basename(fname)
        file_dir = os.path.dirname(fname)
        self.config_obj.modify_raw_table_items('filepath', v=file_dir + '/')
        self.config_obj.modify_raw_table_items('raw_tables', 'jianzhuxinxi', v=file_name_with_extension)
        self.label_8.setText(file_name_with_extension)
        self.permit_next.add(2)
        self.permit_next_judge()

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        # 打开原表3
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', '.', 'Excel文件(*.xls *.xlsx)')
        file_name_with_extension = os.path.basename(fname)
        file_dir = os.path.dirname(fname)
        self.config_obj.modify_raw_table_items('filepath', v=file_dir + '/')
        self.config_obj.modify_raw_table_items('raw_tables', 'shebeixinxi', v=file_name_with_extension)
        self.label_10.setText(file_name_with_extension)
        self.permit_next.add(3)
        self.permit_next_judge()

    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        # 基表1
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', '.', 'Excel文件(*.xls *.xlsx)')
        file_name_with_extension = os.path.basename(fname)
        file_dir = os.path.dirname(fname)
        self.config_obj.modify_raw_table_items('filepath', v=file_dir + '/')
        self.config_obj.modify_raw_table_items('target_table', 'Jibiao1', v=file_name_with_extension)
        self.label_12.setText(file_name_with_extension)
        self.permit_next.add(4)
        self.permit_next_judge()

    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        # 基表2
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', '.', 'Excel文件(*.xls *.xlsx)')
        file_name_with_extension = os.path.basename(fname)
        file_dir = os.path.dirname(fname)
        self.config_obj.modify_raw_table_items('filepath', v=file_dir + '/')
        self.config_obj.modify_raw_table_items('target_table', 'Jibiao2', v=file_name_with_extension)
        self.label_14.setText(file_name_with_extension)
        self.permit_next.add(5)
        self.permit_next_judge()

    @pyqtSlot()
    def on_pushButton_8_clicked(self):
        """
        表格上传完毕后，点击下一步
        :return:
        """
        self.tabWidget.setCurrentIndex(1)

    @pyqtSlot()
    def on_pushButton_10_clicked(self):
        self.tabWidget.setCurrentIndex(0)

    @pyqtSlot()
    def on_pushButton_11_clicked(self):
        self.tabWidget.setCurrentIndex(2)

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
            self.lineEdit_28
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
            "raw_para25"
        ]

        table_nengyuan_dict = self.config_obj.extract_raw_table_items("raw_parameters", "table_nengyuan")
        update_raw_parameters(table_nengyuan_dict, zip(table_nengyuan_key_list, table_nengyuan_input_list))

        # 原表2
        table_jianzhu_input_list = [
            self.lineEdit_29,
            self.lineEdit_30,
            self.lineEdit_31,
            self.lineEdit_32,
            self.lineEdit_33,
            self.lineEdit_34,
            self.lineEdit_35,
            self.lineEdit_36,
            self.lineEdit_37
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
            self.lineEdit_41,
            self.lineEdit_42
        ]

        table_shebei_key_list = [
            "raw_para08(09)",
            "raw_para21"
        ]

        table_shebei_dict = self.config_obj.extract_raw_table_items("raw_parameters", "table_shebei")
        update_raw_parameters(table_shebei_dict, zip(table_shebei_key_list, table_shebei_input_list))

        f = open(self.config_obj.file_path, mode='w')
        json.dump(self.config_obj.file_py_obj, f, ensure_ascii=False, indent=4)
        f.close()

        ret = func_filling_table()
        q = QMessageBox()
        if ret == 0:
            q.about(self, "提示", "成功")
        else:
            q.about(self, "提示", "失败")

    @pyqtSlot()
    def on_pushButton_12_clicked(self):
        # 筛选按钮
        # text_screen1对应第1个筛选条件的内容
        text_screen1 = self.comboBox.currentText()
        # 更新config.json文件中的judge_parameters
        self.config_obj.modify_raw_table_items('judge_parameters', 'judge_para01',
                                               v=text_screen1 if (text_screen1 != '无') else '')
        text_screen2 = self.comboBox_2.currentText()
        self.config_obj.modify_raw_table_items('judge_parameters', 'judge_para02',
                                               v=text_screen2 if (text_screen2 != '无') else '')
        text_screen3 = self.comboBox_3.currentText()
        self.config_obj.modify_raw_table_items('judge_parameters', 'judge_para03',
                                               v=text_screen3 if (text_screen3 != '无') else '')
        text_screen4 = self.comboBox_4.currentText()
        self.config_obj.modify_raw_table_items('judge_parameters', 'judge_para04',
                                               v=text_screen4 if (text_screen4 != '无') else '')
        text_screen5 = self.comboBox_5.currentText()
        self.config_obj.modify_raw_table_items('judge_parameters', 'judge_para05',
                                               v=text_screen5 if (text_screen5 != '无') else '')
        text_screen6 = self.comboBox_6.currentText()
        self.config_obj.modify_raw_table_items('judge_parameters', 'judge_para06',
                                               v=text_screen6 if (text_screen6 != '无') else '')

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
        max_screen3 = self.lineEdit_5.text()
        self.config_obj.modify_raw_table_items('judge_parameters_range', 'judge_range03', 'max',
                                               v=max_screen3 if len(max_screen3) else '')
        min_screen3 = self.lineEdit_6.text()
        self.config_obj.modify_raw_table_items('judge_parameters_range', 'judge_range03', 'min',
                                               v=min_screen3 if len(min_screen3) else '')
        max_screen4 = self.lineEdit_7.text()
        self.config_obj.modify_raw_table_items('judge_parameters_range', 'judge_range04', 'max',
                                               v=max_screen4 if len(max_screen4) else '')
        min_screen4 = self.lineEdit_8.text()
        self.config_obj.modify_raw_table_items('judge_parameters_range', 'judge_range04', 'min',
                                               v=min_screen4 if len(min_screen4) else '')
        max_screen5 = self.lineEdit_9.text()
        self.config_obj.modify_raw_table_items('judge_parameters_range', 'judge_range05', 'max',
                                               v=max_screen5 if len(max_screen5) else '')
        min_screen5 = self.lineEdit_10.text()
        self.config_obj.modify_raw_table_items('judge_parameters_range', 'judge_range05', 'min',
                                               v=min_screen5 if len(min_screen5) else '')
        max_screen6 = self.lineEdit_11.text()
        self.config_obj.modify_raw_table_items('judge_parameters_range', 'judge_range06', 'max',
                                               v=max_screen6 if len(max_screen6) else '')
        min_screen6 = self.lineEdit_12.text()
        self.config_obj.modify_raw_table_items('judge_parameters_range', 'judge_range06', 'min',
                                               v=min_screen6 if len(min_screen6) else '')

        f = open(self.config_obj.file_path, mode='w')
        json.dump(self.config_obj.file_py_obj, f, ensure_ascii=False, indent=4)
        f.close()

        ret = judge()
        q = QMessageBox()
        if ret == 0:
            q.about(self, "提示", "成功")
        else:
            q.about(self, "提示", "失败")

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
