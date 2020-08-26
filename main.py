import asyncio
import os
from typing import Optional, Union
from wechaty import Wechaty, Contact
from wechaty.user import Message, Room
import time
import requests
import traceback
from apscheduler.schedulers.asyncio import AsyncIOScheduler

os.environ['WECHATY_PUPPET']= 'wechaty-puppet-hostie'
os.environ['WECHATY_PUPPET_HOSTIE_TOKEN'] = '...'

def get_time():
    return time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))

async def on_scan(status, qrcode):
    print('status: {}'.format(status))
    print('qrcode: {}'.format(qrcode))
    prompt = 'Scan QR Code to login: {}\nhttps://wechaty.github.io/qrcode/{}'.format(status, qrcode)
    text = 'Wechat scaning...'
    desp = '[{}]: {}'.format(get_time(), prompt)
    requests.get(url.format(text, desp))

async def on_login(user):
    prompt = 'User {} logged in.'.format(user)
    text = 'Wechaty logged in'
    desp = '[{}]: {}'.format(get_time(), prompt)
    requests.get(url.format(text, desp))

async def on_logout(user):
    prompt = 'User {} logged out'.format(user)
    text = 'Wechaty abnormal logout!'
    desp = '[{}]: {}, pls re-login asap.'.format(get_time(), prompt)
    requests.get(url.format(text, desp))

async def on_error(error):
    text = 'Wechaty error!'
    desp = '[{}]: Wechaty error - [{}], pls check.'.format(get_time(), str(error))
    requests.get(url.format(text, desp))

async def on_room_join(room, inviteeList, inviter, timestamp):
    if room.payload.topic:
        conversation: Union[Room, Contact] = room
        for invitee in inviteeList:
            await conversation.ready()
            await conversation.say('欢迎<{}>进群，感谢<{}>的邀请！'.format(invitee.payload.name, inviter.payload.name))
            target_friend = bot.Contact.load('wzhwno1')
            await target_friend.say('<{}>已于<{}>被<{}>邀请进入群聊<{}>！'
                                    .format(invitee.payload.name, timestamp, inviter.payload.name, room.payload.topic))

async def on_room_leave(room, removeeList, remover, timestamp):
    print('room: {}'.format(str(room)))
    print('removeeList: {}'.format(str(removeeList)))
    print('remover: {}'.format(str(remover)))
    print('timestamp: {}'.format(str(timestamp)))
    if room.payload.topic:
        conversation: Union[Room, Contact] = room
        for removee in removeeList:
            await conversation.ready()
            await conversation.say('<{}>已退群，期待下次再见！'.format(removee.payload.name))

async def on_message(msg: Message):
    from_contact = msg.talker()
    text = msg.text()
    room = msg.room()
    conversation: Union[
        Room, Contact] = from_contact if room is None else room
    if text == '#ding':
        await conversation.ready()
        await conversation.say('dong')

async def wechat():
    global bot
    bot = Wechaty()
    bot.on('scan', on_scan)
    bot.on('login', on_login)
    bot.on('message', on_message)
    bot.on('room-join', on_room_join)
    bot.on('room-leave', on_room_leave)
    bot.on('logout', on_logout)
    bot.on('error', on_error)
    await bot.start()

asyncio.run(wechat())
