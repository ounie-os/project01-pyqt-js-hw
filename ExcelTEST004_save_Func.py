########## 00 软件功能说明##########
'''
主体功能：对原表进行判断筛选
操作方式：目前无界面，后期需要制作界面
相关表格文件-原始表：
相关表格文件-目标表：基表1、基表2
配置文件：config.json
程序版本：V1.0
修改人：黄巍
'''


def save():
    import pandas as pd
    import numpy as np
    import json
    import csv
    from ExcelTEST002_judge import judge


    f = open('./config.json')  # 读取配置文件
    t = json.load(f)  # 将json格式的数据映射成list的形式
    f.close()  # 关闭文件

    file01 ,file02 = judge()

    save_filename011 = t['save_filename011']
    save_filename022 = t['save_filename022']
    try:
        file01.to_csv(save_filename011, encoding='utf_8_sig', quoting=csv.QUOTE_NONNUMERIC)
        file02.to_csv(save_filename022, encoding='utf_8_sig', quoting=csv.QUOTE_NONNUMERIC)
        return 0
    except Exception as e:
        print(e)
        return -1

