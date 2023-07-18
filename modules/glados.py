import requests
import json

# glados机场
def init(config) -> dict:
    try:
        sendContent = ''
        origin = "https://glados.rocks"
        url = origin + "/api/user/checkin"
        url2 = origin + "/api/user/status"
        payload = {'token': 'glados.network'}
        headers = {
            'cookie': config['glados_cookie'],
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