#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''player
'''

import os
import sys
import json
import logging
import asyncio

import websockets
import click
import deuces

__author__ = 'ZHUO Qiang'
__date__ = '2017-10-12 10:20:01+0800'
__version__ = '0.1'

DEFAULT_SERVER = 'ws://116.62.203.120'
DEFAULT_SERVER = 'ws://thegame.trendmicro.com.cn'

def enable_debug():
    logger = logging.getLogger('websockets')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())


async def play(server, name):
    async with websockets.connect(server) as s:
        await s.send(json.dumps({
            "eventName": "__join",
            "data": {
                "playerName": name
            }
        }))

        while True:
            r = json.loads(await s.recv())
            action = r['eventName']
            data = r['data']

            if action == "__bet":
                await s.send(json.dumps({
                    "eventName": "__action",
                    "data": {
                        "action": "bet",
                        "playerName": name,
                        "amount": 100
                    }
                }))

            elif action == "__action":
                await s.send(json.dumps({
                    "eventName": "__action",
                    "data": {
                        "action": "call",
                        "playerName": name,
                    }
                }))


@click.command()
@click.version_option(version=__version__)
@click.option('--server', '-s', default=DEFAULT_SERVER, help='server websocket address like "ws://116.62.203.120"')
@click.option('--debug', '-d', is_flag=True, default=False)
@click.argument('name')
def main(server, name, debug):
    '''play texas holdem and WIN!
    '''
    click.echo(f'joining server {server} using player name "{name}" ...')
    if debug:
        enable_debug()
    asyncio.get_event_loop().run_until_complete(play(server, name))


if __name__ == '__main__':
    main()
