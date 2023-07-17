from os import environ
from typing import NoReturn, Optional
import logging
import json
import argparse
import time

from configobj import ConfigObj
import requests

from modules import  pushplus, tieba

"""
签到主体
:param config: 配置文件, ConfigObj 对象或字典
"""
class SignIn:
    def __init__(self, config: ConfigObj | dict):
        self.config = config

    # 隐藏 token
    def __hide_token(self, token) -> str:
        try:
            return token[:4] + '*' * len(token[4:-4]) + token[-4:]
        except IndexError:
            return token

    # 福利吧
    def fuliba(self) -> dict:
        try:
            s = requests.session()
            temp_addr = "https://www.wnflb99.com/"
            if s.get(temp_addr).status_code == 200:
                flb_url = "www.wnflb99.com"
            else:
                # 福利吧导航
                pub_page = "https://fuliba123.net/"
                ret = requests.get(pub_page)
                ret.encoding = "utf-8"
                seachTxt = re.search(r'menu-item-50"><a (.*?)</a>', ret.text)
                if seachTxt:
                    bbs_addr = re.findall(r'href="(.*?)".*?福利吧论坛.*?</a>', seachTxt.group())
                    flb_url = bbs_addr[0]
            headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept - Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'cache-control': 'max-age=0',
                    'Host': flb_url,
                    'Upgrade-Insecure-Requests': '1',
                    'Cookie': self.config['fuliba_cookie'],
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62'}

            # 访问Pc主页
            login_url = 'https://' + flb_url + '/forum.php?mobile=no'
            user_info = s.get(login_url, headers=headers).text
            user_name = re.search(r'title="访问我的空间">(.*?)</a>', user_info)
            username = self.config['fuliba_username']
            if user_name:
                print("登录用户名为：" + user_name.group(1))
                print("环境用户名为：" + username)
            else:
                print("未获取到用户名")
            if user_name is None or (user_name.group(1) != username):
                raise Exception("【福利吧】cookie失效???????")

            # 获取签到链接,并签到
            qiandao_url = re.search(r'}function fx_checkin(.*?);', user_info).group(1)
            qiandao_url = qiandao_url[47:-2]
            # 签到
            s.get('https://' + flb_url + '/' + qiandao_url, headers=headers).text

            # 获取积分
            current_money = re.search(r'<a.*? id="extcreditmenu".*?>(.*?)</a>', user_info).group(1)
            sing_day = re.search(r'<div class="tip_c">(.*?)</div>', user_info).group(1)
            log_info = "{}当前{}".format(sing_day, current_money)
            print(log_info)
            return {
                'content': '福利吧签到：签到成功，' + username + '，' + log_info
            }

        except Exception as e:
            errMsg = "福利吧签到：签到失败，失败原因:"+str(e)
            print(errMsg)
            return {
                'content': errMsg
            }

    # glados机场
    def glados(self) -> dict:
        try:
            sendContent = ''
            origin = "https://glados.rocks"
            url = origin + "/api/user/checkin"
            url2 = origin + "/api/user/status"
            payload = {'token': 'glados.network'}
            headers = {
                'cookie': self.config['glados_cookie'],
                'referer': origin + '/console/checkin',
                'origin': origin,
                'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
            }
            headers2 = headers | {'content-type': 'application/json;charset=UTF-8'}
            checkin = requests.post(url, headers=headers2, data=json.dumps(payload))
            state = requests.get(url2, headers=headers)
            time = state.json()['data']['leftDays']
            time = time.split('.')[0]
            email = state.json()['data']['email']
            if 'message' in checkin.text:
                mess = checkin.json()['message']
                print(email+'----结果--'+mess+'----剩余('+time+')天')
                sendContent += email+'----'+mess+'----剩余('+time+')天\n'
            else:
                print('cookie已失效')
                sendContent = email + '，cookie已失效'
            return {
                'content': 'glados机场签到：签到成功，' + sendContent
            }
        except Exception as e:
            errMsg = "glados机场签到：签到失败，失败原因:"+str(e)
            print(errMsg)
            return {
                'content': errMsg
            }

    # 值得买
    def zdm(self) -> dict:
        try:
            # 状态地址
            current_url = 'https://zhiyou.smzdm.com/user/info/jsonp_get_current'
            # 签到地址
            checkin_url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
            headers = {
                'Referer': 'https://www.smzdm.com/',
                'Host': 'zhiyou.smzdm.com',
                'Cookie': self.config['zdm_cookie'],
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
            }
            data = {}
            sendContent = ''
            res = requests.get(current_url, headers=headers)
            if res.status_code == 200:
                data = json.loads(res.text)
                print(data)
                if data['checkin']['has_checkin']:
                    sendContent = '%s ：%s 你目前积分：%s，经验值：%s，金币：%s，碎银子：%s，威望：%s，等级：%s，已经签到：%s天' % (
                        data['sys_date'], data['nickname'], data['point'], data['exp'], data['gold'], data['silver'], data['prestige'], data['level'], data['checkin']['daily_checkin_num'])
                    print(sendContent)
                else:
                    checkin = req(checkin_url)['data']
                    sendContent = '%s 目前积分：%s，增加积分：%s，经验值：%s，金币：%s，威望：%s，等级：%s' % (
                        data['nickname'], checkin['point'], checkin['add_point'], checkin['exp'], checkin['gold'], checkin['prestige'], checkin['rank'])
                    print(sendContent)
            return {
                'content': '值得买签到：签到成功，' + sendContent
            }
        except Exception as e:
            errMsg = "值得买签到：签到失败，失败原因:"+str(e)
            print(errMsg)
            return {
                'content': errMsg
            }

    def run(self) -> dict:
        results = []
        time.sleep(3)
        if self.config['tieba_bduss']:
            results.append(tieba.init(self.config['tieba_bduss']))
        time.sleep(3)
        if self.config['fuliba_cookie']:
            results.append(self.fuliba())
        time.sleep(3)
        if self.config['glados_cookie']:
            results.append(self.glados())
        time.sleep(3)
        if self.config['zdm_cookie']:
            results.append(self.zdm())
        return results

