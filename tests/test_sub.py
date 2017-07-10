#!/usr/bin/env python


import asyncio
import websockets


async def sub():
    async with websockets.connect('ws://localhost:8000/subscribe/test') as websocket:
        while True:
            greeting = await websocket.recv()
            print("< {}".format(greeting))



asyncio.get_event_loop().run_until_complete(sub())
