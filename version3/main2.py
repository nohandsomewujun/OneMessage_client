import sys
import websocket
import threading
from json import dumps
import requests
from requests import utils
from json import loads
import os
from requests_toolbelt import MultipartEncoder


def deal_message(json_data):
    data = loads(json_data)
    if data['type'] == 'push':
        print('(get push from sever) ===> ' + 'Event:', data['body']['event'] + ' _CID:', data['body']['_CID'])
    elif data['type'] == 'response':
        print('(get response from sever) ===> ')
        if data['body']['code'] != 0:
            print('(something wrong!) ===>' + data['body']['msg'])
        else:
            print('(get response from sever) ===>')
            if 'contacts' in data['body']:
                print('联系人:')
                print(data['body']['contacts'])
            elif 'messages' in data['body']:
                print('消息:')
                print(data['body']['messages'])
            else:
                print('success!')


def on_open(ws):
    print('connect success!')

    def run(*args):
        while True:
            cmd = input()
            body = {}
            for elem in ['sort', 'key', 'num', '_CID', 'lastMsg_MID', 'status', 'message']:
                print('input {}:'.format(elem))
                body[elem] = input()
            data_send = {'cmd': cmd, 'body': body}
            json_data_send = dumps(data_send)
            try:
                ws.send(json_data_send)
            except:
                print('connection is already closed.')
                sys.exit(0)

            print('')
            print('(send) ===> ', json_data_send)
            print('')

    threading.Thread(target=run).start()


def on_error(ws, error):
    print(error)


def on_message(ws, message):
    def run(*args):
        deal_message(message)
        print("Message received...")
        print('')

    threading.Thread(target=run).start()


def on_close(ws, close_status_code, close_msg):
    if close_status_code or close_msg:
        print('close status code:', close_status_code)
        print('close msg:', close_msg)
    try:
        print(">>>>>>CLOSED")
        os._exit(0)
    except:
        pass



url_connect = 'http://192.168.43.219:8080/login'
play_load = {'username': 'huyufan', 'password': 'hu'}
play_load_from_data = MultipartEncoder(play_load)
headers = {'Content-Type': play_load_from_data.content_type}
r = requests.post(url_connect, data=play_load_from_data, headers=headers)
print('connecting to {}'.format(url_connect))
if r.status_code != 200:
    print('登录失败，原因：{}'.format(r.reason))
    exit()
else:
    print('request success!')
cookies_dic = requests.utils.dict_from_cookiejar(r.cookies)
print(cookies_dic)
cookie_str = ''
for key in cookies_dic:
    cookie_str += key + '=' + cookies_dic[key] + ';'
cookie_str = cookie_str.strip(';')
ws_app = websocket.WebSocketApp("ws://192.168.43.219:8080/app",
                                on_open=on_open, on_message=on_message,
                                on_close=on_close, on_error=on_error, cookie=cookie_str)
ws_app.run_forever()
