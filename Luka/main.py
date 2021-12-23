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
import html


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

    return

def group_reply(event, Proc):
    msg = event.data.message
    msg = html.unescape(msg).strip().lstrip("/")
    get_re = re.match("^定义积分单位\s*(.+)$", msg, flags=re.I|re.M)
    if get_re:
        rm.set_currency(event, get_re)
        return
    get_re = re.match("^入群欢迎\s*(.*)$", msg, flags=re.I|re.M)
    if get_re:
        rm.set_welcome(event, get_re)
        return
    get_re = re.match("^离群送别\s*(.*)$", msg, flags=re.I|re.M)
    if get_re:
        rm.set_welgo(event, get_re)
        return
    get_re = re.match("^定义连签上限\s*(\d+)$", msg, flags=re.I|re.M)
    if get_re:
        rm.set_maxday(event, get_re)
        return
    get_re = re.match("^定义连签加值\s*(\d+)$", msg, flags=re.I|re.M)
    if get_re:
        rm.set_conbonus(event, get_re)
        return
    get_re = re.match("^定义基础加值\s*(\d+)$", msg, flags=re.I|re.M)
    if get_re:
        rm.set_basebonus(event, get_re)
        return
    get_re = re.match("^签到$", msg, flags=re.I|re.M)
    if get_re:
        rm.sign_in(event)
        return
    get_re = re.match("^上架\s*([^\[]*[^\[\s])\s*(.+)$", msg, flags=re.I|re.M)
    if get_re:
        rm.goods_on_shelves(event, get_re)
        return
    get_re = re.match("^下架\s*([^\[]*[^\[\s])$", msg, flags=re.I|re.M)
    if get_re:
        rm.goods_off_shelves(event, get_re)
        return
    get_re = re.match("^商店\s*(\d*)\s*$", msg, flags=re.I|re.M)
    if get_re:
        rm.get_page_goods(event, get_re)
        return
    get_re = re.match("^购买\s*([^\[]*[^\[\s])\s*(?:\[(\d{1,3})\])?$", msg, flags=re.I|re.M)
    if get_re:
        rm.group_store_buy(event, get_re)
        return
    get_re = re.match("^使用\s*([^\[]*[^\[\s])\s*(?:\[(\d{1,3})\])?$", msg, flags=re.I|re.M)
    if get_re:
        rm.group_bagpack_use(event, get_re)
        return
    get_re = re.match("^背包\s*(\d*)$", msg, flags=re.I|re.M)
    if get_re:
        rm.group_bagpack_getall(event, get_re)
        return
    get_re = re.match("^查扭蛋池$", msg, flags=re.I|re.M)
    if get_re:
        rm.get_all_gashpool(event, get_re)
        return
    get_re = re.match("^查扭蛋池\s*([^\[]*[^\[\s])$", msg, flags=re.I|re.M)
    if get_re:
        rm.group_bagpack_getall(event, get_re)
        return
    get_re = re.match("^设扭蛋机\s*([^\[]*[^\[\s])\s*(.+)$", msg, flags=re.I|re.M)
    if get_re:
        rm.group_bagpack_getall(event, get_re)
        return
    return




if __name__ != "__main__":
    platform_bot_info = {}