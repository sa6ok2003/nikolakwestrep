from aiogram import types
from misc import dp,bot
import sqlite3
from .sqlit import reg_user
from aiogram.dispatcher import FSMContext
from .sqlit import stata_user
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
t1 = 30 # ВРЕМЯ ЗАДЕРЖКИ ПЕРВОГО КРУГДЯША

video_note_1 = 'DQACAgIAAxkBAAMOYEcqCtnC95WsLzD3z5vKzLoVgR4AAsUMAAKA8DhKYYAYY68lwroeBA'
video_one  = 'BAACAgIAAxkBAAIBeWBIz-xwsxOTqoqBfirSzswu28SZAAJGCwACFd1ISl2Au9LiTOkmHgQ'

class st_reg(StatesGroup):
    st_name = State()
    st_fname = State()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message,state: FSMContext):
    reg_user(message.chat.id)
    await bot.send_video(chat_id=message.chat.id, video=video_one,caption="""Айт🔥 ну что погнали)
Где-то в видео я рассказал как включить бота, и начать проходить 2 бесплатных подготовительных этапа🚀""")
    await st_reg.st_name.set()

@dp.message_handler(state=st_reg.st_name,content_types='text')
async def cmd_star(message: types.Message, state: FSMContext):
    if '+' in message.text :
        await state.finish()
        await bot.send_video_note(chat_id=message.chat.id, video_note=video_note_1)
        await asyncio.sleep(t1)
        markup = types.InlineKeyboardMarkup()
        bat1 = types.InlineKeyboardButton(text='🔥 ДВИЖ 🔥',callback_data='start_go')
        markup.add(bat1)
        await bot.send_message(chat_id=message.chat.id, text="""<b>1) Подготовительный этап</b>
    
Узнаешь:

Что такое арбитраж/трафик?
Сколько на этом можно зарабатывать?
Регистрация на ПП?

Жми на движ и погнали👇""",parse_mode='html',reply_markup=markup)