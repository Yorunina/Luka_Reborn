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

############################
#分群积分/群商店系统
############################

#群定义签到货币
def set_currency(event, get_re):
    content = get_re.group(1)
    if api.onebot(event).check_permission():
        api.DefineGroup().set_currency(event.data.group_id, content)
        event.reply("修改成功！\n从今天起，本群的积分单位就为「%s」了哦~" % content)
    else:
        event.reply("权限不足！\n你必须是本群的管理员/群主！")
    return

#群定义连续签到最大天数
def set_maxday(event, get_re):
    content = int(get_re.group(1))
    if api.onebot(event).check_permission():
        api.DefineGroup().set_maxday(event.data.group_id, content)
        event.reply("修改成功！\n从今天起，本群的连续最大签到天数为「%i天」了哦~" % content)
    else:
        event.reply("权限不足！\n你必须是本群的管理员/群主！")
    return

#群定义连续签到加值
def set_conbonus(event, get_re):
    content = int(get_re.group(1))
    if api.onebot(event).check_permission():
        api.DefineGroup().set_conbonus(event.data.group_id, content)
        event.reply("修改成功！\n从今天起，本群的连续签到加值变为「%i」了哦~" % content)
    else:
        event.reply("权限不足！\n你必须是本群的管理员/群主！")
    return

#群入群欢迎
def set_welcome(event, get_re):
    content = get_re.group(1)
    if not content:
        api.DefineGroup().set_welcome(event.data.group_id, 0)
        event.reply("已清除本群的入群欢迎！")
        return
    if api.onebot(event).check_permission():
        api.DefineGroup().set_welcome(event.data.group_id, content)
        event.reply("是「%s」吗？榴歌完全记住了！" % content)
    else:
        event.reply("权限不足！\n你必须是本群的管理员/群主！")
    return

#关机
def set_state_close(event):
    if api.get_state(event) == 0:
        event.reply("榴歌已经处于关闭状态了哦~")
        return
    if api.onebot(event).check_permission():
        api.DefineGroup().set_welcome(event.data.group_id, 0)
        event.reply("这里不需要榴歌了吗？\n那我就先行退下了。")
    else:
        event.reply("权限不足！\n你必须是本群的管理员/群主！")
    return

#开机
def set_state_open(event):
    if api.get_state(event) == 1:
        event.reply("榴歌已经在这里等很久了，不需要再开启了哦~")
        return
    if api.onebot(event).check_permission():
        api.DefineGroup().set_welcome(event.data.group_id, 1)
        event.reply("是有人在呼唤我吗？榴歌随时待命！")
    else:
        event.reply("权限不足！\n你必须是本群的管理员/群主！")
    return

#分群签到
def sign_in(event):
    group_id = event.data.group_id
    user_id = event.data.user_id
    if api.TimeLimit(user_id, group_id).check_day_record("indegroup_sign_in"):
        point_obj = api.IndePoint(user_id, group_id)
        point_add = random.randint(1,4)
        now_point = point_obj.quick_update_operation("[Point]+%s" % point_add)
        event.reply("签到成功！\n今天您获得积分%i点，目前共有%i点。" % (point_add,now_point))
    else:
        event.reply("今天你已经签到过了哦~")
    return

