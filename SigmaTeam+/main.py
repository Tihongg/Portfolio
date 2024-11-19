import asyncio
import secrets
import aioschedule
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.markdown import hlink
from typing import List, Union
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
import sqlite3
import config
import difflib
import markup
import pinterest
import numpy as np
from crypto_address_validator.validators import default_validator
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import requests
import random
import pycountry
from PIL import Image, ImageFont, ImageDraw
import json
import cv2
from io import BytesIO

storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)

db = sqlite3.connect('data.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER,
        nick TEXT,
        tag BOOLEAN,
        balance FLOAT,
        common_balance FLOAT,
        percent INTEGER,
        proxy INTEGER,
        sms INTEGER,
        ETH TEXT,
        BTC TEXT,
        USDT_TRC_20 TEXT,
        LTC TEXT,
        BNB TEXT,
        proxy_day INTEGER,
        sms_day INTEGER,
        verif BOOLEAN,
        block BOOLEAN,
        dep INTEGER
        )""")
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS application_start(
        id INTEGER,
        time TEXT,
        url TEXT
        )""")
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS application_proxy_sms(
        id INTEGER,
        proxy INTEGER,
        sms INTEGER
        )""")
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS application_money(
        id INTEGER,
        money INTEGER
        )""")
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS mentors(
        name_button INTEGER,
        info TEXT,
        id_user INTEGER,
        all_user TEXT
        )""")
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS proxy(
        USA TEXT,
        France TEXT,
        England TEXT,
        Germany TEXT
        )""")
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS promo(
        id INTEGER,
        money FLOAT,
        promo TEXT
        )""")
db.commit()

sql.execute(f"SELECT count(*) FROM proxy")
if sql.fetchone()[0] == 0:
    id = ['', '', '', '']
    db.execute("INSERT INTO proxy VALUES(?, ?, ?, ?);", id)
    db.commit()


class UserState(StatesGroup):
    yes_start = State()
    time_start = State()
    url_start = State()
    proxy_start = State()
    sms_start = State()
    set_wallet = State()
    set_proxy = State()
    set_sms = State()
    text_for_tag = State()
    promo_name = State()
    promo_money = State()
    get_promo = State()
    tiktok = State()
    withdraw = State()
    tags_video_promo = State()
    tags_video_money = State()
    draw_info = State()
    unic_doc = State()


class AdminState(StatesGroup):
    id_user = State()
    set_user = State()
    add_proxy = State()
    send_all = State()
    get_proxy = State()
    mentors_id = State()
    mentors_button_name = State()
    mentors_info = State()

class AlbumMiddleware(BaseMiddleware):
    """This middleware is for capturing media groups."""

    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        """
        You can provide custom latency to make sure
        albums are handled properly in highload.
        """
        self.latency = latency
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        if not message.media_group_id:
            return

        try:
            self.album_data[message.media_group_id].append(message)
            raise CancelHandler()  # Tell aiogram to cancel handler for this group element
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            message.conf["is_last"] = True
            data["album"] = self.album_data[message.media_group_id]

    async def on_post_process_message(self, message: types.Message, result: dict, data: dict):
        """Clean up after handling our album."""
        if message.media_group_id and message.conf.get("is_last"):
            del self.album_data[message.media_group_id]


def check_string_contains(string, objects):
    for obj in objects:
        if obj in string:
            return True
    return False


async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer("❌ Ошибка. Не флудите")


async def channel_post_handler(message: types.Message):
    if message.sender_chat.username == config.notifications.split('/')[-1]:
        one_line = message.text.split("\n")[0].replace("[", "").replace("]", "").strip()
        if one_line.lower() in "новый депозит":
            num_line = 0
            for search in message.text.split("\n"):
                num_line += 1
                if search != '':
                    contains_object = check_string_contains(search.replace(":", ' ').replace("  ", " "),
                                                            ["Промо", "промо", "Промокод", "промокод"])
                    if contains_object:
                        promo = search.replace(":", ' ').replace("  ", " ").split(" ")[1]
                        sql.execute(f"SELECT id FROM promo WHERE promo = ?", [promo])
                        uid = sql.fetchone()[0]
                        sql.execute(f"SELECT percent FROM users WHERE id = ?", [uid])
                        percent = sql.fetchone()[0]
                        sum_dep = message.text.lower().find("сумма")
                        sum_dep2 = message.text[sum_dep:].strip()
                        sum_dep = sum_dep2.lower().find("$")
                        sum_dep = sum_dep2[sum_dep:].split("\n")[0]

                        spl = sum_dep.split(" ")
                        dollar = spl[0]
                        BTC = ''.join(spl[1:]).strip()[1:-4]

                        sql.execute("UPDATE users SET balance = balance + ? WHERE id = ?", [round(float(dollar[1:]) * float(float(percent) / 100), 2), int(uid)])
                        sql.execute("UPDATE users SET common_balance = common_balance + ? WHERE id = ?", [round(float(dollar[1:]) * float(float(percent) / 100), 2), int(uid)])
                        sql.execute("UPDATE users SET dep = dep + 1 WHERE id = ?", [uid])
                        db.commit()
                        await bot.send_message(uid, f"<b>⚡️ Новый депозит!</b>\n\n<b>⚙️ Воркер: 🔑 Скрыт</b>\n<b>🔗 Домен: bi***com</b>\n<b>🖥 Сеть:</b> BTC (<code>{BTC}</code>)\n\n\n<b>💳 Сумма: {dollar}\n├ Процент воркера:</b> {percent}%\n<b>└ Доля воркера: {round(float(dollar[1:]) * float(float(percent) / 100), 2)}</b>", parse_mode="html")


async def check_time():
    sql.execute("UPDATE users SET proxy_day = 0")
    sql.execute("UPDATE users SET sms_day = 0")
    db.commit()


async def scheduler():
    aioschedule.every().day.at("00:00").do(check_time)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


async def check(message, data):
    if message.chat.id in config.admin_id:
        return True

    if data[16] == 0:
        sql.execute(f"SELECT id FROM application_start WHERE id = {message.chat.id}")
        if sql.fetchone() is None and data[15] == 0:
            await bot.send_message(message.chat.id, "⛔️ Для начала работы пропишите /start")
        else:
            if data[15] == 1:
                return True
            else:
                await bot.send_message(message.chat.id, "📭 Подождите пока администрация проверит вашу заявку")
    else:
        help = hlink('Поддержка', config.help)
        await bot.send_message(message.chat.id, f"⛔️ Вы были заблокированы, пожалуйста наппишите в поддержку: {help}",
                               parse_mode="HTML", disable_web_page_preview=True)


async def tags(count):
    i = 0
    random_tags = []
    while i < int(count):
        i += 1
        tags = random.sample(config.tags, 5)
        random_tags.append(tags)
    return random_tags


async def check_str_in_float(str):
    try:
        float(str)
        return True
    except:
        return False


async def tiktok(account):
    info_user = {}
    HashTags = []
    response = requests.get("https://countik.com/tiktok-analytics/user/" + account).text
    soup = BeautifulSoup(response, "html.parser")
    all_block = soup.findAll("div", class_="block")
    for div in all_block:
        total_followers = div.find("h3", string="Total Followers")
        if total_followers:
            info_user["Total Followers"] = div.find("p").text

        total_followers = div.find("h3", string="Total Videos")
        if total_followers:
            info_user["Total Videos"] = div.find("p").text

        total_followers = div.find("h3", string="Total Likes")
        if total_followers:
            info_user["Total Likes"] = div.find("p").text

        total_followers = div.find("h3", string="Following")
        if total_followers:
            info_user["Following"] = div.find("p").text

        total_followers = div.find("h3", string="Following")
        if total_followers:
            info_user["Following"] = div.find("p").text

    geo = soup.find("span", class_="acc-country").text.replace(" ", '').replace("\n", '')
    info_user["GEO"] = geo

    all_span_tag = soup.findAll("div", class_="bar")
    for i in all_span_tag:
        block = i.find("div", class_="background").find("div", class_="reach").find("span", class_="span-tag")
        choosen = block.find("span", class_="chosen").text
        count = block.find("span", class_="count").text
        HashTags.append(f"{choosen} {count}")

    info_user["HashTags"] = HashTags

    find_post = soup.find("div", class_="recent-posts").findAll("div", class_="item")
    num_video = 0
    all_video = []
    for video in find_post:
        num_video += 1
        if num_video <= 6:
            video_data = {}
            data = video.findAll("div", class_="data")
            for i in data:
                get = i.find("p", class_="title")
                if get.text == "Views":
                    video_data["views"] = i.find("p", class_="value").text

                if get.text == "Likes":
                    video_data["Likes"] = i.find("p", class_="value").text

                if get.text == "Comments":
                    video_data["Comments"] = i.find("p", class_="value").text

                if get.text == "Shares":
                    video_data["Shares"] = i.find("p", class_="value").text

            get_time = video.find("div", class_="create-time").text.strip().replace(",", '')
            date = get_time.split(' ')[0].split('/')
            time = get_time.split(' ')[1]
            type_time = get_time.split(' ')[2]

            year = date[2]
            day = date[1]
            if int(day) < 10:
                day = f"0{day}"
            month = date[0]
            if int(month) < 10:
                month = f"0{month}"

            new_time = f"{year}.{month}.{day} {time} {type_time}"
            final_data = {"reaction": video_data, "time": new_time}

            all_video.append(final_data)
        else:
            break

    info_user["video"] = all_video

    return info_user


async def ip_check(ip):
    url = 'http://ip-api.com/json/' + ip
    response = requests.get(url).json()
    try:

        if response['country'] == 'France':
            return "Франция"

        elif response['country'] == 'United States' or response['country'] == 'US':
            return "США"

        elif response['country'] == 'United Kingdom' or response['country'] == 'UK':
            return "Англия"

        elif response['country'] == 'Germany':
            return "Германия"

        else:
            return False
    except:
        return False


async def is_eth(address):
    if len(address) != 42:
        return False
    if not address.startswith("0x"):
        return False
    if not all(c in "0123456789abcdefABCDEF" for c in address[2:]):
        return False
    return True


async def fake_check(time, amount, amount_valute, date, status, wallet, commission):
    color1 = "#1C0606"
    color2 = "#5acb61"
    color3 = "#8f8e93"
    color4 = "#808080"

    check = Image.open("draw/photo/photo.jpg")
    geo = Image.open("draw/photo/other/geo.png")
    draw_text = ImageDraw.Draw(check)

    x_time = 30
    y_time = 15
    draw_text.text(
        (x_time, y_time),
        time,
        fill=color1,
        font=ImageFont.truetype('draw/font/font.ttf', size=25)
    )
    width, height = 25, 25
    overlay_image = geo.resize((width, height))
    overlay_image = overlay_image.convert("RGBA")
    check.paste(overlay_image, (x_time + 70, y_time - 2), overlay_image)

    top = check.width / 2
    draw_text.text(
        (top, 210),
        "+" + amount,
        fill=color2,
        font=ImageFont.truetype('draw/font/font.ttf', size=50),
        anchor="ms"
    )

    draw_text.text(
        (top, 250),
        amount_valute,
        fill=color3,
        font=ImageFont.truetype('draw/font/font.ttf', size=30),
        anchor="ms"
    )

    x = 545
    y = 305
    width = ImageFont.truetype('draw/font/font.ttf', size=25).getbbox(date)[2] - \
            ImageFont.truetype('draw/font/font.ttf', size=25).getbbox(date)[0]
    draw_text.text(
        (x - width, y),
        date,
        fill=color4,
        font=ImageFont.truetype('draw/font/font.ttf', size=25),
    )

    width = ImageFont.truetype('draw/font/font.ttf', size=25).getbbox(status)[2] - \
            ImageFont.truetype('draw/font/font.ttf', size=25).getbbox(status)[0]
    draw_text.text(
        (x - width, y + 65),
        status,
        fill=color4,
        font=ImageFont.truetype('draw/font/font.ttf', size=25)
    )

    wallet = wallet[:7] + "..." + wallet[-7:]
    width = ImageFont.truetype('draw/font/font.ttf', size=25).getbbox(wallet)[2] - \
            ImageFont.truetype('draw/font/font.ttf', size=25).getbbox(wallet)[0]
    draw_text.text(
        (x - width, y + 130),
        wallet,
        fill=color4,
        font=ImageFont.truetype('draw/font/font.ttf', size=25)
    )

    commission_cripto, commission_dollar = commission.split("(")[0].strip(), "(" + commission.split("(")[1].strip()
    width_cripto = ImageFont.truetype('draw/font/font.ttf', size=25).getbbox(commission_cripto)[2] - \
                   ImageFont.truetype('draw/font/font.ttf', size=25).getbbox(commission_cripto)[0]
    width_dollar = ImageFont.truetype('draw/font/font.ttf', size=25).getbbox(commission_dollar)[2] - \
                   ImageFont.truetype('draw/font/font.ttf', size=25).getbbox(commission_dollar)[0]
    draw_text.text(
        (x - width_cripto, y + 240),
        commission_cripto,
        fill=color4,
        font=ImageFont.truetype('draw/font/font.ttf', size=25)
    )

    draw_text.text(
        (x - width_dollar, y + 265),
        commission_dollar,
        fill=color4,
        font=ImageFont.truetype('draw/font/font.ttf', size=25)
    )

    return check

@dp.message_handler(commands=['start'])
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def start(message: types.Message):
    people_id = message.chat.id
    if people_id in config.admin_id:
        verif = True
    else:
        verif = False
    sql.execute(f"SELECT id FROM users WHERE id = {people_id}")
    data = sql.fetchone()
    if data is None:
        id = [message.chat.id, message.chat.username, True, 0, 0, config.percent, 1, 1, "", "", "", "", "", 0, 0, verif,
              False, '0']
        db.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", id)
        db.commit()

    sql.execute(f"SELECT * FROM users WHERE id = {people_id}")
    data = sql.fetchall()[0]
    verif = data[15]
    block = data[16]
    if people_id not in config.admin_id:
        if block == 0:
            if verif == 0:
                sql.execute(f"SELECT id FROM application_start WHERE id = {people_id}")
                if sql.fetchone() is None:
                    await bot.send_message(people_id,
                                           f"Приветствуем, ты попал в команду {config.name}, хочешь подать заявку?",
                                           reply_markup=markup.start_new_user)
                    await UserState.yes_start.set()
                else:
                    await bot.send_message(message.chat.id, "📭 Подождите пока администрация проверит вашу заявку")
            else:
                await bot.send_message(message.chat.id, "❇️ Вы попали в главное меню", reply_markup=markup.start_user)
        else:
            help = hlink('Поддержка', config.help)
            await bot.send_message(message.chat.id,
                                   f"⛔️ Вы были заблокированы, пожалуйста наппишите в поддержку: {help}",
                                   parse_mode="HTML", disable_web_page_preview=True)
    else:
        await bot.send_message(message.chat.id, "❇️ Вы попали в главное меню", reply_markup=markup.start_admin)


@dp.message_handler(content_types=["text"])
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def text(message: types.Message, state: FSMContext):
    sql.execute(f"SELECT * FROM users WHERE id = ?", [message.chat.id])
    data = sql.fetchall()[0]
    if await check(message, data):
        if message.text == "🙎‍♂ ️Мой профиль":
            if data[1] is None:
                nick = "<code>Нету</code>"
            else:
                if data[2] == 0:
                    nick = f"<tg-spoiler>@{data[1]}</tg-spoiler>"
                else:
                    nick = "@" + data[1]

            data = ["Нет" if x == '' else x for x in data]
            markup_tag = await markup.profile(message)

            mentors = sql.execute(f"SELECT name_button FROM mentors WHERE all_user LIKE '%{message.chat.id}%'").fetchone()
            if mentors is None:
                text_mentors = "<code>Нету</code>"
            else:
                text_mentors = f"<code>{mentors[0]}</code>"

            await bot.send_message(message.chat.id, f"<b>👋 Добро пожаловать в профиль\n{config.name}\n\nℹ️ Информация:\n└ 👉 ID: <code>{message.chat.id}</code>\n└ ❕ Отображение ника в выплатах: {nick}\n└ ⚡️ Наставник: {text_mentors}\n\n📊 Статистика:\n└ 💵Текущий баланс: <code>{data[3]}$</code>\n└ 🤑 Общий оборот: <code>{data[4]}$</code>\n└ 🚀 Процент: <code>{data[5]}%</code>\n└ ➕ Сумма регистраций: <code>{data[17]}</code>\n\n⁉️ Лимиты:\n└ Прокси: <code>{data[6]}</code>\n└ Смс: <code>{data[7]}</code>\n\n💳 Привязанные кошельки:\n└ ETH: <code>{data[8]}</code>\n└ BTC: <code>{data[9]}</code>\n└ USDT TRC 20: <code>{data[10]}</code>\n└ LTC: <code>{data[11]}</code>\n└ BNB: <code>{data[12]}</code></b>", reply_markup=markup_tag, parse_mode="html")

        elif message.text == "⚙️ Инструменты для работы":
            await bot.send_message(message.chat.id, "🛠 Выберите что вам нужно", reply_markup=markup.tools)

        elif message.text == "⚡️ Актуальный домен":
            await bot.send_message(message.chat.id, f"👉 Актуальный домен для работы: {config.domen}")

        elif message.text == "📊 Чекер":
            await bot.send_message(message.chat.id, "👇 Отправь сыллку на тик ток аккаунт")
            await UserState.tiktok.set()

        elif message.text == "⚔️ Топ пользователей":
            text_send = "<b>📋 Топ проекта:</b>\n\n"
            list_emoj = {1: "🥇", 2: "🥈", 3: "🥉", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣", 10: "🔟"}
            query = sql.execute("SELECT * FROM users ORDER BY common_balance DESC LIMIT 10").fetchall()
            i = 0
            for add_text in query:
                i += 1
                nick = add_text[1][0] + ("*" * (len(add_text[1]) - 1))
                common_balance = "$" + str(round(float(add_text[4]), 2))
                x = "x" + str(add_text[17])
                new_text = f"<b>{list_emoj[i]} {nick} • {common_balance} • {x}</b>\n"
                if i == 3:
                    new_text += "\n"

                text_send += new_text

            await bot.send_message(message.chat.id, text_send, parse_mode="html")

        elif message.text == "💸 Наставники":
            mentors = sql.execute(f"SELECT name_button FROM mentors WHERE all_user LIKE '%{message.chat.id}%'").fetchone()
            if mentors is None:
                text_send = "<b>⚡️ Наставники, которые доведут тебя до профитов!</b>"
                mentors = sql.execute("SELECT * FROM mentors").fetchall()
                if mentors:
                    mentors_markup = await markup.mentors(mentors)
                    await bot.send_message(message.chat.id, text_send, parse_mode='html', reply_markup=mentors_markup)
                else:
                    await bot.send_message(message.chat.id, text_send + "\n\n<b>Тут пока никого нету :(</b>", parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f"⚡️ У тебя уже есть наставник - <b>{mentors[0]}</b>", reply_markup=await markup.mentors_rejection_def(mentors[0]), parse_mode='html')

        elif message.text == "📄 Инфо":
            await bot.send_message(message.chat.id, "❇️ Полезные ссылки", reply_markup=markup.info_menu, parse_mode='html')

        elif message.text == "👨‍💻 Админ панель":
            if message.chat.id in config.admin_id:
                await bot.send_message(message.chat.id, "👨‍💻 Добро пожаловать в админ-панель",
                                       reply_markup=markup.admin_menu)

        elif message.text == "👤 Пользователи":
            if message.chat.id in config.admin_id:
                await bot.send_message(message.chat.id, "🆔 Отправь id пользователя с которым хочешь взаимодействовать")
                await AdminState.id_user.set()

        elif message.text == "👨‍💻 Заявки":
            if message.chat.id in config.admin_id:
                await bot.send_message(message.chat.id, "🌟 Выбери тип", reply_markup=markup.application_menu)

        elif message.text == "📨 Добавить Прокси":
            if message.chat.id in config.admin_id:
                await bot.send_message(message.chat.id, "🔐 Отправь proxy в этот чат", reply_markup=markup.add_proxy)
                await AdminState.add_proxy.set()

        elif message.text == "🗣 Рассылка":
            if message.chat.id in config.admin_id:
                await bot.send_message(message.chat.id, "👇 Отправь сообщение для рассылки в этот чат",
                                       reply_markup=markup.add_proxy)
                await AdminState.send_all.set()

        elif message.text == "↩️ Вернуться":
            if message.chat.id in config.admin_id:
                await bot.send_message(message.chat.id, "❇️ Вы попали в главное меню", reply_markup=markup.start_admin)

        elif message.text == "⏏️ Другое":
            if message.chat.id in config.admin_id:
                await bot.send_message(message.chat.id, "❇️ Выберите нужный пункт",
                                       reply_markup=markup.admin_other_menu)

@dp.callback_query_handler(text_startswith='mentors_rejection_')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def mentors_rejection_(call: types.CallbackQuery, state: FSMContext):
    name = call['data'].split("_")[-1]
    all_user = sql.execute("SELECT all_user FROM mentors WHERE name_button = ?", [name]).fetchone()[0]
    ls = all_user.strip().split("\n")
    ls.remove(str(call.from_user.id))
    new_str = '\n'.join(ls).strip()
    sql.execute(f"UPDATE mentors SET all_user = ? WHERE name_button = ?", [new_str, name])
    db.commit()
    await bot.send_message(call.from_user.id, "✅ Вы успешно отказались от наставника")

@dp.callback_query_handler(text_startswith='user_mentors_')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def user_mentors_(call: types.CallbackQuery, state: FSMContext):
    mentor = call['data'].split("_")[-1]
    info = sql.execute("SELECT info FROM mentors WHERE name_button = ?", [mentor]).fetchone()[0]
    id = sql.execute("SELECT id_user FROM mentors WHERE name_button = ?", [mentor]).fetchone()[0]
    smile = random.choice(['⚡️', '⚙️', '🖥'])
    info = f"<b>{smile} {info}</b>"
    await bot.send_message(call.from_user.id, info, parse_mode='html', disable_web_page_preview=True, reply_markup=await markup.mentors_applications(int(id)))

@dp.callback_query_handler(text_startswith='applications_mentors_')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def applications_mentors_(call: types.CallbackQuery, state: FSMContext):
    id_mentors = call['data'].split("_")[-1]
    await bot.send_message(call.from_user.id, "<b>💸Вы успешно подали заявку, ожидайте</b>", parse_mode='html')
    await bot.send_message(int(id_mentors), f"⚡️ Новый пользователь хочет что бы вы были его наставником\n\n🆔 ID: <code>{call.from_user.id}</code>\n👤 Ник: @{call.from_user.username}", parse_mode='html', reply_markup=await markup.mentors_yes_no_def(call.from_user.id))

@dp.callback_query_handler(text_startswith='appment_')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def ok(call: types.CallbackQuery, state: FSMContext):
    type = call['data'].split("_")[1]
    id = call['data'].split("_")[2]
    await call.message.delete()
    mentors = sql.execute(f"SELECT name_button FROM mentors WHERE all_user LIKE '%{id}%'").fetchone()
    if mentors is None:
        if type == "yes":
            all_user = sql.execute("SELECT all_user FROM mentors WHERE id_user = ?", [call.from_user.id]).fetchone()[0]
            new_all_user = (all_user + f'\n{id}').strip()
            sql.execute(f"UPDATE mentors SET all_user = ? WHERE id_user = ?", [new_all_user, call.from_user.id])
            db.commit()
            await bot.send_message(call.from_user.id, f"✅ Вы успешно приняли заявку")
            await bot.send_message(int(id), f"🥳 Вы теперь находитесь на наставничество у @{call.from_user.username}")
        elif type == "no":
            await bot.send_message(call.from_user.id, f"❌ Вы успешно отклонили заявку")
            await bot.send_message(int(id), f"❌ Вам было отклонено, возможно вы не подошли")
    else:
        await bot.send_message(call.from_user.id, "❌ Заявка была отменена, так как пользователь успел перейти к другому натсавнику")


@dp.callback_query_handler(text='admin_mentors')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def admin_mentors(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, "📨 Выбери дейтсвие", reply_markup=markup.admin_mentors)

@dp.callback_query_handler(text_startswith='mentors_')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def mentors_(call: types.CallbackQuery, state: FSMContext):
    type = call['data'].split("_")[1]
    if type == "add":
        await bot.send_message(call.from_user.id, "🆔️ Отправь ID наставника Название кнопки", reply_markup=markup.back)
        await AdminState.mentors_id.set()
    elif type == "delete":
        mentors = sql.execute("SELECT * FROM mentors").fetchall()
        if mentors:
            mentors_markup = await markup.mentors_delete(mentors)
            await bot.send_message(call.from_user.id, "❎ Выбери из списка кого хочешь удалить", reply_markup=mentors_markup)
        else:
            await bot.send_message(call.from_user.id, "😕 Пока что удалять нечего")

@dp.callback_query_handler(text_startswith='MontersDelete_')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def MontersDelete_(call: types.CallbackQuery, state: FSMContext):
    name = call['data'].split("_")[-1]
    sql.execute(f"DELETE FROM mentors WHERE name_button = ?", [name])
    db.commit()
    await bot.send_message(call.from_user.id, f"✅ <b>{name}</b> был успешно удален из наставников", parse_mode='html')

@dp.message_handler(state=AdminState.mentors_id)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def mentors_id(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(id=int(message.text))
        await bot.send_message(message.chat.id, "▶️ Отправь название кнопки", reply_markup=markup.back)
        await AdminState.mentors_button_name.set()
    else:
        await state.finish()
        await bot.send_message(message.chat.id, "❌ Неверный ID")

@dp.message_handler(state=AdminState.mentors_button_name)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def mentors_id(message: types.Message, state: FSMContext):
    await state.update_data(name_button=message.text)
    await bot.send_message(message.chat.id, "💬 Отправь информацию о этом наставнике")
    await AdminState.mentors_info.set()

@dp.message_handler(state=AdminState.mentors_info)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def mentors_info(message: types.Message, state: FSMContext):
    button = (await state.get_data())['name_button']
    id = (await state.get_data())['id']
    info = message.html_text
    await state.finish()
    db.execute("INSERT INTO mentors VALUES(?, ?, ?, ?);", [button, info, id, ''])
    db.commit()
    await bot.send_message(message.chat.id, "✅ Успшено добавлено", reply_markup=markup.back)

@dp.callback_query_handler(text='requests_proxy')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def requests_proxy(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "🌏 Выберите страну", parse_mode='html', reply_markup=markup.requests_proxy_countries)

@dp.callback_query_handler(text_startswith='requests_proxy_')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def requests_proxy_(call: types.CallbackQuery, state: FSMContext):
    sql.execute(f"SELECT proxy, proxy_day FROM users WHERE id = ?", [call.from_user.id])
    data = sql.fetchone()
    proxy = data[0]
    proxy_day = data[1]
    if proxy_day < proxy:
        try:
            await state.finish()
            lst = ['Portugal', 'France', 'United Kingdom', 'Mexico', 'Netherlands', 'Hungary', 'Switzerland',
                   'United States', 'New Zealand', 'Australia', 'Romania', 'Sweden', 'Austria', 'Germany']
            country = call['data'].split("_")[-1]
            country_requests = difflib.get_close_matches(country, lst)
            response = requests.get(
                "https://faceless.cc/api/find-proxy?key=6ltm6F3faO3DLJ8G8r1iz2rqEYGXUKo5&count=1&countryName=" +
                country_requests[0]).text
            id = json.loads(response)['data']['rows'][0]['id']
            response = requests.get(
                f"https://faceless.cc/api/buy-proxy?key=6ltm6F3faO3DLJ8G8r1iz2rqEYGXUKo5&id={id}&period=1").text

            info = json.loads(response)['data']['access'].split("/")[-1].split(" ")[0]
            login = info.split(":")[0].split("@")[0]
            password = info.split(":")[1].split("@")[0]
            ip_port = info.split("@")[1]

            sql.execute(f"UPDATE users SET proxy_day = proxy_day + 1 WHERE id = ?", [call.from_user.id])
            db.commit()
            text = f"<b>IP:Port: <code>{ip_port}</code>\nLogin: <code>{login}</code>\nPassword: <code>{password}</code></b>"

            await bot.send_message(call.from_user.id, "<b>✅ Ваше прокси</b>\n\n" + text, parse_mode='html',
                                   reply_markup=markup.back)
        except:
            await bot.send_message(call.from_user.id, "⛔️ Произошла ошибка, попробуйте еще раз")
    else:
        await bot.send_message(call.from_user.id,
                               "⛔️ Ваше кол-во прокси на сегодня закончилось, возвращайтесь за ними завтра",
                               reply_markup=markup.back)

@dp.callback_query_handler(text='draw')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def draw(call: types.CallbackQuery, state: FSMContext):
    await bot.send_photo(call.from_user.id,
                         photo="AgACAgIAAxkBAAIUf2UZwSNEB7YLl9p2oTepaJtuX7EuAAJtzTEbdMrQSKclXtcSXxaKAQADAgADcwADMAQ",
                         caption="<b>✏️ Введите с новой строки следующие данные: \n\n1️⃣ Время телефона\n2️⃣ Сумма перевода\n3️⃣ Сумма перевода в валюте\n4️⃣ Дата и время транзакции\n5️⃣ Статус транзакции\n6️⃣ Кошелек отправителя\n7️⃣ Комиссия сети</b>\n\n👉🏻 Пример введенных данных:\n\n<code>5:30</code>\n<code>0,32 BTC</code>\n<code>8400,70 $</code>\n<code>Sep 12, 2023 at 3:22 PM</code>\n<code>Completed</code>\n<code>bc1q2jxe5azr6zmhk3258tv7ul6cqtu4eu4mps8f4p</code>\n<code>0,00000576 BTC (0,21 $)</code>\n\nℹ️ Подсказка: для сегодняшнего дня используйте <code>Today at H:M AM/PM</code>, например <code>Today at 5:30 PM</code>",
                         parse_mode='html')
    await UserState.draw_info.set()


@dp.message_handler(state=UserState.draw_info)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def tags_video(message: types.Message, state: FSMContext):
    info = message.text.split("\n")
    await state.finish()
    file_day = await fake_check(info[0], info[1], info[2], info[3], info[4], info[5], info[6])
    byte_stream = BytesIO()
    file_day.save(byte_stream, 'JPEG')
    byte_stream.seek(0)
    photo = byte_stream.getvalue()

    await bot.send_photo(message.chat.id, photo=photo, caption="🌟 Ваш результат")


@dp.callback_query_handler(text='get_materials')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def get_materials(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, "🔽 Выберите пункт ниже", reply_markup=markup.materials)


@dp.callback_query_handler(text='unic')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def unic(call: types.CallbackQuery, state: FSMContext):
    markups = markup.back
    markups.inline_keyboard[0][0].text = '🚫 Отмена'
    await bot.send_message(call.from_user.id, "📷 Отправь мне до 10 изображений (<b>документом</b>), и я уникализирую каждое из них для тебя!", parse_mode='html', reply_markup=markups)
    await UserState.unic_doc.set()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=UserState.unic_doc, is_media_group=False)
async def handle_albums(message: types.Message, state: FSMContext):
    await state.finish()
    await message.photo[-1].download(destination_dir=f"Unic/{str(message.chat.id)}")
    directory = os.fsencode("Unic/" + str(message.chat.id) + "/photos")
    photo = None
    for file in os.listdir(directory):
        image_path = f"Unic/{str(message.chat.id)}/photos/" + os.fsdecode(file)
        image = cv2.imread(image_path)
        brightness = 1.15
        contrast = 1.15
        image2 = cv2.addWeighted(image, contrast, np.zeros(image.shape, image.dtype), 0, brightness)
        image_pil = Image.fromarray(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
        with BytesIO() as output:
            image_pil.save(output, format="JPEG")
            photo = output.getvalue()

        os.remove(image_path)

    await bot.send_photo(message.chat.id, photo=photo, caption="🌟 Ваш результат")

@dp.message_handler(content_types=types.ContentType.PHOTO, state=UserState.unic_doc, is_media_group=True)
async def handle_albums(message: types.Message, album: List[types.Message], state: FSMContext):
    await state.finish()
    media_group = types.MediaGroup()

    for obj in album:
        if obj.photo:
            await obj.photo[-1].download(destination_dir=f"Unic/{str(message.chat.id)}")

    directory = os.fsencode("Unic/" + str(message.chat.id) + "/photos")
    i = 0
    for file in os.listdir(directory):
        i += 1
        image_path = f"Unic/{str(message.chat.id)}/photos/" + os.fsdecode(file)
        image = cv2.imread(image_path)
        brightness = 1.15
        contrast = 1.15
        image2 = cv2.addWeighted(image, contrast, np.zeros(image.shape, image.dtype), 0, brightness)
        cv2.imwrite(image_path, image2)

        if i == 1:
            media_group.attach_photo(types.InputFile(image_path), '🌟 Your result')
        else:
            media_group.attach_photo(types.InputFile(image_path))

    await bot.send_media_group(message.chat.id, media=media_group)

    for file in os.listdir(directory):
        os.remove(f"Unic/{str(message.chat.id)}/photos/" + os.fsdecode(file))


@dp.callback_query_handler(text='kreo')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def kreo(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, "❌ Эта функция еще в разработке")


@dp.callback_query_handler(text='girls')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def girls(call: types.CallbackQuery, state: FSMContext):
    all_q = ["aesthetic girl", "girl aesthetic", "Естетичные девочки", "Милые девочки", "Девочки эстетичные",
             "Азиатки", "Красивые девушки с черными волосами", "Девочка эстетика", "эстетичные девушки", "кареянки", "девушка эстетичная"]
    q = random.choice(all_q)
    await bot.send_chat_action(call.message.chat.id, types.ChatActions.UPLOAD_DOCUMENT)
    get = await bot.send_message(call.from_user.id, "<i>⌛️ Находим картинки...</>", parse_mode="html")
    url_list = pinterest.scraper.scrape(key=q, max_images=5)["url_list"]
    await bot.delete_message(call.from_user.id, get.message_id)
    load = await bot.send_message(call.from_user.id, "<i>🔐 Загружаем картинки...</>", parse_mode="html")
    num = 0
    media = []
    for i in url_list:
        num += 1
        if num == 1:
            media.append(types.InputMediaPhoto(i, '✅ Успешно!'))
        else:
            media.append(types.InputMediaPhoto(i))

    await bot.delete_message(call.from_user.id, load.message_id)
    await bot.send_media_group(call.message.chat.id, media=media)


@dp.callback_query_handler(text='tags')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def get_materials(call: types.CallbackQuery, state: FSMContext):
    promo_markup = await markup.gen_tag(call)
    await bot.send_message(call.from_user.id, "🎴 Выберите промокод из списка", reply_markup=promo_markup)


@dp.callback_query_handler(text_startswith='promo_tags_')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def get_materials(call: types.CallbackQuery, state: FSMContext):
    promo = call['data'].split('_')[-1]
    markup_next = await markup.gen_tag_next(promo, money=None)
    await bot.send_message(call.from_user.id, "#️⃣ Выберите кол-во строк тегов для видео", reply_markup=markup_next)


@dp.callback_query_handler(text_startswith='gen_promo_num_')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def get_materials(call: types.CallbackQuery, state: FSMContext):
    array_smile = ['🌁', '🌌', '❄️', '🦈', '🌿', '🔥', '🌟', '💟']
    data = call['data']
    promo = data.split('_')[3]
    num = int(data.split('_')[4])
    if len(data.split('_')) < 6:
        sql.execute(f"SELECT money FROM promo WHERE promo = ?", [promo])
        money_promo = sql.fetchone()[0]
    else:
        money_promo = data.split('_')[5]

    formatted_num = "{:.2f}".format(round(float(money_promo), 2))
    add_text = f"Био:\n\n<code>tradexopen.com | {promo} | {formatted_num} BTC</code>\n\nОписание видео:\n\n"
    tags_video = await tags(num)
    for add in tags_video:
        smile = random.choice(array_smile)
        text = f"<code>{smile} {promo} {smile} {' '.join(add)}</code>"
        add_text += text + '\n\n'

    await bot.send_message(call.from_user.id, add_text.strip(), parse_mode="html")


@dp.callback_query_handler(text='promo_unique')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def reset_percentages(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, "👇 Отправь в чат свой кастомный промо")
    await UserState.tags_video_promo.set()


@dp.message_handler(state=UserState.tags_video_promo)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def tags_video(message: types.Message, state: FSMContext):
    await state.update_data(promo=message.text)
    await bot.send_message(message.from_user.id, "👇 Отправь в чат сумму промокода")
    await UserState.tags_video_money.set()


@dp.message_handler(state=UserState.tags_video_money)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def tags_video(message: types.Message, state: FSMContext):
    await state.update_data(money=message.text)
    data = await state.get_data()
    await state.finish()
    promo = data["promo"]
    money = data["money"]
    markup_next = await markup.gen_tag_next(promo, money)
    await bot.send_message(message.from_user.id, "#️⃣ Выберите кол-во строк тегов для видео", reply_markup=markup_next)


@dp.callback_query_handler(text='reset_percentages')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def reset_percentages(call: types.CallbackQuery, state: FSMContext):
    sql.execute(f"SELECT * FROM users")
    for change in sql.fetchall():
        uid = change[0]
        sql.execute(f"UPDATE users SET percent = ? WHERE id = ?", [config.percent, uid])
        db.commit()

    await bot.send_message(call.from_user.id, "✅ Сброс выполнен успешно")


@dp.callback_query_handler(text='reset_limits')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def reset_limits(call: types.CallbackQuery, state: FSMContext):
    sql.execute(f"SELECT * FROM users")
    for change in sql.fetchall():
        uid = change[0]
        sql.execute(f"UPDATE users SET proxy_day = 0 WHERE id = ?", [uid])
        sql.execute(f"UPDATE users SET sms_day = 0 WHERE id = ?", [uid])
        db.commit()

    await bot.send_message(call.from_user.id, "✅ Сброс выполнен успешно")


@dp.callback_query_handler(text='connect_wallet')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def connect_wallet(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "👇 Выберите какой кошелек привязать", reply_markup=markup.set_wallet)


@dp.callback_query_handler(text='withdraw_money')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def connect_wallet(call: types.CallbackQuery, state: FSMContext):
    sql.execute(f"SELECT balance FROM users WHERE id = ?", [call.from_user.id])
    balance = sql.fetchone()[0]
    if balance > int(config.min_withdraw):
        await bot.send_message(call.from_user.id, "💸 Отправь сумму для вывода")
        await UserState.withdraw.set()
    else:
        await bot.send_message(call.from_user.id,
                               f"⛔️ Недостаточно средств, минимальная сумма вывода - {config.min_withdraw}$")


@dp.message_handler(state=UserState.withdraw)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def withdraw(message: types.Message, state: FSMContext):
    sql.execute(f"SELECT balance FROM users WHERE id = ?", [message.chat.id])
    balance = sql.fetchone()[0]
    if await check_str_in_float(message.text):
        if float(message.text) <= float(balance):
            sql.execute(f"UPDATE users SET balance = balance - ? WHERE id = ?", [float(message.text), message.chat.id])
            db.commit()
            id = [message.chat.id, float(message.text)]
            db.execute("INSERT INTO application_money VALUES(?, ?);", id)
            db.commit()
            await bot.send_message(message.chat.id, "✅ Ваша заявка успешно принята, ожидайте одобрения администрации",
                                   reply_markup=markup.start_user)
            await state.finish()
        else:
            await state.finish()
            await bot.send_message(message.chat.id, "⛔️ Недостаточно средств")
    else:
        await state.finish()
        await bot.send_message(message.chat.id, "⛔️ Неверный формат")


@dp.callback_query_handler(text_startswith='set_')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def connect_wallet(call: types.CallbackQuery, state: FSMContext):
    wallet = call['data'][4:]
    if wallet == "USDT_TRC":
        set_wallet = "USDT TRC"
    else:
        set_wallet = wallet

    await bot.send_message(call.from_user.id, f"Отправь свой {set_wallet} кошелек в этот чат ✏️",
                           reply_markup=markup.back)
    await UserState.set_wallet.set()
    await state.update_data(type_wallet=wallet)


@dp.message_handler(state=UserState.set_wallet)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def set_wallet(message: types.Message, state: FSMContext):
    await state.update_data(wallet=message.text)
    data = await state.get_data()
    type_wallet = data["type_wallet"]
    wallet = data["wallet"]

    if type_wallet == "USDT_TRC":
        type_text_wallet = "USDT TRC"
        type_wallet = "USDT_TRC_20"
    else:
        type_text_wallet = type_wallet

    if type_wallet == "ETH":
        if await is_eth(wallet):
            sql.execute(f"UPDATE users SET {type_wallet} = ? WHERE id = ?", [wallet, message.chat.id])
            db.commit()
            if message.chat.id in config.admin_id:
                await bot.send_message(message.chat.id, f"✅ Вы успешно изменили {type_text_wallet} кошелек",
                                       reply_markup=markup.start_admin)
            else:
                await bot.send_message(message.chat.id, f"✅ Вы успешно изменили {type_text_wallet} кошелек",
                                       reply_markup=markup.start_user)
            await state.finish()
        else:
            await state.finish()
            await bot.send_message(message.chat.id, f"⛔️ не верный {type_text_wallet} кошелек")
    else:
        if default_validator.is_valid_address(wallet):
            sql.execute(f"UPDATE users SET {type_wallet} = ? WHERE id = ?", [wallet, message.chat.id])
            db.commit()
            if message.chat.id in config.admin_id:
                await bot.send_message(message.chat.id, f"✅ Вы успешно изменили {type_text_wallet} кошелек",
                                       reply_markup=markup.start_admin)
            else:
                await bot.send_message(message.chat.id, f"✅ Вы успешно изменили {type_text_wallet} кошелек",
                                       reply_markup=markup.start_user)
            await state.finish()
        else:
            await state.finish()
            await bot.send_message(message.chat.id, f"⛔️ не верный {type_text_wallet} кошелек")


@dp.message_handler(state=UserState.yes_start)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def yes_start(message: types.Message, state: FSMContext):
    if message.text == "📩 Да, хочу подать заявку":
        await bot.send_message(message.chat.id, "2️⃣  Сколько времени готовы уделять?")
        await UserState.time_start.set()


@dp.message_handler(state=UserState.time_start)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def yes_start(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)
    await bot.send_message(message.chat.id, "❇️ Пришлите ссылку на ваш профиль на zelenka.guru",
                           reply_markup=markup.zelenka)


@dp.callback_query_handler(text='url_zelenka', state=UserState.time_start)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def url_Zelenka(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, "💬 Отправь ссылку на свой профиль с zelenka.guru")
    await UserState.url_start.set()


@dp.callback_query_handler(text='next_zelenka', state=UserState.time_start)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def next_Zelenka(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, "📨 Вам нужны номера/прокси? Если да, укажите желаемый лимит в день.",
                           reply_markup=markup.proxy_sms)


@dp.message_handler(state=UserState.url_start)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def url_start(message: types.Message, state: FSMContext):
    await state.update_data(url=message.text)
    await bot.send_message(message.chat.id, "📨 Вам нужны номера/прокси? Если да, укажите желаемый лимит в день.",
                           reply_markup=markup.proxy_sms)


@dp.callback_query_handler(text='proxy_sms_yes', state=[UserState.time_start, UserState.url_start])
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def next_Zelenka(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, "📂 Отправьте желаемое кол-во прокси")
    await UserState.proxy_start.set()


@dp.callback_query_handler(text='proxy_sms_no', state=[UserState.time_start, UserState.url_start])
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def next_Zelenka(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    try:
        url = data["url"]
    except:
        url = "Не указано"
    id = [call.from_user.id, data["time"], url]
    db.execute("INSERT INTO application_start VALUES(?, ?, ?);", id)
    db.commit()
    await bot.send_message(config.application_chat_id, f"🆔 ID: <code>{call.from_user.id}</code>\n👤 Ник: @{call.from_user.username}\n\n⌛️ Готов уделять времени: <code>{data['time']}</code>\n🔗 Сыллка на аккаунт: <code>{url}</code>", parse_mode="html", reply_markup=await markup.application_start(call.from_user.id))
    await bot.send_message(call.from_user.id, f"<b>Вы подали заявку в команду {config.name}, ожидайте принятия решения от администрации</b>", parse_mode="html")


@dp.message_handler(state=UserState.proxy_start)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def set_proxy(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if int(message.text) <= config.max_proxy:
            await state.update_data(proxy=message.text)
            await bot.send_message(message.chat.id, "💬 Отправьте желаемое кол-во смс")
            await UserState.sms_start.set()
        else:
            await bot.send_message(message.chat.id,
                                   f"⛔️ Макс. кол-во {config.max_proxy}, отправьте число равное или менее {config.max_proxy}-ти")
    else:
        await bot.send_message(message.chat.id, "⛔️ Отправьте целое число")


@dp.message_handler(state=UserState.sms_start)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def set_proxy(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if int(message.text) <= config.max_sms:
            await state.update_data(sms=message.text)
            data = await state.get_data()
            await state.finish()
            try:
                url = data["url"]
            except:
                url = "Не указано"
            id = [message.chat.id, data["proxy"], data["sms"]]
            db.execute("INSERT INTO application_proxy_sms VALUES(?, ?, ?);", id)
            id = [message.chat.id, data["time"], url]
            db.execute("INSERT INTO application_start VALUES(?, ?, ?);", id)
            db.commit()
            await bot.send_message(config.application_chat_id, f"🆔 ID: <code>{message.chat.id}</code>\n👤 Ник: @{message.chat.username}\n\n🌐 Кол-во прокси: <code>{data['proxy']}</code>\n📱 Кол-во смс: <code>{data['sms']}</code>", parse_mode="html", reply_markup=await markup.application_proxy_sms(message.chat.id))
            await bot.send_message(config.application_chat_id, f"🆔 ID: <code>{message.from_user.id}</code>\n👤 Ник: @{message.from_user.username}\n\n⌛️ Готов уделять времени: <code>{data['time']}</code>\n🔗 Сыллка на аккаунт: <code>{url}</code>", parse_mode="html", reply_markup=await markup.application_start(message.from_user.id))
            await bot.send_message(message.chat.id, f"<b>Вы подали заявку в команду {config.name}, ожидайте принятия решения от администрации</b>", parse_mode="html")
        else:
            await bot.send_message(message.chat.id,
                                   f"⛔️ Макс. кол-во {config.max_sms}, отправьте число равное или менее {config.max_sms}-ти")
    else:
        await bot.send_message(message.chat.id, "⛔️ Отправьте целое число")


@dp.callback_query_handler(text='off_tag')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def on_tag(call: types.CallbackQuery):
    message_id = call.message.message_id
    sql.execute(f"UPDATE users SET tag = ? WHERE id = ?", [False, call.from_user.id])
    db.commit()
    sql.execute(f"SELECT * FROM users WHERE id = ?", [call.from_user.id])
    data = sql.fetchall()[0]
    if data[1] is None:
        nick = "<code>Нету</code>"
    else:
        nick = f"<tg-spoiler>@{data[1]}</tg-spoiler>"

    data = ["Нет" if x == '' else x for x in data]
    markup_tag = await markup.profile(call)

    mentors = sql.execute(f"SELECT name_button FROM mentors WHERE all_user LIKE '%{call.from_user.id}%'").fetchone()
    if mentors is None:
        text_mentors = "<code>Нету</code>"
    else:
        text_mentors = f"<code>{mentors[0]}</code>"

    await bot.edit_message_text(chat_id=call.from_user.id, message_id=message_id, text=f"<b>👋 Добро пожаловать в профиль\n{config.name}\n\nℹ️ Информация:\n└ 👉 ID: <code>{call.from_user.id}</code>\n└ ❕ Отображение ника в выплатах: {nick}\n└ ⚡️ Наставник: {text_mentors}\n\n📊 Статистика:\n└ 💵Текущий баланс: <code>{data[3]}$</code>\n└ 🤑 Общий оборот: <code>{data[4]}$</code>\n└ 🚀 Процент: <code>{data[5]}%</code>\n└ ➕ Сумма регистраций: <code>{data[17]}</code>\n\n⁉️ Лимиты:\n└ Прокси: <code>{data[6]}</code>\n└ Смс: <code>{data[7]}</code>\n\n💳 Привязанные кошельки:\n└ ETH: <code>{data[8]}</code>\n└ BTC: <code>{data[9]}</code>\n└ USDT TRC 20: <code>{data[10]}</code>\n└ LTC: <code>{data[11]}</code>\n└ BNB: <code>{data[12]}</code></b>", reply_markup=markup_tag, parse_mode="html")


@dp.callback_query_handler(text='on_tag')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def on_tag(call: types.CallbackQuery):
    message_id = call.message.message_id
    sql.execute(f"UPDATE users SET tag = ? WHERE id = ?", [True, call.from_user.id])
    db.commit()
    sql.execute(f"SELECT * FROM users WHERE id = ?", [call.from_user.id])
    data = sql.fetchall()[0]
    if data[1] is None:
        nick = "<code>Нету</code>"
    else:
        nick = "@" + data[1]

    data = ["Нет" if x == '' else x for x in data]
    markup_tag = await markup.profile(call)

    mentors = sql.execute(f"SELECT name_button FROM mentors WHERE all_user LIKE '%{call.from_user.id}%'").fetchone()
    if mentors is None:
        text_mentors = "<code>Нету</code>"
    else:
        text_mentors = f"<code>{mentors[0]}</code>"

    await bot.edit_message_text(chat_id=call.from_user.id, message_id=message_id,
                                text=f"<b>👋 Добро пожаловать в профиль\n{config.name}\n\nℹ️ Информация:\n└ 👉 ID: <code>{call.from_user.id}</code>\n└ ❕ Отображение ника в выплатах: {nick}\n└ ⚡️ Наставник: {text_mentors}\n\n📊 Статистика:\n└ 💵Текущий баланс: <code>{data[3]}$</code>\n└ 🤑 Общий оборот: <code>{data[4]}$</code>\n└ 🚀 Процент: <code>{data[5]}%</code>\n└ ➕ Сумма регистраций: <code>{data[17]}</code>\n\n⁉️ Лимиты:\n└ Прокси: <code>{data[6]}</code>\n└ Смс: <code>{data[7]}</code>\n\n💳 Привязанные кошельки:\n└ ETH: <code>{data[8]}</code>\n└ BTC: <code>{data[9]}</code>\n└ USDT TRC 20: <code>{data[10]}</code>\n└ LTC: <code>{data[11]}</code>\n└ BNB: <code>{data[12]}</code></b>",
                                reply_markup=markup_tag, parse_mode="html")


@dp.callback_query_handler(text='add_limit')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def add_limit(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, "📂 Отправьте желаемое кол-во прокси", reply_markup=markup.back)
    await UserState.set_proxy.set()


@dp.message_handler(state=UserState.set_proxy)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def set_proxy(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if int(message.text) <= config.max_proxy:
            await state.update_data(proxy=message.text)
            await bot.send_message(message.chat.id, "💬 Отправьте желаемое кол-во смс", reply_markup=markup.back)
            await UserState.set_sms.set()
        else:
            await bot.send_message(message.chat.id,
                                   f"⛔️ Макс. кол-во {config.max_proxy}, отправьте число равное или менее {config.max_proxy}-ти")
    else:
        await bot.send_message(message.chat.id, "⛔️ Отправьте целое число")


@dp.message_handler(state=UserState.set_sms)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def set_sms(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if int(message.text) <= config.max_sms:
            await state.update_data(sms=message.text)
            data = await state.get_data()
            await state.finish()
            id = [message.chat.id, data["proxy"], data["sms"]]
            db.execute("INSERT INTO application_proxy_sms VALUES(?, ?, ?);", id)
            db.commit()
            await bot.send_message(config.application_chat_id, f"🆔 ID: <code>{message.chat.id}</code>\n👤 Ник: @{message.chat.username}\n\n🌐 Кол-во прокси: <code>{data['proxy']}</code>\n📱 Кол-во смс: <code>{data['sms']}</code>", parse_mode="html", reply_markup=await markup.application_proxy_sms(message.chat.id))
            if message.chat.id in config.admin_id:
                await bot.send_message(message.chat.id,
                                       f"<b>✅ Вы успешно подали заявку на увеличение лимитов, ожидайте принятия решения от администрации</b>",
                                       parse_mode="html", reply_markup=markup.start_admin)
            else:
                await bot.send_message(message.chat.id,
                                       f"<b>✅ Вы успешно подали заявку на увеличение лимитов, ожидайте принятия решения от администрации</b>",
                                       parse_mode="html", reply_markup=markup.start_user)
        else:
            await bot.send_message(message.chat.id,
                                   f"⛔️ Макс. кол-во {config.max_sms}, отправьте число равное или менее {config.max_sms}-ти")
    else:
        await bot.send_message(message.chat.id, "⛔️ Отправьте целое число")


@dp.callback_query_handler(text='get_proxy')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def back(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, "🗳 Выберите прокси, которые хотите получить",
                           reply_markup=markup.get_proxy)


@dp.callback_query_handler(text='service_proxy')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def service(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, "🚩 Выбери страну", reply_markup=markup.get_proxy_countries)


@dp.callback_query_handler(text_startswith='proxy_')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def get_proxy(call: types.CallbackQuery, state: FSMContext):
    countries = call['data'][6:]
    sql.execute(f"SELECT proxy, proxy_day FROM users WHERE id = ?", [call.from_user.id])
    data = sql.fetchone()
    proxy = data[0]
    proxy_day = data[1]
    if proxy_day < proxy:
        sql.execute(f"SELECT {countries} FROM proxy")
        proxy = sql.fetchone()[0]
        if proxy != "":
            one_proxy = proxy.splitlines()[0]
            lines = proxy.split("\n")
            lines.pop(0)
            new_proxy = "\n".join(lines)
            sql.execute(f"UPDATE proxy SET {countries} = ?", [new_proxy])
            sql.execute(f"UPDATE users SET proxy_day = proxy_day + 1 WHERE id = ?", [call.from_user.id])
            db.commit()
            await bot.send_message(call.from_user.id, f"🔐 Ваше прокси: {one_proxy}")
        else:
            await bot.send_message(call.from_user.id, "❌ Нету свободных прокси ")
    else:
        await bot.send_message(call.from_user.id,
                               "⛔️ Ваше кол-во прокси на сегодня закончилось, возвращайтесь за ними завтра",
                               reply_markup=markup.back)


@dp.callback_query_handler(text='get_number')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def get_sms(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, "🚩 Выберите страну", reply_markup=markup.get_sms)


@dp.callback_query_handler(text_startswith='sms_')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def get_sms(call: types.CallbackQuery, state: FSMContext):
    sql.execute(f"SELECT sms, sms_day FROM users WHERE id = ?", [call.from_user.id])
    data = sql.fetchone()
    sms = data[0]
    sms_day = data[1]
    if sms_day < sms:
        countries = call['data'][4:]
        operators = {
            "england": "any",
            "canada": "any"
        }
        operator_sms = operators[countries]
        url = 'https://5sim.biz/v1/user/buy/activation/' + countries + '/' + operator_sms + '/' + "tiktok"
        response = requests.get(url, headers=config.headers).text
        try:
            json_response = json.loads(response)
            phone = json_response["phone"]
            await bot.send_message(call.from_user.id, "⌛️ Получаем доступ к телефону, пожалуйста подождите...")
            id = json_response["id"]
            url_check = "https://5sim.biz/v1/user/check/" + str(id)
            next_sms = 0
            await state.update_data(id_sms=id)
            num_send = 0
            while True:
                sms = requests.get(url_check, headers=config.headers).text
                json_sms = json.loads(sms)
                status = json_sms["status"]
                if status == "RECEIVED":
                    num_send += 1
                    if num_send == 1:
                        sql.execute(f"UPDATE users SET sms_day = sms_day + 1 WHERE id = ?", [call.from_user.id])
                        db.commit()
                        await bot.send_message(call.from_user.id,
                                               f"📱 Номер телефона: <code>{phone}</code>\n\n<code>❗️ Номер будет активен в течение 15 минут после его получения</code>",
                                               parse_mode="html")
                    if json_sms["sms"]:
                        if next_sms == 0 or next_sms != 0 and json_sms["sms"][0]["code"] != next_sms:
                            next_sms = json_sms["sms"][0]["code"]
                            await bot.send_message(call.from_user.id,
                                                   f'📱 Ваш код: <code>{json_sms["sms"][0]["code"]}</code>',
                                                   parse_mode="html")
                            await asyncio.sleep(1)

                elif status == "FINISHED":
                    await bot.send_message(call.from_user.id,
                                           f"❗️ Время активации номера <code>{phone}</code> истекло.",
                                           parse_mode="html", reply_markup=markup.back)
                    break

                await asyncio.sleep(1)

            if next_sms == 0:
                requests.get('https://5sim.biz/v1/user/cancel/' + id, headers=config.headers)

        except:
            await bot.send_message(call.from_user.id, "⛔️ Нету свободных номеров", reply_markup=markup.back)
    else:
        await bot.send_message(call.from_user.id,
                               "⛔️ Ваше кол-во номеров на сегодня закончилось, возвращайтесь за ними завтра",
                               reply_markup=markup.back)


@dp.callback_query_handler(text='generator_tag')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def generator_tag(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, "✏️ Отправьте текст для генерации хешетегов",
                           reply_markup=markup.next_tag)
    await UserState.text_for_tag.set()


@dp.callback_query_handler(text='next_tag', state=UserState.text_for_tag)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def generator_tag(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(text='')
    await bot.send_message(call.from_user.id, "📨 Выберите кол-во хештегов", reply_markup=markup.count_tag)


@dp.message_handler(state=UserState.text_for_tag)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def set_sms(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "📨 Выберите кол-во хештегов", reply_markup=markup.count_tag)


@dp.callback_query_handler(text_startswith='tag_', state=UserState.text_for_tag)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def tag_(call: types.CallbackQuery, state: FSMContext):
    count_tag = call['data'][4:]
    await state.finish()
    tag = await tags(count_tag)
    tags_text = ""
    for add in tag:
        line = "<code>"
        el = 0
        for add2 in add:
            el += 1
            if el == 5:
                line += add2 + "</code>"
            else:
                line += add2 + " "
        tags_text += line
        tags_text += '\n'
    await bot.send_message(call.from_user.id,
                           f"✅ Теги успешно сгенерированы\n<code>❗️ Обязательно посмотрите теги по просмотрам, если на тегах мало просмотров, произведите генерацию снова</code>\n\n🚀 Сгенерированные теги:\n{tags_text}",
                           parse_mode="html")


@dp.callback_query_handler(text='get_check_promo')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def get_check_promo(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, "👉 Выберите действие", reply_markup=markup.get_check_promo)


@dp.callback_query_handler(text_startswith='promo_get')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def promo_get(call: types.CallbackQuery, state: FSMContext):
    button = call["data"][6:]
    if button == "get":
        await bot.send_message(call.from_user.id, "🌟 Выберите домен для промокода",
                               reply_markup=markup.get_create_promo_domen)

    elif button == "get_info":
        all_promo = ""
        sql.execute(f"SELECT promo FROM promo WHERE id = ?", [call.from_user.id])
        data = sql.fetchall()
        i = 0
        for add in data:
            i += 1
            if i == len(data):
                all_promo += f"<code>{add[0]}</code>"
            else:
                all_promo += f"<code>{add[0]}</code>" + ", "

        promo_markup = await markup.get_markup_all_promo(call)
        await bot.send_message(call.from_user.id,
                               f"🖥 Ваши промокоды:\n{all_promo}\n\n✏️ Нажмите на нужный промокод или отправьте его для получения информации",
                               parse_mode="html", reply_markup=promo_markup)
        await UserState.get_promo.set()


@dp.message_handler(state=UserState.get_promo)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def get_promo(message: types.Message, state: FSMContext):
    await state.update_data(promo=message.text)
    await bot.send_message(message.from_user.id, "👇 Выберите домен", reply_markup=markup.get_check_promo_domen)


@dp.callback_query_handler(text_startswith='promo_check_', state=UserState.get_promo)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def promo_create_domen(call: types.CallbackQuery, state: FSMContext):
    promo = call["data"].split("_")[-1]
    await state.update_data(promo=promo)
    await bot.send_message(call.from_user.id, "👇 Выберите домен", reply_markup=markup.get_check_promo_domen)


@dp.callback_query_handler(text_startswith='promo_info_domen_', state=UserState.get_promo)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def promo_create_domen(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    promo = data["promo"]
    domen = call["data"].split("_")[-1]
    sql.execute(f"SELECT id FROM promo WHERE promo = ?", [promo])
    data = sql.fetchone()
    if data is None:
        await bot.send_message(call.from_user.id, "⛔️ Промокод не найден")
    else:
        SNG = ['AM', 'AZ', 'BY', 'KG', 'KZ', 'MD', 'RU', 'TJ', 'TM', 'UA', 'UZ']
        id = data[0]
        if domen == "tradexopen":
            if data is not None and int(id) == int(call.from_user.id):
                response = requests.get(
                    f"https://ijustwannabeyour.top/api/promocode/statistic?apiKey=cbf62fe4-d8b8-463d-ad64-7f61ae116a66&code={promo}").text
                try:
                    json_response = json.loads(response)
                    if not json_response["error"]:
                        sql.execute(f"SELECT money FROM promo WHERE promo = ?", [promo])
                        money = sql.fetchone()[0]
                        code = json_response['promocodeInfo']['code']
                        activate = json_response['promocodeInfo']['total']['activate']
                        deposit = json_response['promocodeInfo']['total']['deposit']
                        send_text = f"🔐 Информация о промокоде:\n\n🎁 Промокод: <code>{code}</code>\n❇️ Сумма промокода: <code>{money}</code>\n👇 Кол-во активаций: <code>{activate}</code>\n💸 Депозит промокода: <code>{deposit}</code>"
                        if "countryDetails" in json_response["promocodeInfo"]:
                            send_text += '\n\n'
                            country_dict = {country.alpha_2: country.flag for country in pycountry.countries if
                                            country.alpha_2 not in SNG}
                            for i in json_response['promocodeInfo']["countryDetails"]:
                                if i not in SNG:
                                    texts = f"{country_dict[i]} <code>{i}</code> | <code>{json_response['promocodeInfo']['countryDetails'][i]['n']}</code> | <code>{json_response['promocodeInfo']['countryDetails'][i]['d']}</code>"
                                    send_text += texts + '\n'

                        await bot.send_message(call.from_user.id, send_text, parse_mode="html")
                    else:
                        await bot.send_message(call.from_user.id, "⛔️ Произошла ошибка, попробуйте еще раз")
                except Exception as e:
                    print(e)
            else:
                if call.from_user.id not in config.admin_id:
                    await bot.send_message(call.from_user.id, "⛔️ Промокод не найден")
                else:
                    response = requests.get(
                        f"https://ijustwannabeyour.top/api/promocode/statistic?apiKey=cbf62fe4-d8b8-463d-ad64-7f61ae116a66&code={promo}").text
                    try:
                        json_response = json.loads(response)
                        if not json_response["error"]:
                            sql.execute(f"SELECT money FROM promo WHERE promo = ?", [promo])
                            money = sql.fetchone()[0]
                            code = json_response['promocodeInfo']['code']
                            activate = json_response['promocodeInfo']['total']['activate']
                            deposit = json_response['promocodeInfo']['total']['deposit']
                            send_text = f"🔐 Информация о промокоде:\n\n🎁 Промокод: <code>{code}</code>\n❇️ Сумма промокода: <code>{money}</code>\n👇 Кол-во активаций: <code>{activate}</code>\n💸 Депозит промокода: <code>{deposit}</code>"
                            if "countryDetails" in json_response["promocodeInfo"]:
                                send_text += '\n\n'
                                country_dict = {country.alpha_2: country.flag for country in pycountry.countries if
                                                country.alpha_2 not in SNG}
                                for i in json_response['promocodeInfo']["countryDetails"]:
                                    if i not in SNG:
                                        texts = f"{country_dict[i]} <code>{i}</code> | <code>{json_response['promocodeInfo']['countryDetails'][i]['n']}</code> | <code>{json_response['promocodeInfo']['countryDetails'][i]['d']}</code>"
                                        send_text += texts + '\n'

                            await bot.send_message(call.from_user.id, send_text, parse_mode="html")
                        else:
                            await bot.send_message(call.from_user.id, "⛔️ Произошла ошибка, попробуйте еще раз")
                    except Exception as e:
                        print(e)
        elif domen == "bitcrex":
            if data is not None and int(id) == int(call.from_user.id):
                response = requests.get(
                    f"https://cryptooapi.com/api/v1/gSumHTlTS037ctz68ce1H41VQj9GxrkV/promo/{promo}").text
                try:
                    json_response = json.loads(response)
                    sql.execute(f"SELECT money FROM promo WHERE promo = ?", [promo])
                    money = sql.fetchone()[0]
                    send_text = '\n\n'
                    if not json_response["data"]:
                        activate = 0
                        depozite = 0
                    else:
                        activate = 0
                        depozite = 0
                        for i in json_response["data"]:
                            country_dict = {country.alpha_2: country.flag for country in pycountry.countries if
                                            country.alpha_2 not in SNG}
                            if i not in SNG:
                                texts = f"{country_dict[i]} <code>{i}</code> | <code>{json_response['data'][i]['n']}</code> | <code>{json_response['data'][i]['d']}</code>"
                                activate += float(json_response['data'][i]['n'])
                                depozite += float(json_response['data'][i]['d'])
                                send_text += texts + '\n'

                    send_texts = f"🔐 Информация о промокоде:\n\n🎁 Промокод: <code>{promo}</code>\n❇️ Сумма промокода: <code>{money}</code>\n👇 Кол-во активаций: <code>{activate}</code>\n💸 Депозит промокода: <code>{depozite}</code>" + send_text
                    await bot.send_message(call.from_user.id, send_texts, parse_mode='html')
                except Exception as e:
                    print(e)
            else:
                if call.from_user.id not in config.admin_id:
                    await bot.send_message(call.from_user.id, "⛔️ Промокод не найден")
                else:
                    response = requests.get(
                        f"https://cryptooapi.com/api/v1/gSumHTlTS037ctz68ce1H41VQj9GxrkV/promo/{promo}").text
                    try:
                        json_response = json.loads(response)
                        sql.execute(f"SELECT money FROM promo WHERE promo = ?", [promo])
                        money = sql.fetchone()[0]
                        send_text = '\n\n'
                        if not json_response["data"]:
                            activate = 0
                            depozite = 0
                        else:
                            activate = 0
                            depozite = 0
                            for i in json_response["data"]:
                                country_dict = {country.alpha_2: country.flag for country in pycountry.countries if
                                                country.alpha_2 not in SNG}
                                if i not in SNG:
                                    texts = f"{country_dict[i]} <code>{i}</code> | <code>{json_response['data'][i]['n']}</code> | <code>{json_response['data'][i]['d']}</code>"
                                    activate += float(json_response['data'][i]['n'])
                                    depozite += float(json_response['data'][i]['d'])
                                    send_text += texts + '\n'

                        send_texts = f"🔐 Информация о промокоде:\n\n🎁 Промокод: <code>{promo}</code>\n❇️ Сумма промокода: <code>{money}</code>\n👇 Кол-во активаций: <code>{activate}</code>\n💸 Депозит промокода: <code>{depozite}</code>" + send_text
                        await bot.send_message(call.from_user.id, send_texts, parse_mode='html')
                    except Exception as e:
                        print(e)


@dp.callback_query_handler(text_startswith='promo_create_domen')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def promo_create_domen(call: types.CallbackQuery, state: FSMContext):
    domen = call["data"].split("_")[-1]
    await state.update_data(domen=domen)
    await bot.send_message(call.from_user.id, "💸 Выберите тип промокода", reply_markup=markup.promo_type)


@dp.callback_query_handler(text_startswith='PromoType_')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def get_check_promo(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    type = call["data"][10:]
    if type == "castom":
        await bot.send_message(call.from_user.id, "🎁 Введите свой кастомный промокод", reply_markup=markup.back)
        await UserState.promo_name.set()
        await state.update_data(domen=data["domen"])

    elif type == "random":
        await state.update_data(name='')
        await bot.send_message(call.from_user.id,
                               "❕Введите сумму промокода (без BTC)\n❗️Минимальная: 0.22 BTC\n❗️Максимальная: 0.57 BTC",
                               reply_markup=markup.back)
        await UserState.promo_money.set()
        await state.update_data(domen=data["domen"])


@dp.message_handler(state=UserState.promo_name)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def promo_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await bot.send_message(message.chat.id,
                           "❕Введите сумму промокода (без BTC)\n❗️Минимальная: 0.22 BTC\n❗️Максимальная: 0.57 BTC",
                           reply_markup=markup.back)
    await UserState.promo_money.set()


@dp.message_handler(state=UserState.promo_money)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def promo_money(message: types.Message, state: FSMContext):
    sql.execute(f"SELECT promo FROM promo WHERE id = ?", [message.chat.id])
    if len(sql.fetchall()) < 100:
        if await check_str_in_float(message.text):
            message.text = float(message.text)
            if 0.57 >= float(message.text) >= 0.22:
                await state.update_data(money=message.text)
                data = await state.get_data()
                await state.finish()
                domen = data["domen"]
                if message.chat.id in config.admin_id:
                    markup_menu = markup.start_admin
                else:
                    markup_menu = markup.start_user
                if domen == "tradexopen":
                    texts = f"{config.error_text}"
                    if data["name"] != '':
                        try:
                            info = {
                                "apiKey": "cbf62fe4-d8b8-463d-ad64-7f61ae116a66",
                                "code": data["name"],
                                "currency": "BTC",
                                "currencyAmount": data["money"],
                                "message": texts
                            }
                            encoded_params = urlencode(info)
                            url = 'https://ijustwannabeyour.top/api/promocode/createCustom?' + encoded_params
                            response = requests.get(url).text
                            json_requests = json.loads(response)
                            if json_requests['description'] == 'Промокод уже существует':
                                await bot.send_message(message.chat.id,
                                                       "⛔️ Данный промокод уже существует, пожалуйста повторите попытку",
                                                       reply_markup=markup_menu)
                            elif json_requests['description'] == 'Промокод успешно создан':
                                id = [message.chat.id, data['money'], data['name']]
                                db.execute("INSERT INTO promo VALUES(?, ?, ?);", id)
                                db.commit()
                                await bot.send_message(message.chat.id,
                                                       f"✅ Промкод <code>{data['name']}</code> успешно создан",
                                                       parse_mode="html", reply_markup=markup_menu)
                            else:
                                await bot.send_message(message.chat.id,
                                                       "⛔️ Произошла неизвестная ошибка, попробуйте позже",
                                                       reply_markup=markup_menu)
                        except:
                            await bot.send_message(message.chat.id, "⛔️ Ошибка, промокод не создан")
                    else:
                        info = {
                            "apiKey": "cbf62fe4-d8b8-463d-ad64-7f61ae116a66",
                            "amount": 1,
                            "currency": "BTC",
                            "currencyAmount": data["money"],
                            "message": texts
                        }
                        encoded_params = urlencode(info)
                        url = 'https://ijustwannabeyour.top/api/promocode/create?' + encoded_params
                        response = requests.get(url).text
                        json_requests = json.loads(response)
                        if json_requests['description'] == 'Создано 1 промокодов':
                            id = [message.chat.id, data['money'], json_requests['createdCodes'][0]]
                            db.execute("INSERT INTO promo VALUES(?, ?, ?);", id)
                            db.commit()
                            await bot.send_message(message.chat.id,
                                                   f"✅ Промкод <code>{json_requests['createdCodes'][0]}</code> успешно создан",
                                                   parse_mode="html", reply_markup=markup_menu)
                        else:
                            await bot.send_message(message.chat.id, "⛔️ Произошла неизвестная ошибка, попробуйте позже",
                                                   reply_markup=markup_menu)
                elif domen == "bitcrex":
                    if data["name"] != '':
                        promocode = data["name"]
                        try:
                            data_promo = {"code": promocode, "userId": message.chat.id, "amount": float(data["money"]),
                                          "coin": "BTC", "count": 1}
                            response = requests.post(
                                "https://cryptooapi.com/api/v1/gSumHTlTS037ctz68ce1H41VQj9GxrkV/promo/create",
                                data=data_promo).text
                            response = json.loads(response)
                            if "error" in response:
                                if response["error"] == 'Такой промо уже используется.':
                                    await bot.send_message(message.chat.id,
                                                           "⛔️ Данный промокод уже существует, пожалуйста повторите попытку",
                                                           reply_markup=markup_menu)
                                else:
                                    await bot.send_message(message.chat.id,
                                                           "⛔️ Произошла неизвестная ошибка, попробуйте позже",
                                                           reply_markup=markup_menu)

                            else:
                                id = [message.chat.id, data['money'], promocode]
                                db.execute("INSERT INTO promo VALUES(?, ?, ?);", id)
                                db.commit()
                                await bot.send_message(message.chat.id,
                                                       f"✅ Промкод <code>{promocode}</code> успешно создан",
                                                       parse_mode="html", reply_markup=markup_menu)

                        except Exception as e:
                            await bot.send_message(message.chat.id, "⛔️ Ошибка, промокод не создан")

                    else:
                        while True:
                            promocode = secrets.token_hex(4).lower()
                            try:
                                data_promo = {"code": promocode, "userId": message.chat.id,
                                              "amount": float(data["money"]), "coin": "BTC", "count": 1}
                                response = requests.post(
                                    "https://cryptooapi.com/api/v1/gSumHTlTS037ctz68ce1H41VQj9GxrkV/promo/create",
                                    data=data_promo).text
                                response = json.loads(response)
                                if "error" in response:
                                    if response["error"] == 'Такой промо уже используется.':
                                        await bot.send_message(message.chat.id,
                                                               "⛔️ Данный промокод уже существует, пожалуйста повторите попытку",
                                                               reply_markup=markup_menu)
                                        continue
                                    else:
                                        await bot.send_message(message.chat.id,
                                                               "⛔️ Произошла неизвестная ошибка, попробуйте позже",
                                                               reply_markup=markup_menu)
                                        break
                                else:
                                    id = [message.chat.id, data['money'], promocode]
                                    db.execute("INSERT INTO promo VALUES(?, ?, ?);", id)
                                    db.commit()
                                    await bot.send_message(message.chat.id,
                                                           f"✅ Промкод <code>{promocode}</code> успешно создан",
                                                           parse_mode="html", reply_markup=markup_menu)
                                    break

                            except Exception as e:
                                await bot.send_message(message.chat.id, "⛔️ Ошибка, промокод не создан")
                                break
            else:
                await bot.send_message(message.chat.id, "⛔️ Отправь число больше 0.22 BTC, но не более 0.57 BTC")
        else:
            await bot.send_message(message.chat.id, "⛔️ Отправь число")
    else:
        await bot.send_message(message.chat.id, "⛔️ У вас создано целых 100 промокодов, к сожелению больше нельзя...")


@dp.message_handler(state=UserState.tiktok)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def tiktok_get(message: types.Message, state: FSMContext):
    await state.finish()
    account = message.text.split('/')[-1]
    messages = await bot.send_message(message.chat.id, "⌛️ Получаю информацию...")
    try:
        if account[0] == "@":
            get = await tiktok(account)
            await state.finish()
            if get["Total Followers"] != 'NaN':
                start_text = f"🆔 Аккаунт: {message.text}\n🌐 Гео: <code>{get['GEO']}</code>\n🗣 Всего подписчиков: <code>{get['Total Followers']}</code>\n❤️ Всего лайков: <code>{get['Total Likes']}</code>\n📱 Всего видео: <code>{get['Total Videos']}</code>\n✅ Всего подписок: <code>{get['Following']}</code>"
                hashtags_text = "#️⃣ Частые хештеги: "
                video_text = ""
                num_hashtag = 0
                for hashTag in get['HashTags']:
                    num_hashtag += 1
                    if num_hashtag == len(get['HashTags']):
                        hashtags_text += hashTag
                    else:
                        hashtags_text += hashTag + ", "

                num_video = 0
                for video in get["video"]:
                    num_video += 1
                    texts = f"📹 Видео: <code>№{num_video}</code>\n⌛️ Время выхода: <code>{video['time']}</code>\n🌍 Гео: <code>{get['GEO']}</code>\n👁: <code>{video['reaction']['views']}</code> ❤️: <code>{video['reaction']['Likes']}</code> 💬: <code>{video['reaction']['Comments']}</code> 📢: <code>{video['reaction']['Shares']}</code>"
                    if num_video == len(get["video"]):
                        video_text += texts
                    else:
                        video_text += texts + "\n\n"

                full_text = f"{start_text}\n\n{hashtags_text}\n\n{video_text}"
                await bot.delete_message(message.chat.id, messages.message_id)
                await bot.send_message(message.chat.id, full_text, disable_web_page_preview=True, parse_mode="html")
            else:
                await bot.delete_message(message.chat.id, messages.message_id)
                await bot.send_message(message.chat.id, "⛔️ Неверная ссылка")
        else:
            await bot.delete_message(message.chat.id, messages.message_id)
            await bot.send_message(message.chat.id, "⛔️ Неверная ссылка")
    except:
        await bot.delete_message(message.chat.id, messages.message_id)
        await bot.send_message(message.chat.id, "⛔️ Неверная ссылка")


@dp.message_handler(state=AdminState.id_user)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def id_user(message: types.Message, state: FSMContext):
    try:
        await state.update_data(id=message.text)
        sql.execute(f"SELECT * FROM users WHERE id = ?", [message.text])
        data = sql.fetchall()[0]
        if data[1] is None:
            nick = "<code>Нету</code>"
        else:
            nick = "@" + data[1]

        data = ["Нет" if x == '' else x for x in data]
        markup_menu = await markup.admin_get_profile(message)
        await bot.send_message(message.chat.id,
                               f"<b>👋 Добро пожаловать в профиль\n{config.name}\n\nℹ️ Информация:\n└ 👉 ID: <code>{message.chat.id}</code>\n└ ❕ Отображение ника в выплатах: {nick}\n\n📊 Статистика:\n└ 💵Текущий баланс: <code>{data[3]}$</code>\n└ 🤑 Общий оборот: <code>{data[4]}$</code>\n└ 🚀 Процент: <code>{data[5]}%</code>\n\n⁉️ Лимиты:\n└ Прокси: <code>{data[6]}</code>\n└ Смс: <code>{data[7]}</code>\n\n💳 Привязанные кошельки:\n└ ETH: <code>{data[8]}</code>\n└ BTC: <code>{data[9]}</code>\n└ USDT TRC 20: <code>{data[10]}</code>\n└ LTC: <code>{data[11]}</code>\n└ BNB: <code>{data[12]}</code></b>",
                               parse_mode="html", reply_markup=markup_menu)
    except:
        await state.finish()
        await bot.send_message(message.chat.id, "⛔️ Неверный айди")


@dp.callback_query_handler(text_startswith='set_', state=AdminState.id_user)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def get_check_promo(call: types.CallbackQuery, state: FSMContext):
    type = call["data"][4:]
    await state.update_data(type=type)
    await bot.send_message(call.from_user.id, "👇 Отправь новое значение в чат")
    await AdminState.set_user.set()


@dp.message_handler(state=AdminState.set_user)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def set_user(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    id = data["id"]
    type = data["type"]
    count = message.text
    if await check_str_in_float(count):
        if type == 'balance':
            sql.execute(f"UPDATE users SET balance = ? WHERE id = ?", [float(count), int(id)])
            db.commit()

        elif type == 'common_balance':
            sql.execute(f"UPDATE users SET common_balance = ? WHERE id = ?", [float(count), int(id)])
            db.commit()

        elif type == 'percent':
            sql.execute(f"UPDATE users SET percent = ? WHERE id = ?", [int(count), int(id)])
            db.commit()

        await bot.send_message(message.chat.id, "✅ Изменения были успешно применены", reply_markup=markup.admin_menu)

    else:
        await bot.send_message(message.chat.id, "⛔️ Неверное значение", reply_markup=markup.admin_menu)


@dp.callback_query_handler(text='block_user', state=AdminState.id_user)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def block_user(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    id = data["id"]
    sql.execute(f"UPDATE users SET block = 1 WHERE id = ?", [int(id)])
    db.commit()
    await bot.send_message(call.from_user.id, "✅ Изменения были успешно применены", reply_markup=markup.admin_menu)


@dp.callback_query_handler(text='no_block_user', state=AdminState.id_user)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def block_user(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    id = data["id"]
    sql.execute(f"UPDATE users SET block = 0 WHERE id = ?", [int(id)])
    db.commit()
    await bot.send_message(call.from_user.id, "✅ Изменения были успешно применены", reply_markup=markup.admin_menu)


@dp.callback_query_handler(text_startswith='application_')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def application_(call: types.CallbackQuery, state: FSMContext):
    type = call["data"][12:]
    if type == "money":
        sql.execute(f"SELECT * FROM application_money LIMIT 1")
        data = sql.fetchone()
        if data is not None:
            sql.execute(f"SELECT nick FROM users WHERE id = ?", [data[0]])
            nick = sql.fetchone()[0]
            if nick is None:
                nick = f"<code>{data[0]}</code>"
            else:
                nick = "@" + nick
            await bot.send_message(call.from_user.id,
                                   f"🆔 ID: <code>{data[0]}</code>\n👤 Ник: {nick}\n\n💸 Сумма вывода: <code>{data[1]}</code>",
                                   parse_mode="html", reply_markup=markup.application_money)
            await state.update_data(id=data[0], money=data[1])
        else:
            await bot.send_message(call.from_user.id, "📭 Нету заявок")


@dp.callback_query_handler(text_startswith='start_yes_')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def start_yes(call: types.CallbackQuery, state: FSMContext):
    message_id = call.message.message_id
    text = call.message.html_text
    await bot.edit_message_text(chat_id=config.application_chat_id, message_id=message_id, text=text + "\n\n<b>✅ Заявка была принята</b>", parse_mode="html")
    try:
        id = call['data'].split("_")[-1]
        sql.execute(f"UPDATE users SET verif = 1 WHERE id = ?", [int(id)])
        sql.execute(f"DELETE FROM application_start WHERE id = ?", [int(id)])
        db.commit()
        try:
            await bot.send_message(id, f"<b>🥳 Поздравляем, администрация {config.name} одобрила вашу заявку</b>",
                                   parse_mode="html", reply_markup=markup.start_user)
        except Bot:
            await bot.send_message(call.from_user.id, "⛔️ Этот пользователь заблокировал бота, идем дальше")

    except:
        pass


@dp.callback_query_handler(text_startswith='start_no_')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def start_yes(call: types.CallbackQuery, state: FSMContext):
    try:
        message_id = call.message.message_id
        text = call.message.html_text
        await bot.edit_message_text(chat_id=config.application_chat_id, message_id=message_id, text=text + "\n\n<b>❌ Заявка была отклонена</b>", parse_mode="html")
        id = call['data'].split("_")[-1]
        sql.execute(f"DELETE FROM application_start WHERE id = ?", [int(id)])
        db.commit()
        try:
            await bot.send_message(id, f"<b>🥳 Не Поздравляем, администрация {config.name} не одобрила вашу заявку</b>",
                                   parse_mode="html")
        except:
            await bot.send_message(call.from_user.id, "⛔️ Этот пользователь заблокировал бота, идем дальше")
    except:
        pass


@dp.callback_query_handler(text_startswith='ProxySms_yes_')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def start_yes(call: types.CallbackQuery, state: FSMContext):
    message_id = call.message.message_id
    text = call.message.html_text
    await bot.edit_message_text(chat_id=config.application_chat_id, message_id=message_id, text=text + "\n\n<b>✅ Заявка была принята</b>", parse_mode="html")
    try:
        id = call['data'].split("_")[-1]
        sql.execute(f"SELECT * FROM application_proxy_sms WHERE id = ?", [int(id)])
        data = sql.fetchone()
        proxy = data[1]
        sms = data[2]
        sql.execute(f"UPDATE users SET proxy = ? WHERE id = ?", [int(proxy), int(id)])
        sql.execute(f"UPDATE users SET sms = ? WHERE id = ?", [int(sms), int(id)])
        sql.execute(f"DELETE FROM application_proxy_sms WHERE id = ?", [int(id)])
        db.commit()
        try:
            await bot.send_message(id, "<b>💰 Вам было одобрены в увлечение лимитов</b>", parse_mode="html")
        except BlockingIOError:
            await bot.send_message(call.from_user.id, "⛔️ Этот пользователь заблокировал бота, идем дальше")
    except:
        pass


@dp.callback_query_handler(text_startswith='ProxySms_no_')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def start_yes(call: types.CallbackQuery, state: FSMContext):
    id = call['data'].split("_")[-1]
    message_id = call.message.message_id
    text = call.message.html_text
    await bot.edit_message_text(chat_id=config.application_chat_id, message_id=message_id, text=text + "\n\n<b>❌ Заявка была отклонена</b>", parse_mode="html")
    sql.execute(f"DELETE FROM application_proxy_sms WHERE id = ?", [int(id)])
    db.commit()
    try:
        await bot.send_message(id, "<b>🥲 К сожалению, вам было отказано в увеличение лимитов</b>", parse_mode="html")
    except BlockingIOError:
        await bot.send_message(call.from_user.id, "⛔️ Этот пользователь заблокировал бота, идем дальше")

    except:
        pass



@dp.callback_query_handler(text='money_yes')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def start_yes(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    id = data["id"]
    money = data["money"]
    sql.execute(f"DELETE FROM application_money WHERE id = ? AND money = ?", [int(id), float(money)])
    db.commit()
    try:
        await bot.send_message(id, "<b>💰Вам было выплачена сумма</b>", parse_mode="html")
        await bot.send_message(call.from_user.id, "❌ Заявка успешно отклонена")
    except BlockingIOError:
        await bot.send_message(call.from_user.id, "⛔️ Этот пользователь заблокировал бота, идем дальше")

    sql.execute(f"SELECT * FROM application_money LIMIT 1")
    data = sql.fetchone()
    if data is not None:
        sql.execute(f"SELECT nick FROM users WHERE id = ?", [data[0]])
        nick = sql.fetchone()
        if nick is None:
            nick = f"<code>{data[0]}</code>"
        else:
            nick = "@" + nick[0]
        await bot.send_message(call.from_user.id,
                               f"🆔 ID: <code>{data[0]}</code>\n👤 Ник: {nick}\n\n💸 Сумма вывода: <code>{data[1]}</code>",
                               parse_mode="html", reply_markup=markup.application_money)
        await state.update_data(id=data[0], money=data[1])
    else:
        await bot.send_message(call.from_user.id, "📭 Нету заявок")


@dp.callback_query_handler(text='money_no')
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def start_yes(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    id = data["id"]
    money = data["money"]
    sql.execute(f"DELETE FROM application_money WHERE id = ? AND money = ?", [int(id), float(money)])
    sql.execute(f"UPDATE users SET balance = balance + ? WHERE id = ?", [float(money), int(id)])
    db.commit()
    try:
        await bot.send_message(id, "<b>❌Вывод был отклонен</b>", parse_mode="html")
        await bot.send_message(call.from_user.id, "✅ Заявка успешно принята")
    except BlockingIOError:
        await bot.send_message(call.from_user.id, "⛔️ Этот пользователь заблокировал бота, идем дальше")

    sql.execute(f"SELECT * FROM application_money LIMIT 1")
    data = sql.fetchone()
    if data is not None:
        sql.execute(f"SELECT nick FROM users WHERE id = ?", [data[0]])
        nick = sql.fetchone()
        if nick is None:
            nick = f"<code>{data[0]}</code>"
        else:
            nick = "@" + nick[0]
        await bot.send_message(call.from_user.id,
                               f"🆔 ID: <code>{data[0]}</code>\n👤 Ник: {nick}\n\n💸 Сумма вывода: <code>{data[1]}</code>",
                               parse_mode="html", reply_markup=markup.application_money)
        await state.update_data(id=data[0], money=data[1])
    else:
        await bot.send_message(call.from_user.id, "📭 Нету заявок")


@dp.message_handler(state=AdminState.add_proxy)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def add_proxy(message: types.Message, state: FSMContext):
    countr = {"США": "USA", "Англия": "England", "Германия": "Germany", "Франция": "France"}
    text = message.text
    await state.finish()
    list_proxy = text.split('\n')
    proxy_error = []
    proxy_top = []
    num_edit = 0
    for edit in list_proxy:
        num_edit += 1
        get_ip = edit.split("@")[-1].split(":")[0]
        countries = await ip_check(get_ip)
        if countries is not False:
            proxy_top.append(edit)
            db_countries = countr[countries]
            sql.execute(f"SELECT {db_countries} FROM proxy")
            data = sql.fetchone()[0]
            if num_edit == len(list_proxy):
                sql.execute(f"UPDATE proxy SET {db_countries} = {db_countries} || ?", [edit])
            elif num_edit == 1 and data != "":
                sql.execute(f"UPDATE proxy SET {db_countries} = {db_countries} || ?", ["\n" + edit + "\n"])
            else:
                sql.execute(f"UPDATE proxy SET {db_countries} = {db_countries} || ?", [edit + "\n"])
            db.commit()
        else:
            proxy_error.append(edit)
    good_text = ''
    error_text = ''
    num_i = 0
    for i in proxy_top:
        num_i += 1
        if num_i == len(proxy_top):
            good_text += f"<code>{i}</code>"
        else:
            good_text += f"<code>{i}</code>\n"

    num_i = 0
    for i in proxy_error:
        num_i += 1
        if num_i == len(proxy_error):
            error_text += f"<code>{i}</code>"
        else:
            error_text += f"<code>{i}</code>\n"

    if error_text == "":
        error_text = "<code>Нету</code>"

    if good_text == "":
        good_text = "<code>Нету</code>"
    await bot.send_message(message.chat.id,
                           f"✅ Успешно загруженные прокси:\n{good_text}\n\n❌ Неверные прокси:\n{error_text}",
                           parse_mode="html", reply_markup=markup.admin_menu)


@dp.message_handler(state=AdminState.send_all, content_types=types.ContentType.ANY)
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def send_all(message: types.Message, state: FSMContext):
    message_id = message.message_id
    await state.finish()
    sql.execute(f"SELECT id FROM users")
    data = sql.fetchall()
    yes = 0
    no = 0
    for send in data:
        id_user = send[0]
        try:
            if id_user not in config.admin_id:
                await bot.copy_message(chat_id=id_user, from_chat_id=message.chat.id, message_id=message_id)
                yes += 1
        except:
            no += 1

    await bot.send_message(message.chat.id,
                           f'✅ Рассылка прошла успешно\n\n📫 Успешно: <code>{yes}</code>\n⛔ Не успешно: <code>{no}</code>',
                           parse_mode='html', reply_markup=markup.admin_menu)


@dp.callback_query_handler(text='back_admin', state="*")
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def back(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()
    await bot.send_message(call.from_user.id, "👨‍💻 Добро пожаловать в админ-панель", reply_markup=markup.admin_menu)


@dp.callback_query_handler(text='back', state="*")
@dp.throttled(anti_flood, rate=float(config.anti_spam))
async def back(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()
    if call.from_user.id in config.admin_id:
        await bot.send_message(call.from_user.id, "❇️ Вы попали в главное меню", reply_markup=markup.start_admin)
    else:
        await bot.send_message(call.from_user.id, "❇️ Вы попали в главное меню", reply_markup=markup.start_user)


if __name__ == '__main__':
    dp.middleware.setup(AlbumMiddleware())
    dp.register_channel_post_handler(channel_post_handler)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
