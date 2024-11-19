from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import config
from main import sql

yes_start = KeyboardButton("📩 Да, хочу подать заявку")
start_new_user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(yes_start)

profile = KeyboardButton("🙎‍♂ ️Мой профиль")
tools_work = KeyboardButton("⚙️ Инструменты для работы")
domen = KeyboardButton("⚡️ Актуальный домен")
check = KeyboardButton("📊 Чекер")
top_user = KeyboardButton("⚔️ Топ пользователей")
info = KeyboardButton("📄 Инфо")
mentors = KeyboardButton("💸 Наставники")
start_user = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(profile, tools_work, domen, check, top_user, mentors, info)

admin = KeyboardButton("👨‍💻 Админ панель")
start_admin = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(profile, tools_work, domen, check, top_user, mentors, info).row(admin)

admin_menu_user = KeyboardButton("👤 Пользователи")
admin_menu_application = KeyboardButton("👨‍💻 Заявки")
admin_menu_proxy = KeyboardButton("📨 Добавить Прокси")
admin_menu_send = KeyboardButton("🗣 Рассылка")
admin_menu_other = KeyboardButton("⏏️ Другое")
admin_menu_back = KeyboardButton("↩️ Вернуться")
admin_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(admin_menu_user, admin_menu_application, admin_menu_proxy, admin_menu_send).row(admin_menu_other).row(admin_menu_back)

admin_other_menu = InlineKeyboardMarkup(row_width=1)
admin_other_menu.insert(InlineKeyboardButton(text='🔄 Сбросить процент', callback_data='reset_percentages'))
admin_other_menu.insert(InlineKeyboardButton(text='❇️ Сбросить всем лимиты', callback_data='reset_limits'))
admin_other_menu.insert(InlineKeyboardButton(text='⚡️ Наставники', callback_data='admin_mentors'))

admin_mentors = InlineKeyboardMarkup(row_width=1)
admin_mentors.insert(InlineKeyboardButton(text='✅ Добавить', callback_data='mentors_add'))
admin_mentors.insert(InlineKeyboardButton(text='❌ Удалить', callback_data='mentors_delete'))

tools = InlineKeyboardMarkup(row_width=2)
tools.insert(InlineKeyboardButton(text='🔗 Получить прокси', callback_data='get_proxy'))
tools.insert(InlineKeyboardButton(text='📱 Получить номер', callback_data='get_number'))
tools.insert(InlineKeyboardButton(text='📄 Генератор тегов', callback_data='generator_tag'))
tools.insert(InlineKeyboardButton(text='⚙ ️Материалы', callback_data='get_materials'))
tools.insert(InlineKeyboardButton(text='✏️ Отрисовщик', callback_data='draw'))
tools.insert(InlineKeyboardButton(text='🌟️ Уникализация', callback_data='unic'))
tools.insert(InlineKeyboardButton(text='🖥 Промокоды', callback_data='get_check_promo'))

materials = InlineKeyboardMarkup(row_width=2)
materials.row(InlineKeyboardButton(text='#️⃣ Теги', callback_data='tags'))
materials.row(InlineKeyboardButton(text='👩 Girls', callback_data='girls'))
materials.insert(InlineKeyboardButton(text='🔥 Крео', callback_data='kreo'))
materials.row(InlineKeyboardButton(text='◀️ Назад', callback_data='back'))

info_menu = InlineKeyboardMarkup(row_width=3)
info_menu.insert(InlineKeyboardButton(text='💬 Чат', url=config.chat))
info_menu.insert(InlineKeyboardButton(text='💰 Выплаты', url=config.money))
info_menu.insert(InlineKeyboardButton(text='📃 Мануал', url=config.manual))
info_menu.insert(InlineKeyboardButton(text='🆘 Поддержка', url=config.help))
info_menu.insert(InlineKeyboardButton(text='💸 Отзывы', url=config.feedback))
info_menu.insert(InlineKeyboardButton(text='❗️ Инфо', url=config.info))

get_proxy = InlineKeyboardMarkup(row_width=1)
get_proxy.insert(InlineKeyboardButton(text='🌐 Сервис №1 (от 0$)', callback_data='service_proxy'))
get_proxy.insert(InlineKeyboardButton(text='🕊 faceless (от 0$)', callback_data='requests_proxy'))

