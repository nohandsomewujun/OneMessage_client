import asyncio
import websockets
from time import sleep
from json import dumps

d = {
    "type": "response",
    "body": {
        "code": 0,
        "contacts": ['alen', 'miki', 'lucy']
    }
}
dd = {
    "type": "push",
    "body": {
        "event": 'StatusChange',
        "_CID": 232
    }
}


async def echo(websocket):
    async for message in websocket:
        await websocket.send(dumps(d))
        sleep(3)
        for i in range(3):
            sleep(3)
            await websocket.send(dumps(dd))


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever


asyncio.run(main())
