# cython: language_level=3


import json
import os.path
import sys
import time

from PyQt5 import QtCore, QtWidgets
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
        # self.init_data_screen_text()
        self.init_tooltip()

        self.checkBox.stateChanged[int].connect(self.checkbox_change)
        self.checkBox_2.stateChanged[int].connect(self.checkBox_2_change)
        self.checkBox_8.stateChanged[int].connect(self.checkBox_8_change)
        self.checkBox_14.stateChanged[int].connect(self.checkBox_14_change)
        self.checkBox_20.stateChanged[int].connect(self.checkBox_20_change)
        self.checkBox_26.stateChanged[int].connect(self.checkBox_26_change)
        self.checkBox_32.stateChanged[int].connect(self.checkBox_32_change)
        self.checkBox_38.stateChanged[int].connect(self.checkBox_38_change)
        self.checkBox_44.stateChanged[int].connect(self.checkBox_44_change)
        self.checkBox_50.stateChanged[int].connect(self.checkBox_50_change)

        self.generate_table_thread.started.connect(self.started_generate_table_thread)
        self.generate_table_thread.finished.connect(self.finished_generate_table_thread)

        self.db_write_thread.started.connect(self.started_db_write_thread)
        self.db_write_thread.finished.connect(self.finished_db_write_thread)

        self.tabWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.checkBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.tabWidget.currentChanged.connect(self.on_tabWidget_currentChanged)
        self.checkbox_name_ro_mapping = {
            self.checkBox_2: 'Jiguan_ro',
            self.checkBox_8: 'Tiyu_ro',
            self.checkBox_14: 'Wenhua_ro',
            self.checkBox_20: 'Jiaoyu_ro',
            self.checkBox_26: 'Tuanti_ro',
            self.checkBox_32: 'Qitabangong_ro',
            self.checkBox_38: 'Keji_ro',
            self.checkBox_44: 'Weisheng_ro',
            self.checkBox_50: 'Qita_ro',

            self.checkBox_3: 'Danweimianjihaodianliang',
            self.checkBox_4: 'Renjundianhao',
            self.checkBox_5: 'Danweimianjinenghao',
            self.checkBox_6: 'Renjunzonghenenghao',
            self.checkBox_7: 'Renjunshuihao',

            self.checkBox_9: 'Danweimianjihaodianliang',
            self.checkBox_10: 'Renjundianhao',
            self.checkBox_11: 'Danweimianjinenghao',
            self.checkBox_12: 'Renjunzonghenenghao',
            self.checkBox_13: 'Renjunshuihao',

            self.checkBox_15: 'Danweimianjihaodianliang',
            self.checkBox_16: 'Renjundianhao',
            self.checkBox_17: 'Danweimianjinenghao',
            self.checkBox_18: 'Renjunzonghenenghao',
            self.checkBox_19: 'Renjunshuihao',

            self.checkBox_21: 'Danweimianjihaodianliang',
            self.checkBox_22: 'Renjundianhao',
            self.checkBox_23: 'Danweimianjinenghao',
            self.checkBox_24: 'Renjunzonghenenghao',
            self.checkBox_25: 'Renjunshuihao',

            self.checkBox_27: 'Danweimianjihaodianliang',
            self.checkBox_28: 'Renjundianhao',
            self.checkBox_29: 'Danweimianjinenghao',
            self.checkBox_30: 'Renjunzonghenenghao',
            self.checkBox_31: 'Renjunshuihao',

            self.checkBox_33: 'Danweimianjihaodianliang',
            self.checkBox_34: 'Renjundianhao',
            self.checkBox_35: 'Danweimianjinenghao',
            self.checkBox_36: 'Renjunzonghenenghao',
            self.checkBox_37: 'Renjunshuihao',

            self.checkBox_39: 'Danweimianjihaodianliang',
            self.checkBox_40: 'Renjundianhao',
            self.checkBox_41: 'Danweimianjinenghao',
            self.checkBox_42: 'Renjunzonghenenghao',
            self.checkBox_43: 'Renjunshuihao',

            self.checkBox_45: 'Danweimianjihaodianliang',
            self.checkBox_46: 'Renjundianhao',
            self.checkBox_47: 'Danweimianjinenghao',
            self.checkBox_48: 'Renjunzonghenenghao',
            self.checkBox_49: 'Renjunshuihao',

            self.checkBox_51: 'Danweimianjihaodianliang',
            self.checkBox_52: 'Renjundianhao',
            self.checkBox_53: 'Danweimianjinenghao',
            self.checkBox_54: 'Renjunzonghenenghao',
            self.checkBox_55: 'Renjunshuihao',
        }

        self.checkbox_name_rw_mapping = {
            self.checkBox_2: ('Jiguan', 'Leixing01'),
            self.checkBox_8: ('Tiyu', 'Leixing02'),
            self.checkBox_14: ('Wenhua', 'Leixing03'),
            self.checkBox_20: ('Jiaoyu', 'Leixing04'),
            self.checkBox_26: ('Tuanti', 'Leixing05'),
            self.checkBox_32: ('Qitabangong', 'Leixing06'),
            self.checkBox_38: ('Keji', 'Leixing07'),
            self.checkBox_44: ('Weisheng', 'Leixing08'),
            self.checkBox_50: ('Qita', 'Leixing09'),

            self.checkBox_3: ('Jiguan', 'Danweimianjihaodianliang', 'name'),
            self.checkBox_4: ('Jiguan', 'Renjundianhao', 'name'),
            self.checkBox_5: ('Jiguan', 'Danweimianjinenghao', 'name'),
            self.checkBox_6: ('Jiguan', 'Renjunzonghenenghao', 'name'),
            self.checkBox_7: ('Jiguan', 'Renjunshuihao', 'name'),

            self.checkBox_9: ('Tiyu', 'Danweimianjihaodianliang', 'name'),
            self.checkBox_10: ('Tiyu', 'Renjundianhao', 'name'),
            self.checkBox_11: ('Tiyu', 'Danweimianjinenghao', 'name'),
            self.checkBox_12: ('Tiyu', 'Renjunzonghenenghao', 'name'),
            self.checkBox_13: ('Tiyu', 'Renjunshuihao', 'name'),

            self.checkBox_15: ('Wenhua', 'Danweimianjihaodianliang', 'name'),
            self.checkBox_16: ('Wenhua', 'Renjundianhao', 'name'),
            self.checkBox_17: ('Wenhua', 'Danweimianjinenghao', 'name'),
            self.checkBox_18: ('Wenhua', 'Renjunzonghenenghao', 'name'),
            self.checkBox_19: ('Wenhua', 'Renjunshuihao', 'name'),

            self.checkBox_21: ('Jiaoyu', 'Danweimianjihaodianliang', 'name'),
            self.checkBox_22: ('Jiaoyu', 'Renjundianhao', 'name'),
            self.checkBox_23: ('Jiaoyu', 'Danweimianjinenghao', 'name'),
            self.checkBox_24: ('Jiaoyu', 'Renjunzonghenenghao', 'name'),
            self.checkBox_25: ('Jiaoyu', 'Renjunshuihao', 'name'),

            self.checkBox_27: ('Tuanti', 'Danweimianjihaodianliang', 'name'),
            self.checkBox_28: ('Tuanti', 'Renjundianhao', 'name'),
            self.checkBox_29: ('Tuanti', 'Danweimianjinenghao', 'name'),
            self.checkBox_30: ('Tuanti', 'Renjunzonghenenghao', 'name'),
            self.checkBox_31: ('Tuanti', 'Renjunshuihao', 'name'),

            self.checkBox_33: ('Qitabangong', 'Danweimianjihaodianliang', 'name'),
            self.checkBox_34: ('Qitabangong', 'Renjundianhao', 'name'),
            self.checkBox_35: ('Qitabangong', 'Danweimianjinenghao', 'name'),
            self.checkBox_36: ('Qitabangong', 'Renjunzonghenenghao', 'name'),
            self.checkBox_37: ('Qitabangong', 'Renjunshuihao', 'name'),

            self.checkBox_39: ('Keji', 'Danweimianjihaodianliang', 'name'),
            self.checkBox_40: ('Keji', 'Renjundianhao', 'name'),
            self.checkBox_41: ('Keji', 'Danweimianjinenghao', 'name'),
            self.checkBox_42: ('Keji', 'Renjunzonghenenghao', 'name'),
            self.checkBox_43: ('Keji', 'Renjunshuihao', 'name'),

            self.checkBox_45: ('Weisheng', 'Danweimianjihaodianliang', 'name'),
            self.checkBox_46: ('Weisheng', 'Renjundianhao', 'name'),
            self.checkBox_47: ('Weisheng', 'Danweimianjinenghao', 'name'),
            self.checkBox_48: ('Weisheng', 'Renjunzonghenenghao', 'name'),
            self.checkBox_49: ('Weisheng', 'Renjunshuihao', 'name'),

            self.checkBox_51: ('Qita', 'Danweimianjihaodianliang', 'name'),
            self.checkBox_52: ('Qita', 'Renjundianhao', 'name'),
            self.checkBox_53: ('Qita', 'Danweimianjinenghao', 'name'),
            self.checkBox_54: ('Qita', 'Renjunzonghenenghao', 'name'),
            self.checkBox_55: ('Qita', 'Renjunshuihao', 'name')
        }

    def init_tooltip(self):
        self.pushButton.setToolTip(self.config_obj.extract_raw_table_items('hint1'))
        self.pushButton_2.setToolTip(self.config_obj.extract_raw_table_items('hint2'))
        self.pushButton_3.setToolTip(self.config_obj.extract_raw_table_items('hint3'))
        self.pushButton_4.setToolTip(self.config_obj.extract_raw_table_items('hint4'))
        self.pushButton_5.setToolTip(self.config_obj.extract_raw_table_items('hint5'))

    def label_border_radius_color_change(self, obj, status):
        if status == 1:
            obj.setStyleSheet("border:2px solid rgb(85, 170, 255);\n"
                              "border-radius:6px;color: rgb(85, 170, 255);")
        else:
            obj.setStyleSheet("border:2px solid rgb(150, 150, 150);\n"
                              "border-radius:6px;color: rgb(150, 150, 150);")

    def font_color_change(self, obj, status):
        if status == 1:
            obj.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                              "font: 12pt \"黑体\";\n"
                              "color: rgb(85, 170, 255);")
        else:
            obj.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                              "font: 12pt \"黑体\";\n"
                              "color: rgb(150, 150, 150);")

    def subcheckbox_font_color_change(self, obj, status):
        if status == 1:
            obj.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                              "font: 12pt \"黑体\";\n"
                              "color: rgb(0, 0, 0);")
        else:
            obj.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                              "font: 12pt \"黑体\";\n"
                              "color: rgb(150, 150, 150);")

    def set_obj_enable(self, obj_list: [QtWidgets.QCheckBox], status: int):
        if status == 1:
            for obj in obj_list:
                obj.setEnabled(True)
        else:
            for obj in obj_list:
                obj.setChecked(False)
                # emit必须加上参数，参数值任意，整数即可
                # 通知复选框对应的输入框改变状态
                obj.stateChanged.emit(1)
                obj.setEnabled(False)

    def set_widget_checkbox_color(self, label: QtWidgets.QLabel, main_obj: QtWidgets.QCheckBox,
                                  child_obj_list: [QtWidgets.QCheckBox]):
        '''筛选界面，勾选大标题，label和checkbox状态显示切换'''
        if main_obj.isChecked():
            # 被勾选，字体变成蓝色
            self.label_border_radius_color_change(label, 1)
            self.font_color_change(main_obj, 1)
            self.set_obj_enable(child_obj_list, 1)
        else:
            self.label_border_radius_color_change(label, 0)
            self.font_color_change(main_obj, 0)
            self.set_obj_enable(child_obj_list, 0)

    def set_lineEdit_enable(self, check_box_obj: QtWidgets.QCheckBox, line_edit_list: [QtWidgets.QLineEdit],
                            label_list: [QtWidgets.QLabel]):
        if check_box_obj.isChecked():
            self.subcheckbox_font_color_change(check_box_obj, 1)
            for obj in label_list:
                self.subcheckbox_font_color_change(obj, 1)
            for obj in line_edit_list:
                obj.setEnabled(True)
                self.subcheckbox_font_color_change(obj, 1)
        else:
            self.subcheckbox_font_color_change(check_box_obj, 0)
            for obj in label_list:
                self.subcheckbox_font_color_change(obj, 0)
            for obj in line_edit_list:
                obj.setEnabled(False)
                self.subcheckbox_font_color_change(obj, 0)
                obj.setText('')

    def update_checkbox_config_name(self, obj: QtWidgets.QCheckBox):
        if obj.isChecked():
            name_to_fill = self.checkbox_name_ro_mapping[obj]
            name = self.config_obj.extract_raw_table_items(name_to_fill)
            paths = self.checkbox_name_rw_mapping[obj]
            self.config_obj.modify_raw_table_items(*paths, v=name)
        else:
            paths = self.checkbox_name_rw_mapping[obj]
            self.config_obj.modify_raw_table_items(*paths, v="")

        self.config_obj.dump_to_file()

    def checkBox_2_change(self):
        child_checkbox_list = [
            self.checkBox_3,
            self.checkBox_4,
            self.checkBox_5,
            self.checkBox_6,
            self.checkBox_7
        ]
        self.set_widget_checkbox_color(self.label_54, self.checkBox_2, child_checkbox_list)

    def on_checkBox_3_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_5,
            self.lineEdit_6
        ]
        child_label_list = [
            self.label_30,
            self.label_31
        ]
        self.set_lineEdit_enable(self.checkBox_3, child_line_edit_list, child_label_list)

    def on_checkBox_4_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_7,
            self.lineEdit_8
        ]
        child_label_list = [
            self.label_32,
            self.label_33
        ]
        self.set_lineEdit_enable(self.checkBox_4, child_line_edit_list, child_label_list)

    def on_checkBox_5_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_9,
            self.lineEdit_10
        ]
        child_label_list = [
            self.label_34,
            self.label_35
        ]
        self.set_lineEdit_enable(self.checkBox_5, child_line_edit_list, child_label_list)

    def on_checkBox_6_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_11,
            self.lineEdit_12
        ]
        child_label_list = [
            self.label_36,
            self.label_37
        ]
        self.set_lineEdit_enable(self.checkBox_6, child_line_edit_list, child_label_list)

    def on_checkBox_7_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_48,
            self.lineEdit_49
        ]
        child_label_list = [
            self.label_38,
            self.label_53
        ]
        self.set_lineEdit_enable(self.checkBox_7, child_line_edit_list, child_label_list)

    def checkBox_8_change(self):
        child_checkbox_list = [
            self.checkBox_9,
            self.checkBox_10,
            self.checkBox_11,
            self.checkBox_12,
            self.checkBox_13
        ]
        self.set_widget_checkbox_color(self.label_55, self.checkBox_8, child_checkbox_list)

    def on_checkBox_9_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_50,
            self.lineEdit_51
        ]
        child_label_list = [
            self.label_56,
            self.label_57
        ]
        self.set_lineEdit_enable(self.checkBox_9, child_line_edit_list, child_label_list)

    def on_checkBox_10_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_52,
            self.lineEdit_53
        ]
        child_label_list = [
            self.label_58,
            self.label_59
        ]
        self.set_lineEdit_enable(self.checkBox_10, child_line_edit_list, child_label_list)

    def on_checkBox_11_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_54,
            self.lineEdit_55
        ]
        child_label_list = [
            self.label_60,
            self.label_61
        ]
        self.set_lineEdit_enable(self.checkBox_11, child_line_edit_list, child_label_list)

    def on_checkBox_12_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_56,
            self.lineEdit_57
        ]
        child_label_list = [
            self.label_62,
            self.label_63
        ]
        self.set_lineEdit_enable(self.checkBox_12, child_line_edit_list, child_label_list)

    def on_checkBox_13_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_58,
            self.lineEdit_59
        ]
        child_label_list = [
            self.label_64,
            self.label_65
        ]
        self.set_lineEdit_enable(self.checkBox_13, child_line_edit_list, child_label_list)

    def checkBox_14_change(self):
        child_checkbox_list = [
            self.checkBox_15,
            self.checkBox_16,
            self.checkBox_17,
            self.checkBox_18,
            self.checkBox_19
        ]
        self.set_widget_checkbox_color(self.label_66, self.checkBox_14, child_checkbox_list)

    def on_checkBox_15_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_60,
            self.lineEdit_61
        ]
        child_label_list = [
            self.label_67,
            self.label_68
        ]
        self.set_lineEdit_enable(self.checkBox_15, child_line_edit_list, child_label_list)

    def on_checkBox_16_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_62,
            self.lineEdit_63
        ]
        child_label_list = [
            self.label_69,
            self.label_70
        ]
        self.set_lineEdit_enable(self.checkBox_16, child_line_edit_list, child_label_list)

    def on_checkBox_17_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_64,
            self.lineEdit_65
        ]
        child_label_list = [
            self.label_71,
            self.label_72
        ]
        self.set_lineEdit_enable(self.checkBox_17, child_line_edit_list, child_label_list)

    def on_checkBox_18_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_66,
            self.lineEdit_67
        ]
        child_label_list = [
            self.label_73,
            self.label_74
        ]
        self.set_lineEdit_enable(self.checkBox_18, child_line_edit_list, child_label_list)

    def on_checkBox_19_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_68,
            self.lineEdit_69
        ]
        child_label_list = [
            self.label_75,
            self.label_76
        ]
        self.set_lineEdit_enable(self.checkBox_19, child_line_edit_list, child_label_list)

    def checkBox_20_change(self):
        child_checkbox_list = [
            self.checkBox_21,
            self.checkBox_22,
            self.checkBox_23,
            self.checkBox_24,
            self.checkBox_25
        ]
        self.set_widget_checkbox_color(self.label_77, self.checkBox_20, child_checkbox_list)

    def on_checkBox_21_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_70,
            self.lineEdit_71
        ]
        child_label_list = [
            self.label_78,
            self.label_79
        ]
        self.set_lineEdit_enable(self.checkBox_21, child_line_edit_list, child_label_list)

    def on_checkBox_22_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_72,
            self.lineEdit_73
        ]
        child_label_list = [
            self.label_80,
            self.label_81
        ]
        self.set_lineEdit_enable(self.checkBox_22, child_line_edit_list, child_label_list)

    def on_checkBox_23_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_74,
            self.lineEdit_75
        ]
        child_label_list = [
            self.label_82,
            self.label_83
        ]
        self.set_lineEdit_enable(self.checkBox_23, child_line_edit_list, child_label_list)

    def on_checkBox_24_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_76,
            self.lineEdit_77
        ]
        child_label_list = [
            self.label_84,
            self.label_85
        ]
        self.set_lineEdit_enable(self.checkBox_24, child_line_edit_list, child_label_list)

    def on_checkBox_25_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_78,
            self.lineEdit_79
        ]
        child_label_list = [
            self.label_86,
            self.label_87
        ]
        self.set_lineEdit_enable(self.checkBox_25, child_line_edit_list, child_label_list)

    def checkBox_26_change(self):
        child_checkbox_list = [
            self.checkBox_27,
            self.checkBox_28,
            self.checkBox_29,
            self.checkBox_30,
            self.checkBox_31
        ]
        self.set_widget_checkbox_color(self.label_88, self.checkBox_26, child_checkbox_list)

    def on_checkBox_27_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_80,
            self.lineEdit_81
        ]
        child_label_list = [
            self.label_89,
            self.label_90
        ]
        self.set_lineEdit_enable(self.checkBox_27, child_line_edit_list, child_label_list)

    def on_checkBox_28_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_82,
            self.lineEdit_83
        ]
        child_label_list = [
            self.label_91,
            self.label_92
        ]
        self.set_lineEdit_enable(self.checkBox_28, child_line_edit_list, child_label_list)

    def on_checkBox_29_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_84,
            self.lineEdit_85
        ]
        child_label_list = [
            self.label_93,
            self.label_94
        ]
        self.set_lineEdit_enable(self.checkBox_29, child_line_edit_list, child_label_list)

    def on_checkBox_30_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_86,
            self.lineEdit_87
        ]
        child_label_list = [
            self.label_95,
            self.label_96
        ]
        self.set_lineEdit_enable(self.checkBox_30, child_line_edit_list, child_label_list)

    def on_checkBox_31_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_88,
            self.lineEdit_89
        ]
        child_label_list = [
            self.label_97,
            self.label_98
        ]
        self.set_lineEdit_enable(self.checkBox_31, child_line_edit_list, child_label_list)

    def checkBox_32_change(self):
        child_checkbox_list = [
            self.checkBox_33,
            self.checkBox_34,
            self.checkBox_35,
            self.checkBox_36,
            self.checkBox_37
        ]
        self.set_widget_checkbox_color(self.label_99, self.checkBox_32, child_checkbox_list)

    def on_checkBox_33_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_90,
            self.lineEdit_91
        ]
        child_label_list = [
            self.label_100,
            self.label_101
        ]
        self.set_lineEdit_enable(self.checkBox_33, child_line_edit_list, child_label_list)

    def on_checkBox_34_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_92,
            self.lineEdit_93
        ]
        child_label_list = [
            self.label_102,
            self.label_103
        ]
        self.set_lineEdit_enable(self.checkBox_34, child_line_edit_list, child_label_list)

    def on_checkBox_35_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_94,
            self.lineEdit_95
        ]
        child_label_list = [
            self.label_104,
            self.label_105
        ]
        self.set_lineEdit_enable(self.checkBox_35, child_line_edit_list, child_label_list)

    def on_checkBox_36_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_96,
            self.lineEdit_97
        ]
        child_label_list = [
            self.label_106,
            self.label_107
        ]
        self.set_lineEdit_enable(self.checkBox_36, child_line_edit_list, child_label_list)

    def on_checkBox_37_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_98,
            self.lineEdit_99
        ]
        child_label_list = [
            self.label_108,
            self.label_109
        ]
        self.set_lineEdit_enable(self.checkBox_37, child_line_edit_list, child_label_list)

    def checkBox_38_change(self):
        child_checkbox_list = [
            self.checkBox_39,
            self.checkBox_40,
            self.checkBox_41,
            self.checkBox_42,
            self.checkBox_43
        ]
        self.set_widget_checkbox_color(self.label_110, self.checkBox_38, child_checkbox_list)

    def on_checkBox_39_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_100,
            self.lineEdit_101
        ]
        child_label_list = [
            self.label_111,
            self.label_112
        ]
        self.set_lineEdit_enable(self.checkBox_39, child_line_edit_list, child_label_list)

    def on_checkBox_40_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_102,
            self.lineEdit_103
        ]
        child_label_list = [
            self.label_113,
            self.label_114
        ]
        self.set_lineEdit_enable(self.checkBox_40, child_line_edit_list, child_label_list)

    def on_checkBox_41_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_104,
            self.lineEdit_105
        ]
        child_label_list = [
            self.label_115,
            self.label_116
        ]
        self.set_lineEdit_enable(self.checkBox_41, child_line_edit_list, child_label_list)

    def on_checkBox_42_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_106,
            self.lineEdit_107
        ]
        child_label_list = [
            self.label_117,
            self.label_118
        ]
        self.set_lineEdit_enable(self.checkBox_42, child_line_edit_list, child_label_list)

    def on_checkBox_43_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_108,
            self.lineEdit_109
        ]
        child_label_list = [
            self.label_119,
            self.label_120
        ]
        self.set_lineEdit_enable(self.checkBox_43, child_line_edit_list, child_label_list)

    def checkBox_44_change(self):
        child_checkbox_list = [
            self.checkBox_45,
            self.checkBox_46,
            self.checkBox_47,
            self.checkBox_48,
            self.checkBox_49
        ]
        self.set_widget_checkbox_color(self.label_121, self.checkBox_44, child_checkbox_list)

    def on_checkBox_45_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_110,
            self.lineEdit_111
        ]
        child_label_list = [
            self.label_122,
            self.label_123
        ]
        self.set_lineEdit_enable(self.checkBox_45, child_line_edit_list, child_label_list)

    def on_checkBox_46_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_112,
            self.lineEdit_113
        ]
        child_label_list = [
            self.label_124,
            self.label_125
        ]
        self.set_lineEdit_enable(self.checkBox_46, child_line_edit_list, child_label_list)

    def on_checkBox_47_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_114,
            self.lineEdit_115
        ]
        child_label_list = [
            self.label_126,
            self.label_127
        ]
        self.set_lineEdit_enable(self.checkBox_47, child_line_edit_list, child_label_list)

    def on_checkBox_48_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_116,
            self.lineEdit_117
        ]
        child_label_list = [
            self.label_128,
            self.label_129
        ]
        self.set_lineEdit_enable(self.checkBox_48, child_line_edit_list, child_label_list)

    def on_checkBox_49_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_118,
            self.lineEdit_119
        ]
        child_label_list = [
            self.label_130,
            self.label_131
        ]
        self.set_lineEdit_enable(self.checkBox_49, child_line_edit_list, child_label_list)

    def checkBox_50_change(self):
        child_checkbox_list = [
            self.checkBox_51,
            self.checkBox_52,
            self.checkBox_53,
            self.checkBox_54,
            self.checkBox_55
        ]
        self.set_widget_checkbox_color(self.label_132, self.checkBox_50, child_checkbox_list)

    def on_checkBox_51_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_120,
            self.lineEdit_121
        ]
        child_label_list = [
            self.label_133,
            self.label_134
        ]
        self.set_lineEdit_enable(self.checkBox_51, child_line_edit_list, child_label_list)

    def on_checkBox_52_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_122,
            self.lineEdit_123
        ]
        child_label_list = [
            self.label_135,
            self.label_136
        ]
        self.set_lineEdit_enable(self.checkBox_52, child_line_edit_list, child_label_list)

    def on_checkBox_53_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_124,
            self.lineEdit_125
        ]
        child_label_list = [
            self.label_137,
            self.label_138
        ]
        self.set_lineEdit_enable(self.checkBox_53, child_line_edit_list, child_label_list)

    def on_checkBox_54_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_126,
            self.lineEdit_127
        ]
        child_label_list = [
            self.label_139,
            self.label_140
        ]
        self.set_lineEdit_enable(self.checkBox_54, child_line_edit_list, child_label_list)

    def on_checkBox_55_stateChanged(self):
        child_line_edit_list = [
            self.lineEdit_128,
            self.lineEdit_129
        ]
        child_label_list = [
            self.label_141,
            self.label_142
        ]
        self.set_lineEdit_enable(self.checkBox_55, child_line_edit_list, child_label_list)

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
        self.pushButton_14.setEnabled(True)
        # 可以将筛选结果保存到文件
        self.pushButton_13.setEnabled(True)
        self.pushButton_15.setEnabled(True)
        # 完成按钮可以点击
        self.pushButton_17.setEnabled(True)
        self.pushButton_18.setEnabled(True)

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
            if k == 'raw_para11':
                continue
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
        save_filename022_name = self.config_obj.extract_raw_table_items('save_filename022_name')
        save_filename0111_name = self.config_obj.extract_raw_table_items('save_filename0111_name')
        save_filename0222_name = self.config_obj.extract_raw_table_items('save_filename0222_name')
        self.config_obj.modify_raw_table_items('save_filename01', v=save_dir + '/' + save_filename01_name)
        self.config_obj.modify_raw_table_items('save_filename02', v=save_dir + '/' + save_filename02_name)
        self.config_obj.modify_raw_table_items('judge_filename01', v=save_dir + '/' + save_filename01_name)
        self.config_obj.modify_raw_table_items('judge_filename02', v=save_dir + '/' + save_filename02_name)
        self.config_obj.modify_raw_table_items('save_filename011', v=save_dir + '/' + save_filename011_name)
        self.config_obj.modify_raw_table_items('save_filename022', v=save_dir + '/' + save_filename022_name)
        self.config_obj.modify_raw_table_items('save_filename0111', v=save_dir + '/' + save_filename0111_name)
        self.config_obj.modify_raw_table_items('save_filename0222', v=save_dir + '/' + save_filename0222_name)

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

        with open('result01.json') as f:
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

        first_tree_name = ['Jiguan', 'Tiyu', 'Wenhua', 'Jiaoyu', 'Tuanti', 'Qitabangong', 'Keji', 'Weisheng', 'Qita']
        second_tree_name = ['Danweimianjihaodianliang', 'Renjundianhao', 'Danweimianjinenghao', 'Renjunzonghenenghao',
                            'Renjunshuihao']
        value_list = [
            {
                second_tree_name[0]: [self.lineEdit_5, self.lineEdit_6],
                second_tree_name[1]: [self.lineEdit_7, self.lineEdit_8],
                second_tree_name[2]: [self.lineEdit_9, self.lineEdit_10],
                second_tree_name[3]: [self.lineEdit_11, self.lineEdit_12],
                second_tree_name[4]: [self.lineEdit_48, self.lineEdit_49]
            },
            {
                second_tree_name[0]: [self.lineEdit_50, self.lineEdit_51],
                second_tree_name[1]: [self.lineEdit_52, self.lineEdit_53],
                second_tree_name[2]: [self.lineEdit_54, self.lineEdit_55],
                second_tree_name[3]: [self.lineEdit_56, self.lineEdit_57],
                second_tree_name[4]: [self.lineEdit_58, self.lineEdit_59]
            },
            {
                second_tree_name[0]: [self.lineEdit_60, self.lineEdit_61],
                second_tree_name[1]: [self.lineEdit_62, self.lineEdit_63],
                second_tree_name[2]: [self.lineEdit_64, self.lineEdit_65],
                second_tree_name[3]: [self.lineEdit_66, self.lineEdit_67],
                second_tree_name[4]: [self.lineEdit_68, self.lineEdit_69]
            },
            {
                second_tree_name[0]: [self.lineEdit_70, self.lineEdit_71],
                second_tree_name[1]: [self.lineEdit_72, self.lineEdit_73],
                second_tree_name[2]: [self.lineEdit_74, self.lineEdit_75],
                second_tree_name[3]: [self.lineEdit_76, self.lineEdit_77],
                second_tree_name[4]: [self.lineEdit_78, self.lineEdit_79]
            },
            {
                second_tree_name[0]: [self.lineEdit_80, self.lineEdit_81],
                second_tree_name[1]: [self.lineEdit_82, self.lineEdit_83],
                second_tree_name[2]: [self.lineEdit_84, self.lineEdit_85],
                second_tree_name[3]: [self.lineEdit_86, self.lineEdit_87],
                second_tree_name[4]: [self.lineEdit_88, self.lineEdit_89]
            },
            {
                second_tree_name[0]: [self.lineEdit_90, self.lineEdit_91],
                second_tree_name[1]: [self.lineEdit_92, self.lineEdit_93],
                second_tree_name[2]: [self.lineEdit_94, self.lineEdit_95],
                second_tree_name[3]: [self.lineEdit_96, self.lineEdit_97],
                second_tree_name[4]: [self.lineEdit_98, self.lineEdit_99]
            },
            {
                second_tree_name[0]: [self.lineEdit_100, self.lineEdit_101],
                second_tree_name[1]: [self.lineEdit_102, self.lineEdit_103],
                second_tree_name[2]: [self.lineEdit_104, self.lineEdit_105],
                second_tree_name[3]: [self.lineEdit_106, self.lineEdit_107],
                second_tree_name[4]: [self.lineEdit_108, self.lineEdit_109]
            },
            {
                second_tree_name[0]: [self.lineEdit_110, self.lineEdit_111],
                second_tree_name[1]: [self.lineEdit_112, self.lineEdit_113],
                second_tree_name[2]: [self.lineEdit_114, self.lineEdit_115],
                second_tree_name[3]: [self.lineEdit_116, self.lineEdit_117],
                second_tree_name[4]: [self.lineEdit_118, self.lineEdit_119]
            },
            {
                second_tree_name[0]: [self.lineEdit_120, self.lineEdit_121],
                second_tree_name[1]: [self.lineEdit_122, self.lineEdit_123],
                second_tree_name[2]: [self.lineEdit_124, self.lineEdit_125],
                second_tree_name[3]: [self.lineEdit_126, self.lineEdit_127],
                second_tree_name[4]: [self.lineEdit_128, self.lineEdit_129]
            },
        ]

        for i in range(len(first_tree_name)):
            for j in range(len(second_tree_name)):
                for k in range(2):
                    self.config_obj.modify_raw_table_items(first_tree_name[i], second_tree_name[j],
                                                           'max' if k == 0 else 'min',
                                                           v=value_list[i][second_tree_name[j]][k].text())
        all_checkbox_list = [self.checkBox_3,
                             self.checkBox_4,
                             self.checkBox_5,
                             self.checkBox_6,
                             self.checkBox_7,

                             self.checkBox_9,
                             self.checkBox_10,
                             self.checkBox_11,
                             self.checkBox_12,
                             self.checkBox_13,

                             self.checkBox_15,
                             self.checkBox_16,
                             self.checkBox_17,
                             self.checkBox_18,
                             self.checkBox_19,

                             self.checkBox_21,
                             self.checkBox_22,
                             self.checkBox_23,
                             self.checkBox_24,
                             self.checkBox_25,

                             self.checkBox_27,
                             self.checkBox_28,
                             self.checkBox_29,
                             self.checkBox_30,
                             self.checkBox_31,

                             self.checkBox_33,
                             self.checkBox_34,
                             self.checkBox_35,
                             self.checkBox_36,
                             self.checkBox_37,

                             self.checkBox_39,
                             self.checkBox_40,
                             self.checkBox_41,
                             self.checkBox_42,
                             self.checkBox_43,

                             self.checkBox_45,
                             self.checkBox_46,
                             self.checkBox_47,
                             self.checkBox_48,
                             self.checkBox_49,

                             self.checkBox_51,
                             self.checkBox_52,
                             self.checkBox_53,
                             self.checkBox_54,
                             self.checkBox_55,

                             self.checkBox_2,
                             self.checkBox_8,
                             self.checkBox_14,
                             self.checkBox_20,
                             self.checkBox_26,
                             self.checkBox_32,
                             self.checkBox_38,
                             self.checkBox_44,
                             self.checkBox_50,
                             ]
        for checkbox_obj in all_checkbox_list:
            self.update_checkbox_config_name(checkbox_obj)

        self.config_obj.dump_to_file()

        judge03()

        with open('result01_1.json') as f:
            result = json.load(f)
            rate = round(result['NumPer'], 2)
            self.label_22.setText(str(result['raw_dataNum']))
            self.label_40.setText(str(result['new_dataNum']))
            self.label_41.setText(str(rate))

    @pyqtSlot()
    def on_pushButton_15_clicked(self):
        # 第二个保存按钮
        ret, info = save2()
        q = QMessageBox()
        if ret == 0:
            q.about(self, "提示", "成功")
        else:
            q.about(self, "提示", info)

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
    def on_lineEdit_46_editingFinished(self):
        self.config_obj.modify_raw_table_items('Xishu_dian', v=self.lineEdit_46.text())
        self.config_obj.dump_to_file()

    @pyqtSlot()
    def on_lineEdit_47_editingFinished(self):
        self.config_obj.modify_raw_table_items('Xishu_tianranqi', v=self.lineEdit_47.text())
        self.config_obj.dump_to_file()

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

    def dump_to_file(self):
        file_fp = open(self.file_path, mode='w')
        json.dump(self.file_py_obj, file_fp, ensure_ascii=False, indent=4)
        file_fp.flush()
        file_fp.close()

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
