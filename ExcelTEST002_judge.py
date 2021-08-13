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
'''
六个可选参数：
"judge_para01":"建筑面积(平方米)",
"judge_para02":"总能耗(千克标准煤)",
"judge_para03":"面积均能耗",
"judge_para04":"总用水",
"judge_para05":"总用电",
"judge_para06":"天然气总用量"
'''

def judge():
    import pandas as pd
    import numpy as np
    import json
    import csv

    f = open('./config.json')  # 读取配置文件
    t = json.load(f)  # 将json格式的数据映射成list的形式
    f.close()  # 关闭文件

    filename01 = t['judge_filename01']   #基表1名称
    filename02 = t['judge_filename02']   #基表2名称
    judge_para01 = t['judge_parameters']['judge_para01']   #筛选参数1，建筑面积(平方米)
    judge_para02 = t['judge_parameters']['judge_para02']   #筛选参数2，总能耗(千克标准煤)
    judge_para03 = t['judge_parameters']['judge_para03']   #筛选参数3，面积均能耗
    judge_para04 = t['judge_parameters']['judge_para04']   #筛选参数4，总用水
    judge_para05 = t['judge_parameters']['judge_para05']   #筛选参数5，总用电
    judge_para06 = t['judge_parameters']['judge_para06']   #筛选参数6，天然气总用量

    judge_para01_max = t['judge_parameters_range']['judge_range01']['max']   #筛选参数1的上限
    judge_para01_min = t['judge_parameters_range']['judge_range01']['min']   #筛选参数1的下限
    judge_para02_max = t['judge_parameters_range']['judge_range02']['max']   #筛选参数2的上限
    judge_para02_min = t['judge_parameters_range']['judge_range02']['min']   #筛选参数2的下限
    judge_para03_max = t['judge_parameters_range']['judge_range03']['max']   #筛选参数3的上限
    judge_para03_min = t['judge_parameters_range']['judge_range03']['min']   #筛选参数3的下限
    judge_para04_max = t['judge_parameters_range']['judge_range04']['max']   #筛选参数4的上限
    judge_para04_min = t['judge_parameters_range']['judge_range04']['min']   #筛选参数4的下限
    judge_para05_max = t['judge_parameters_range']['judge_range05']['max']   #筛选参数5的上限
    judge_para05_min = t['judge_parameters_range']['judge_range05']['min']   #筛选参数5的下限
    judge_para06_max = t['judge_parameters_range']['judge_range06']['max']   #筛选参数6的上限
    judge_para06_min = t['judge_parameters_range']['judge_range06']['min']   #筛选参数6的下限

    try:
        file01 = pd.read_csv(filename01, encoding='utf_8')  # 读入基表1
        file02 = pd.read_csv(filename02, encoding='utf_8')  # 读入基表2

        raw_dataNum = file01.shape[0]   #原始项目数量

        def select_max(num):
            if num == '':
                num = 9999999999999999999999999
            else:
                num = num
            return num

        def select_min(num):
            if num == '':
                num = -9999999999999999999999999
            else:
                num = num
            return num

        judge_para01_max = select_max(judge_para01_max)
        judge_para01_min = select_min(judge_para01_min)
        judge_para02_max = select_max(judge_para02_max)
        judge_para02_min = select_min(judge_para02_min)
        judge_para03_max = select_max(judge_para03_max)
        judge_para03_min = select_min(judge_para03_min)
        judge_para04_max = select_max(judge_para04_max)
        judge_para04_min = select_min(judge_para04_min)
        judge_para05_max = select_max(judge_para05_max)
        judge_para05_min = select_min(judge_para05_min)
        judge_para06_max = select_max(judge_para06_max)
        judge_para06_min = select_min(judge_para06_min)

        def judge01(file):
            file[file.loc[:, judge_para01] >= float(judge_para01_max)] = np.nan
            file[file.loc[:, judge_para01] <= float(judge_para01_min)] = np.nan
            file.dropna(axis=0, how='any', subset=[judge_para01], inplace=True)

        def judge02(file):
            file[file.loc[:, judge_para02] >= float(judge_para02_max)] = np.nan
            file[file.loc[:, judge_para02] <= float(judge_para02_min)] = np.nan
            file.dropna(axis=0, how='any', subset=[judge_para02], inplace=True)

        def judge03(file):
            file[file.loc[:, judge_para03] >= float(judge_para03_max)] = np.nan
            file[file.loc[:, judge_para03] <= float(judge_para03_min)] = np.nan
            file.dropna(axis=0, how='any', subset=[judge_para03], inplace=True)

        def judge04(file):
            file[file.loc[:, judge_para04] >= float(judge_para04_max)] = np.nan
            file[file.loc[:, judge_para04] <= float(judge_para04_min)] = np.nan
            file.dropna(axis=0, how='any', subset=[judge_para04], inplace=True)

        def judge05(file):
            file[file.loc[:, judge_para05] >= float(judge_para05_max)] = np.nan
            file[file.loc[:, judge_para05] <= float(judge_para05_min)] = np.nan
            file.dropna(axis=0, how='any', subset=[judge_para05], inplace=True)

        def judge06(file):
            file[file.loc[:, judge_para06] >= float(judge_para06_max)] = np.nan
            file[file.loc[:, judge_para06] <= float(judge_para06_min)] = np.nan
            file.dropna(axis=0, how='any', subset=[judge_para06], inplace=True)

        if judge_para01 == '':
            pass
        else:
            judge01(file01)
            judge01(file02)
            if judge_para02 == '':
                pass
            else:
                judge02(file01)
                judge02(file02)
                if judge_para03 == '':
                    pass
                else:
                    judge03(file01)
                    judge03(file02)
                    if judge_para04 == '':
                        pass
                    else:
                        judge04(file01)
                        judge04(file02)
                        if judge_para05 == '':
                            pass
                        else:
                            judge05(file01)
                            judge05(file02)
                            if judge_para06 == '':
                                pass
                            else:
                                judge06(file01)
                                judge06(file02)

        ###保存计算结果###
        new_dataNum = file01.shape[0]  # 处理后项目数量
        NumPer = new_dataNum/raw_dataNum*100   #计算百分比
        # print(raw_dataNum)
        # print(new_dataNum)
        # print(NumPer)
        result_json = {
            'raw_dataNum':raw_dataNum,
            'new_dataNum':new_dataNum,
            'NumPer':NumPer
        }
        result_json = json.dumps(result_json,ensure_ascii=False)
        tmp_f = open("result.json","w")
        tmp_f.write(result_json)
        tmp_f.flush()
        tmp_f.close()

        # def save_Func():
        #     save_filename011 = t['save_filename011']
        #     save_filename022 = t['save_filename022']
        #     file01.to_csv(save_filename011 + '.csv', encoding='utf_8_sig', quoting=csv.QUOTE_NONNUMERIC)
        #     file02.to_csv(save_filename022 + '.csv', encoding='utf_8_sig', quoting=csv.QUOTE_NONNUMERIC)

    except:
        print('-----------------ERROR-----------------')
    return file01,file02