requests_proxy_countries = InlineKeyboardMarkup(row_width=3)
requests_proxy_countries.insert(InlineKeyboardButton(text='🇵🇹 Portugal', callback_data='requests_proxy_Portugal'))
requests_proxy_countries.insert(InlineKeyboardButton(text='🇫🇷 France', callback_data='requests_proxy_France'))
requests_proxy_countries.insert(InlineKeyboardButton(text='🇬🇧 United Kingdom', callback_data='requests_proxy_United Kingdom'))
requests_proxy_countries.insert(InlineKeyboardButton(text='🇲🇽 Mexico', callback_data='requests_proxy_Mexico'))
requests_proxy_countries.insert(InlineKeyboardButton(text='🇳🇱 Netherlands', callback_data='requests_proxy_Netherlands'))
requests_proxy_countries.insert(InlineKeyboardButton(text='🇭🇺 Hungary', callback_data='requests_proxy_Hungary'))
requests_proxy_countries.insert(InlineKeyboardButton(text='🇨🇭 Switzerland', callback_data='requests_proxy_Switzerland'))
requests_proxy_countries.insert(InlineKeyboardButton(text='🇺🇸 United States', callback_data='requests_proxy_United States'))
requests_proxy_countries.insert(InlineKeyboardButton(text='🇳🇿 New Zealand', callback_data='requests_proxy_New Zealand'))
requests_proxy_countries.insert(InlineKeyboardButton(text='🇦🇺 Australia', callback_data='requests_proxy_Australia'))
requests_proxy_countries.insert(InlineKeyboardButton(text='🇷🇴 Romania', callback_data='requests_proxy_Romania'))
requests_proxy_countries.insert(InlineKeyboardButton(text='🇸🇪 Sweden', callback_data='requests_proxy_Sweden'))
requests_proxy_countries.insert(InlineKeyboardButton(text='🇦🇹 Austria', callback_data='requests_proxy_Austria'))
requests_proxy_countries.insert(InlineKeyboardButton(text='🇩🇪 Germany', callback_data='requests_proxy_Germany'))

get_proxy_countries = InlineKeyboardMarkup(row_width=3)
get_proxy_countries.insert(InlineKeyboardButton(text='Англия', callback_data='proxy_England'))
get_proxy_countries.insert(InlineKeyboardButton(text='Франция', callback_data='proxy_France'))
get_proxy_countries.insert(InlineKeyboardButton(text='Германия', callback_data='proxy_Germany'))
get_proxy_countries.insert(InlineKeyboardButton(text='США', callback_data='proxy_USA'))

get_sms = InlineKeyboardMarkup(row_width=3)
get_sms.insert(InlineKeyboardButton(text='Канада', callback_data='sms_canada'))
get_sms.insert(InlineKeyboardButton(text='Англия', callback_data='sms_england'))

next_tag = InlineKeyboardMarkup(row_width=1)
next_tag.insert(InlineKeyboardButton(text='▶️ Пропустить', callback_data='next_tag'))

count_tag = InlineKeyboardMarkup(row_width=5)
count_tag.insert(InlineKeyboardButton(text='1️⃣', callback_data='tag_1'))
count_tag.insert(InlineKeyboardButton(text='2️⃣', callback_data='tag_2'))
count_tag.insert(InlineKeyboardButton(text='3️⃣', callback_data='tag_3'))
count_tag.insert(InlineKeyboardButton(text='4️⃣', callback_data='tag_4'))
count_tag.insert(InlineKeyboardButton(text='5️⃣', callback_data='tag_5'))

zelenka = InlineKeyboardMarkup(row_width=2)
zelenka.insert(InlineKeyboardButton(text='✏️ Указать', callback_data='url_zelenka'))
zelenka.insert(InlineKeyboardButton(text='😔 У меня нету профиля', callback_data='next_zelenka'))

proxy_sms = InlineKeyboardMarkup(row_width=2)
proxy_sms.insert(InlineKeyboardButton(text='✏️ Указать', callback_data='proxy_sms_yes'))
proxy_sms.insert(InlineKeyboardButton(text='❎ Не нужно', callback_data='proxy_sms_no'))

async def profile(message):
    profile_menu = InlineKeyboardMarkup(row_width=3)
    sql.execute(f"SELECT * FROM users WHERE id = ?", [message.from_user.id])
    data = sql.fetchall()[0]
    profile_menu.insert(InlineKeyboardButton(text='📎 Привязать кошелек', callback_data='connect_wallet'))
    profile_menu.insert(InlineKeyboardButton(text='💲 Вывести баланс', callback_data='withdraw_money'))
    if data[2] == 0:
        profile_menu.insert(InlineKeyboardButton(text='🕶 Показать тег', callback_data='on_tag'))
    else:
        profile_menu.insert(InlineKeyboardButton(text='🕶 Скрыть тег', callback_data='off_tag'))
    profile_menu.insert(InlineKeyboardButton(text='🖍 Поддержка', url=config.help))
    profile_menu.insert(InlineKeyboardButton(text='⚡️ Увеличить лимиты', callback_data='add_limit'))

    return profile_menu

