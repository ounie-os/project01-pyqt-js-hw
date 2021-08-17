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
def DB_Write_test():
    import pymysql
    import pandas as pd
    import json
    import datetime

    error_reason = ""

    ########## Step 01 读取配置文件 ##########
    f = open('./config.json')  # 读取配置文件
    t = json.load(f)  # 将json格式的数据映射成list的形式
    f.close()  # 关闭文件
    host01 = t['DB_connect']['host']
    port01 = t['DB_connect']['port']
    username01 = t['DB_connect']['username']
    password01 = t['DB_connect']['password']
    database01 = t['DB_connect']['database']

    try:
        db_target = pymysql.connect(host=host01,  # 连入配置信息所在数据库
                                    database=database01,
                                    user=username01,
                                    password=password01,
                                    charset="utf8")
        cursor = db_target.cursor()
        # find_sql = "SELECT COUNT(*)TABLES FROM information_schema.TABLES WHERE table_schema = 'database01'"
        db_target.commit()
        db_target.close()
        result = 0
    except Exception as e:
        error_reason = str(e)
        result = -1

    result_json = {
        "connection_result":result
    }
    result_json = json.dumps(result_json, ensure_ascii=False)
    print(result_json)
    tmp_f = open("result02.json", "w")
    tmp_f.write(result_json)
    tmp_f.flush()
    tmp_f.close()

    return error_reason

if __name__ == '__main__':
    DB_Write_test()
