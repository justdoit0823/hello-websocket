
"""Hello websocket client."""

import asyncio
import binascii
import os
import random

import aiohttp
import click


async def send_message(ws):

    while True:
        message = binascii.hexlify(os.urandom(32)).decode()
        await ws.send_str(message)

        interval = random.randint(100, 200)
        await asyncio.sleep(interval / 1000)


async def run_client(url):
    print('try to conenct websocket server', url)

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url) as ws:
            loop = asyncio.get_event_loop()
            loop.create_task(send_message(ws))

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == 'close cmd':
                        await ws.close()
                        break
                    else:
                        print('receive message', msg.data)
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break


@click.group()
def main():
    pass


@main.command('run', help='start websocket client.')
@click.argument('token', type=str)
@click.argument('host', type=str, default='127.0.0.1')
@click.argument('port', type=int, default=8989)
def start_client(**kwargs):
    url = 'http://{host}:{port}/ws?token={token}'.format(**kwargs)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_client(url))


if __name__ == '__main__':
    main()