"""
从环境变量获取配置
:return: 配置字典, 配置缺失返回 None
"""
def get_config_from_env() -> Optional[dict]:
    try:
        return {
            'zdm_cookie': environ['ZDM_COOKIE'],
            'tieba_bduss': environ['TIEBA_BDUSS'],
            'glados_cookie': environ['GLADOS_COOKIE'],
            'fuliba_cookie': environ['FULIBA_COOKIE'],
            'fuliba_username': environ['FULIBA_USERNAME'],
            'pushplus_token': environ['PUSHPLUS_TOKEN'],
            'pushplus_topic': environ['PUSHPLUS_TOPIC'],
        }
    except KeyError as e:
        logging.error(f'环境变量 {e} 缺失.')
        return None

"""
获取命令行参数
:return: 命令行参数
"""
def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='自动签到')

    parser.add_argument('-a', '--action', help='由 GitHub Actions 调用', action='store_true', default=False)
    parser.add_argument('-d', '--debug', help='调试模式, 会输出更多调试数据', action='store_true', default=False)

    return parser.parse_args()

# 推送
def push(config: ConfigObj | dict, content: str, content_html: str, title: Optional[str] = None) -> NoReturn:
    pushplus.push(config, content, content_html, title)

# 日志
def init_logger(debug: Optional[bool] = False) -> NoReturn:
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    log_format = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s')

    # Console
    ch = logging.StreamHandler()
    log.setLevel(logging.DEBUG if debug else logging.INFO)
    ch.setFormatter(log_format)
    log.addHandler(ch)

    # Log file
    log_name = 'auto_signin.log'
    fh = logging.FileHandler(log_name, mode='a', encoding='utf-8')
    log.setLevel(logging.DEBUG if debug else logging.INFO)
    fh.setFormatter(log_format)
    log.addHandler(fh)

# 初始化
def main():
    environ['NO_PROXY'] = '*'  # 禁止代理

    args = get_args()
    init_logger(args.debug)  # 初始化日志系统

    # 获取配置
    config = get_config_from_env()
    if not config:
        logging.error('获取配置失败.')
        raise ValueError('获取配置失败.')

    # 执行签到程序
    results = SignIn(config).run()

    # 合并推送
    text = '\n\n'.join([i['content'] for i in results])
    logging.info('refresh tokens 更新成功.')
    push(config, text, '', '签到日志')

if __name__ == '__main__':
    main()
