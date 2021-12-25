"""
青云自动签到脚本
by scoful
"""
'''
cron: 0 2 */5 * * ? qingcloud_auto_sign_bot.py
new Env('青云自动签到');
'''

import datetime
import os
import sys

import requests

"""
http headers
"""
DEFAULT_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'points.qingcloud.com',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
}

# 签到用的url
SIGN_URL = 'https://points.qingcloud.com/api/scorecheckin/checkin?'

# 环境变量中用于存放cookie的key值
KEY_OF_COOKIE = "QINGCLOUD_COOKIE"


class SignBot(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = DEFAULT_HEADERS

    def __json_check(self, msg):
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
        self.session.headers['Cookie'] = cookies

    def checkin(self, cookies):
        """
        签到函数
        """
        msg = self.session.get(SIGN_URL + cookies)
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
    bot = SignBot()
    cookies = os.environ[KEY_OF_COOKIE]
    cookieList = cookies.split("&")
    logout("检测到{}个cookie记录\n开始签到".format(len(cookieList)))
    index = 0
    load_send()
    for c in cookieList:
        bot.load_cookie_str(c)
        result = bot.checkin(c)
        logout(result)
        if result["msg"] == "请刷新页面以同步登录状态":
            msg = "Cookie过期了！"
        else:
            msg = "签到成功！"
        logout(msg)
        if send:
            send("青云自动签到:" + msg, msg)
        index += 1
    logout("签到结束")
