from telethon.sync import TelegramClient
from telethon import events
from datetime import datetime, timedelta
from WebApp import get_info_in_webapp
import asyncio
import random
import config

client = TelegramClient(session=config.Name_Session, api_id=config.api_id, api_hash=config.api_hash,
                        system_version="Android 9 (P30), 4.2.1")
client.start()
print("Запущен работаем")

s = False

@client.on(events.NewMessage(chats=[config.Channel_id_get_info]))
async def main(event):
    if event.original_update.message.entities:
        for x in event.original_update.message.entities:
            if hasattr(x, 'url'):
                if "startapp" in x.url:
                    global s
                    text_for_output = ''

                    signal_id = str(x.url).split("startapp=")[1]

                    Time_now = datetime.now().replace(microsecond=0)
                    time_slp = random.randrange(config.time_sleep[0], config.time_sleep[1])

                    get_info = await get_info_in_webapp(signal_id, client)
                    await asyncio.sleep(time_slp)

                    text_for_output += "-----------------------------------\n"
                    text_for_output += f"Url: https://t.me/makscontrol_bot/Signal?startapp={signal_id}\n"
                    text_for_output += f"Time_public: {Time_now}\n"
                    text_for_output += f"Delay_time: {time_slp}\n"
                    text_for_output += f"Full url: {get_info['for_output']['Full_url']}\n"
                    text_for_output += f"Captcha: {get_info['for_output']['Captcha']}\n"
                    text_for_output += f"Status_send: {get_info['for_output']['Status_send']}\n"
                    text_for_output += f"Time_send: {datetime.now().replace(microsecond=0)}"

                    print(text_for_output)

                    if get_info["img_url"].split("signals")[1] != "/":
                        await client.send_file(config.Channel_id_send_message, get_info["img_url"],
                                               caption=get_info["text"], parse_mode="html")
                    else:
                        await client.send_message(config.Channel_id_send_message, message=get_info["text"],
                                                  parse_mode="html")


async def check_connection():
    while True:
        try:
            await client.get_me()
            print("Connection check: OK")
        except Exception as e:
            print(f"Connection check failed: {e}")
            await client.disconnect()
            await client.connect()
        await asyncio.sleep(3000)  # Проверка каждые 5 минут

client.loop.create_task(check_connection())
client.run_until_disconnected()