async def gen_tag(message):
    promo_menu = InlineKeyboardMarkup(row_width=1)
    sql.execute(f"SELECT promo FROM promo WHERE id = ?", [message.from_user.id])
    for promo in sql.fetchall():
        promo_menu.insert(InlineKeyboardButton(text=promo[0], callback_data=f'promo_tags_{promo[0]}'))

    promo_menu.insert(InlineKeyboardButton(text="✏️ Свой текст", callback_data=f'promo_unique'))
    promo_menu.insert(InlineKeyboardButton(text="◀️ Назад", callback_data=f'back'))

    return promo_menu

async def get_markup_all_promo(message):
    promo_menu = InlineKeyboardMarkup(row_width=4)
    sql.execute(f"SELECT promo FROM promo WHERE id = ?", [message.from_user.id])
    for promo in sql.fetchall():
        promo_menu.insert(InlineKeyboardButton(text=promo[0], callback_data=f'promo_check_{promo[0]}'))

    promo_menu.row(InlineKeyboardButton(text="◀️ Назад", callback_data=f'back'))

    return promo_menu

async def mentors(data):
    mentors = InlineKeyboardMarkup(row_width=1)
    for i in data:
        mentors.insert(InlineKeyboardButton(text=i[0], callback_data=f'user_mentors_{i[0]}'))

    return mentors


async def mentors_applications(id):
    mentors = InlineKeyboardMarkup(row_width=1)
    mentors.insert(InlineKeyboardButton(text="📌 Подать заявку", callback_data=f'applications_mentors_{id}'))

    return mentors

async def mentors_delete(data):
    mentors = InlineKeyboardMarkup(row_width=1)
    for i in data:
        mentors.insert(InlineKeyboardButton(text=i[0], callback_data=f'MontersDelete_{i[0]}'))

    return mentors

async def gen_tag_next(promo, money):
    promo_menu = InlineKeyboardMarkup(row_width=5)
    if money is None:
        promo_menu.insert(InlineKeyboardButton(text="1", callback_data=f'gen_promo_num_{promo}_1'))
        promo_menu.insert(InlineKeyboardButton(text="2", callback_data=f'gen_promo_num_{promo}_2'))
        promo_menu.insert(InlineKeyboardButton(text="3", callback_data=f'gen_promo_num_{promo}_3'))
        promo_menu.insert(InlineKeyboardButton(text="4", callback_data=f'gen_promo_num_{promo}_4'))
        promo_menu.insert(InlineKeyboardButton(text="5", callback_data=f'gen_promo_num_{promo}_5'))
    else:
        promo_menu.insert(InlineKeyboardButton(text="1", callback_data=f'gen_promo_num_{promo}_1_{money}'))
        promo_menu.insert(InlineKeyboardButton(text="2", callback_data=f'gen_promo_num_{promo}_2_{money}'))
        promo_menu.insert(InlineKeyboardButton(text="3", callback_data=f'gen_promo_num_{promo}_3_{money}'))
        promo_menu.insert(InlineKeyboardButton(text="4", callback_data=f'gen_promo_num_{promo}_4_{money}'))
        promo_menu.insert(InlineKeyboardButton(text="5", callback_data=f'gen_promo_num_{promo}_5_{money}'))
    return promo_menu

async def mentors_yes_no_def(id):
    mentors_yes_no = InlineKeyboardMarkup(row_width=1)
    mentors_yes_no.insert(InlineKeyboardButton(text="✅ Принять", callback_data=f'appment_yes_{id}'))
    mentors_yes_no.insert(InlineKeyboardButton(text="❌ Отклонить", callback_data=f'appment_no_{id}'))
    return mentors_yes_no

async def mentors_rejection_def(name):
    mentors_rejection = InlineKeyboardMarkup(row_width=1)
    mentors_rejection.insert(InlineKeyboardButton(text="❌ Отказаться", callback_data=f'mentors_rejection_{name}'))
    return mentors_rejection

