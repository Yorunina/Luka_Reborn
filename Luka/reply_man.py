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

from multiprocessing import pool
import Luka.storage_man as sm
import Luka.api as api
import random
import time
import re

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

#商品上架
def goods_on_shelves(event, get_re):
    group_id = event.data.group_id
    displayname = get_re.group(1)
    main_content = get_re.group(2)
    price_get_re = re.search("\[价格?(\d+)\]", main_content, flags=re.I|re.M)
    if price_get_re:
        price = int(price_get_re.group(1))
    else:
        event.reply("上架物品必须带有价格哦~\n如/上架测试[价格12]")
        return
    buylimit_get_re = re.search("\[限购?(\d+)\]", main_content, flags=re.I|re.M)
    if buylimit_get_re:
        buylimit = int(buylimit_get_re.group(1))
    else:
        buylimit = -1
    description_get_re = re.search("\[描述?(^\])\]", main_content, flags=re.I|re.M)
    if description_get_re:
        description = description_get_re.group(1)
    else:
        description = ""
    if api.DefineGroupStore().add_new_goods(group_id, displayname, price, buylimit, description):
        event.reply("上架成功！\n您成功上架商品[%s]！" % displayname)
    else:
        event.reply("诶？似乎已经存在这样商品了~\n不过我还是把[%s]重新上架了一遍哦。" % displayname)
    return

#商品下架
def goods_off_shelves(event, get_re):
    group_id = event.data.group_id
    displayname = get_re.group(1)
    if api.DefineGroupStore().del_old_goods(group_id, displayname):
        event.reply("下架成功！\n您成功下架商品[%s]！" % displayname)
    else:
        event.reply("诶？似乎商店并不存在名为[%s]的商品哦？" % displayname)
    return

#查看商店
def get_page_goods(event, get_re):
    per_page = 8
    group_id = event.data.group_id
    page = int(get_re.group(1)) if get_re.group(1) else 1
    all_goods = api.GetGroupStore(group_id).get_all_goods()
    currency = api.GetGroupDefine(group_id).currency
    goods_amount = len(all_goods)
    all_page = goods_amount//per_page + 1
    if goods_amount == 0:
        event.reply("「欢迎光临群%s兑换店」\n不过似乎你没有上架任何商品哦~" % currency)
        return
    if page <= all_page and page >= 1:
        num = page*per_page - per_page
        goods_str = ["「欢迎光临群%s兑换店」" % currency]
        while num <= min(goods_amount-1, page*per_page):
            this_good = all_goods[num]
            this_str = "%s | %i×%s" % (this_good[0],this_good[1],currency)
            if this_good[2] != -1:
                this_str += " | 剩余%i份" % this_good[2]
            goods_str.append(this_str)
            num += 1
        goods_str.append("当前页数/总页数：%i / %i" % (page, all_page))
        event.reply("\n".join(goods_str))
        return
    else:
        event.reply("群商店总共[ %i ]页，请输入一个合法的页数哦~" % (all_page))
    return

#购买
def group_store_buy(event, get_re):
    displayname = get_re.group(1)
    buytimes = int(get_re.group(2)) if get_re.group(2) else 1
    if buytimes <= 0:
        event.reply("请输入一个合理的数字！")
        return
    group_id = event.data.group_id
    user_id = event.data.user_id
    goods_state = api.GetGroupStore(group_id).get_goods(displayname)
    if not goods_state:
        event.reply("似乎并不存在这件商品哦~\n快用/商店来看看到底有些什么吧！")
        return
    price = goods_state[1]
    buylimit = goods_state[2]
    group_point_obj = api.IndePoint(user_id, group_id)
    old_point = group_point_obj.get_operation()
    currency = api.GetGroupDefine(group_id).currency
    if buylimit >= buytimes or buylimit == -1:
        if old_point >= price * buytimes:
            now_count = api.IndeBagPack(user_id,group_id).quick_update_operation(displayname, "[count]+%i" % buytimes)
            now_point = api.IndePoint(user_id,group_id).set_operation(old_point-price*buytimes)
            if buylimit != -1:
                api.DefineGroupStore().set_limit(group_id, displayname, buylimit-buytimes)
            event.reply("购买成功！\n你当前拥有%s[%i]个\n%s %i→%i" % (displayname,now_count,currency,old_point,now_point))
            return
        else:
            event.reply("似乎你没有这么多的%s呢. . .\n你需要%s[%i]个，而你当前仅有[%i]个" %
            (currency,currency,price*buytimes,old_point))
            return
    else:
        event.reply("商店里货品数量不够啦！\n你最多可以购买[%i]个%s！" % (buylimit, displayname))
        return

