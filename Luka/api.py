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
from tokenize import group
from OlivOS.onebotSDK import event_action as onebotSDK
import Luka.storage_man as sm
import time

def clamp(n, minn, maxn): 
    return max(min(maxn, n), minn)

class onebot:
    def __init__(self, event):
        self.event = event
        return
    def group_member_info(self):
        group_id = self.event.data.group_id
        user_id = self.event.data.user_id
        return onebotSDK.get_group_member_info(self.event, group_id, user_id)
        
    def check_permission(self, role = "admin"):
        member_role = self.group_member_info()['data']['role']
        permission_dict = {"owner":3,"admin":2,"member":1}
        if permission_dict[member_role] >= permission_dict[role]:
            return True
        else:
            return False

#群积分操作
class IndePoint(sm.sqliteOperation):
    def __init__(self, user_id:int, group_id:int = 0):
        sm.sqliteOperation.__init__(self)
        self.user_id = user_id
        self.group_id = group_id
        return

    def get_operation(self):
        res = self.get_exec("SELECT Point FROM IndePoint WHERE Userid=? AND Groupid=?", (self.user_id, self.group_id))
        if not res:
            self.exec("INSERT INTO IndePoint (Userid,Groupid,Point) VALUES (?,?,?)",(self.user_id, self.group_id, 0))
            point = 0
        else:
            point = res[0]
        self.point = point
        return point

    def quick_update_operation(self, expr:str = ""):
        #存在注入风险，请勿暴露
        ori_point = self.get_operation()
        if expr:
            #将预留自我标识符号替换为变量
            expr = expr.replace("[Point]",str(ori_point))
            point = eval(expr)
            self.exec("UPDATE IndePoint SET Point=? WHERE Groupid=? AND Userid=?", (point, self.group_id, self.user_id))
            self.point = point
            return (ori_point,point)
        else:
            return (ori_point,ori_point)

    def group_rank_operation(self, num:int = 10):
        res = self.get_exec("SELECT Userid,Point FROM IndePoint WHERE Groupid=? ORDER BY Point DESC LIMIT ?",(self.group_id, num), -1)
        return res

#时间限制操作
class TimeLimit(sm.sqliteOperation):
    def __init__(self, user_id:int, group_id:int = 0):
        sm.sqliteOperation.__init__(self)
        self.user_id = user_id
        self.group_id = group_id
        return

    def get_record(self, mark:str):
        #获取记录时间和次数
        res = self.get_exec("SELECT Ts,Times FROM TimeLimit WHERE Groupid=? AND Userid=? AND Mark=?", (self.group_id, self.user_id, mark))
        self.get_ts = int(time.time())
        if not res:
            res = (self.get_ts,0)
        self.ts = res[0]
        self.times = res[1]
        return (self.ts,self.times)

    def check_interval_record(self, mark:str, interval:int = 86400, limit:int = 1, auto_increase:int = 1):
        self.get_record(mark)
        if auto_increase != 0 and self.times == 0:
            #不存在且允许自增
            self.exec("REPLACE INTO TimeLimit (Groupid,Userid,Mark,Ts,Times) VALUES (?,?,?,?,?)",
            (self.group_id, self.user_id, mark, self.get_ts, auto_increase))
        elif self.ts + interval < self.get_ts:
            #超时，重新计数
            self.exec("REPLACE INTO TimeLimit (Groupid,Userid,Mark,Ts,Times) VALUES (?,?,?,?,?)",
            (self.group_id, self.user_id, mark, self.get_ts, auto_increase))
        elif self.times >= limit:
            #超限
            return False
        else:
            self.exec("UPDATE TimeLimit SET Times=? WHERE Groupid=? AND Userid=? AND Mark=?",
            (self.times+auto_increase, self.group_id, self.user_id, mark))
        return True
    
    def check_day_record(self, mark:str, interval:int = 1, limit:int = 1):
        self.get_record(mark)
        day = (self.ts+28800)//86400
        get_day = (self.get_ts+28800)//86400
        if self.times == 0:
            #不存在且允许自增
            self.exec("REPLACE INTO TimeLimit (Groupid,Userid,Mark,Ts,Times) VALUES (?,?,?,?,?)",
            (self.group_id, self.user_id, mark, self.get_ts, 1))
        elif day + interval < get_day or day > get_day:
            #超时，重新计数
            self.exec("REPLACE INTO TimeLimit (Groupid,Userid,Mark,Ts,Times) VALUES (?,?,?,?,?)",
            (self.group_id, self.user_id, mark, self.get_ts, 1))
        elif self.times >= limit:
            #超限
            return False
        else:
            self.exec("UPDATE TimeLimit SET Times=? WHERE Groupid=? AND Userid=? AND Mark=?",
            (self.times+1, self.group_id, self.user_id, mark))
        return True

