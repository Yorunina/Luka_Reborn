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
import turtle

class sqliteOperation(object):
    def __init__(self):
        #链接数据库，真男人从不用游标
        self.db = msg_db
        return

    def init_table(self):
        #获取所有表的名称
        all_table_get_sen = "SELECT name FROM sqlite_master WHERE type='table';"
        table_list = []
        ori_table_list = self.get_exec(all_table_get_sen,times = -1)
        #将所有表的名称转移到列表中
        for table_name in ori_table_list:
            table_list.append(table_name[0])
        #初始化新建表字典
        table_dict = {
            #存储群积分相关
            "IndePoint":"CREATE TABLE IndePoint (Groupid INT NOT NULL,Userid  INT NOT NULL,Point INT NOT NULL DEFAULT (0) );CREATE UNIQUE INDEX OnlyGroupPoint ON IndePoint (Groupid,Userid);",
            #存储间隔回复
            "TimeLimit":"CREATE TABLE TimeLimit (Groupid INT NOT NULL,Userid  INT NOT NULL,Mark TEXT NOT NULL,Ts INT NOT NULL,Times INT NOT NULL DEFAULT (1));CREATE UNIQUE INDEX OnlyTimeLimit ON TimeLimit (Groupid,Userid,Mark);",
            #存储群特定信息，包含签到定义
            "DefineGroup":"CREATE TABLE DefineGroup (Groupid INT NOT NULL UNIQUE,Currency INT DEFAULT 胡桃夹 NOT NULL,Welcome TEXT DEFAULT (0) NOT NULL,Welgo TEXT DEFAULT (0) NOT NULL,State INT NOT NULL DEFAULT (1),Maxday INT NOT NULL DEFAULT (7),Conbonus DEFAULT (1) NOT NULL,Basebonus DEFAULT (1) NOT NULL);",
            #存储连续签到数据
            "ConSign":"CREATE TABLE ConSign (Groupid INT NOT NULL,Userid INT NOT NULL,LastSign INT NOT NULL,BeginSign INT NOT NULL);CREATE UNIQUE INDEX OnlyGroupSign ON ConSign (Groupid,Userid);",
            #群商店储存
            "GroupStore":"CREATE TABLE GroupStore (Groupid INT NOT NULL,DisplayName TEXT NOT NULL,Price INT NOT NULL,BuyLimit INT NOT NULL DEFAULT (-1),Description TEXT);CREATE UNIQUE INDEX OnlyGroupGoods ON GroupStore (Groupid,DisplayName);",
            #群背包储存
            "IndeBagPack":"CREATE TABLE IndeBagPack (Groupid INT NOT NULL,Userid INT NOT NULL,Item TEXT NOT NULL,Count INT NOT NULL DEFAULT (1));CREATE UNIQUE INDEX OnlyGroupBag ON IndeBagPack (Groupid,Userid,Item);",
            #群扭蛋物品储存
            "GashaponItem":"CREATE TABLE GashaponItem (Groupid INT NOT NULL,Pool TEXT NOT NULL,Item TEXT NOT NULL,Count INT NOT NULL DEFAULT (1));CREATE UNIQUE INDEX OnlyGashaponItem ON GashaponItem (Groupid,Pool,Item);",
            #群扭蛋池定义储存
            "GashaponPool":"CREATE TABLE GashaponPool (Groupid INT NOT NULL,Pool TEXT NOT NULL,Type INT DEFAULT (0) NOT NULL,Token TEXT NOT NULL DEFAULT 积分,Price INT NOT NULL DEFAULT (1));CREATE UNIQUE INDEX OnlyGashaponPool ON GashaponPool (Groupid,Pool);"
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
    #创建牌堆目录
    if not os.path.exists(data_file + "/deck"):
        os.mkdir(data_file + "/deck")
    msg_db = sqlite3.connect(data_file + '/storage.db', isolation_level=None, check_same_thread=False)
    #手动初始化校对数据库模式
    sqliteOperation().init_table()