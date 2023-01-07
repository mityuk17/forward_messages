import asyncio

from pyrogram import Client
import os
api_id = 9411854
api_hash = '499c76606cefdeadd4b1ece84a5a9932'
app = Client('my_account', api_id=api_id, api_hash=api_hash)

def get_messages():
    if not os.path.exists('messages_ids.txt'):
        print('Не найден файл messages_ids.txt')
        return False
    with open('messages_ids.txt','r',encoding='utf8') as file:
        messages = file.readlines()
    for i in range(len(messages)):
        post_number = messages[i].split('/')[-1]
        channel_link = messages[i].split('/')[1]
        messages[i] =  tuple([channel_link,int(post_number)])
    return messages

def get_Xchannels():
    if not os.path.exists('Xchannels_ids.txt'):
        print('Не найден файл Xchannels_ids.txt')
        return False
    with open('Xchannels_ids.txt', 'r', encoding='utf8') as file:
        channel_ids = file.readlines()
    for i in range(len(channel_ids)):
        channel_ids[i] = [channel_ids[i].rstrip().split('/')[-1], 0]
    return channel_ids


async def get_message(message_info):
    channel_messages = app.get_chat_history(message_info[0])
    total_msg = await app.get_chat_history_count(message_info[0])
    print(total_msg)
    target = total_msg - message_info[1] + 1
    i = 0
    async for message_i in channel_messages:
        print(message_i)
        i += 1
        if i == target:
            message = message_i
            return message
async def main():
    await app.start()
    messages_for_forwarding = get_messages()
    channels_to_forward = get_Xchannels()
    if not(messages_for_forwarding) or not(channels_to_forward):
        print('Ошибка')
        return False
    for message_i in messages_for_forwarding:
        message = await get_message(message_i)
        await app.forward_messages(channels_to_forward[-1][0],from_chat_id=message_i[0], message_ids=message.id)
        if channels_to_forward[-1][1] ==17:
            channels_to_forward.pop()
asyncio.run(main())