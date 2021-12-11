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

import storage_man as sm

class MsgWindow(object):
    def __init__(group_id, user_id):
        return

class IndePoint(sm.sqliteOperation):
    def get_operation(self, group_id:int, user_id:int):
        res = self.get_exec("SELECT Point FROM IndePoint WHERE Userid=? AND Groupid=?", (user_id, group_id))
        if res:
            self.exec("INSERT INTO IndePoint (Userid,Gourpid,Point) VALUES (?,?,?)",(user_id, group_id, 0))
            point = 0
        else:
            point = res[0]
        return point
    def quick_update_operation(self, group_id:int, user_id:int, expr:str = ""):
        #存在注入风险，请勿暴露
        ori_point = self.get_operation(group_id, user_id)
        if expr:
            #将预留自我标识符号替换为变量
            expr = expr.replace("[P]",str(ori_point))
            point = eval(expr)
            self.exec("UPDATE IndePoint SET Point=? WHERE Groupid=? AND Userid=?", (point, group_id, user_id))
            return (ori_point,point)
        else:
            return (ori_point,ori_point)
    def group_rank_operation(self, group_id:int, num:int = 10):
        res = self.get_exec("SELECT Userid,Point FROM IndePoint WHERE Groupid=? ORDER BY Point DESC LIMIT ?",(group_id, num), -1)
        return res

class TimeLimit(sm.sqliteOperation):
    def get_record(self, group_id:int, user_id:int, keyword:str):
        return