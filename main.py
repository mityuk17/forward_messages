import asyncio
from pyrogram import Client, errors
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
        msg = messages[i].replace('https://', '')
        post_number = msg.split('/')[-1]
        channel_link = msg.split('/')[1]
        messages[i] = tuple([channel_link,int(post_number)])
    return messages

def get_Xchannels():
    if not os.path.exists('Xchannels_ids.txt'):
        print('Не найден файл Xchannels_ids.txt')
        return False
    with open('Xchannels_ids.txt', 'r', encoding='utf8') as file:
        channel_ids = file.readlines()
    for i in range(len(channel_ids)):
        channel_ids[i] = channel_ids[i].replace('https://', '')
        channel_ids[i] = [channel_ids[i].rstrip().split('/')[-1], 0]
    return channel_ids

async def main():
    await app.start()
    messages_for_forwarding = get_messages()
    channels_to_forward = get_Xchannels()
    if not messages_for_forwarding:
        print('Ошибка, не получены сообщения для пересылки')
        return False
    elif not channels_to_forward:
        print('Ошибка, не получены каналы для пересылки')
        return False
    #Рассылка по каналам по порядку
    while channels_to_forward and messages_for_forwarding:
        message_i = messages_for_forwarding.pop()
        print(message_i[0], message_i[1])
        try:
            await app.forward_messages(channels_to_forward[-1][0],from_chat_id=message_i[0], message_ids=message_i[1])
            channels_to_forward[ -1 ][ 1 ] += 1
        except errors.exceptions.bad_request_400.MessageIdInvalid:
            print(f'Не найдено сообщение по ссылке t.me/{message_i[0]}/{message_i[1]}')
        if channels_to_forward[-1][1] ==17:
            channels_to_forward.pop()

    #Рассылка по каналам равномерно
    # while channels_to_forward:
    #     for index,channel in enumerate(channels_to_forward):
    #         if channel[1] > 17:
    #             channels_to_forward.remove(channel)
    #             continue
    #         msg = messages_for_forwarding.pop()
    #         try:
    #             await app.forward_messages(channel[0], from_chat_id=msg[0], message_ids=msg[1])
    #             channels_to_forward[index][1] += 1
    #         except errors.exceptions.bad_request_400.MessageIdInvalid:
    #             print(f'Не найдено сообщение по ссылке t.me/{msg[0]}/{msg[1]}')

    if messages_for_forwarding:
        print(f'Закончились каналы для пересылки, осталось не пересланных сообщений: {len(messages_for_forwarding)}')
    else:
        print('Все сообщения были пересланы')
asyncio.run(main())