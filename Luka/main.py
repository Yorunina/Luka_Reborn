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
import json
import os
import Luka.storage_man as sm
import Luka.api as api
import Luka.reply_man as rs

class Event(object):
    def init(plugin_event, Proc):
        global log
        bot_dict = Proc.Proc_data['bot_info_dict']
        for value in bot_dict.values():
            if value.platform["platform"] == "dodo":
                platform_bot_info["dodo"] = value
            elif value.platform["platform"] == "qq":
                platform_bot_info["qq"] = value
            log = Proc.log
        return

    def private_message(plugin_event, Proc):
        private_reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        group_reply(plugin_event, Proc)

    def save(plugin_event, Proc):
        pass




def private_reply(plugin_event, Proc):
    #消息直插数据库
    return

def group_reply(plugin_event, Proc):
    #消息直插数据库
    return



if __name__ != "__main__":
    platform_bot_info = {}