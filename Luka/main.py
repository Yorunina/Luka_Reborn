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

import OlivOS
import re
import Luka.storage_man as sm
import Luka.api as api
import Luka.reply_man as rm

class Event(object):
    def init(plugin_event, Proc):
        global log
        bot_dict = Proc.Proc_data['bot_info_dict']
        for value in bot_dict.values():
            if value.platform["platform"] == "qq":
                platform_bot_info["qq"] = value
            log = Proc.log
        return

    def private_message(plugin_event, Proc):
        private_reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        if plugin_event.data.message.startswith("/"):
            if plugin_event.data.message == "/榴歌关闭":
                rm.set_state_close(plugin_event)
            elif plugin_event.data.message == "/榴歌开启":
                rm.set_state_open(plugin_event)
            else:
                if api.GetGroupDefine(plugin_event.data.group_id).state != 0:
                    group_reply(plugin_event, Proc)

    def group_member_increase(plugin_event, Proc):
        #获取当前群的入群欢迎
        welcome = api.GetGroupDefine(plugin_event.data.group_id).welcome
        if welcome != 0:
            plugin_event.reply(welcome)
        return

    def group_member_decrease(plugin_event, Proc):
        #获取当前群的离群语
        welgo = api.GetGroupDefine(plugin_event.data.group_id).welgo
        if welgo != 0:
            plugin_event.reply(welgo)
        return

    def save(plugin_event, Proc):
        pass




def private_reply(event, Proc):
    #消息直插数据库

    return

def group_reply(event, Proc):
    msg = event.data.message

    get_re = re.match("\/定义积分单位\s*(.+)", msg, flags=re.I|re.M)
    if get_re:
        rm.set_currency(event, get_re)
        return
    get_re = re.match("\/入群欢迎\s*(.*)\s*", msg, flags=re.I|re.M)
    if get_re:
        rm.set_welcome(event, get_re)
        return
    get_re = re.match("\/离群送别\s*(.*)\s*", msg, flags=re.I|re.M)
    if get_re:
        rm.set_welgo(event, get_re)
        return
    get_re = re.match("\/定义连签上限\s*(\d+)", msg, flags=re.I|re.M)
    if get_re:
        rm.set_maxday(event, get_re)
        return
    get_re = re.match("\/定义连签加值\s*(\d+)", msg, flags=re.I|re.M)
    if get_re:
        rm.set_conbonus(event, get_re)
        return
    get_re = re.match("\/定义基础加值\s*(\d+)", msg, flags=re.I|re.M)
    if get_re:
        rm.set_basebonus(event, get_re)
        return
    get_re = re.match("\/签到", msg, flags=re.I|re.M)
    if get_re:
        rm.sign_in(event)
        return
    get_re = re.match("\/上架\s*([^\[]+)(?:\[限(\d{1,3})\])?\s*\[价(\d+)\]\s*(?:\[描述(.+)\])?\s*", msg, flags=re.I|re.M)
    if get_re:
        rm.goods_shelves(event, get_re)
        return
    get_re = re.match("\/签到", msg, flags=re.I|re.M)
    if get_re:
        rm.sign_in(event)
        return
    return



if __name__ != "__main__":
    platform_bot_info = {}