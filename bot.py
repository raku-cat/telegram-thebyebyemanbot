#!/usr/bin/env python3
import asyncio
import aiofiles
try:
    import simplejson as json
except ImportError:
    import json
import sys
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop

with open(sys.path[0] + '/keys.json', 'r') as f:
    key = json.load(f)
bot = telepot.aio.Bot(key['telegram'])


async def on_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    # print(msg)
    # print(content_type)
    from_id = msg['from']['id']
    if content_type == 'new_chat_member':
        # print(msg)
        # print('test')
        new_member_id = msg['new_chat_members'][0]['id']
        # print(new_member_id)
        with open('users.json', 'r') as f:
            users_list = json.loads(f.read())
        if new_member_id not in users_list:
            if from_id == new_member_id:
                users_list.append(new_member_id)
            elif from_id in users_list:
                for bad_boy in [new_member_id, from_id]:
                    await bot.kickChatMember(chat_id, bad_boy)
                users_list.remove(from_id)
            async with aiofiles.open('users.json', 'w') as ul:
                await ul.write(json.dumps(users_list))
        else:
            return
    else:
        try:
            with open('users.json', 'r') as f:
                users_list = json.loads(f.read())
            if from_id in users_list:
                users_list.remove(from_id)
            async with aiofiles.open('users.json', 'w') as ul:
                await ul.write(json.dumps(users_list))
        except ValueError:
            return

    # print(msg)

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot, on_message).run_forever())
print('Started...')
loop.run_forever()
