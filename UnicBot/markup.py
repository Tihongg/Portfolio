from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

import config

user = KeyboardButton("👤 Профиль")
kreo = KeyboardButton("🔥 Крео")
start_user = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(user, kreo)

async def sub_channel(list_channel: list):
    markup = InlineKeyboardMarkup(row_width=1)
    count = 0
    for x in list_channel:
        count += 1
        for a in config.SUB_CHANNEL:
            if a['id'] == x:
                markup.insert(InlineKeyboardButton(text=f'{count} Канал', url=a['url']))

    return markup

