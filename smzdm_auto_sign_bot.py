"""
什么值得买自动签到脚本
by sunflo
借鉴（copy）自lws1122,fork 自:https://gitee.com/lsw1122/smzdm_bot
原地址：https://github.com/sunflo/smzdm_sign_bot
"""
'''
cron: 0 1 * * * smzdm_auto_sign_bot.py
new Env('什么值得买自动签到');
'''

import datetime
import os
import sys

import requests

"""
http headers
"""
DEFAULT_HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'zhiyou.smzdm.com',
    'Referer': 'https://www.smzdm.com/',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
}

# 签到用的url
SIGN_URL = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'

# 环境变量中用于存放cookie的key值
KEY_OF_COOKIE = "SMZDM_COOKIE"


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
            logout(f'Error : {e}')
            return False

    def load_cookie_str(self, cookies):
        """
        起一个什么值得买的，带cookie的session
        cookie 为浏览器复制来的字符串
        :param cookie: 登录过的社区网站 cookie
        """
        self.session.headers['Cookie'] = cookies

    def checkin(self):
        """
        签到函数
        """
        msg = self.session.get(SIGN_URL)
        if self.__json_check(msg):
            return msg.json()
        return msg.content


def logout(self):
    print("[{0}]: {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self))
    sys.stdout.flush()


def load_send() -> None:
    print("加载推送功能中...")
    global send
    send = None
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    if os.path.exists(cur_path + "/notify.py"):
        try:
            from notify import send
        except Exception:
            send = None
            print(f"❌加载通知服务失败!!!\n{traceback.format_exc()}")


if __name__ == '__main__':
    bot = SignBot()
    cookies = os.environ[KEY_OF_COOKIE]
    cookieList = cookies.split("&")
    logout("检测到{}个cookie记录\n开始签到".format(len(cookieList)))
    index = 0
    load_send()
    for c in cookieList:
        bot.load_cookie_str(c)
        result = bot.checkin()
        msg = "\n⭐⭐⭐签到成功{1}天⭐⭐⭐\n🏅🏅🏅金币[{2}]\n🏅🏅🏅积分[{3}]\n🏅🏅🏅经验[{4}],\n🏅🏅🏅等级[{5}]\n🏅🏅补签卡[{6}]".format(
            index,
            result['data']["checkin_num"],
            result['data']["gold"],
            result['data']["point"],
            result['data']["exp"],
            result['data']["rank"],
            result['data']["cards"])
        logout(msg)
        if send:
            send("什么值得买自动签到", msg)
        index += 1
    logout("签到结束")
