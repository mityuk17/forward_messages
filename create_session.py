import telethon
import os
api_id = 9411854
api_hash = '499c76606cefdeadd4b1ece84a5a9932'
while True:
    name = input('Введите название для новой сессии')
    if os.path.exists(f'sessions/{name}.session'):
        print('Сессия с таким название уже существует!')
    else:
        break
client = telethon.TelegramClient(f'sessions/{name}', api_id=api_id, api_hash=api_hash)
client.start()