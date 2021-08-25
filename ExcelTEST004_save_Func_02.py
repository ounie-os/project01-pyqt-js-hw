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


def save2():
    import pandas as pd
    import numpy as np
    import json
    import csv
    from ExcelTEST002_judge03 import judge03


    f = open('./config.json')  # 读取配置文件
    t = json.load(f)  # 将json格式的数据映射成list的形式
    f.close()  # 关闭文件

    try:
        file0001 ,file0002 = judge03()

        save_filename011 = t['save_filename0111']
        save_filename022 = t['save_filename0222']

        file0001.to_csv(save_filename011, encoding='utf_8_sig', quoting=csv.QUOTE_NONNUMERIC)
        file0002.to_csv(save_filename022, encoding='utf_8_sig', quoting=csv.QUOTE_NONNUMERIC)
        return 0, None
    except Exception as e:
        print(e)
        return -1, e

    # return file0001,file0002
