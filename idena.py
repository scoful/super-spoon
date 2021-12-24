"""
idena检测是否掉线脚本
by scoful
"""
'''
cron: 0 1 * * * idena_check_online_bot.py
new Env('idena检测是否掉线');
'''

import datetime
import os
import sys

import requests

# 检测用的url
CHECK_URL = 'https://api.idena.org/api/onlineidentity/'

# 环境变量中用于存放account的key值
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
    for c in accountList:
        result = bot.checkOnline(c)
        msg = ""
        if result["result"] == None:
            msg = c + " 似乎写错了，检查一下！"
        else:
            if result["result"]["online"] == False:
                msg = c + " 掉线啦！快瞅瞅"
        if send and len(msg) > 0:
            send("idena检测:", msg)
        index += 1
    logout("检测结束")
