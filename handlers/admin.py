from aiogram import types
from misc import dp, bot
import sqlite3
from aiogram.dispatcher import FSMContext
from .sqlit import stata_user
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

ADMIN_ID_1 = 494588959 #Cаня
ADMIN_ID_2 = 44520977 #Коля
ADMIN_ID_3 = 941730379 #Бекир

ADMIN_ID =[ADMIN_ID_1,ADMIN_ID_2,ADMIN_ID_3]

class reg(StatesGroup):
    name = State()
    fname = State()

class reg0(StatesGroup):
    name0 = State()
    fname0 = State()

@dp.message_handler(commands=['admin'])
async def admin_ka(message: types.Message):
    id = message.from_user.id
    if id in ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='Трафик', callback_data='list_members')
        bat_b = types.InlineKeyboardButton(text='Рассылка, кто прошел квест', callback_data='write_message')
        bat_с = types.InlineKeyboardButton(text='Рассылка, кто не прошел квест', callback_data='write_message0')
        markup.add(bat_a)
        markup.add(bat_b)
        markup.add(bat_с)
        await bot.send_message(message.chat.id,'Выбери что хочешь сделать:',reply_markup=markup)


@dp.callback_query_handler(text='list_members')
async def admin_1(call: types.callback_query):
    status = stata_user()
    status0 = status[0]
    status1 = status[1]
    mes = await bot.send_message(call.message.chat.id, f'Всего пользователей: {status0+status1}\n\n'
                                                 f'Прошли квест: {status1}\n\n'
                                                 f'Еще не прошли квест: {status0}')
    await asyncio.sleep(10)
    await bot.delete_message(message_id=mes.message_id,chat_id=call.message.chat.id)



@dp.callback_query_handler(text='write_message')
async def rassilka (call:types.callback_query,state: FSMContext):
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА',callback_data='otemena')
    murkap.add(bat0)
    await bot.send_message(call.message.chat.id,'Перешли мне уже готовый пост и я разошлю тем кто прошел квест',reply_markup=murkap)
    await reg.name.set()


@dp.message_handler(state=reg.name,content_types=['text','photo','video','video_note'])
async def fname_step(message: types.Message, state: FSMContext):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    await state.finish()
    users = sql.execute("SELECT id FROM user_time WHERE status_ref = 1").fetchall()
    bad = 0
    good = 0
    await bot.send_message(message.chat.id,
                           f"<b>Всего пользователей: <code>{len(users)}</code></b>\n\n<b>Расслыка начата!</b>",
                           parse_mode="html")
    for i in users:
        await asyncio.sleep(1)
        try:
            await message.copy_to(i[0])
            good += 1
        except:
            bad += 1

    await bot.send_message(
        message.chat.id,
        "<u>Рассылка окончена\n\n</u>"
        f"<b>Всего пользователей:</b> <code>{len(users)}</code>\n"
        f"<b>Отправлено:</b> <code>{good}</code>\n"
        f"<b>Не удалось отправить:</b> <code>{bad}</code>",
        parse_mode="html"
    )
################# СНИЗУ РАССЫЛКА ДЛЯ ТЕХ, КТО НЕ ПРОШЕЛ КВЕСТ
@dp.callback_query_handler(text='write_message0')
async def rassilka0 (call:types.callback_query,state: FSMContext):
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА',callback_data='otemena')
    murkap.add(bat0)
    await bot.send_message(call.message.chat.id,'Перешли мне уже готовый пост и я разошлю его всем юзерам кто не прошел квест',reply_markup=murkap)
    await reg0.name0.set()


@dp.message_handler(state=reg0.name0,content_types=['text','photo','video','video_note'])
async def fname_step0(message: types.Message, state: FSMContext):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    await state.finish()
    users = sql.execute("SELECT id FROM user_time WHERE status_ref = 0").fetchall()
    bad = 0
    good = 0
    await bot.send_message(message.chat.id,
                           f"<b>Всего пользователей: <code>{len(users)}</code></b>\n\n<b>Расслыка начата!</b>",
                           parse_mode="html")
    for i in users:
        await asyncio.sleep(1)
        try:
            await message.copy_to(i[0])
            good += 1
        except:
            bad += 1

    await bot.send_message(
        message.chat.id,
        "<u>Рассылка окончена\n\n</u>"
        f"<b>Всего пользователей:</b> <code>{len(users)}</code>\n"
        f"<b>Отправлено:</b> <code>{good}</code>\n"
        f"<b>Не удалось отправить:</b> <code>{bad}</code>",
        parse_mode="html"
    )




@dp.callback_query_handler(state=reg.name,text='otemena')
async def rassilka_otmena (call:types.callback_query,state: FSMContext):
    await state.finish()
    await bot.delete_message(message_id=call.message.message_id,chat_id=call.message.chat.id)