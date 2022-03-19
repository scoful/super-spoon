"""
科技玩家自动签到脚本
by scoful
"""
'''
cron: 2 */5 * * * kejiwanjia_auto_sign_bot.py
new Env('科技玩家自动签到');
'''

import datetime
import os
import sys

import httpx

DEFAULT_HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'connection': 'keep-alive',
    'content-Length': '0',
    'dnt': '1',
    'host': 'www.kejiwanjia.com',
    'origin': 'https://www.kejiwanjia.com',
    'pragma': 'no-cache',
    'referer': 'https://www.kejiwanjia.com/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}

"""
http headers
"""

# 签到用的url
SIGN_URL = 'https://www.kejiwanjia.com/wp-json/b2/v1/userMission'
GET_USER_INFO_URL = 'https://www.kejiwanjia.com/wp-json/b2/v1/getUserInfo'

# 环境变量中用于存放cookie的key值，多个号用|分隔
KEY_OF_COOKIE = "KEJIWANJIA_COOKIE"


class SignBot(object):
    def __init__(self):
        self.client = httpx.Client(headers=DEFAULT_HEADERS, http2=True)

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
        self.client.headers['authorization'] = 'Bearer ' + cookies
        self.client.headers['cookie'] = 'b2_token=' + cookies

    def checkin(self, cookies):
        """
        签到函数
        """
        msg = self.client.post(SIGN_URL)
        if self.json_check(msg):
            return msg.json()
        return msg.content

    def getUserInfo(self, cookies):
        msg = self.client.post(GET_USER_INFO_URL)
        if msg.status_code == 403:
            return False
        else:
            return True


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
        if bot.getUserInfo(c):
            result = bot.checkin(c)
            logout(result)
            credit = 0
            try:
                credit = result["credit"]
            except Exception as e:
                credit = int(result)
            if send:
                send("科技玩家自动签到，获得 : " + str(credit) + " 分", "good job！")
        else:
            if send:
                send("科技玩家token失效！", "oop!!!")
        index += 1
    logout("签到结束")
