"""
idena检测是否掉线脚本
by scoful
"""
'''
cron: */1 * * * * idena_check_online_bot.py
new Env('idena检测是否掉线');
'''

import datetime
import datetime as dt
import os
import sys

import requests

# 检测用的url
CHECK_URL = 'https://api.idena.org/api/onlineidentity/'

# 获取epoch信息
EPOCH_URL = 'https://api.idena.io/api/epoch/last'

# 环境变量中用于存放account的key值,多个用&分隔
KEY_OF_ACCOUNT = "IDENA_ACCOUNT"


class CheckBot(object):
    def __init__(self):
        logout("检测开始")

    def checkOnline(self, account):
        msg = requests.get(CHECK_URL + account)
        if self.__json_check(msg):
            return msg.json()
        return msg.content

    def __json_check(self, msg):
        """
        判断是否 json 形式
        """
        try:
            msg.json()
            return True
        except Exception as e:
            return False

    def getEpochInfo(self):
        msg = requests.get(EPOCH_URL)
        if self.__json_check(msg):
            return msg.json()
        return msg.content


def load_send() -> None:
    logout("加载推送功能中...")
    global send
    send = None
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    if os.path.exists(cur_path + "/notify.py"):
        try:
            from notify import send
        except Exception:
            send = None
            logout(f"❌加载通知服务失败!!!\n{traceback.format_exc()}")


def logout(self):
    print("[{0}]: {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self))
    sys.stdout.flush()


if __name__ == '__main__':
    bot = CheckBot()
    accounts = os.environ[KEY_OF_ACCOUNT]
    accountList = accounts.split("&")
    logout("检测到{}个账号记录\n开始".format(len(accountList)))
    index = 0
    load_send()
    epoch = bot.getEpochInfo()
    validationTimeStr = epoch["result"]["validationTime"]
    validationTime = dt.datetime.strptime(validationTimeStr, '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=8)
    for c in accountList:
        result = bot.checkOnline(c)
        msg = ""
        if result["result"] != None:
            if result["result"]["online"] == False:
                msg = "第" + str(index + 1) + "个账号：" + c + " 掉线啦！快瞅瞅\n注意下次考试时间:" + validationTime.strftime("%Y-%m-%d %H:%M:%S")
        if send and len(msg) > 0:
            send("idena检测:", msg)
        index += 1
    logout("检测结束")
