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

import Luka.storage_man as sm
import Luka.api as api
import random
def indegroup_sign_in(event):
    group_id = event.data.group_id
    user_id = event.data.user_id
    if api.TimeLimit(user_id, group_id).check_day_record("indegroup_sign_in"):
        point_obj = api.IndePoint(user_id, group_id)
        point_add = random.randint(1,4)
        now_point = point_obj.quick_update_operation("[Point]+%s"%point_add)
        event.reply("签到成功！\n今天您获得积分%i点，目前共有%i点。" % (point_add,now_point))
    else:
        event.reply("今天你已经签到过了哦~")
    return