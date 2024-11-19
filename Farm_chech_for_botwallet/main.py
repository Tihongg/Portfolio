from telethon.sync import TelegramClient, events
from telethon.tl.types import UpdateNewChannelMessage, MessageEntityTextUrl, KeyboardButtonUrl
import re
import difflib
import asyncio
import config
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest

client = TelegramClient(session=config.Session, api_id=config.api_id, api_hash=config.api_hash, system_version="4.16.30-vxCUSTOM")
print("Вход выполнен!!!")

client.start()

get_money = 0

list_used_check = []

@client.on(events.NewMessage)
async def my_event_handler(event):
    global get_money
    channel_delete = []
    if event.is_channel or event.is_group:
        if isinstance(event.original_update, UpdateNewChannelMessage):
            url = None
            bot = None
            message = event.original_update.message.message
            if 'wallet?start' in message.lower():
                urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                  message)
                url = difflib.get_close_matches('https://t.me/wallet?start=', urls)[0]
                bot = "wallet"

            if event.original_update.message.entities:
                for i in event.original_update.message.entities:
                    if isinstance(i, MessageEntityTextUrl):
                        if 'wallet?start' in i.url.lower():
                            url = i.url
                            bot = "wallet"

            if event.message.reply_markup:
                for i in event.message.reply_markup.rows:
                    if isinstance(i.buttons[0], KeyboardButtonUrl):
                        url_find = i.buttons[0].url
                        if 'wallet?start' in url_find.lower():
                            url = url_find
                            bot = "wallet"
                            break

            if url is not None:
                url_split = int(url.find("start"))
                send_command = "/" + url[url_split:].replace("=", " ")
                if send_command.split(" ")[1] not in list_used_check:
                    if bot == "wallet":
                        await client.send_message("@wallet", send_command)

                list_used_check.append(send_command.split(" ")[1])

    if event.sender_id == 1985737506:  # wallet bot
        one_simbal = event.message.message[0]
        if one_simbal == "✅":
            get_money += float(event.message.message.split("~")[1].split(" ")[0])
            print(get_money)

        if one_simbal == "⚠":
            if event.message.reply_markup:
                for i in event.message.reply_markup.rows:
                    if i.buttons[0].text != "Активировать чек":
                        try:
                            channel = await client.get_entity(i.buttons[0].url)
                            channel_delete.append(channel.id)
                            await client(JoinChannelRequest(channel))
                        except:
                            break

                        await asyncio.sleep(0.1)
                    else:
                        send_command = "/" + i.buttons[0].url.split("?")[1].replace("=", " ")
                        await client.send_message("@wallet", send_command)

        del_messages = []

        async for message in client.iter_messages("@wallet", 10):
            if message.text is not None:
                if "/start " in message.text:
                    del_messages.append(message.id)

        channel_delete = list(set(channel_delete))
        if channel_delete:
            for id in channel_delete:
                await client(LeaveChannelRequest(id))

        await client.delete_messages(entity="@wallet", message_ids=del_messages)
        await client.delete_messages(entity="@wallet", message_ids=[event.message.id])


client.run_until_disconnected()
