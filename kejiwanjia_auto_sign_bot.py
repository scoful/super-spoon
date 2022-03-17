"""
科技玩家自动签到脚本
by scoful
"""
'''
cron: 2 */5 * * * kejiwanjia_auto_sign_bot.py
new Env('科技玩家自动签到');
'''

import datetime
import json

DEFAULT_HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '0',
    'DNT': '1',
    'Host': 'www.kejiwanjia.com',
    'Origin': 'https://www.kejiwanjia.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.kejiwanjia.com/gold/credit',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}
import os
import sys

import requests

"""
http headers
"""

# 签到用的url
SIGN_URL = 'https://www.kejiwanjia.com/wp-json/b2/v1/userMission'
UserAgent = ''

# 环境变量中用于存放cookie的key值，多个号用|分隔
KEY_OF_COOKIE = "KEJIWANJIA_COOKIE"


class SignBot(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = DEFAULT_HEADERS

    def json_check(self, msg):
        """
        判断是否 json 形式
        """
        try:
            msg.json()
            return True
        except Exception as e:
            return False

    def load_cookie_str(self, cookies):
        """
        起一个带cookie的session
        """
        self.session.headers['Authorization'] = cookies
        self.session.headers['Cookie'] = 'b2_token=' + cookies

    def checkin(self, cookies):
        """
        签到函数
        """
        msg = self.session.post(SIGN_URL)
        if self.json_check(msg):
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
    bot = SignBot()
    cookies = os.environ[KEY_OF_COOKIE]
    cookieList = cookies.split("|")
    logout("检测到{}个cookie记录\n开始签到".format(len(cookieList)))
    index = 0
    load_send()
    for c in cookieList:
        bot.load_cookie_str(c)
        result = bot.checkin(c)
        logout(result)
        credit = 0
        if result.isdigit():
            credit = int(result)
        else:
            js = json.loads(json.dumps(eval(bytes.decode(result))))
            if bot.json_check(js):
                credit = js["credit"]
            else:
                credit = int(result)
        if send:
            send("科技玩家自动签到，获得 : " + str(credit) + " 分", "good job！")
        index += 1
    logout("签到结束")
