
"""Hello websocket server."""

import aio_pika
import asyncio
import json

import aiohttp
from aiohttp import web
import click


loop = asyncio.get_event_loop()


registered_connection = {}
pub_channel = None


async def init_queue():
    connection = await aio_pika.connect_robust(
        'amqp://guest:guest@127.0.0.1/', loop=loop)

    channel = await connection.channel()

    queue_name = 'hello'
    queue = await channel.declare_queue(queue_name, auto_delete=False)

    return queue


async def get_channel(*args):
    global pub_channel

    if pub_channel is not None:
        return pub_channel

    connection = await aio_pika.connect_robust(
        'amqp://guest:guest@127.0.0.1/', loop=loop)

    print(connection)

    channel = await connection.channel()
    pub_channel = channel

    return channel


async def receive_message(ws, token):

    async for msg in ws:
        msg_type = msg.type

        if msg_type == aiohttp.WSMsgType.TEXT:
            msg_data = msg.data
            if msg_data == 'close':
                await ws.close()

            print('receive message %s from %s.' % (msg_data, token))
        elif msg_type == aiohttp.WSMsgType.ERROR:
            print('error')


async def send_message(*args):

    queue = await init_queue()

    async for message in queue:
        with message.process():
            data = json.loads(message.body)
            token = data['token']
            body = data['body']
            try:
                ws = registered_connection[token]
            except KeyError:
                print('no conenction', token)
                continue
            else:
                await ws.send_str(body)


async def websocket_handler(request):

    token = request.query['token']
    if not token:
        return web.HttpResponse('invalid user')

    old_connection = registered_connection.pop(token, None)
    if old_connection is not None:
        old_connection.close()

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    registered_connection[token] = ws

    await receive_message(ws, token)

    return ws


async def push_message_handler(request):

    token = request.query['token']
    body = request.query['body']

    channel = await get_channel()
    routing_key = 'hello'

    data = json.dumps({'token': token, 'body': body})

    await channel.default_exchange.publish(
        aio_pika.Message(body=data.encode()),
        routing_key=routing_key
    )

    return web.Response(text='ok')


@click.group()
def main():
    pass


@main.command('run', help='start websocket server.')
@click.argument('host', type=str, default='127.0.0.1')
@click.argument('port', type=str, default=8989)
def run(**kwargs):
    host = kwargs['host']
    port = kwargs['port']

    app = web.Application()
    app.add_routes([
        web.get('/ws', websocket_handler),
        web.get('/pub', push_message_handler)
    ])

    app.on_startup.append(get_channel)
    loop.create_task(send_message())

    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
