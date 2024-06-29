from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError

api_id = 24458626
api_hash = 'f8a6254631c54633c0f5202fe0f1f72f'
bot_token = '7339589451:AAGAwB9Ciqj0VM84p799kFtqa40HqMb77BA' #توكن بوتك
bot = TelegramClient('session', api_id, api_hash)
bot.start(bot_token=bot_token)

phone_regex = r'^\+((?:9[679]|8[035789]|6[789]|5[90]|42|3[578]|2[1-689])|9[0-58]|8[1246]|6[0-6]|5[1-8]|4[013-9]|3[0-469]|2[70]|7|1)(?:\W*\d){0,13}\d$'
@bot.on(events.NewMessage(pattern=phone_regex, func=lambda e: e.is_private))
async def my_event_handler(event):
    phone = event.raw_text
    client = TelegramClient(StringSession(), api_id, api_hash)
    await client.connect()
    await client.send_code_request(phone)
    async with bot.conversation(event.chat_id, timeout=None, total_timeout=None) as conv:
        await conv.send_message("قوم بارسال الكود الذي تم ارساله لحسابك بين كل رقم . لعدم تقيدك")
        code = ''.join((await conv.get_response()).text.split('.'))
        # print(code)
        if code.isdigit() and len(code) == 5:
            try:
                await client.sign_in(phone, code)
                await conv.send_message(client.session.save())
            except SessionPasswordNeededError:
                await conv.send_message("قوم بارسال باسورد الحساب")
                password = (await conv.get_response()).text
                await client.sign_in(phone, password=password)
                await conv.send_message(client.session.save())

bot.run_until_disconnected()