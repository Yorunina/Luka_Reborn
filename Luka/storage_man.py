#####################################################
#  .---.       ___    _   .--.   .--.      ____     #
#  | ,_|     .'   |  |  | |  | _/  /     .'  __ `.  #
#,-./  )     |   .'  |  | | (`' ) /     /   '  \  \ #
#\  '_ '`)   .'  '_  |  | |(_ ()_)      |___|  /  | #
# > (_)  )   '   ( \.-. | | (_,_)   __     _.-`   | #
#(  .  .-'   ' (`. _` / | |  |\ \  |  | .'   _    | #
# `-'`-'|___ | (_ (_) _)| |    \ `'   / |  _( )_  | #
#  |        \ \ /  . \  / |  |  \    /  \ (_ o _) / #
#  `--------`  ``-'`-''   `--'   `'-'    '.(_,_).'  #
#####################################################

import sqlite3
import os
#
data_file = "./plugin/data/Luka"
msg_db = sqlite3.connect(data_file + '/storage.db', isolation_level=None, check_same_thread=False)
#
class sqliteOperation(object):
    def __init__(self):
        #链接数据库，真男人从不用游标
        self.db = msg_db
        self.init_table()
        return

    def init_table(self):
        #获取所有表的名称
        all_table_get_sen = "SELECT name FROM sqlite_master WHERE type='table';"
        table_list = []
        ori_table_list = self.db.execute(all_table_get_sen).fetchall()
        #将所有表的名称转移到列表中
        for table_name in ori_table_list:
            table_list.append(table_name[0])
        #初始化新建表字典
        table_dict = {
            "IndePoint":"CREATE TABLE IndePoint (Groupid INT NOT NULL,Userid  INT NOT NULL,Point INT NOT NULL DEFAULT (0) );CREATE UNIQUE INDEX OnlyGroupPoint ON IndePoint (Groupid,Userid);",
            "TimeLimit":""
            }
        for table_name, create_sen in table_dict.items():
            #如果表名不存在在表列表中
            if table_name not in table_list:
                #执行表创建
                self.muti_exec(create_sen)
        return
    
    def muti_exec(self, muti_sen):
        #分割多条sql，并且逐个执行，但无返回值
        sql_list = muti_sen.split(';')
        for sql_sen in sql_list:
            self.db.execute(sql_sen)
        return

    def get_exec(self, sen, params = (),times = 1):
        #获取型执行
        if times == 1:
            res = self.db.execute(sen, params).fetchone()
        elif times == -1:
            res = self.db.execute(sen, params).fetchall()
        else:
            res = self.db.execute(sen, params).fetchmany(times)
        return res

    def exec(self, sen, params = ()):
        self.db.execute(sen, params)
        return

if __name__ != "__main__":
    #创建数据目录
    data_file = "./plugin/data/Luka"
    if not os.path.exists(data_file):
        os.mkdir(data_file)
    msg_db = sqlite3.connect(data_file + '/storage.db', isolation_level=None, check_same_thread=False)