application_menu = InlineKeyboardMarkup(row_width=1)
application_menu.insert(InlineKeyboardButton(text='💸 На вывод', callback_data='application_money'))
application_menu.insert(InlineKeyboardButton(text='↩️ Вернуться', callback_data='back_admin'))

async def application_start(id):
    application_start = InlineKeyboardMarkup(row_width=1)
    application_start.insert(InlineKeyboardButton(text='✅ Принять', callback_data=f'start_yes_{id}'))
    application_start.insert(InlineKeyboardButton(text='❌️ Отклонить', callback_data=f'start_no_{id}'))
    return application_start

async def application_proxy_sms(id):
    application_proxy_sms = InlineKeyboardMarkup(row_width=1)
    application_proxy_sms.insert(InlineKeyboardButton(text='✅ Принять', callback_data=f'ProxySms_yes_{id}'))
    application_proxy_sms.insert(InlineKeyboardButton(text='❌️ Отклонить', callback_data=f'ProxySms_no_{id}'))
    return application_proxy_sms

application_money = InlineKeyboardMarkup(row_width=1)
application_money.insert(InlineKeyboardButton(text='✅ Принять', callback_data='money_yes'))
application_money.insert(InlineKeyboardButton(text='❌️ Отклонить', callback_data='money_no'))

application_proxy = InlineKeyboardMarkup(row_width=1)
application_proxy.insert(InlineKeyboardButton(text='❌️ Отклонить', callback_data='proxy_no'))

set_wallet = InlineKeyboardMarkup(row_width=3)
set_wallet.insert(InlineKeyboardButton(text='LTC', callback_data='set_LTC'))
set_wallet.insert(InlineKeyboardButton(text='BTC', callback_data='set_BTC'))
set_wallet.insert(InlineKeyboardButton(text='ETH', callback_data='set_ETH'))
set_wallet.insert(InlineKeyboardButton(text='USTD TRC', callback_data='set_USDT_TRC'))
set_wallet.insert(InlineKeyboardButton(text='BNB', callback_data='set_BNB'))

get_check_promo = InlineKeyboardMarkup(row_width=2)
get_check_promo.insert(InlineKeyboardButton(text='📄 Получить промокод', callback_data='promo_get'))
get_check_promo.insert(InlineKeyboardButton(text='🪧 Запросить информацию', callback_data='promo_get_info'))

get_check_promo_domen = InlineKeyboardMarkup(row_width=2)
get_check_promo_domen.insert(InlineKeyboardButton(text='Bitxmer', callback_data='promo_info_domen_tradexopen'))
get_check_promo_domen.insert(InlineKeyboardButton(text='Bitcrex', callback_data='promo_info_domen_bitcrex'))

get_create_promo_domen = InlineKeyboardMarkup(row_width=2)
get_create_promo_domen.insert(InlineKeyboardButton(text='Bitxmer', callback_data='promo_create_domen_tradexopen'))
get_create_promo_domen.insert(InlineKeyboardButton(text='Bitcrex', callback_data='promo_create_domen_bitcrex'))

promo_type = InlineKeyboardMarkup(row_width=2)
promo_type.insert(InlineKeyboardButton(text='Кастомный', callback_data='PromoType_castom'))
promo_type.insert(InlineKeyboardButton(text='Случайный', callback_data='PromoType_random'))

add_proxy = InlineKeyboardMarkup(row_width=2)
add_proxy.insert(InlineKeyboardButton(text='↩️ Вернуться', callback_data='back_admin'))
async def admin_get_profile(message):
    profile_menu = InlineKeyboardMarkup(row_width=1)
    sql.execute(f"SELECT block FROM users WHERE id = ?", [message.from_user.id])
    block = sql.fetchone()[0]
    profile_menu.insert(InlineKeyboardButton(text='💸 Изменить баланс', callback_data='set_balance'))
    profile_menu.insert(InlineKeyboardButton(text='🤑 Изменить общий оборот', callback_data='set_common_balance'))
    profile_menu.insert(InlineKeyboardButton(text='🚀 Изменить процент', callback_data='set_percent'))
    if block == 0:
        profile_menu.insert(InlineKeyboardButton(text='🚫 Заблокировать', callback_data='block_user'))
    else:
        profile_menu.insert(InlineKeyboardButton(text='✅ Разблокировать', callback_data='no_block_user'))
    profile_menu.insert(InlineKeyboardButton(text='↩️ Вернуться', callback_data='back_admin'))

    return profile_menu

back = InlineKeyboardMarkup(row_width=1)
back.insert(InlineKeyboardButton(text='↩️️ Вернуться', callback_data='back'))
