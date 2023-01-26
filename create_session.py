import telethon
import os
api_id =0
api_hash = ''
while True:
    name = input('Введите название для новой сессии')
    if os.path.exists(f'sessions/{name}.session'):
        print('Сессия с таким название уже существует!')
    else:
        break
client = telethon.TelegramClient(f'sessions/{name}', api_id=api_id, api_hash=api_hash)
client.start()
