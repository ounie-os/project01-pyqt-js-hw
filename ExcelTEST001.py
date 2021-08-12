########## 00 软件功能说明##########
'''
主体功能：填表
操作方式：目前无界面，后期需要制作界面
相关表格文件-原始表：能源资源表、建筑信息表、设备信息表
相关表格文件-目标表：基表1、基表2
配置文件：config.json
程序版本：V1.0
修改人：Mr.HW

'''


def func_filling_table():
    ########## 导入模块 ##########
    import json
    import time  # 导入时间模块
    import pandas as pd
    import datetime as dt  # 导入时间处理模块
    # import xlwt
    import csv

    start_time = time.time()  # 程序开始，第一次计时。
    ########## Step 01 读取配置文件 ##########
    f = open('./config.json')  # 读取配置文件
    t = json.load(f)  # 将json格式的数据映射成list的形式
    f.close()  # 关闭文件

    ########## Step 02 读取表数据 ##########
    ##### 02.1 读取表路径 #####
    filepath = t['filepath']  # 表格文件所在路径
    tableName_nengyuan = t['raw_tables']['nengyuanziyuan']  # 能源资源表的表名
    table1 = filepath + tableName_nengyuan  # 路径+文件名，用于定位读取文件
    tableName_jianzhu = t['raw_tables']['jianzhuxinxi']  # 建筑基本信息表的表名
    table2 = filepath + tableName_jianzhu  # 路径+文件名，用于定位读取文件
    tableName_shebei = t['raw_tables']['shebeixinxi']  # 能耗设备信息表的表名
    table3 = filepath + tableName_shebei  # 路径+文件名，用于定位读取文件
    tableName_jibiao1 = t['target_table']['Jibiao1']  # 基表1的表名
    table4 = filepath + tableName_jibiao1  # 路径+文件名，用于定位读取文件
    tableName_jibiao2 = t['target_table']['Jibiao2']  # 基表2的表名
    table5 = filepath + tableName_jibiao2  # 路径+文件名，用于定位读取文件

    ##### 02.2 读取表内容 ######
    def read_table(tableName):  # 定义函数，根据路径与表名获取表格内容
        # table = pd.read_excel(tableName, encoding='utf_8')
        table = pd.read_excel(tableName)
        return table  # 返回读取到的文件内容

    try:
        # table_nengyuan = pd.read_excel(table1, encoding='utf_8', dtype={'固定电话': str})  # 能源资源表
        table_nengyuan = pd.read_excel(table1, dtype={'固定电话': str})  # 能源资源表
        table_jianzhu = read_table(table2)  # 建筑信息表
        table_shebei = read_table(table3)  # 用能设备表
        table_jibiao1 = read_table(table4)  # 基表1
        table_jibiao2 = read_table(table5)  # 基表2
    except Exception as e:
        print(e)
        print('请检查配置文件中的表格路径格式与表名')

    table_data = t['table_data']  # 人为配置的填表日期

    ########### Step 03 读取表参数 ##########
    ###### 03.1 读取源表参数 ######
    raw_para01 = t['raw_parameters']['table_nengyuan']['raw_para01']  # 单位名称
    raw_para02 = t['raw_parameters']['table_nengyuan']['raw_para02']  # 地址
    raw_para03 = t['raw_parameters']['table_jianzhu']['raw_para03']  # 竣工时间
    raw_para04 = t['raw_parameters']['table_jianzhu']['raw_para04']  # 建筑类型
    raw_para05 = t['raw_parameters']['table_jianzhu']['raw_para05']  # 建筑功能
    raw_para05_1 = t['raw_parameters']['table_nengyuan']['raw_para05_1']  # 单位类型
    raw_para06 = t['raw_parameters']['table_jianzhu']['raw_para06']  # 地上层数
    raw_para07_1 = t['raw_parameters']['table_nengyuan']['raw_para07_1']  # 办公建筑面积
    raw_para07_2 = t['raw_parameters']['table_jianzhu']['raw_para07_2']  # 建筑面积(平方米)
    raw_para07_3 = t['raw_parameters']['table_jianzhu']['raw_para07_3']  # 自用建筑面积(平方米)
    raw_para08_09 = t['raw_parameters']['table_shebei']['raw_para08(09)']  # 设备名称
    raw_para10 = t['raw_parameters']['table_jianzhu']['raw_para10']  # 建筑节能标准
    raw_para11 = t['raw_parameters']['table_nengyuan']['raw_para11']  # 是否实施节能改造（原表中没有）
    raw_para12 = t['raw_parameters']['table_nengyuan']['raw_para12']  # 联络员
    raw_para13 = t['raw_parameters']['table_nengyuan']['raw_para13']  # 固定电话
    raw_para14 = t['raw_parameters']['table_nengyuan']['raw_para14']  # 总用电(千瓦时)
    raw_para15 = t['raw_parameters']['table_nengyuan']['raw_para15']  # 天然气总用量(立方米)
    raw_para16 = t['raw_parameters']['table_nengyuan']['raw_para16']  # 总用水(吨)
    raw_para19 = t['raw_parameters']['table_jianzhu']['raw_para19']  # 单位名称，原表2
    raw_para20 = t['raw_parameters']['table_jianzhu']['raw_para20']  # 建筑名称，原表2
    raw_para21 = t['raw_parameters']['table_shebei']['raw_para21']  # 单位名称，原表3
    raw_para22 = t['raw_parameters']['table_nengyuan']['raw_para22']  # 所属行政区
    raw_para24 = t['raw_parameters']['table_nengyuan']['raw_para24']  # 总能耗(千克标准煤)
    raw_para25 = t['raw_parameters']['table_nengyuan']['raw_para25']  # 面积均能耗(千克标准煤/平方米)

    ##### 03.2 读取目标表参数 #####
    tar_para01 = t['target_parameters']['table_jibiao1']['tar_para01']  # 建筑详细名称
    tar_para02 = t['target_parameters']['table_jibiao1']['tar_para02']  # 建筑详细地址
    tar_para03 = t['target_parameters']['table_jibiao1']['tar_para03']  # 竣工年度
    tar_para04 = t['target_parameters']['table_jibiao1']['tar_para04']  # 建筑类型
    tar_para05 = t['target_parameters']['table_jibiao1']['tar_para05']  # 建筑功能
    tar_para06 = t['target_parameters']['table_jibiao1']['tar_para06']  # 建筑层数(层)
    tar_para07 = t['target_parameters']['table_jibiao1']['tar_para07']  # 建筑面积(平方米)
    tar_para08 = t['target_parameters']['table_jibiao1']['tar_para08']  # 供热方式
    tar_para09 = t['target_parameters']['table_jibiao1']['tar_para09']  # 供冷方式
    tar_para10 = t['target_parameters']['table_jibiao1']['tar_para10']  # 所执行的建筑节能标准
    tar_para11 = t['target_parameters']['table_jibiao1']['tar_para11']  # 是否实施节能改造
    tar_para12 = t['target_parameters']['table_jibiao1']['tar_para12']  # 联系人
    tar_para13 = t['target_parameters']['table_jibiao1']['tar_para13']  # 联系电话
    tar_para14 = t['target_parameters']['table_jibiao2']['tar_para14']  # 电力
    tar_para15 = t['target_parameters']['table_jibiao2']['tar_para15']  # 天然气
    tar_para16 = t['target_parameters']['table_jibiao2']['tar_para16']  # 水
    tar_para17 = t['target_parameters']['table_jibiao1']['tar_para17']  # 填表时间
    tar_para18 = t['target_parameters']['table_jibiao2']['tar_para18']  # 建筑详细名称（基表2）
    tar_para23 = t['target_parameters']['table_jibiao1']['tar_para23']  # 建筑所属行政区划

    ########### Step 04 原表1字段进行处理 ##########根据不同单位类型中包含的关键字来判断该单位的单位类型
    def panduan(A, B):  # 定义函数，用于判断字段中是否包含特定字段
        list01 = []
        re = False
        for i in range(len(B)):
            tmp = B[i] in A
            list01.append(tmp)
        if True in list01:
            re = True
        else:
            pass
        return re

    def table_nengyuan_chuli():
        table_nengyuan['单位类型（编码)'] = 0
        for i in range(table_nengyuan.shape[0]):  # 对表中“建筑功能”列遍历
            leixing01 = ['居住建筑', '国家机关', '国家办公']  # 填0
            leixing02 = ['教育', '培训', '学校', '小学', '中学', '大学', '初中', '高中']  # 填5
            leixing03 = ['医疗', '卫生', '疾控', '医院']  # 填4
            leixing04 = ['酒店', '宾馆', '住宿', '饭店']  # 填3
            leixing05 = ['商场', '超市', '购物']  # 填2
            leixing06 = ['办公', '写字楼']  # 填1

            result01 = panduan(table_nengyuan.loc[i, raw_para05_1], leixing01)  # 若包含以上字段，则为居住建筑活国家办公建筑，不填
            result02 = panduan(table_nengyuan.loc[i, raw_para05_1], leixing02)  # 若包含以上字段，则为文化教育建筑，填5
            result03 = panduan(table_nengyuan.loc[i, raw_para05_1], leixing03)  # 若包含以上字段，则为医疗卫生建筑，填4
            result04 = panduan(table_nengyuan.loc[i, raw_para05_1], leixing04)  # 若包含以上字段，则为宾馆饭店建筑，填3
            result05 = panduan(table_nengyuan.loc[i, raw_para05_1], leixing05)  # 若包含以上字段，则为宾馆饭店建筑，填3
            result06 = panduan(table_nengyuan.loc[i, raw_para05_1], leixing06)  # 若包含以上字段，则为宾馆饭店建筑，填3

            if result01 == True:  # 若为国家机关建筑，可不填
                table_nengyuan.loc[i, '单位类型（编码)'] = 0
            elif result02 == True:
                table_nengyuan.loc[i, '单位类型（编码)'] = 5
            elif result03 == True:
                table_nengyuan.loc[i, '单位类型（编码)'] = 4
            elif result04 == True:
                table_nengyuan.loc[i, '单位类型（编码)'] = 3
            elif result05 == True:
                table_nengyuan.loc[i, '单位类型（编码)'] = 2
            elif result06 == True:
                table_nengyuan.loc[i, '单位类型（编码)'] = 1
            else:
                table_nengyuan.loc[i, '单位类型（编码)'] = 6  # 若不属于以上，则为其他                #这里的判断后续可能还需要完善

    table_nengyuan_chuli()
    # table_nengyuan.to_csv('tmpNengyuan.csv',encoding='utf_8_sig')

    ##### 04.1 能源表相关信息填入基1表 #####
    table_jibiao1[tar_para01] = table_nengyuan[raw_para01]  # 参数：单位名称，填入基1表对应位置
    table_jibiao1[tar_para02] = table_nengyuan[raw_para02]  # 参数：地址，填入基1表对应位置
    table_jibiao1[tar_para05] = table_nengyuan['单位类型（编码)']  # 参数：建筑功能，填入基1表对应位置
    table_jibiao1['面积一'] = table_nengyuan[raw_para07_1]  # 能源表中的面积
    table_jibiao1[tar_para12] = table_nengyuan[raw_para12]  # 参数：联络员，填入基1表对应位置
    table_jibiao1[tar_para13] = table_nengyuan[raw_para13]  # 参数：固定电话，填入基1表对应位置
    table_jibiao1[tar_para17] = table_data  # 统计时间
    table_jibiao1['所属行政区'] = table_nengyuan[raw_para22]  # 参数：所属行政区
    table_jibiao1['建筑功能01'] = table_nengyuan[raw_para05_1]  # 参数：建筑功能，便于后期人为修改
    table_jibiao1['总能耗(千克标准煤)'] = table_nengyuan[raw_para24]  # 参数：总能耗(千克标准煤)   #用于后续筛选数据
    table_jibiao1['面积均能耗'] = table_nengyuan[raw_para25]  # 参数：面积均能耗(千克标准煤/平方米)   #用于后续筛选数据
    table_jibiao1['总用水'] = table_nengyuan[raw_para16]  # 参数：总用水(吨)   #用于后续筛选数据
    table_jibiao1['总用电'] = table_nengyuan[raw_para14]  # 参数：总用电(千瓦时)   #用于后续筛选数据
    table_jibiao1['天然气总用量'] = table_nengyuan[raw_para15]  # 参数：天然气总用量(立方米)   #用于后续筛选数据

    table_jibiao2[tar_para14] = table_nengyuan[raw_para14]  # 参数：电力，填入基2表对应位置
    table_jibiao2[tar_para15] = table_nengyuan[raw_para15]  # 参数：天然气，填入基2表对应位置
    table_jibiao2[tar_para16] = table_nengyuan[raw_para16]  # 参数：水，填入基2表对应位置+
    table_jibiao2[tar_para18] = table_nengyuan[raw_para01]  # 参数：建筑详细名称，基2表中的“建筑详细名称” = 基1表中的“单位名称”
    table_jibiao2['所属行政区'] = table_nengyuan[raw_para22]  # 参数：所属行政区
    table_jibiao2['总能耗(千克标准煤)'] = table_nengyuan[raw_para24]  # 参数：总能耗(千克标准煤)   #用于后续筛选数据
    table_jibiao2['面积均能耗'] = table_nengyuan[raw_para25]  # 参数：面积均能耗(千克标准煤/平方米)   #用于后续筛选数据
    table_jibiao2['总用水'] = table_nengyuan[raw_para16]  # 参数：总用水(吨)   #用于后续筛选数据
    table_jibiao2['总用电'] = table_nengyuan[raw_para14]  # 参数：总用电(千瓦时)   #用于后续筛选数据
    table_jibiao2['天然气总用量'] = table_nengyuan[raw_para15]  # 参数：天然气总用量(立方米)   #用于后续筛选数据

    ########### Step 05 原表2字段进行处理 ##########
    ##### 05.1 建筑表提取竣工年份,存入建筑表 #####
    def table_jianzhu_chuli01():  # 定义函数，提取原表2中的竣工时间
        table_jianzhu['竣工时间'].fillna('2222/01/01 00:00:00', inplace=True)  # 填补空值，替换为'2222/01/01 00:00:00'
        for i in range(table_jianzhu.shape[0]):
            try:
                table_jianzhu.loc[i, '竣工时间'] = pd.to_datetime(table_jianzhu.loc[i, '竣工时间'])  # 转为时间格式
            except:
                table_jianzhu.loc[i, '竣工时间'] = '2222/01/01 00:00:00'
            else:
                table_jianzhu.loc[i, '竣工时间'] = pd.to_datetime(table_jianzhu.loc[i, '竣工时间'])

        table_jianzhu['竣工时间'] = pd.to_datetime(table_jianzhu['竣工时间'])  # 读取时间格式
        table_jianzhu['竣工年度'] = table_jianzhu['竣工时间'].dt.year  # 提取年份
        return table_jianzhu

    table_jianzhu = table_jianzhu_chuli01()

    # table_jianzhu.to_csv('./tmpJianzhu.csv',encoding='utf_8_sig')

    ##### 05.2 获取同一单位不同建筑的下面积之和，并获取最大面积，用于填表 #####
    def table_jianzhu_chuli02():  # 定义函数，对原表2进行处理
        table_jianzhu02 = pd.DataFrame()
        for i in range(table_nengyuan.shape[0]):  # 从原表1中获取项目名称，在原表2中匹配对应单位下的所有建筑
            name = table_nengyuan.loc[i, raw_para01]
            tmp_table = table_jianzhu[table_jianzhu[raw_para19] == name]  # 同一单位下所有建筑组成的表
            if not tmp_table.empty:  # 进行判断，若不为空矩阵,则进行操作
                tmp_table.fillna(0, inplace=True)  # 填充所有的空值为0
                max_cengshu = max(tmp_table.loc[:, raw_para06])  # 同一单位下所有建筑的最高层数
                total_area07_2 = sum(tmp_table.loc[:, raw_para07_2])  # 同一单位下所有建筑的建筑面积之和
                total_area07_3 = sum(tmp_table.loc[:, raw_para07_3])  # 同一单位下所有建筑的自由建筑面积之和
                tmp_table['最高层数'] = max_cengshu
                tmp_table['最大面积'] = max(total_area07_2, total_area07_3)
                tmp_table_01 = tmp_table.iloc[[0], :]  # 第一行数据，同一单位下所有建筑取第一行就行
                table_jianzhu02 = pd.concat([table_jianzhu02, tmp_table_01], axis=0)  # 按行合并，追加数据
            else:
                pass
        table_jianzhu02 = table_jianzhu02.reset_index(drop=True)  # 重新设置项目编号
        return table_jianzhu02

    table_jianzhu02 = table_jianzhu_chuli02()  # 运行以上程序

    # table_jianzhu02.to_csv('tmpJianzhu02.csv',encoding='utf_8_sig')

    ########### Step 06 原表3字段进行处理 ##########获取同一单位不同用能设备类型，并根据字段中是否包含关键字来判断供冷供热方式
    def table_shebei_chuli():  # 定义函数，对原表3进行处理
        table_shebei02 = pd.DataFrame()
        for name02 in table_nengyuan[raw_para01]:  # 从原表1中获取项目名称，在原表2中匹配对应单位下的所有建筑
            tmp_table = table_shebei[table_shebei[raw_para21] == name02]
            tmp_table['供冷供热方式'] = 0
            if not tmp_table.empty:  # 进行判断，若不为空矩阵,则进行操作
                tmp_table.fillna(0, inplace=True)  # 填充所有的空值为0
                for shebei_name in tmp_table[raw_para08_09]:
                    shebei_name = str(shebei_name)
                    # result = False
                    # result = '中央空调' in shebei_name
                    if '中央空调' in shebei_name:  # 判断“设备名称”中是否包含“中央空调”字段，若是，则为True
                        tmp_table['供冷供热方式'] = 1
                    elif '水泵' in shebei_name:
                        tmp_table['供冷供热方式'] = 1
                    else:
                        tmp_table['供冷供热方式'] = 2
                tmp_table_02 = tmp_table.iloc[[0], :]
                table_shebei02 = pd.concat([table_shebei02, tmp_table_02], axis=0)
            else:  # 进行判断，若为空矩阵，则跳过
                pass
        table_shebei02 = table_shebei02.reset_index(drop=True)  # 重新设置项目编号
        return table_shebei02  # 返回处理好的设备表

    table_shebei02 = table_shebei_chuli()

    # table_shebei02.to_csv('tmpShebei02.csv',encoding='utf_8_sig')

    # ########### Step 07 所有处理好的信息填入基1表 ##########
    # def jianzhuleixing(A):   #定义函数，由建筑类型返回相应的代码。
    #     A = str(A)
    #     B = 0
    #     if A == '居住建筑':
    #         B = 1
    #     elif A == '中小型公共建筑':
    #         B = 2
    #     elif A == '大型公共建筑':
    #         B = 3
    #     elif A == '国家机关办公建筑':
    #         B = 4
    #     else :
    #         B = 0
    #     B = float(B)
    #     return B
    def jianzhuleixing(A):  # 定义函数，由建筑类型返回相应的代码。
        A = str(A)
        r1 = '居住' in A
        r2 = '中小型公共' in A
        r3 = '大型公共' in A
        r4 = '国家机关' in A
        B = 0
        if r1 == True:
            B = 1
        if r2 == True:
            B = 2
        if r3 == True:
            B = 3
        if r4 == True:
            B = 4
        B = float(B)
        return B

    # def jienengbiaozhun(A):   #定义函数，由建筑执行的节能标准返回相应的代码。
    #     A = str(A)
    #     B = 0
    #     if A == '执行节能65%标准':
    #         B = 2
    #     elif A == '执行节能50%标准':
    #         B = 1
    #     elif A == '执行节能75%标准' :
    #         B = 3
    #     else :
    #         B = 0
    #     B = float(B)
    #     return B
    def jienengbiaozhun(A):  # 定义函数，由建筑执行的节能标准返回相应的代码。
        A = str(A)
        B = 0
        r1 = '50%' in A
        r2 = '65%' in A
        r3 = '75%' in A
        if r1 == True:
            B = 1
        if r2 == True:
            B = 2
        if r3 == True:
            B = 3
        B = float(B)
        return B

    def xingzhengqu(A):  # 定义函数，根据所在行政区填入对应代码
        A = str(A)
        B = 320000
        if '高淳' in A:
            B = 320125
        if '鼓楼' in A:
            B = 320126
        if '建邺' in A:
            B = 320105
        if '江宁' in A:
            B = 320115
        if '溧水' in A:
            B = 320124
        if '六合' in A:
            B = 320116
        if '浦口' in A:
            B = 320111
        if '栖霞' in A:
            B = 320113
        if '秦淮' in A:
            B = 320104
        if '玄武' in A:
            B = 320102
        if '雨花台' in A:
            B = 320114
        else:
            pass
        return B

    table_jibiao1.fillna(0, inplace=True)  # 首先对基表中的所有空值填充为0
    for i in range(table_jibiao1.shape[0]):  # 对于基表1中所有单位的循环
        table_jibiao1.loc[i, tar_para23] = xingzhengqu(table_jibiao1.loc[i, '所属行政区'])  # 调用函数，根据所在行政区填入对应代码
        name03 = table_jibiao1.loc[i, tar_para01]  # 获取的单位名称
        tmp_jianzhu = table_jianzhu02[table_jianzhu02[raw_para01] == name03]  # 临时表，用于存放某一单位的信息
        tmp_jianzhu = pd.DataFrame(tmp_jianzhu)  # 转为矩阵格式，应该可以删除
        tmp_jianzhu = tmp_jianzhu.reset_index(drop=True)  # 重新设置项目编号,此处全设为0

        tmp_number = table_jibiao1.loc[i, tar_para13]
        if tmp_number != 0:
            table_jibiao1.loc[i, tar_para13] = tmp_number[-8:].split()
            table_jibiao1.loc[i, tar_para13] = str(table_jibiao1.loc[i, tar_para13])
            table_jibiao1.loc[i, tar_para13] = '025-' + table_jibiao1.loc[i, tar_para13]  # 号码前加上区号025
        else:
            table_jibiao1.loc[i, tar_para13] = tmp_number

        if not tmp_jianzhu.empty:
            tmp_jungongnianfen = tmp_jianzhu.loc[[0], '竣工年度']
            tmp_jungongnianfen = float(tmp_jungongnianfen)
            table_jibiao1.loc[[i], tar_para03] = tmp_jungongnianfen  # 竣工年度=竣工年度

            tmp_001 = tmp_jianzhu.loc[[0], raw_para04]  # 获取列表中的建筑类型名称
            tmp_001 = tmp_001.astype(str)  # 将该名称强制转为字符串
            tmp_leixing = jianzhuleixing(tmp_001)  # 调用函数，返回对应的类型代码
            table_jibiao1.loc[[i], tar_para04] = float(tmp_leixing)  # 建筑类型

            table_jibiao1.loc[[i], tar_para06] = float(tmp_jianzhu.loc[[0], '最高层数'])  # 建筑层数

            table_jibiao1.loc[[i], '面积二'] = float(tmp_jianzhu.loc[[0], '最大面积'])  # 建筑层数
            table_jibiao1.loc[[i], tar_para07] = max(float(table_jibiao1.loc[[i], '面积一']),
                                                     float(table_jibiao1.loc[[i], '面积二']))

            tmp_002 = tmp_jianzhu.loc[[0], raw_para10]  # 获取列表中的执行节能标准名称
            tmp_002 = tmp_002.astype(str)  # 将该名称强制转为字符串
            tmp_biaozhun = jienengbiaozhun(tmp_002)  # 调用函数，返回对应的类型代码
            table_jibiao1.loc[[i], tar_para10] = float(tmp_biaozhun)  # 所执行的节能标准

        else:
            pass

        tmp_shebei = table_shebei02[table_shebei02[raw_para21] == name03]
        tmp_shebei = tmp_shebei.reset_index(drop=True)  # 重新设置项目编号,此处全设为0

        if not tmp_shebei.empty:
            table_jibiao1.loc[[i], tar_para08] = table_jibiao1.loc[[i], tar_para09] = float(
                tmp_shebei.loc[[0], '供冷供热方式'])
        else:
            pass
    table_jibiao2['建筑面积(平方米)'] = table_jibiao1[tar_para07]  # 建筑面积(平方米)   #用于判断筛选

    ##########  Step 08  保存表 ##########
    save_filename01 = t['save_filename01']
    save_filename02 = t['save_filename02']
    # table_jibiao1 = table_jibiao1.drop(['面积一','面积二','所属行政区'], axis=1)   #上交的表需要把后面的删除
    table_jibiao1.to_csv(save_filename01, encoding='utf_8_sig', quoting=csv.QUOTE_NONNUMERIC)
    table_jibiao2.to_csv(save_filename02, encoding='utf_8_sig', quoting=csv.QUOTE_NONNUMERIC)

    end_time = time.time()
    print('运行时间：', end_time - start_time)
    print('---------------------程序运行结束---------------------')
    return 0


if __name__ == '__main__':
    func_filling_table()
