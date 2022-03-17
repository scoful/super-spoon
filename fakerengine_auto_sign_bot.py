"""
faker engine自动签到脚本
by scoful
"""
'''
cron: 2 */5 * * * fakerengine_auto_sign_bot.py
new Env('faker engine自动签到');
'''

import datetime
import json
import os
import sys

import requests

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
}

# 签到用的url
SIGN_URL = 'https://www.fakerengine.com/wp-json/b2/v1/userMission'
UserAgent = ''

# 环境变量中用于存放cookie的key值，多个号用|分隔
KEY_OF_COOKIE = "FAKERENGINE_COOKIE"


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
        self.session.headers['authorization'] = cookies
        self.session.headers['cookie'] = 'b2_token=' + cookies

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
            send("faker engine自动签到，获得 : " + str(credit) + " 分", "good job！")
        index += 1
    logout("签到结束")
