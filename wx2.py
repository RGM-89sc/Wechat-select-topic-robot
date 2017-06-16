# -*- coding:utf-8 -*-
import itchat
import time
import datetime
import re


@itchat.msg_register(itchat.content.TEXT)
# 消息回复
def text_reply(msg):
    # 信息编号（月+日+时+分+秒+毫秒）
    msg_num = time.strftime("%m%d%H%M%S", time.localtime(time.time())) + str(datetime.datetime.now().microsecond)
    # 获取当前本机系统的时间
    localtime = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(time.time()))
    # 对方发送的文本段
    text = str(msg["Text"])

    remarkname = msg["User"]["RemarkName"]

    print(remarkname + " : " + text)  # 在本机控制台打印对方发送的文本段

    # Java大作业选题
    match = re.match(r"^#.*",text, re.M | re.I)
    if match:
        return "Your send: " + text + "\nTime: " + localtime + "\nMsgNum: " + msg_num + "\n状态: 请等待处理"

    # 其他信息
    return "Your send: " + text + "\nTime: " + localtime + "\nMsgNum: " + msg_num + "\n备注: 机器人存活"

itchat.auto_login(hotReload=True)
itchat.run()
