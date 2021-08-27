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
用于二次筛选的五个参数为：
单位面积电耗（kWh/㎡）
人均电耗（kWh/p）
单位面积能耗（kgce/㎡）
人均综合能耗（kgce/p）
人均水耗（m³/p）
'''

def judge03():
    import pandas as pd
    import numpy as np
    import json
    import csv
    from ExcelTEST002_judge02 import judge02

    f = open('./config.json')  # 读取配置文件
    t = json.load(f)  # 将json格式的数据映射成list的形式
    f.close()  # 关闭文件

    # tar_para05 = t['target_parameters']['table_jibiao1']['tar_para05']  # 建筑功能
    Jibiao01,Jibiao02 ,raw_dataNum= judge02()
    print('第一次筛选后的项目数：',Jibiao01.shape[0])

    save_file01 = t['save_filename0111']   #最后筛选完的基表1
    save_file02 = t['save_filename0222']   #最后筛选完的基表2

    Jiguan_name = t['Jiguan']['Leixing01']   #机关建筑名称
    Jiguan_Danweimianjidianhao_name = t['Jiguan']['Danweimianjihaodianliang']['name']   #单位面积耗电量-参数名
    Jiguan_Danweimianjidianhao_max = t['Jiguan']['Danweimianjihaodianliang']['max']   #单位面积耗电量-上限
    Jiguan_Danweimianjidianhao_min = t['Jiguan']['Danweimianjihaodianliang']['min']   #单位面积耗电量-下限
    Jiguan_Renjundianhao_name = t['Jiguan']['Renjundianhao']['name']   #人均电耗-参数名
    Jiguan_Renjundianhao_max = t['Jiguan']['Renjundianhao']['max']   #人均电耗-上限
    Jiguan_Renjundianhao_min = t['Jiguan']['Renjundianhao']['min']   #人均电耗-下限
    Jiguan_Danweimianjinenghao_name = t['Jiguan']['Danweimianjinenghao']['name']   #单位面积能耗-参数名
    Jiguan_Danweimianjinenghao_max = t['Jiguan']['Danweimianjinenghao']['max']   #单位面积能耗-上限
    Jiguan_Danweimianjinenghao_min = t['Jiguan']['Danweimianjinenghao']['min']   #单位面积能耗-下限
    Jiguan_Renjunzonghenenghao_name = t['Jiguan']['Renjunzonghenenghao']['name']   #人均综合能耗-参数名
    Jiguan_Renjunzonghenenghao_max = t['Jiguan']['Renjunzonghenenghao']['max']   #人均综合能耗-上限
    Jiguan_Renjunzonghenenghao_min = t['Jiguan']['Renjunzonghenenghao']['min']   #人均综合能耗-下限
    Jiguan_Renjunshuihao_name = t['Jiguan']['Renjunshuihao']['name']   #人均水耗-参数名
    Jiguan_Renjunshuihao_max = t['Jiguan']['Renjunshuihao']['max']   #人均水耗-上限
    Jiguan_Renjunshuihao_min = t['Jiguan']['Renjunshuihao']['min']   #人均水耗-下限

    Tiyu_name = t['Tiyu']['Leixing02']   #机关建筑名称
    Tiyu_Danweimianjidianhao_name = t['Tiyu']['Danweimianjihaodianliang']['name']   #单位面积耗电量-参数名
    Tiyu_Danweimianjidianhao_max = t['Tiyu']['Danweimianjihaodianliang']['max']   #单位面积耗电量-上限
    Tiyu_Danweimianjidianhao_min = t['Tiyu']['Danweimianjihaodianliang']['min']   #单位面积耗电量-下限
    Tiyu_Renjundianhao_name = t['Tiyu']['Renjundianhao']['name']   #人均电耗-参数名
    Tiyu_Renjundianhao_max = t['Tiyu']['Renjundianhao']['max']   #人均电耗-上限
    Tiyu_Renjundianhao_min = t['Tiyu']['Renjundianhao']['min']   #人均电耗-下限
    Tiyu_Danweimianjinenghao_name = t['Tiyu']['Danweimianjinenghao']['name']   #单位面积能耗-参数名
    Tiyu_Danweimianjinenghao_max = t['Tiyu']['Danweimianjinenghao']['max']   #单位面积能耗-上限
    Tiyu_Danweimianjinenghao_min = t['Tiyu']['Danweimianjinenghao']['min']   #单位面积能耗-下限
    Tiyu_Renjunzonghenenghao_name = t['Tiyu']['Renjunzonghenenghao']['name']   #人均综合能耗-参数名
    Tiyu_Renjunzonghenenghao_max = t['Tiyu']['Renjunzonghenenghao']['max']   #人均综合能耗-上限
    Tiyu_Renjunzonghenenghao_min = t['Tiyu']['Renjunzonghenenghao']['min']   #人均综合能耗-下限
    Tiyu_Renjunshuihao_name = t['Tiyu']['Renjunshuihao']['name']   #人均水耗-参数名
    Tiyu_Renjunshuihao_max = t['Tiyu']['Renjunshuihao']['max']   #人均水耗-上限
    Tiyu_Renjunshuihao_min = t['Tiyu']['Renjunshuihao']['min']   #人均水耗-下限

    Wenhua_name = t['Wenhua']['Leixing03']   #机关建筑名称
    Wenhua_Danweimianjidianhao_name = t['Wenhua']['Danweimianjihaodianliang']['name']   #单位面积耗电量-参数名
    Wenhua_Danweimianjidianhao_max = t['Wenhua']['Danweimianjihaodianliang']['max']   #单位面积耗电量-上限
    Wenhua_Danweimianjidianhao_min = t['Wenhua']['Danweimianjihaodianliang']['min']   #单位面积耗电量-下限
    Wenhua_Renjundianhao_name = t['Wenhua']['Renjundianhao']['name']   #人均电耗-参数名
    Wenhua_Renjundianhao_max = t['Wenhua']['Renjundianhao']['max']   #人均电耗-上限
    Wenhua_Renjundianhao_min = t['Wenhua']['Renjundianhao']['min']   #人均电耗-下限
    Wenhua_Danweimianjinenghao_name = t['Wenhua']['Danweimianjinenghao']['name']   #单位面积能耗-参数名
    Wenhua_Danweimianjinenghao_max = t['Wenhua']['Danweimianjinenghao']['max']   #单位面积能耗-上限
    Wenhua_Danweimianjinenghao_min = t['Wenhua']['Danweimianjinenghao']['min']   #单位面积能耗-下限
    Wenhua_Renjunzonghenenghao_name = t['Wenhua']['Renjunzonghenenghao']['name']   #人均综合能耗-参数名
    Wenhua_Renjunzonghenenghao_max = t['Wenhua']['Renjunzonghenenghao']['max']   #人均综合能耗-上限
    Wenhua_Renjunzonghenenghao_min = t['Wenhua']['Renjunzonghenenghao']['min']   #人均综合能耗-下限
    Wenhua_Renjunshuihao_name = t['Wenhua']['Renjunshuihao']['name']   #人均水耗-参数名
    Wenhua_Renjunshuihao_max = t['Wenhua']['Renjunshuihao']['max']   #人均水耗-上限
    Wenhua_Renjunshuihao_min = t['Wenhua']['Renjunshuihao']['min']   #人均水耗-下限

    Jiaoyu_name = t['Jiaoyu']['Leixing04']   #机关建筑名称
    Jiaoyu_Danweimianjidianhao_name = t['Jiaoyu']['Danweimianjihaodianliang']['name']   #单位面积耗电量-参数名
    Jiaoyu_Danweimianjidianhao_max = t['Jiaoyu']['Danweimianjihaodianliang']['max']   #单位面积耗电量-上限
    Jiaoyu_Danweimianjidianhao_min = t['Jiaoyu']['Danweimianjihaodianliang']['min']   #单位面积耗电量-下限
    Jiaoyu_Renjundianhao_name = t['Jiaoyu']['Renjundianhao']['name']   #人均电耗-参数名
    Jiaoyu_Renjundianhao_max = t['Jiaoyu']['Renjundianhao']['max']   #人均电耗-上限
    Jiaoyu_Renjundianhao_min = t['Jiaoyu']['Renjundianhao']['min']   #人均电耗-下限
    Jiaoyu_Danweimianjinenghao_name = t['Jiaoyu']['Danweimianjinenghao']['name']   #单位面积能耗-参数名
    Jiaoyu_Danweimianjinenghao_max = t['Jiaoyu']['Danweimianjinenghao']['max']   #单位面积能耗-上限
    Jiaoyu_Danweimianjinenghao_min = t['Jiaoyu']['Danweimianjinenghao']['min']   #单位面积能耗-下限
    Jiaoyu_Renjunzonghenenghao_name = t['Jiaoyu']['Renjunzonghenenghao']['name']   #人均综合能耗-参数名
    Jiaoyu_Renjunzonghenenghao_max = t['Jiaoyu']['Renjunzonghenenghao']['max']   #人均综合能耗-上限
    Jiaoyu_Renjunzonghenenghao_min = t['Jiaoyu']['Renjunzonghenenghao']['min']   #人均综合能耗-下限
    Jiaoyu_Renjunshuihao_name = t['Jiaoyu']['Renjunshuihao']['name']   #人均水耗-参数名
    Jiaoyu_Renjunshuihao_max = t['Jiaoyu']['Renjunshuihao']['max']   #人均水耗-上限
    Jiaoyu_Renjunshuihao_min = t['Jiaoyu']['Renjunshuihao']['min']   #人均水耗-下限

    Tuanti_name = t['Tuanti']['Leixing05']   #机关建筑名称
    Tuanti_Danweimianjidianhao_name = t['Tuanti']['Danweimianjihaodianliang']['name']   #单位面积耗电量-参数名
    Tuanti_Danweimianjidianhao_max = t['Tuanti']['Danweimianjihaodianliang']['max']   #单位面积耗电量-上限
    Tuanti_Danweimianjidianhao_min = t['Tuanti']['Danweimianjihaodianliang']['min']   #单位面积耗电量-下限
    Tuanti_Renjundianhao_name = t['Tuanti']['Renjundianhao']['name']   #人均电耗-参数名
    Tuanti_Renjundianhao_max = t['Tuanti']['Renjundianhao']['max']   #人均电耗-上限
    Tuanti_Renjundianhao_min = t['Tuanti']['Renjundianhao']['min']   #人均电耗-下限
    Tuanti_Danweimianjinenghao_name = t['Tuanti']['Danweimianjinenghao']['name']   #单位面积能耗-参数名
    Tuanti_Danweimianjinenghao_max = t['Tuanti']['Danweimianjinenghao']['max']   #单位面积能耗-上限
    Tuanti_Danweimianjinenghao_min = t['Tuanti']['Danweimianjinenghao']['min']   #单位面积能耗-下限
    Tuanti_Renjunzonghenenghao_name = t['Tuanti']['Renjunzonghenenghao']['name']   #人均综合能耗-参数名
    Tuanti_Renjunzonghenenghao_max = t['Tuanti']['Renjunzonghenenghao']['max']   #人均综合能耗-上限
    Tuanti_Renjunzonghenenghao_min = t['Tuanti']['Renjunzonghenenghao']['min']   #人均综合能耗-下限
    Tuanti_Renjunshuihao_name = t['Tuanti']['Renjunshuihao']['name']   #人均水耗-参数名
    Tuanti_Renjunshuihao_max = t['Tuanti']['Renjunshuihao']['max']   #人均水耗-上限
    Tuanti_Renjunshuihao_min = t['Tuanti']['Renjunshuihao']['min']   #人均水耗-下限

    Qitabangong_name = t['Qitabangong']['Leixing06']   #机关建筑名称
    Qitabangong_Danweimianjidianhao_name = t['Qitabangong']['Danweimianjihaodianliang']['name']   #单位面积耗电量-参数名
    Qitabangong_Danweimianjidianhao_max = t['Qitabangong']['Danweimianjihaodianliang']['max']   #单位面积耗电量-上限
    Qitabangong_Danweimianjidianhao_min = t['Qitabangong']['Danweimianjihaodianliang']['min']   #单位面积耗电量-下限
    Qitabangong_Renjundianhao_name = t['Qitabangong']['Renjundianhao']['name']   #人均电耗-参数名
    Qitabangong_Renjundianhao_max = t['Qitabangong']['Renjundianhao']['max']   #人均电耗-上限
    Qitabangong_Renjundianhao_min = t['Qitabangong']['Renjundianhao']['min']   #人均电耗-下限
    Qitabangong_Danweimianjinenghao_name = t['Qitabangong']['Danweimianjinenghao']['name']   #单位面积能耗-参数名
    Qitabangong_Danweimianjinenghao_max = t['Qitabangong']['Danweimianjinenghao']['max']   #单位面积能耗-上限
    Qitabangong_Danweimianjinenghao_min = t['Qitabangong']['Danweimianjinenghao']['min']   #单位面积能耗-下限
    Qitabangong_Renjunzonghenenghao_name = t['Qitabangong']['Renjunzonghenenghao']['name']   #人均综合能耗-参数名
    Qitabangong_Renjunzonghenenghao_max = t['Qitabangong']['Renjunzonghenenghao']['max']   #人均综合能耗-上限
    Qitabangong_Renjunzonghenenghao_min = t['Qitabangong']['Renjunzonghenenghao']['min']   #人均综合能耗-下限
    Qitabangong_Renjunshuihao_name = t['Qitabangong']['Renjunshuihao']['name']   #人均水耗-参数名
    Qitabangong_Renjunshuihao_max = t['Qitabangong']['Renjunshuihao']['max']   #人均水耗-上限
    Qitabangong_Renjunshuihao_min = t['Qitabangong']['Renjunshuihao']['min']   #人均水耗-下限

    Keji_name = t['Keji']['Leixing07']   #机关建筑名称
    Keji_Danweimianjidianhao_name = t['Keji']['Danweimianjihaodianliang']['name']   #单位面积耗电量-参数名
    Keji_Danweimianjidianhao_max = t['Keji']['Danweimianjihaodianliang']['max']   #单位面积耗电量-上限
    Keji_Danweimianjidianhao_min = t['Keji']['Danweimianjihaodianliang']['min']   #单位面积耗电量-下限
    Keji_Renjundianhao_name = t['Keji']['Renjundianhao']['name']   #人均电耗-参数名
    Keji_Renjundianhao_max = t['Keji']['Renjundianhao']['max']   #人均电耗-上限
    Keji_Renjundianhao_min = t['Keji']['Renjundianhao']['min']   #人均电耗-下限
    Keji_Danweimianjinenghao_name = t['Keji']['Danweimianjinenghao']['name']   #单位面积能耗-参数名
    Keji_Danweimianjinenghao_max = t['Keji']['Danweimianjinenghao']['max']   #单位面积能耗-上限
    Keji_Danweimianjinenghao_min = t['Keji']['Danweimianjinenghao']['min']   #单位面积能耗-下限
    Keji_Renjunzonghenenghao_name = t['Keji']['Renjunzonghenenghao']['name']   #人均综合能耗-参数名
    Keji_Renjunzonghenenghao_max = t['Keji']['Renjunzonghenenghao']['max']   #人均综合能耗-上限
    Keji_Renjunzonghenenghao_min = t['Keji']['Renjunzonghenenghao']['min']   #人均综合能耗-下限
    Keji_Renjunshuihao_name = t['Keji']['Renjunshuihao']['name']   #人均水耗-参数名
    Keji_Renjunshuihao_max = t['Keji']['Renjunshuihao']['max']   #人均水耗-上限
    Keji_Renjunshuihao_min = t['Keji']['Renjunshuihao']['min']   #人均水耗-下限

    Weisheng_name = t['Weisheng']['Leixing08']   #机关建筑名称
    Weisheng_Danweimianjidianhao_name = t['Weisheng']['Danweimianjihaodianliang']['name']   #单位面积耗电量-参数名
    Weisheng_Danweimianjidianhao_max = t['Weisheng']['Danweimianjihaodianliang']['max']   #单位面积耗电量-上限
    Weisheng_Danweimianjidianhao_min = t['Weisheng']['Danweimianjihaodianliang']['min']   #单位面积耗电量-下限
    Weisheng_Renjundianhao_name = t['Weisheng']['Renjundianhao']['name']   #人均电耗-参数名
    Weisheng_Renjundianhao_max = t['Weisheng']['Renjundianhao']['max']   #人均电耗-上限
    Weisheng_Renjundianhao_min = t['Weisheng']['Renjundianhao']['min']   #人均电耗-下限
    Weisheng_Danweimianjinenghao_name = t['Weisheng']['Danweimianjinenghao']['name']   #单位面积能耗-参数名
    Weisheng_Danweimianjinenghao_max = t['Weisheng']['Danweimianjinenghao']['max']   #单位面积能耗-上限
    Weisheng_Danweimianjinenghao_min = t['Weisheng']['Danweimianjinenghao']['min']   #单位面积能耗-下限
    Weisheng_Renjunzonghenenghao_name = t['Weisheng']['Renjunzonghenenghao']['name']   #人均综合能耗-参数名
    Weisheng_Renjunzonghenenghao_max = t['Weisheng']['Renjunzonghenenghao']['max']   #人均综合能耗-上限
    Weisheng_Renjunzonghenenghao_min = t['Weisheng']['Renjunzonghenenghao']['min']   #人均综合能耗-下限
    Weisheng_Renjunshuihao_name = t['Weisheng']['Renjunshuihao']['name']   #人均水耗-参数名
    Weisheng_Renjunshuihao_max = t['Weisheng']['Renjunshuihao']['max']   #人均水耗-上限
    Weisheng_Renjunshuihao_min = t['Weisheng']['Renjunshuihao']['min']   #人均水耗-下限

    Qita_name = t['Qita']['Leixing09']   #机关建筑名称
    Qita_Danweimianjidianhao_name = t['Qita']['Danweimianjihaodianliang']['name']   #单位面积耗电量-参数名
    Qita_Danweimianjidianhao_max = t['Qita']['Danweimianjihaodianliang']['max']   #单位面积耗电量-上限
    Qita_Danweimianjidianhao_min = t['Qita']['Danweimianjihaodianliang']['min']   #单位面积耗电量-下限
    Qita_Renjundianhao_name = t['Qita']['Renjundianhao']['name']   #人均电耗-参数名
    Qita_Renjundianhao_max = t['Qita']['Renjundianhao']['max']   #人均电耗-上限
    Qita_Renjundianhao_min = t['Qita']['Renjundianhao']['min']   #人均电耗-下限
    Qita_Danweimianjinenghao_name = t['Qita']['Danweimianjinenghao']['name']   #单位面积能耗-参数名
    Qita_Danweimianjinenghao_max = t['Qita']['Danweimianjinenghao']['max']   #单位面积能耗-上限
    Qita_Danweimianjinenghao_min = t['Qita']['Danweimianjinenghao']['min']   #单位面积能耗-下限
    Qita_Renjunzonghenenghao_name = t['Qita']['Renjunzonghenenghao']['name']   #人均综合能耗-参数名
    Qita_Renjunzonghenenghao_max = t['Qita']['Renjunzonghenenghao']['max']   #人均综合能耗-上限
    Qita_Renjunzonghenenghao_min = t['Qita']['Renjunzonghenenghao']['min']   #人均综合能耗-下限
    Qita_Renjunshuihao_name = t['Qita']['Renjunshuihao']['name']   #人均水耗-参数名
    Qita_Renjunshuihao_max = t['Qita']['Renjunshuihao']['max']   #人均水耗-上限
    Qita_Renjunshuihao_min = t['Qita']['Renjunshuihao']['min']   #人均水耗-下限

    # try:
    def select_max(num):  # 若有输入，则以输入值为准；若无，则无穷。
        if num == '' :
            num = 9999999999999999999999999
        else:
            num = num
        return num

    def select_min(num):  # 若有输入，则以输入值为准；若无，则无穷。
        if num == '':
            num = -9999999999999999999999999
        else:
            num = num
        return num

    def judge01(file,para_name,para_max,para_min):
        file = pd.DataFrame(file)
        file[file.loc[:, para_name] > float(para_max)] = np.nan
        file[file.loc[:, para_name] <= float(para_min)] = np.nan
        file.dropna(axis=0, how='any', subset=[para_name], inplace=True)
        return file

    '''
    用于二次筛选的五个参数为：
    单位面积电耗（kWh/㎡）
    人均电耗（kWh/p）
    单位面积能耗（kgce/㎡）
    人均综合能耗（kgce/p）
    人均水耗（m³/p）
    '''
    # print(tar_para05)
    # print(Jibiao01[tar_para05])
    def zhibiao_Func(file,name,para01,para02,para03,para04,para05):   #name：类型，para:[参数名，最大值，最小值]
        jianzhu_gongneng = '建筑功能02'
        file = pd.DataFrame(file)
        if name == '':   #如果未选择改建筑类型，则跳过。
            file01 = pd.DataFrame(columns=['empty'])
            pass
        else:
            file01 = file[file.loc[:,jianzhu_gongneng] == name]   #将类型为name的数据全部拿出来
            # print('file01',file01)
            # file01.to_csv('名字为机关办公建筑.csv', encoding='utf_8_sig', quoting=csv.QUOTE_NONNUMERIC)

            if para01[0] == '':   #如果未选择参数1（单位面积电耗），则跳过
                pass
            else:
                para01[1] = select_max(para01[1])   #参数最大值
                para01[2] = select_min(para01[2])   #参数最小值
                file01 = judge01(file01,para01[0],para01[1],para01[2])   #返回筛选后的表格

            if para02[0] == '':  # 如果未选择参数2（人均电耗），则跳过
                pass
            else:
                para02[1] = select_max(para02[1])  # 参数最大值
                para02[2] = select_min(para02[2])  # 参数最小值
                file01 = judge01(file01, para02[0], para02[1], para02[2])  # 返回筛选后的表格


            if para03[0] == '':  # 如果未选择参数3（单位面积能耗），则跳过
                pass
            else:
                para03[1] = select_max(para03[1])  # 参数最大值
                para03[2] = select_min(para03[2])  # 参数最小值
                file01 = judge01(file01, para03[0], para03[1], para03[2])  # 返回筛选后的表格

            if para04[0] == '':  # 如果未选择参数4（人均综合能耗），则跳过
                pass
            else:
                para04[1] = select_max(para04[1])  # 参数最大值
                para04[2] = select_min(para04[2])  # 参数最小值
                file01 = judge01(file01, para04[0], para04[1], para04[2])  # 返回筛选后的表格

            if para05[0] == '':  # 如果未选择参数5（人均水耗），则跳过
                pass
            else:
                para05[1] = select_max(para05[1])  # 参数最大值
                para05[2] = select_min(para05[2])  # 参数最小值
                file01 = judge01(file01, para05[0], para05[1], para05[2])  # 返回筛选后的表格
        return file01
    Jiguan_para01 = [Jiguan_Danweimianjidianhao_name,Jiguan_Danweimianjidianhao_max,Jiguan_Danweimianjidianhao_min]   #机关，单位面积耗电量
    Jiguan_para02 = [Jiguan_Renjundianhao_name,Jiguan_Renjundianhao_max,Jiguan_Renjundianhao_min]   #机关，人均电耗
    Jiguan_para03 = [Jiguan_Danweimianjinenghao_name,Jiguan_Danweimianjinenghao_max,Jiguan_Danweimianjinenghao_min]   #机关，单位面积能耗
    Jiguan_para04 = [Jiguan_Renjunzonghenenghao_name,Jiguan_Renjunzonghenenghao_max,Jiguan_Renjunzonghenenghao_min]   #机关，人均综合能耗
    Jiguan_para05 = [Jiguan_Renjunshuihao_name,Jiguan_Renjunshuihao_max,Jiguan_Renjunshuihao_min]   #机关，人均水耗

    Tiyu_para01 = [Tiyu_Danweimianjidianhao_name,Tiyu_Danweimianjidianhao_max,Tiyu_Danweimianjidianhao_min]   #体育，单位面积耗电量
    Tiyu_para02 = [Tiyu_Renjundianhao_name,Tiyu_Renjundianhao_max,Tiyu_Renjundianhao_min]   #体育，人均电耗
    Tiyu_para03 = [Tiyu_Danweimianjinenghao_name,Tiyu_Danweimianjinenghao_max,Tiyu_Danweimianjinenghao_min]   #体育，单位面积能耗
    Tiyu_para04 = [Tiyu_Renjunzonghenenghao_name,Tiyu_Renjunzonghenenghao_max,Tiyu_Renjunzonghenenghao_min]   #体育，人均综合能耗
    Tiyu_para05 = [Tiyu_Renjunshuihao_name,Tiyu_Renjunshuihao_max,Tiyu_Renjunshuihao_min]   #体育，人均水耗

    Wenhua_para01 = [Wenhua_Danweimianjidianhao_name,Wenhua_Danweimianjidianhao_max,Wenhua_Danweimianjidianhao_min]   #文化，单位面积耗电量
    Wenhua_para02 = [Wenhua_Renjundianhao_name,Wenhua_Renjundianhao_max,Wenhua_Renjundianhao_min]   #文化，人均电耗
    Wenhua_para03 = [Wenhua_Danweimianjinenghao_name,Wenhua_Danweimianjinenghao_max,Wenhua_Danweimianjinenghao_min]   #文化，单位面积能耗
    Wenhua_para04 = [Wenhua_Renjunzonghenenghao_name,Wenhua_Renjunzonghenenghao_max,Wenhua_Renjunzonghenenghao_min]   #文化，人均综合能耗
    Wenhua_para05 = [Wenhua_Renjunshuihao_name,Wenhua_Renjunshuihao_max,Wenhua_Renjunshuihao_min]   #文化，人均水耗

    Jiaoyu_para01 = [Jiaoyu_Danweimianjidianhao_name,Jiaoyu_Danweimianjidianhao_max,Jiaoyu_Danweimianjidianhao_min]   #教育，单位面积耗电量
    Jiaoyu_para02 = [Jiaoyu_Renjundianhao_name,Jiaoyu_Renjundianhao_max,Jiaoyu_Renjundianhao_min]   #教育，人均电耗
    Jiaoyu_para03 = [Jiaoyu_Danweimianjinenghao_name,Jiaoyu_Danweimianjinenghao_max,Jiaoyu_Danweimianjinenghao_min]   #教育，单位面积能耗
    Jiaoyu_para04 = [Jiaoyu_Renjunzonghenenghao_name,Jiaoyu_Renjunzonghenenghao_max,Jiaoyu_Renjunzonghenenghao_min]   #教育，人均综合能耗
    Jiaoyu_para05 = [Jiaoyu_Renjunshuihao_name,Jiaoyu_Renjunshuihao_max,Jiaoyu_Renjunshuihao_min]   #教育，人均水耗

    Tuanti_para01 = [Tuanti_Danweimianjidianhao_name,Tuanti_Danweimianjidianhao_max,Tuanti_Danweimianjidianhao_min]   #团体，单位面积耗电量
    Tuanti_para02 = [Tuanti_Renjundianhao_name,Tuanti_Renjundianhao_max,Tuanti_Renjundianhao_min]   #团体，人均电耗
    Tuanti_para03 = [Tuanti_Danweimianjinenghao_name,Tuanti_Danweimianjinenghao_max,Tuanti_Danweimianjinenghao_min]   #团体，单位面积能耗
    Tuanti_para04 = [Tuanti_Renjunzonghenenghao_name,Tuanti_Renjunzonghenenghao_max,Tuanti_Renjunzonghenenghao_min]   #团体，人均综合能耗
    Tuanti_para05 = [Tuanti_Renjunshuihao_name,Tuanti_Renjunshuihao_max,Tuanti_Renjunshuihao_min]   #团体，人均水耗

    Qitabangong_para01 = [Qitabangong_Danweimianjidianhao_name,Qitabangong_Danweimianjidianhao_max,Qitabangong_Danweimianjidianhao_min]   #其他办公，单位面积耗电量
    Qitabangong_para02 = [Qitabangong_Renjundianhao_name,Qitabangong_Renjundianhao_max,Qitabangong_Renjundianhao_min]   #其他办公，人均电耗
    Qitabangong_para03 = [Qitabangong_Danweimianjinenghao_name,Qitabangong_Danweimianjinenghao_max,Qitabangong_Danweimianjinenghao_min]   #其他办公，单位面积能耗
    Qitabangong_para04 = [Qitabangong_Renjunzonghenenghao_name,Qitabangong_Renjunzonghenenghao_max,Qitabangong_Renjunzonghenenghao_min]   #其他办公，人均综合能耗
    Qitabangong_para05 = [Qitabangong_Renjunshuihao_name,Qitabangong_Renjunshuihao_max,Qitabangong_Renjunshuihao_min]   #其他办公，人均水耗

    Keji_para01 = [Keji_Danweimianjidianhao_name,Keji_Danweimianjidianhao_max,Keji_Danweimianjidianhao_min]   #科技，单位面积耗电量
    Keji_para02 = [Keji_Renjundianhao_name,Keji_Renjundianhao_max,Keji_Renjundianhao_min]   #科技，人均电耗
    Keji_para03 = [Keji_Danweimianjinenghao_name,Keji_Danweimianjinenghao_max,Keji_Danweimianjinenghao_min]   #科技，单位面积能耗
    Keji_para04 = [Keji_Renjunzonghenenghao_name,Keji_Renjunzonghenenghao_max,Keji_Renjunzonghenenghao_min]   #科技，人均综合能耗
    Keji_para05 = [Keji_Renjunshuihao_name,Keji_Renjunshuihao_max,Keji_Renjunshuihao_min]   #科技，人均水耗

    Weisheng_para01 = [Weisheng_Danweimianjidianhao_name,Weisheng_Danweimianjidianhao_max,Weisheng_Danweimianjidianhao_min]   #卫生，单位面积耗电量
    Weisheng_para02 = [Weisheng_Renjundianhao_name,Weisheng_Renjundianhao_max,Weisheng_Renjundianhao_min]   #卫生，人均电耗
    Weisheng_para03 = [Weisheng_Danweimianjinenghao_name,Weisheng_Danweimianjinenghao_max,Weisheng_Danweimianjinenghao_min]   #卫生，单位面积能耗
    Weisheng_para04 = [Weisheng_Renjunzonghenenghao_name,Weisheng_Renjunzonghenenghao_max,Weisheng_Renjunzonghenenghao_min]   #卫生，人均综合能耗
    Weisheng_para05 = [Weisheng_Renjunshuihao_name,Weisheng_Renjunshuihao_max,Weisheng_Renjunshuihao_min]   #卫生，人均水耗

    Qita_para01 = [Qita_Danweimianjidianhao_name,Qita_Danweimianjidianhao_max,Qita_Danweimianjidianhao_min]   #其他，单位面积耗电量
    Qita_para02 = [Qita_Renjundianhao_name,Qita_Renjundianhao_max,Qita_Renjundianhao_min]   #其他，人均电耗
    Qita_para03 = [Qita_Danweimianjinenghao_name,Qita_Danweimianjinenghao_max,Qita_Danweimianjinenghao_min]   #其他，单位面积能耗
    Qita_para04 = [Qita_Renjunzonghenenghao_name,Qita_Renjunzonghenenghao_max,Qita_Renjunzonghenenghao_min]   #其他，人均综合能耗
    Qita_para05 = [Qita_Renjunshuihao_name,Qita_Renjunshuihao_max,Qita_Renjunshuihao_min]   #其他，人均水耗



    file0001 = zhibiao_Func(Jibiao01,Jiguan_name,Jiguan_para01,Jiguan_para02,Jiguan_para03,Jiguan_para04,Jiguan_para05)   #满足以上条件的项目
    # file0001.to_csv('并满足第二个条件.csv' ,encoding='utf_8_sig', quoting=csv.QUOTE_NONNUMERIC)
    file0002 = zhibiao_Func(Jibiao01,Tiyu_name,Tiyu_para01,Tiyu_para02,Tiyu_para03,Tiyu_para04,Tiyu_para05)   #满足以上条件的项目
    file0003 = zhibiao_Func(Jibiao01,Wenhua_name,Wenhua_para01,Wenhua_para02,Wenhua_para03,Wenhua_para04,Wenhua_para05)   #满足以上条件的项目
    file0004 = zhibiao_Func(Jibiao01,Jiaoyu_name,Jiaoyu_para01,Jiaoyu_para02,Jiaoyu_para03,Jiaoyu_para04,Jiaoyu_para05)   #满足以上条件的项目
    file0005 = zhibiao_Func(Jibiao01,Tuanti_name,Tuanti_para01,Tuanti_para02,Tuanti_para03,Tuanti_para04,Tuanti_para05)   #满足以上条件的项目
    file0006 = zhibiao_Func(Jibiao01,Qitabangong_name,Qitabangong_para01,Qitabangong_para02,Qitabangong_para03,Qitabangong_para04,Qitabangong_para05)   #满足以上条件的项目
    file0007 = zhibiao_Func(Jibiao01,Keji_name,Keji_para01,Keji_para02,Keji_para03,Keji_para04,Keji_para05)   #满足以上条件的项目
    file0008 = zhibiao_Func(Jibiao01,Weisheng_name,Weisheng_para01,Weisheng_para02,Weisheng_para03,Weisheng_para04,Weisheng_para05)   #满足以上条件的项目
    file0009 = zhibiao_Func(Jibiao01,Qita_name,Qita_para01,Qita_para02,Qita_para03,Qita_para04,Qita_para05)   #满足以上条件的项目
    # print(file0001.shape[0],file0002.shape[0],file0003.shape[0],file0004.shape[0],file0005.shape[0],file0006.shape[0],file0007.shape[0],file0008.shape[0],file0009.shape[0])
    result_Jibiao01 = pd.concat([file0001,file0002,file0003,file0004,file0005,file0006,file0007,file0008,file0009],axis=0)
    #机关，体育，文化，教育，团体，其他办公，科技，卫生，其他。



    file00011 = zhibiao_Func(Jibiao02,Jiguan_name,Jiguan_para01,Jiguan_para02,Jiguan_para03,Jiguan_para04,Jiguan_para05)   #满足以上条件的项目
    file00022 = zhibiao_Func(Jibiao02,Tiyu_name,Tiyu_para01,Tiyu_para02,Tiyu_para03,Tiyu_para04,Tiyu_para05)   #满足以上条件的项目
    file00033 = zhibiao_Func(Jibiao02,Wenhua_name,Wenhua_para01,Wenhua_para02,Wenhua_para03,Wenhua_para04,Wenhua_para05)   #满足以上条件的项目
    file00044 = zhibiao_Func(Jibiao02,Jiaoyu_name,Jiaoyu_para01,Jiaoyu_para02,Jiaoyu_para03,Jiaoyu_para04,Jiaoyu_para05)   #满足以上条件的项目
    file00055 = zhibiao_Func(Jibiao02,Tuanti_name,Tuanti_para01,Tuanti_para02,Tuanti_para03,Tuanti_para04,Tuanti_para05)   #满足以上条件的项目
    file00066 = zhibiao_Func(Jibiao02,Qitabangong_name,Qitabangong_para01,Qitabangong_para02,Qitabangong_para03,Qitabangong_para04,Qitabangong_para05)   #满足以上条件的项目
    file00077 = zhibiao_Func(Jibiao02,Keji_name,Keji_para01,Keji_para02,Keji_para03,Keji_para04,Keji_para05)   #满足以上条件的项目
    file00088 = zhibiao_Func(Jibiao02,Weisheng_name,Weisheng_para01,Weisheng_para02,Weisheng_para03,Weisheng_para04,Weisheng_para05)   #满足以上条件的项目
    file00099 = zhibiao_Func(Jibiao02,Qita_name,Qita_para01,Qita_para02,Qita_para03,Qita_para04,Qita_para05)   #满足以上条件的项目
    # print(file00011.shape[0],file00022.shape[0],file00033.shape[0],file00044.shape[0],file00055.shape[0],file00066.shape[0],file00077.shape[0],file00088.shape[0],file00099.shape[0])
    result_Jibiao02 = pd.concat([file00011,file00022,file00033,file00044,file00055,file00066,file00077,file00088,file00099],axis=0)
    #机关，体育，文化，教育，团体，其他办公，科技，卫生，其他。

    # result_Jibiao01.to_csv(save_file01,encoding='utf_8_sig')
    # print(result_Jibiao01.shape[0])
    # result_Jibiao02.to_csv(save_file02,encoding='utf_8_sig')
    # print(result_Jibiao02.shape[0])

    def Zhanbi(raw,new):
        if raw != 0:
            aa = new / raw
            aa = aa * 100
            aa = round(aa, 2)
        else:
            new = 0
            aa = 0
        return new,aa
    N1,P1 = Zhanbi(raw_dataNum,file00011.shape[0])   #类型一占比，机关
    N2,P2 = Zhanbi(raw_dataNum, file00022.shape[0])  # 类型一占比，机关
    N3,P3 = Zhanbi(raw_dataNum, file00033.shape[0])  # 类型一占比，机关
    N4,P4 = Zhanbi(raw_dataNum, file00044.shape[0])  # 类型一占比，机关
    N5,P5 = Zhanbi(raw_dataNum, file00055.shape[0])  # 类型一占比，机关
    N6,P6 = Zhanbi(raw_dataNum, file00066.shape[0])  # 类型一占比，机关
    N7,P7 = Zhanbi(raw_dataNum, file00077.shape[0])  # 类型一占比，机关
    N8,P8 = Zhanbi(raw_dataNum, file00088.shape[0])  # 类型一占比，机关
    N9,P9 = Zhanbi(raw_dataNum, file00099.shape[0])  # 类型一占比，机关
    zhanbi_json = {
        "筛选后各类型建筑所剩项目及占比：":{
        '机关办公建筑': {"总数":N1,"占比":P1},
        '体育系统建筑': {"总数":N2,"占比":P2},
        '文化系统建筑': {"总数":N3,"占比":P3},
        '教育系统建筑': {"总数":N4,"占比":P4},
        '团体组织建筑': {"总数":N5, "占比":P5},
        '其他办公建筑': {"总数":N6, "占比":P6},
        '科技系统建筑': {"总数":N7, "占比":P7},
        '卫生系统建筑': {"总数":N8, "占比":P8},
        '其他建筑': {"总数":N9, "占比":P9}
        }
    }
    zhanbi_json = json.dumps(zhanbi_json, ensure_ascii=False)
    tmp_f = open("筛选后各建筑类型占比.json", "w")
    tmp_f.write(zhanbi_json)
    tmp_f.close()

    new_dataNum = result_Jibiao01.shape[0]
    NumPer = new_dataNum / raw_dataNum * 100  # 计算百分比
    NumPer = round(NumPer, 2)
    # print(raw_dataNum)
    # print(new_dataNum)
    # print(NumPer)
    result_json = {
        'raw_dataNum': raw_dataNum,
        'new_dataNum': new_dataNum,
        'NumPer': NumPer
    }
    result_json = json.dumps(result_json, ensure_ascii=False)
    tmp_f = open("result01_1.json", "w")
    tmp_f.write(result_json)
    tmp_f.flush()
    tmp_f.close()

    return result_Jibiao01,result_Jibiao02


# judge03()