from json import dumps
import requests.utils
import websocket


def on_message(ws, message):
    print('(get) ===> ', message)


def on_error(ws, error):
    print(error)


def deal_message():
    ws = websocket.WebSocketApp("ws://baidu.com/",
                                cookie=cookie_str,
                                on_message=on_message,
                                on_error=on_error)
    cmd = input('input your command:')
    body = {}
    for elem in ['sort', 'key', 'num', '_CID', 'lastMsg_MID', 'status', 'message']:
        print('input {}:'.format(elem))
        body[elem] = input()
    data_send = {'cmd': cmd, 'body': body}
    json_data_send = dumps(data_send)

    ws.send(json_data_send)  # 传输数据
    print(f"(send) ===> {json_data_send}")
    ws.run_forever()


url_connect = 'https://baidu.com/'
play_load = {'username': '$wu_jun', 'password': '$123456789'}
headers = {}
r = requests.post(url_connect, data=dumps(play_load), headers=headers)
print('connecting to {}'.format(url_connect))
if r.status_code != 200:
    print('登录失败，原因：{}'.format(r.reason))
    exit()
cookies_dic = requests.utils.dict_from_cookiejar(r.cookies)
print(cookies_dic)
cookie_str = ''
for key in cookies_dic:
    cookie_str += key + '=' + cookies_dic[key] + ';'
cookie_str = cookie_str.strip(';')
print(cookie_str)
deal_message()
