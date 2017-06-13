# -*- coding:utf-8 -*-
import itchat
import time
import datetime
import re

count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
remarkname_list = {}
nickname_list = {}
num_dict = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}

# 获取好友列表 RemarkName为备注名，NickName为对方昵称
for i in itchat.get_friends():
    remarkname_list.setdefault(i["RemarkName"], 0)
    nickname_list.setdefault(i["NickName"], 0)


@itchat.msg_register(itchat.content.TEXT)
# 消息回复
def text_reply(msg):
    # 信息编号（月+日+时+分+秒+毫秒）
    msg_num = time.strftime("%m%d%H%M%S", time.localtime(time.time())) + str(datetime.datetime.now().microsecond)
    # 获取当前本机系统的时间
    localtime = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(time.time()))
    # 对方发送的文本段
    text = str(msg["Text"])

    NickName = msg["User"]["NickName"]
    RemarkName = msg["User"]["RemarkName"]

    print(RemarkName + " : " + text)  # 在本机控制台打印对方发送的文本段

    # 刷新好友名字信息
    for j in itchat.get_friends():
        remarkname_list.setdefault(j["RemarkName"], 0)
        nickname_list.setdefault(j["NickName"], 0)

    # Java大作业选题
    match_fir = re.match(r"^#.*第?(\d|10|[一二三四五六七八九十])题?.*", msg["Text"], re.M | re.I)
    match_sec = re.match(r"^.*改.*第?(\d|10|[一二三四五六七八九十])题?.*", msg["Text"], re.M | re.I)
    if match_fir:
        nickname_list[NickName] += 1
        remarkname_list[RemarkName] += 1

        if nickname_list[NickName] > 1 or remarkname_list[RemarkName] > 1:
            return "你已经选过题了"
        return "Your send: " + text + "\nTime: " + localtime + "\nMsgNum: " + msg_num + "\n状态: " + str(match_return(match_fir))

    if (nickname_list[NickName] > 0 or remarkname_list[RemarkName]) and match_sec:
        if count[int(match_sec.group(1))] > 0:
            try:
                count[int(match_sec.group(1))] -= 1
            except BaseException:
                count[num_dict[match.group(1)]] -= 1

        if nickname_list[NickName] > 2 or remarkname_list[RemarkName] > 2:
            return "你已经改过题了"

        nickname_list[NickName] += 1
        remarkname_list[RemarkName] += 1

        return "Your send: " + text + "\nTime: " + localtime + "\nMsgNum: " + msg_num + "\n状态: " + str(match_return(match_sec))


def match_return(match):
    try:
        sub = int(match.group(1))
    except BaseException:
        sub = num_dict[match.group(1)]
    count[sub] += 1
    if count[sub] <= 1:
        return "你是第 " + str(count[sub]) + " 位报第" + str(sub) + "题"
    return "人数已满，请选其他题目，排名: " + str(count[sub])

itchat.auto_login(hotReload=True)
itchat.run()
