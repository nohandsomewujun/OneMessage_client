from json import dumps
import requests.utils
import websocket
import requests


# ws的各个函数对应的处理

def on_message(ws, message):
    print('(get) ===> ', message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    if close_status_code or close_msg:
        print('close_status_code:' + str(close_status_code))
        print('close_msg' + str(close_msg))


def on_open(ws):
    print('Opened connection!')


def deal_message():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url='',
                                cookie=cookie_str,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    ws.run_forever()
    cmd = input('input your command:')
    body = {}
    for elem in ['sort', 'key', 'num', '_CID', 'lastMsg_MID', 'status', 'message']:
        print('input {}:'.format(elem))
        body[elem] = input()
    data_send = {'cmd': cmd, 'body': body}
    json_data_send = dumps(data_send)

    ws.send(json_data_send)  # 传输数据
    print(f"(send) ===> {json_data_send}")


url_connect = ''
play_load = {'username': '', 'password': ''}
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
