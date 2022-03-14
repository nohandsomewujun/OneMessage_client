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


async def echo(websocket):
    async for message in websocket:
        await websocket.send(dumps(d))


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever


asyncio.run(main())
