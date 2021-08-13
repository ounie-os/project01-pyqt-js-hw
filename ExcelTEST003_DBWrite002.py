########## 00 软件功能说明##########
'''
主体功能：将基表写入数据库
操作方式：目前无界面，后期需要制作界面
相关表格文件-原始表：
相关表格文件-目标表：基表1、基表2
配置文件：config.json
程序版本：V1.0
修改人：黄巍
'''
def DB_Write():
    import pymysql
    import pandas as pd
    import json
    import datetime

    ########## Step 01 读取配置文件 ##########
    f = open('./config.json')  # 读取配置文件
    t = json.load(f)  # 将json格式的数据映射成list的形式
    f.close()  # 关闭文件
    host01 = t['DB_connect']['host']
    port01 = t['DB_connect']['port']
    username01 = t['DB_connect']['username']
    password01 = t['DB_connect']['password']
    database01 = t['DB_connect']['database']

    file01_name = t['save_filename01']
    file02_name = t['save_filename02']
    file01 = pd.read_csv(file01_name, encoding='utf_8')   #为筛选之前的表
    file02 = pd.read_csv(file02_name, encoding='utf_8')

    db_target = pymysql.connect(host=host01,  # 连入配置信息所在数据库
                                database=database01,
                                user=username01,
                                password=password01,
                                charset="utf8")
    cursor = db_target.cursor()   #获取游标
