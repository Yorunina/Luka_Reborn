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
        # 清除空格和首位
            if plugin_event.data.message == "/榴歌关闭":
                rm.set_state_close(plugin_event)
            elif plugin_event.data.message == "/榴歌开启":
                rm.set_state_open(plugin_event)
            else:
                if api.GetGroup().get_state(plugin_event) != 0:
                    group_reply(plugin_event, Proc)

    def group_member_increase(plugin_event, Proc):
        #获取当前群的入群欢迎
        welcome = api.GetGroup().get_welcome(plugin_event)
        if welcome:
            plugin_event.reply(welcome)
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
    get_re = re.match("\/定义连签上限\s*(\d+)", msg, flags=re.I|re.M)
    if get_re:
        rm.set_maxday(event, get_re)
        return
    get_re = re.match("\/定义连签加值\s*(\d+)", msg, flags=re.I|re.M)
    if get_re:
        rm.set_conbonus(event, get_re)
        return
    return



if __name__ != "__main__":
    platform_bot_info = {}