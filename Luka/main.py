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


from threading import Thread
import Luka.api as api
import Luka.reply_man as rm
import Luka.match as match

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
                reply_thd = Thread(target=group_reply, args=(plugin_event, Proc))
                reply_thd.start()


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
    match.reply.match_catch(event, Proc)
    return

if __name__ != "__main__":
    platform_bot_info = {}