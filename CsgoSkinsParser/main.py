from parser import main_parser
from find_benefit import get_benefit
import asyncio
import logging
from datetime import datetime
import config
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from csgo_market_api import CSGOMarket
from config import market_api_key

logging.basicConfig(level=logging.INFO)
bot = Bot(config.Token)
dp = Dispatcher()
dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

market = CSGOMarket(api_key=market_api_key)

async def scheduled():
    while True:
        data = await main_parser()
        a = await get_benefit(data)
        for admin in config.id_admin:
            for message in a:
                send = True
                item = message['item']
                cheaply = message['platforms'].split("-")[0]
                price_cheaply = message['price_pay']
                expensive = message['platforms'].split("-")[1]
                price_expensive = message['price_sell']

                benefit = message['benefit']
                benefit_on_dollars = message['benefit_on_dollars']
                if "https://market.csgo.com/" in message['platforms'].split("-"):
                    data_item = market.get_list_items_info(list_hash_name=[item, ])
                    if data_item['success']:
                        history_item = data_item['data'][item]['history']
                        top_5_price = [x[1] for x in history_item][:5]
                        if "https://market.csgo.com/" == message['platforms'].split("-")[0]:
                            price_item = price_cheaply
                        elif "https://market.csgo.com/" == message['platforms'].split("-")[1]:
                            price_item = price_expensive
                        if price_item / (sum(top_5_price) / len(top_5_price)) > 1.15:
                            send = False
                if send:
                    text = f"""
Предмет: {item}
Дешевле на сайте: {cheaply} - {price_cheaply['on_percent']}$ ({price_cheaply['off_percent']}$)
Дороже на сайте: {expensive} - {price_expensive['on_percent']}$ ({price_expensive['off_percent']}$)

Выгода: {round(benefit['on_percent'], 2)} - {benefit_on_dollars['on_percent']}$ ({round(benefit['off_percent'], 2)} - {benefit_on_dollars['off_percent']}$)
                    """.strip()

                    buttons = [
                        [InlineKeyboardButton(text='Купить', url=message['url_pay'])],
                        [InlineKeyboardButton(text='Продать', url=message['url_sell'])]
                    ]

                    urlkb = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=2)

                    await bot.send_photo(chat_id=admin, photo=message['image_url'], caption=text.strip(), reply_markup=urlkb)
                    asyncio.sleep(0.5)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.chat.id in config.id_admin:
        await message.answer(f"Привет, этот бот будет отправлять тебе выгодные предложения по кс2 💸", parse_mode="html")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
