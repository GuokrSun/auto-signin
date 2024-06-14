import requests
import re

# 福利吧
def init(config) -> dict:
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
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            'cookie': config['fuliba_cookie'],
        }
        # 访问Pc主页
        login_url = 'https://' + flb_url + '/forum.php?mobile=no'
        user_info = s.get(login_url, headers=headers).text
        user_name = re.search(r'title="访问我的空间">(.*?)</a>', user_info)
        username = config['fuliba_username']
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
        print('qiandao_url', qiandao_url)
        # 签到
        user_info = s.get('https://' + flb_url + '/' + qiandao_url, headers=headers).text

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