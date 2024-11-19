import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import config
import datetime
import functions
import markup
from io import BytesIO
import io
from PIL import Image

storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)

db = sqlite3.connect('data.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER,
        date_start TIMESTAMP,
        count_kreo INTEGER
        )""")
db.commit()

class UserState(StatesGroup):
    photo_kreo = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    sql.execute(f"SELECT id FROM users WHERE id = {message.chat.id}")
    data = sql.fetchone()
    if data is None:
        id = [message.chat.id, datetime.datetime.now().date(), 0]
        db.execute("INSERT INTO users VALUES(?, ?, ?);", id)
        db.commit()

    sub = await functions.check_sub_channel(message.chat.id)
    if sub is not True:
        markup_for_message = await markup.sub_channel(sub)
        await bot.send_message(message.chat.id, "Для работы с ботом нужно подписаться на каналы ❗️", reply_markup=markup_for_message)
    else:
        await bot.send_message(message.chat.id, "🌟 Приятного пользования", reply_markup=markup.start_user)

@dp.message_handler(content_types=["text"])
async def text(message: types.Message, state: FSMContext):
    if message.text == "🔥 Крео":
        await bot.send_message(message.chat.id, "👇 Отправьте скриншот телеграмм канала")
        await UserState.photo_kreo.set()


@dp.message_handler(state=UserState.photo_kreo, content_types='photo')
async def photo_kreo(message: types.Message, state: FSMContext):
    with BytesIO() as io_obj:
        photo = message.photo[-1]
        await photo.download(io_obj)
        image = Image.open(io_obj)

        Finish_Photo = await functions.set_rand_background(image)
        image = await functions.unique_image(Finish_Photo)
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        three_photo = img_byte_array

    one_photo = await functions.add_text_to_image(config.one_photo)
    one_photo_img_byte_array = io.BytesIO()
    one_photo.save(one_photo_img_byte_array, format='PNG')
    one_photo_img_byte_array.seek(0)
    await bot.send_photo(message.chat.id, photo=one_photo_img_byte_array)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)