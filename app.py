from os import environ
from typing import NoReturn, Optional
import logging
import requests
import json
import argparse
import time
import re

from configobj import ConfigObj

from modules import  pushplus, tieba, fuliba, glados

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

    def run(self) -> dict:
        results = []
        time.sleep(3)
        if self.config['glados_cookie']:
            results.append(glados.init(self.config))
        time.sleep(3)
        if self.config['fuliba_cookie']:
            results.append(fuliba.init(self.config))
        time.sleep(3)
        if self.config['tieba_bduss']:
            results.append(tieba.init(self.config))
        return results

"""
从环境变量获取配置
:return: 配置字典, 配置缺失返回 None
"""
def get_config_from_env() -> Optional[dict]:
    try:
        return {
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
