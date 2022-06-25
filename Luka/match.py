import re
import Luka.api as api
import Luka.reply_man as rm

class Reply_Struct():
    def __init__(self, func, key, match_type, priority):
        self.func = func
        self.key = key
        self.type = match_type
        self.pri = priority
        return

class Reply_Seq():
    def __init__(self):
        self.reply_seq = []
        return
    def register(self, func, key, match_type, priority):
        self.reply_seq.append(Reply_Struct(func, key, match_type, priority))
        return
    def match_filter(self, event):
        msg = api.format_msg(event)
        if msg.startswith("/"):
            return True
        return False
    def match_catch(self, event, Proc):
        msg = event.data.message
        if not self.match_filter(event):
            return
        for obj in self.reply_seq:
            # 进行正则匹配
            if obj.type == 'reg':
                # 正则表达式匹配
                match_obj = re.match(obj.key, msg, re.M | re.I)
                # 如果成功
                if match_obj:
                    # 调用函数
                    Proc.log(2,"已匹配关键词" + obj.key)
                    obj.func(event)
                    break
            # 进行完全匹配
            if obj.type == 'abs' and msg == obj.key:
                Proc.log(2,"已匹配关键词" + obj.key)
                obj.func(event)
                break
            # 进行前缀匹配
            if obj.type == 'pre' and msg.lower().startswith(obj.key):
                Proc.log(2,"已匹配关键词" + obj.key)
                obj.func(event)
                break
        return

def bot_state(event):
    event.reply("SimpleDeckBot v0.1\nBased on OlivOS")
    return

def bot_help(event):
    event.reply("SimpleDeckBotの使用方法：\n/bot"+format("查询机器人版本信息",">20") + 
    "\n/draw [词集名]" + format("从某词集中抽取"," >20") + 
    "\n/info [词集名]" + format("查询某词集系列的信息"," >20") + 
    "\n/set [词集名] [内容]" + format("新建/向某词集中插入单行内容"," >20"))
    return

if __name__ != "__main__":
    reply = Reply_Seq()
    reply.register(bot_state, "/bot", "abs", 0)
    reply.register(bot_help, "/help", "abs", 0)

    reply.register(rm.set_currency, "^/定义积分单位\s*#?(.+)$", "reg", 0)
    reply.register(rm.set_welcome, "^/入群欢迎\s*#?(.*)$", "reg", 0)
    reply.register(rm.set_welgo, "^/离群送别\s*#?(.*)$", "reg", 0)
    reply.register(rm.set_maxday, "^/定义连签上限\s*#?(\d+)$", "reg", 0)
    reply.register(rm.set_conbonus, "^/定义连签加值\s*#?(\d+)$", "reg", 0)
    reply.register(rm.set_basebonus, "^/定义基础加值\s*#?(\d+)$", "reg", 0)
    reply.register(rm.sign_in, "^/签到$", "reg", 0)
    reply.register(rm.goods_on_shelves, "^/上架\s*#?([^#]+)\s*#(.+)$", "reg", 0)
    reply.register(rm.goods_off_shelves, "^/下架\s*#?([^#]+)$", "reg", 0)
    reply.register(rm.get_page_goods, "^/商店\s*#?(\d*)$", "reg", 0)
    reply.register(rm.group_store_buy, "^/购买\s*#?([^#]+)\s*#?(\d{1,3})?$", "reg", 0)
    reply.register(rm.group_bagpack_use, "^/使用\s*#?([^#]+)\s*#?(\d{1,3})?$", "reg", 0)
    reply.register(rm.group_bagpack_getall, "^/背包\s*(\d*)$", "reg", 0)
    reply.register(rm.get_all_gashpool, "^/查扭蛋池$", "reg", 10)
    reply.register(rm.get_pool_all_item, "^/查扭蛋池\s*#?([^#]+)\s*#?(\d{1,3})?$", "reg", 0)
    reply.register(rm.set_gashpool, "^/设扭蛋池\s*#?([^#]+)\s*#(.+)$", "reg", 0)
    reply.register(rm.add_pool_item, "^/添加?扭蛋\s*#?([^#]+)\s*#(\S+)\s*#?(\d{1,3})?$", "reg", 0)