#定义群属性
class DefineGroup(sm.sqliteOperation):
    def __init__(self):
        sm.sqliteOperation.__init__(self)
        return

    def check_exist(self, group_id):
        res = self.get_exec("SELECT Groupid FROM DefineGroup WHERE Groupid=?",(group_id,))
        if res:
            return True
        else:
            return False

    def set_welcome(self, group_id, content):
        if not self.check_exist(group_id):
            #如果不存在就新建
            self.exec("INSERT INTO DefineGroup (Groupid) VALUES (?)",(group_id,))
        self.exec("UPDATE DefineGroup SET Welcome=? WHERE Groupid=?",(content, group_id))
        return
    
    def set_welgo(self, group_id, content):
        if not self.check_exist(group_id):
            #如果不存在就新建
            self.exec("INSERT INTO DefineGroup (Groupid) VALUES (?)",(group_id,))
        self.exec("UPDATE DefineGroup SET Welgo=? WHERE Groupid=?",(content, group_id))
        return
    
    def set_maxday(self, group_id, content):
        if not self.check_exist(group_id):
            #如果不存在就新建
            self.exec("INSERT INTO DefineGroup (Groupid) VALUES (?)",(group_id,))
        self.exec("UPDATE DefineGroup SET Maxday=? WHERE Groupid=?",(content, group_id))
        return
    
    def set_conbonus(self, group_id, content):
        if not self.check_exist(group_id):
            #如果不存在就新建
            self.exec("INSERT INTO DefineGroup (Groupid) VALUES (?)",(group_id,))
        self.exec("UPDATE DefineGroup SET Conbonus=? WHERE Groupid=?",(content, group_id))
        return

    def set_basebonus(self, group_id, content):
        if not self.check_exist(group_id):
            #如果不存在就新建
            self.exec("INSERT INTO DefineGroup (Groupid) VALUES (?)",(group_id,))
        self.exec("UPDATE DefineGroup SET Basebonus=? WHERE Groupid=?",(content, group_id))
        return

    def set_currency(self, group_id, content):
        #鉴权
        if not self.check_exist(group_id):
            #如果不存在就新建
            self.exec("INSERT INTO DefineGroup (Groupid) VALUES (?)",(group_id,))
        self.exec("UPDATE DefineGroup SET Currency=? WHERE Groupid=?",(content, group_id))
        return
    
    def set_state(self, group_id, state):
        #开关
        if not self.check_exist(group_id):
            #如果不存在就新建
            self.exec("INSERT INTO DefineGroup (Groupid) VALUES (?)",(group_id,))
        self.exec("UPDATE DefineGroup SET State=? WHERE Groupid=?",(state, group_id))
        return

#获取群属性
class GetGroupDefine(sm.sqliteOperation):
    def __init__(self, group_id):
        sm.sqliteOperation.__init__(self)
        res = self.get_exec("SELECT * FROM DefineGroup WHERE Groupid=?", (group_id,))
        if not res:
            self.exec("INSERT INTO DefineGroup (Groupid) VALUES (?)",(group_id,))
            res = (group_id,"胡桃夹", 0, 0, 1, 7, 1, 1)
        (self.group_id,
        self.currency,
        self.welcome,
        self.welgo,
        self.state,
        self.maxday,
        self.conbonus,
        self.basebonus) = res
        return

#定义群商店
class DefineGroupStore(sm.sqliteOperation):
    def __init__(self):
        sm.sqliteOperation.__init__(self)
        return
    def check_exist(self, group_id):
        res = self.get_exec("SELECT Groupid FROM GroupStore WHERE Groupid=?",(group_id,))
        if res:
            return True
        else:
            return False
    #添加新商品
    def add_new_goods(self, group_id:int, displayname:str, price:int, buylimit:int = -1, description:str = ""):
        rowid = self.get_exec("SELECT rowid FROM GroupStore WHERE Groupid=? AND DisplayName=?",(group_id,displayname))
        re_bool = True
        if rowid:
            re_bool = False
        self.exec("REPLACE INTO GroupStore (Groupid, DisplayName, Price, BuyLimit, Description) VALUES (?,?,?,?,?)",
        (group_id,displayname,price,buylimit,description))
        return re_bool
    #下架商品
    def del_old_goods(self, group_id:int, displayname:str):
        rowid = self.get_exec("SELECT rowid FROM GroupStore WHERE Groupid=? AND DisplayName=?",(group_id,displayname))
        if rowid:
            self.exec("DELETE FROM GroupStore WHERE rowid=?",rowid)
        else:
            return False
        return True
    #下架所有商品
    def del_all_goods(self, group_id:int):
        self.exec("DELETE FROM GroupStore WHERE Groupid=?",(group_id,))
        return
    #减少限量状态
    def refresh_limit(self, group_id:int, displayname:str, buytimes:int = 1):
        (rowid,buylimit) = self.get_exec("SELECT rowid,BuyLimit FROM GroupStore WHERE Groupid=? AND DisplayName=?",(group_id,displayname))
        if rowid:
            if buylimit - buytimes > 0:
                self.exec("UPDATE GroupStore SET BuyLimit=? WHERE rowid=?",(buylimit - buytimes,rowid))
                return 1
            elif buylimit - buytimes == 0:
                self.exec("DELETE FROM GroupStore WHERE rowid=?",rowid)
            elif buylimit < 0:
                return 1
            elif buylimit - buytimes < 0:
                return -1
        return -2

#获取群商店
class GetGroupStore(sm.sqliteOperation):
    def __init__(self,group_id:int):
        sm.sqliteOperation.__init__(self)
        self.group_id = group_id
        return
    def get_all_goods(self):
        res = self.get_exec("SELECT DisplayName,Price,BuyLimit,Description FROM GroupStore WHERE Groupid=?",(self.group_id,),-1)
        return res
    def get_goods(self,displayname):
        res = self.get_exec("SELECT DisplayName,Price,BuyLimit,Description FROM GroupStore WHERE Groupid=? AND DisplayName=?",(self.group_id,displayname))
        return res