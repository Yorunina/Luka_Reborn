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
from OlivOS.onebotSDK import event_action as onebotSDK
import Luka.storage_man as sm
import time

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

class IndePoint(sm.sqliteOperation):
    def __init__(self, user_id:int, group_id:int = 0):
        sm.sqliteOperation.__init__(self)
        self.user_id = user_id
        self.group_id = group_id
        return

    def get_operation(self):
        res = self.get_exec("SELECT Point FROM IndePoint WHERE Userid=? AND Groupid=?", (self.user_id, self.group_id))
        if res:
            self.exec("INSERT INTO IndePoint (Userid,Gourpid,Point) VALUES (?,?,?)",(self.user_id, self.group_id, 0))
            point = 0
        else:
            point = res[0]
        self.point = point
        return point

    def quick_update_operation(self, expr:str = ""):
        #存在注入风险，请勿暴露
        ori_point = self.get_operation(self.group_id, self.user_id)
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
        day = self.ts//86400
        get_day = self.get_ts//86400
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

class GetGroup(sm.sqliteOperation):
    def __init__(self):
        sm.sqliteOperation.__init__(self)
        return
    def get_state(self, event):
        #获取开关状态
        res = self.get_exec("SELECT State FROM DefineGroup WHERE Groupid=?", (event.data.group_id,))
        if res:
            return res[0]
        else:
            return 1
    def get_welcome(self, event):
        #获取群欢迎
        res = self.get_exec("SELECT Welcome FROM DefineGroup WHERE Groupid=?", (event.data.group_id,))
        if res:
            return res[0]
        else:
            return