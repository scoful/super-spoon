"""
faker engine自动签到脚本
by scoful
"""

'''
cron: 2 23 * * * fakerengine_auto_sign_bot.py
new Env('faker engine自动签到');
'''

import datetime
import json
import os
import sys

import httpx

"""
http headers
"""
DEFAULT_HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'connection': 'keep-alive',
    'host': 'www.fakerengine.com',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'referer': 'https://www.fakerengine.com/gold/credit',
    'origin': 'https://www.fakerengine.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}

# 签到用的url
LOG_IN_URL = 'https://www.fakerengine.com/wp-json/jwt-auth/v1/token'
SIGN_URL = 'https://www.fakerengine.com/wp-json/b2/v1/userMission'

KEY_OF_INFO = "FAKERENGINE_INFO"


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

    def logIn(self, username, password):
        data = {'username': username, 'password': password}
        msg = self.client.post(url=LOG_IN_URL, data=data)
        data = json.loads(msg.text)
        return data['token']

    def checkin(self):
        """
        签到函数
        """
        msg = self.client.post(SIGN_URL)
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
    info = os.environ[KEY_OF_INFO]
    infoList = info.split("|")
    username = infoList[0]
    password = infoList[1]
    load_send()
    token = bot.logIn(username, password)
    bot.load_cookie_str(token)
    result = bot.checkin()
    logout(result)
    credit = 0
    try:
        credit = result["credit"]
    except Exception as e:
        credit = int(result)
    if send:
        send("faker engine自动签到，获得 : " + str(credit) + " 分", "good job！")
    logout("签到结束")
