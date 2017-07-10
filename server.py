# -*- coding: utf-8 -*-

from uvitools.routing import Route, Router
from uvitools.routing import ChannelSwitch
from uvitools.broadcast import BroadcastMiddleware


async def channel_publish(message,channels):

    channel = message['args'].get('channel')

    body = await channels['body'].receive()

    print(body)

    if not channel is None:
        await channels['groups'].send({
            'group': channel,
            'send': {'text': body['content'].decode("utf-8")}
            })

    await channels['reply'].send({
            'status': 200,
            'headers': [
                    [b'content-type', b'text/html'],
                ],
            'content':b'ok'
        })




async def  channel_connect(message,channels):

    print('channel_connect')
    print('channels ', channels)
    print('app clients', app.clients)

    channel = message['args'].get('channel')

    if not channel is None:
        await channels['groups'].send({
            'group': channel,
            'add': channels['reply'].name
        })


async def  channel_disconnect(message,channels):

    print('channel_disconnect')
    print('channles ', channels)
    print('app clients', app.clients)

    channel = message['args'].get('channel')

    if not channel is None:
        await channels['groups'].send({
            'group': channel,
            'discard': channels['reply'].name
            })


async def  channel_receive(message,channels):

    print('channel_receive')
    print('channels ', channles)
    print('app clients ', app.clients)
    print('message ', message)

    # todo
    # maybe wo need proxy this to http server


app = ChannelSwitch({
    'http.*':
        Router([
            Route('/publish/<channel>', channel_publish, methods=['POST']),
        ]),
    'websocket.*':
        Router([
            Route('/subscribe/<channel>',
                ChannelSwitch({
                    'websocket.connect': channel_connect,
                    'websocket.disconnect': channel_disconnect,
                    'websocket.receive': channel_receive
                    }),
                name='websocket'
                )
            ])

    })


app = BroadcastMiddleware(app, 'localhost', 6379)