#使用道具
def group_bagpack_use(event, get_re):
    group_id = event.data.group_id
    user_id = event.data.user_id
    item = get_re.group(1)
    usetimes = int(get_re.group(2)) if get_re.group(2) else 1
    item_count = api.IndeBagPack(user_id, group_id).quick_update_operation(item, "[count]-%i"%usetimes)
    if not item_count:
        event.reply("似乎你得背包中并没有这么多的[%s]呢~" % item)
    else:
        event.reply("成功使用[%s]×%i！\n当前剩余[%s]×%i" % (item, usetimes, item, item_count))
    return

#获取背包中物品
def group_bagpack_getall(event, get_re):
    group_id = event.data.group_id
    user_id = event.data.user_id
    page = int(get_re.group(1)) if get_re.group(1) else 1
    per_page = 8
    all_items = api.IndeBagPack(user_id, group_id).get_all_item()
    item_len = len(all_items)
    all_page = item_len//per_page + 1
    if not all_items:
        event.reply("你的背包内空空如也！不要再看啦！")
        return
    else:
        if page <= all_page and page >= 1:
            num = page*per_page - per_page
            reply_list = ["背包内容："]
            while num <= min(item_len-1, page*page):
                this_item = all_items[num]
                item_name = this_item[0]
                item_count = this_item[1]
                reply_list.append("%s × %i" % (item_name, item_count))
                num += 1
            reply_list.append("当前页数/总页数：%i / %i" % (page, all_page))
            event.reply("\n".join(reply_list))
        else:
            event.reply("请输入一个合法的页数！")   
    return

#获取所有扭蛋池
def get_all_gashpool(event):
    group_id = event.data.group_id
    pool_list = api.Gashapon(group_id).get_pool_list()
    if not pool_list:
        event.reply("本群似乎还没有设置扭蛋机哦~\n快使用 /设扭蛋机榴歌池[价格20] 来设置一个扭蛋机吧！")
    else:
        msg_list = ["本群扭蛋池如下："]
        for pool in pool_list:
            pool_name = pool[0]
            pool_type = "变化" if pool[1]==1 else "固定"
            pool_token = pool[2]
            pool_price = pool[3]
            if pool_token == "积分":
                pool_token = api.GetGroupDefine(group_id).currency
            msg_list.append("%s %s %i×%s" % (pool_name,pool_type,pool_token,pool_price))
        event.reply("\n".join(msg_list))
    return

#添加新的扭蛋池
def set_gashpool(event, get_re):
    group_id = event.data.group_id
    pool_name = get_re(1)
    main_content = get_re.group(2)
    type_get_re = re.search("\[类型(可变|固定)]", main_content, flags=re.I|re.M)
    if type_get_re:
        if "卡" in type_get_re.group(1):
            pool_type = 1
        else:
            pool_type = 0
    else:
        pool_type = 0
    price_get_re = re.search("\[价格?(\d+)\]", main_content, flags=re.I|re.M)
    if price_get_re:
        pool_price = price_get_re.group(1)
    else:
        event.reply("请记得设置单价哦~\n在参数后带 [价格20] 就可以设置价格为20了哦~")
        return
    token_get_re = re.search("\[货?币([^\]]+)\]", main_content, flags=re.I|re.M)
    if token_get_re:
        pool_token = token_get_re.group(1)
    else:
        pool_token = "积分"
    gashapon_obj = api.Gashapon(group_id)
    if not gashapon_obj.get_pool_pro(pool_name):
        msg_list = ["覆盖原有扭蛋池%s" % pool_name]
    else:
        msg_list = ["新增扭蛋池%s" % pool_name]
    gashapon_obj.add_pool(pool_name, pool_type, pool_token, pool_price)
    str_type = "可变" if pool_type==0 else "固定"
    msg_list.append("类型：%s\n代币：%s\n单价：%i" % (str_type,pool_token,pool_price))
    event.reply("\n".join(msg_list))
    return

#查扭蛋池内容
def get_pool_all_item(event, get_re):
    return