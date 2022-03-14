"""
faker engine自动签到脚本
by scoful
"""
'''
cron: 2 */5 * * * fakerengine_auto_sign_bot.py
new Env('faker engine自动签到');
'''

import datetime
import os
import random
import sys

import requests

"""
http headers
"""
DEFAULT_HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'www.fakerengine.com',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://www.fakerengine.com/gold/credit',
    'Origin': 'https://www.fakerengine.com',
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
        self.session.headers['User-Agent'] = self.userAgent()

    def checkin(self, cookies):
        """
        签到函数
        """
        msg = self.session.post(SIGN_URL)
        if self.json_check(msg):
            return msg.json()
        return msg.content

    def userAgent(self):
        """
        随机生成一个UA
        :return: jdapp;iPhone;9.4.8;14.3;xxxx;network/wifi;ADID/201EDE7F-5111-49E8-9F0D-CCF9677CD6FE;supportApplePay/0;hasUPPay/0;hasOCPay/0;model/iPhone13,4;addressid/2455696156;supportBestPay/0;appBuild/167629;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1
        """
        if not UserAgent:
            uuid = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 40))
            addressid = ''.join(random.sample('1234567898647', 10))
            iosVer = ''.join(
                random.sample(["14.5.1", "14.4", "14.3", "14.2", "14.1", "14.0.1", "13.7", "13.1.2", "13.1.1"], 1))
            iosV = iosVer.replace('.', '_')
            iPhone = ''.join(random.sample(["8", "9", "10", "11", "12", "13"], 1))
            ADID = ''.join(random.sample('0987654321ABCDEF', 8)) + '-' + ''.join(
                random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(
                random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(
                random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 12))
            return f'jdapp;iPhone;10.0.4;{iosVer};{uuid};network/wifi;ADID/{ADID};supportApplePay/0;hasUPPay/0;hasOCPay/0;model/iPhone{iPhone},1;addressid/{addressid};supportBestPay/0;appBuild/167629;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS {iosV} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1'
        else:
            return UserAgent


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
        if bot.json_check(result):
            credit = int(result["credit"])
            logout(credit)
        else:
            credit = int(result)
        if send:
            send("faker engine自动签到，获得 : " + str(credit) + " 分", "good job！")
        index += 1
    logout("签到结束")
