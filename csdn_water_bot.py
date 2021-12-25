"""
CSDN水阅读量脚本
by scoful
"""
'''
cron: */10 * * * * ? csdn_water_bot.py
new Env('CSDN水阅读量');
'''

import datetime
import os
import sys

import requests

# 环境变量中用于存放cookie的key值，多个号用|分隔
KEY_OF_COOKIE = "CSDN_ARTICLE_ID"
KEY_OF_ACCOUNT = "CSDN_ACCOUNT"


def logout(self):
    print("[{0}]: {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self))
    sys.stdout.flush()


def water(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    }
    try:
        r = requests.get(url, headers=header,
                         timeout=10)
    except Exception as e:
        logout("failed")
    else:
        logout("successful")
    return None


if __name__ == '__main__':
    cookies = os.environ[KEY_OF_COOKIE]
    account = os.environ[KEY_OF_ACCOUNT]
    cookieList = cookies.split("&")
    logout("检测到{}个文章记录\n开始水".format(len(cookieList)))
    for c in cookieList:
        water("https://blog.csdn.net/" + account + "/article/details/" + c)
    logout("CSDN刷阅读量结束")
