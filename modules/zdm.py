# -*- coding:utf-8 -*-
import requests
import json

def req(url, headers):
    url = url
    res = requests.get(url, headers)
    if res.status_code == 200:
        data = json.loads(res.text)
        return data

# 值得买
def init(cookies):
    try:
        # 状态地址
        current_url = 'https://zhiyou.smzdm.com/user/info/jsonp_get_current'
        # 签到地址
        checkin_url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        headers = {
            'Referer': 'https://www.smzdm.com/',
            'Host': 'zhiyou.smzdm.com',
            'Cookie': cookies,
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
        data = {}
        sendContent = ''
        res = requests.get(current_url, headers=headers)
        if res.status_code == 200:
            data = json.loads(res.text)
            if data['checkin']['has_checkin']:
                sendContent = '%s ：%s 你目前积分：%s，经验值：%s，金币：%s，碎银子：%s，威望：%s，等级：%s，已经签到：%s天' % (
                    data['sys_date'], data['nickname'], data['point'], data['exp'], data['gold'], data['silver'], data['prestige'], data['level'], data['checkin']['daily_checkin_num'])
                print(sendContent)
            else:
                checkin = req(checkin_url, headers)['data']
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
