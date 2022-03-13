import json
import requests
from json import dumps
import websockets
import asyncio


def deal_message(msg):
    msg_get = json.loads(msg)
# TO BE DONE
#    if msg_get['code'] ==
    if 'contacts' in msg_get:
        print('联系人如下所示:')
        for contact in msg_get['contacts']:
            print(contact)
    elif 'messages' in msg_get:
        print('消息如下所示:')
        for message in msg_get['messages']:
            print(message)


async def response_message():
    async with websockets.connect('') as ws:
        while True:
            cmd = input('input your command:')
            body = {}
            for elem in ['sort', 'key', 'num', '_CID', 'lastMsg_MID', 'status', 'message']:
                print('input {}:'.format(elem))
                body[elem] = input()
            data_send = {'cmd': cmd, 'body': body}
            await ws.send(data_send)
            message = await ws.recv()
            deal_message(message)


url_connect = ''
play_load = {'username': '', 'password': ''}
headers = {}
r = requests.post(url_connect, data=dumps(play_load), headers=headers)
print('connecting to {}'.format(url_connect))
if r.status_code != 200:
    print('登录失败，原因：{}'.format(r.reason))
    exit()
asyncio.get_event_loop().run_until_complete(response_message())