##########  用时间来命名表格 ##########
    now_time = datetime.datetime.now()   #当前时间
    now_date = now_time.date()   #当前日期
    now_date = str(now_date)
    now_hour = now_time.hour   #当前小时
    now_hour = str(now_hour)
    now_minute = now_time.minute   #当前分钟
    now_minute = str(now_minute)
    # print(now_time)
    # print(now_date)
    table_name01 = now_date + now_hour + now_minute + 'Jibiao01'
    table_name01 = table_name01.replace('-','')
    # print(table_name01)
    table_name02 = now_date + now_hour + now_minute + 'Jibiao02'
    table_name02 = table_name02.replace('-', '')
    # print(table_name02)

    try:
        creat_sql01 = "CREATE TABLE IF NOT EXISTS %s(序号 VARCHAR(255) NOT NULL,建筑所属行政区划 VARCHAR(255) NOT NULL, 建筑代码 VARCHAR(255) NOT NULL," \
                      "建筑详细名称 VARCHAR(255) NOT NULL,建筑详细地址 VARCHAR(255) NOT NULL,竣工年度 VARCHAR(255) NOT NULL,建筑类型 VARCHAR(255) NOT NULL," \
                      "建筑功能 VARCHAR(255) NOT NULL,建筑层数 VARCHAR(255) NOT NULL,建筑面积平方米 VARCHAR(255) NOT NULL,供热方式 VARCHAR(255) NOT NULL," \
                      "供冷方式 VARCHAR(255) NOT NULL,所执行的建筑节能标准 VARCHAR(255) NOT NULL,是否实施节能改造 VARCHAR(255) NOT NULL," \
                      "联系人 VARCHAR(255) NOT NULL,联系电话 VARCHAR(255) NOT NULL,统计时间 VARCHAR(255) NOT NULL,面积一 VARCHAR(255) NOT NULL," \
                      "所属行政区 VARCHAR(255) NOT NULL,建筑功能01 VARCHAR(255) NOT NULL,总能耗千克标准煤 VARCHAR(255) NOT NULL," \
                      "面积均能耗 VARCHAR(255) NOT NULL, 总用水 VARCHAR(255) NOT NULL,总用电 VARCHAR(255) NOT NULL," \
                      "天然气总用量 VARCHAR(255) NOT NULL,面积二 VARCHAR(255) NOT NULL)" % (table_name01)
        # creat_sql02 = "CREATE TABLE IF NOT EXISTS %s(tmp01 VARCHAR(100) NOT NULL)"%(table_name02)
        cursor.execute(creat_sql01)

        for i in range(file01.shape[0]):
            value01 = file01.iloc[i, 0]
            value02 = file01.iloc[i, 1]
            value03 = file01.iloc[i, 2]
            value04 = file01.iloc[i, 3]
            value05 = file01.iloc[i, 4]
            value06 = file01.iloc[i, 5]
            value07 = file01.iloc[i, 6]
            value08 = file01.iloc[i, 7]
            value09 = file01.iloc[i, 8]
            value10 = file01.iloc[i, 9]
            value11 = file01.iloc[i, 10]
            value12 = file01.iloc[i, 11]
            value13 = file01.iloc[i, 12]
            value14 = file01.iloc[i, 13]
            value15 = file01.iloc[i, 14]
            value16 = file01.iloc[i, 15]
            value17 = file01.iloc[i, 16]
            value18 = file01.iloc[i, 17]
            value19 = file01.iloc[i, 18]
            value20 = file01.iloc[i, 19]
            value21 = file01.iloc[i, 20]
            value22 = file01.iloc[i, 21]
            value23 = file01.iloc[i, 22]
            value24 = file01.iloc[i, 23]
            value25 = file01.iloc[i, 24]
            value26 = file01.iloc[i, 25]
            insert_sql = "INSERT INTO %s(序号,建筑所属行政区划,建筑代码,建筑详细名称,建筑详细地址,竣工年度,建筑类型,建筑功能,建筑层数,建筑面积平方米,供热方式," \
                         "供冷方式,所执行的建筑节能标准,是否实施节能改造,联系人,联系电话,统计时间,面积一,所属行政区,建筑功能01,总能耗千克标准煤,面积均能耗," \
                         "总用水,总用电,天然气总用量,面积二) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" \
                         ",'%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                         table_name01, str(value01), str(value02), str(value03), str(value04),
                         str(value05), str(value06), str(value07), str(value08), str(value09), str(value10),
                         str(value11), str(value12), str(value13),
                         str(value14), str(value15), str(value16), str(value17), str(value18), str(value19),
                         str(value20), str(value21), str(value22)
                         , str(value23), str(value24), str(value25), str(value26))
            cursor.execute(insert_sql)
    except:
        print('ERROR')

    try:
        creat_sql02 = "CREATE TABLE IF NOT EXISTS %s(序号 VARCHAR(255) NOT NULL,建筑代码 VARCHAR(255) NOT NULL, 建筑详细名称 VARCHAR(255) NOT NULL," \
                      "电力 VARCHAR(255) NOT NULL,天然气 VARCHAR(255) NOT NULL,水 VARCHAR(255) NOT NULL," \
                      "所属行政区 VARCHAR(255) NOT NULL,总能耗千克标准煤 VARCHAR(255) NOT NULL,面积均能耗 VARCHAR(255) NOT NULL,总用水 VARCHAR(255) NOT NULL," \
                      "总用电 VARCHAR(255) NOT NULL,天然气总用量 VARCHAR(255) NOT NULL,建筑面积平方米 VARCHAR(255) NOT NULL)" % (table_name02)
        # creat_sql02 = "CREATE TABLE IF NOT EXISTS %s(tmp01 VARCHAR(100) NOT NULL)"%(table_name02)
        cursor.execute(creat_sql02)
        for i in range(file02.shape[0]):
            value001 = file02.iloc[i, 0]
            value002 = file02.iloc[i, 1]
            value003 = file02.iloc[i, 2]
            value004 = file02.iloc[i, 3]
            value005 = file02.iloc[i, 5]
            value006 = file02.iloc[i, 13]
            value007 = file02.iloc[i, 19]
            value008 = file02.iloc[i, 20]
            value009 = file02.iloc[i, 21]
            value010 = file02.iloc[i, 22]
            value011 = file02.iloc[i, 23]
            value012 = file02.iloc[i, 24]
            value013 = file02.iloc[i, 25]

            insert_sql02 = "INSERT INTO %s(序号,建筑代码,建筑详细名称,电力,天然气,水,所属行政区,总能耗千克标准煤,面积均能耗,总用水,总用电," \
                         "天然气总用量,建筑面积平方米) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                             table_name02, str(value001), str(value002), str(value003), str(value004),
                             str(value005), str(value006), str(value007), str(value008), str(value009), str(value010),
                             str(value011), str(value012), str(value013))
            cursor.execute(insert_sql02)
    except:
        print('ERROR')

    #	建筑代码,建筑详细名称,电力,天然气,水,所属行政区,总能耗千克标准煤,面积均能耗,总用水,总用电,天然气总用量,建筑面积平方米


    db_target.commit()
    db_target.close()

if __name__ == '__main__':
    DB_Write()
