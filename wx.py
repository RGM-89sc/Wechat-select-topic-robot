# -*- coding: utf-8 -*-
import itchat
import time
import datetime
import re
import os

topic = 20  # 题目总数
quota = 5  # 每题名额上限
count = [0 for num in range(topic)]  # 题目名额计数
remarkname_list = {}  # 参与选题者名单


# 获取好友列表 RemarkName为备注名，NickName为对方昵称
def get_friends():
    for i in itchat.get_friends():
        remarkname_list.setdefault(i["RemarkName"], 0)
    print("[console]：成功获取好友列表")


# 重启后读取文件数据
def read():
    for i in range(topic):
        try:
            file = open("E:/选题名单/第" + str(i) + "题.txt")
        except FileNotFoundError:
            continue
        for line in file:
            if line[:-1] != "\n":
                remarkname_list[line[:-1]] = 1
                count[i] += 1
    print("[console]: 名单文件读取完毕")


# 统计结果
def match_return(sub, RemarkName):
    count[sub] += 1
    if count[sub] <= quota:
        # 新建目录
        try:
            os.mkdir("E:/选题名单")
        except FileExistsError:
            pass
        # 读写方式打开文件，如果文件存在，文件指针会放在文件结尾，文件打开时是追加模式，如果文件不存在，创建新文件
        file = open("E:/选题名单/第" + str(sub) + "题.txt", "a+")
        file.write(RemarkName + "\n")
        file.close()
        itchat.send(RemarkName + ": 第" + str(sub) + "题", "filehelper")
        return "你是第 " + str(count[sub]) + " 位报第" + str(sub) + "题"
    remarkname_list[RemarkName] -= 1
    count[sub] -= 1
    return "人数已满，请选其他题目，排名: " + str(count[sub] + 1) + "\n目前名额未满的题目有：" + check_topic()


# 检索剩余可选题目
def check_topic():
    f = ""
    n = 0
    while n < topic:
        if count[n] < quota:
            f += str(n + 1) + "  "
        n += 1
    return f


# 把名单转发到群
def send_to_chatroom(num):
    file = open("E:/选题名单/第" + num + "题.txt")
    time.sleep(1)
    itchat.send("第" + num + "题:\n" + file.read(), "@@380b4e4c709271d43e16f003815f477afe1fd27d8d83148275d807b7766caa5a")


########################################################################################################################


# 读取文件补全名单
read()

# 入口
while 1:
    itchat.configured_reply()

    @itchat.msg_register(itchat.content.TEXT)  # 文字信息注册
    # 消息回复
    def text_reply(msg):
        # 获取当前本机系统的时间（月+日+时+分+秒+毫秒）
        localtime = time.strftime("Date: %Y-%m-%d\nTime: %H:%M:%S.", time.localtime(time.time()))\
                    + str(datetime.datetime.now().microsecond)
        # 对方发送的文本段
        text = msg["Text"]

        if not remarkname_list:
            get_friends()

        # 获取当前信息发送者的信息
        RemarkName = msg["User"]["RemarkName"]

        print("[" + RemarkName + "]: " + text)  # 在控制台打印对方发送的文本段

        # 选题
        match = re.match(r"(?:^#.*第?([1-9][0-9])题?.*)|(?:^#.*第?([1-9])题?.*)", text, re.M)
        if match:
            try:
                sub = int(match.group(1))
            except TypeError:
                sub = int(match.group(2))

            if sub > topic:
                time.sleep(1)
                return "该题号不在可选范围内"

            remarkname_list[RemarkName] += 1

            if remarkname_list[RemarkName] > 1:
                time.sleep(1)
                return "你已经选过题了"
            time.sleep(1)
            return match_return(sub, RemarkName) + "\n" + localtime

        # 查看名额未满的题目
        if re.match(r"[还剩].*题", text, re.M):
            time.sleep(1)
            return "目前名额未满的题目有：" + check_topic()

        # 活性测试
        if re.match(r"^-test$", text, re.I):
            time.sleep(1)
            return "正常运行中"

        # 把名单转发到群
        m = re.match(r"^-stc([1-9])|-stc([1-9][0-9])$", text, re.I)
        if m:
            if m.group(1):
                num = m.group(1)
            else:
                num = m.group(2)
            send_to_chatroom(num)


    itchat.auto_login(hotReload=True)
    itchat.run()
    time.sleep(.2)
