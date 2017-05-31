# -*- coding:utf-8 -*-
import itchat
import time
import datetime
import re


@itchat.msg_register(itchat.content.TEXT)
# 消息回复
def text_reply(msg):
    print(msg["FromUserName"] + " : " + msg["Text"])  # 在本机控制台打印对方发送的文本段

    # Java大作业选题
    match = re.match(r".*第?(\d|[一二三四五六七八九十])题?.*", msg["Text"], re.M | re.I)
    if match:
        return "yes"

    # 收到红包
    if msg["MsgType"] == 49:
        print("[收到红包，请在手机中查看]")
        return "自动回复：红包收到了，谢谢老板~"

    # 其他信息
    text = str(msg["Text"])  # 对方发送的文本段
    localtime = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(time.time()))  # 获取当前本机系统的时间
    num = time.strftime("%m%d%H%M%S", time.localtime(time.time())) + str(datetime.datetime.now().microsecond)  # 信息编号（月+日+时+分+秒+毫秒）
    return "Your send: " + text + "\nTime: " + localtime + "\nMsgNum: " + num + "\n状态：等待处理\n备注：本自动回复机器人正在开发中~"  # 回复

itchat.auto_login(hotReload=True)
itchat.run()
