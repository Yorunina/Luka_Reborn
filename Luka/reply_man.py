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

from locale import currency
import Luka.storage_man as sm
import Luka.api as api
import random
import time

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

#群定义基础签到加值
def set_basebonus(event, get_re):
    content = int(get_re.group(1))
    if api.onebot(event).check_permission():
        api.DefineGroup().set_basebonus(event.data.group_id, content)
        event.reply("修改成功！\n从今天起，本群的基础签到加值变为「%i」了哦~" % content)
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

#群离群送别
def set_welgo(event, get_re):
    content = get_re.group(1)
    if not content:
        api.DefineGroup().set_welcome(event.data.group_id, 0)
        event.reply("已清除本群的送别语！")
        return
    if api.onebot(event).check_permission():
        api.DefineGroup().set_welgo(event.data.group_id, content)
        event.reply("是「%s」吗？榴歌完全记住了！" % content)
    else:
        event.reply("权限不足！\n你必须是本群的管理员/群主！")
    return

#关机
def set_state_close(event):
    if api.GetGroupDefine(event.data.group_id) == 0:
        event.reply("榴歌已经处于关闭状态了哦~")
        return
    if api.onebot(event).check_permission():
        api.DefineGroup().set_state(event.data.group_id, 0)
        event.reply("这里不需要榴歌了吗？\n那我就先行退下了。")
    else:
        event.reply("权限不足！\n你必须是本群的管理员/群主！")
    return

#开机
def set_state_open(event):
    if api.GetGroupDefine(event.data.group_id) == 1:
        event.reply("榴歌已经在这里等很久了，不需要再开启了哦~")
        return
    if api.onebot(event).check_permission():
        api.DefineGroup().set_state(event.data.group_id, 1)
        event.reply("是有人在呼唤我吗？榴歌随时待命！")
    else:
        event.reply("权限不足！\n你必须是本群的管理员/群主！")
    return

#分群签到
def sign_in(event):
    group_id = event.data.group_id
    user_id = event.data.user_id
    db = sm.sqliteOperation()
    res = db.get_exec("SELECT LastSign,BeginSign FROM ConSign WHERE Groupid=? AND Userid=?",(group_id, user_id))
    now_ts = int(time.time())
    now_day = (now_ts+28800)//86400
    if res:
        (last_sign, begin_sign) = res
        begin_day = (begin_sign+28800)//86400
        last_day = (last_sign+28800)//86400
    else:
        last_day = 0
        begin_day = now_day
    if last_day == now_day:
        event.reply("今天你已经签到过了哦~不许贪心！")
        return
    group_define_obj = api.GetGroupDefine(group_id)
    point_obj = api.IndePoint(user_id, group_id)
    if last_day + 1 == now_day:
        con_day_count =now_day - begin_day; 
        point_add = group_define_obj.conbonus*api.clamp(con_day_count,0,group_define_obj.maxday) + group_define_obj.basebonus
        now_point = point_obj.quick_update_operation("[Point]+%s" % point_add)[1]
        event.reply("签到成功！连续签到%i天。\n今天您获得%i×%s，目前共有%i×%s。" % 
        (con_day_count,point_add,group_define_obj.currency,now_point,group_define_obj.currency))
    elif last_day == 0:
        point_add = group_define_obj.basebonus
        now_point = point_obj.quick_update_operation("[Point]+%s" % point_add)[1]
        event.reply("诶？是第一次签到吗？欢迎加入这个大家庭哦~\n今天您获得%i×%s，目前共有%i×%s。" % 
        (point_add,group_define_obj.currency,now_point,group_define_obj.currency))
        begin_sign = now_ts
    else:
        point_add = group_define_obj.basebonus
        now_point = point_obj.quick_update_operation("[Point]+%s" % point_add)[1]
        last_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(last_sign))
        event.reply("您上一次签到时间为[%s]\n今天您获得%i×%s，目前共有%i×%s。" % 
        (last_str,point_add,group_define_obj.currency,now_point,group_define_obj.currency))
        begin_sign = now_ts
    db.exec("REPLACE INTO ConSign (Groupid,Userid,LastSign,BeginSign) VALUES (?,?,?,?)",(group_id,user_id,now_ts,begin_sign))
    return

