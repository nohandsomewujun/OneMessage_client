import websocket
import threading
from json import dumps
import requests
from requests import utils

websocket.enableTrace(True)


# TO BE DONE
# def deal_message():



def on_open(ws):
    def run(*args):
        while True:
            cmd = input('input your command:')
            body = {}
            for elem in ['sort', 'key', 'num', '_CID', 'lastMsg_MID', 'status', 'message']:
                print('input {}:'.format(elem))
                body[elem] = input()
            data_send = {'cmd': cmd, 'body': body}
            json_data_send = dumps(data_send)
            ws.send(json_data_send)
            print('(send) ===> ', json_data_send)

    threading.Thread(target=run).start()


def on_message(ws, message):
    def run(*args):
        print('(get) ===> ', message)
        ws.close()
        print("Message received...")

    threading.Thread(target=run).start()


def on_close(ws, close_status_code, close_msg):
    print(">>>>>>CLOSED")


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
wsapp = websocket.WebSocketApp("wss://api.bitfinex.com/ws/1",
                               on_open=on_open, on_message=on_message, on_close=on_close, cookie=cookie_str)
wsapp.run_forever()
