from aiogram import types
from misc import dp, bot
import sqlite3
from aiogram.dispatcher import FSMContext
from .sqlit import update_user
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
time_dz_1 = 240 #ВРЕМЯ НА ВЫПОЛНЕНИЕ ПЕРВОГО ДЗ
time_dz_2 = 240 #ВРЕМЯ НА ВЫПОЛНЕНИЕ ВТОРОГО ДЗ

video_bekir1 = 'BAACAgIAAxkBAAIBiWBI0Yu1RzM4eiR0BT8prxUmiGDjAAINCwACTtVBSjzvizhTrXK3HgQ'
video_bekir2 = 'BAACAgIAAxkBAAIBiGBI0WcIDnpQM3t9vZ57IFp8T2pjAALfCwACTtVBSnlxtxhf_GB2HgQ'


video_sdelal_dz = 'DQACAgIAAxkBAAOOYEc72lyzLp5nZT8CSBEBruPxSIQAAkgOAAJbYDhKik35-Yyx0qoeBA'

photo1 = "AgACAgIAAxkBAAPdYEdPsr9pyzZdVjUKFAHcUePm-i4AAqKyMRtO1TlKE4VoSolVSoCsQtGaLgADAQADAgADbQADwU0DAAEeBA"
photo2 = "AgACAgIAAxkBAAIBLGBHVQRTqqpiZu7mrO3L5UJ7UMiAAAKwsjEbTtU5SkVKRyiZPqVsdqd0ly4AAwEAAwIAA20AAxZZBwABHgQ"

video_finish = 'BAACAgIAAxkBAAIC_2BI46nL2oKOAAHz8jl7pzdEecW-mQACkwwAAhXdSErBFPQpJW3H9x4E'

time_day = 86400
class regs(StatesGroup):
    names = State()
    fnames = State()

@dp.callback_query_handler(text='start_go')
async def start_1(call: types.callback_query,state: FSMContext):
    await bot.send_video(chat_id=call.message.chat.id, video=video_bekir1,caption='Отправляй домашнее задание прямо сюда в бота\n'
                                                                                  '(скрин фоткой, а не файлом)\n\n'
                                                                                  'Сайт : www.admitad.com\n\n'
                                                                                  'Если возникли сложности, то пиши в поддержку @JaysonAdmin')
    await regs.names.set()
    await state.update_data(key1 =0)
    await state.update_data(key = 0)
    await asyncio.sleep(time_dz_1)
    await state.update_data(key= 1)

    await asyncio.sleep(time_day)
    data = await state.get_data()
    if data['key1'] == 0:
        await bot.send_message(chat_id=call.message.chat.id,text="""Эхх😔 так и не узнаешь что тебя ждёт дальше(
        
Ещё не поздно отправить задание, это же так просто.

Если возникли сложности, то пиши в поддержку @JaysonAdmin""")
        await asyncio.sleep(time_day)
        data = await state.get_data()
        if data['key1'] == 0:
            await bot.send_photo(chat_id=call.message.chat.id,photo=photo1,caption=""" Это последний раз, когда я напоминаю🔥действуй🔥 

Возникли трудности пиши в поддержку: @JaysonAdmin""")


@dp.message_handler(state=regs.names, content_types='photo')
async def domashka(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data = data['key']
    if data == 0:
        await bot.send_message(chat_id=message.chat.id,text='Не хитри ! Выполняй домашку и кидай скрин')
    else:
        await state.update_data(key1=1)
        await regs.fnames.set()
        await bot.send_video_note(chat_id=message.chat.id,video_note=video_sdelal_dz)
        await asyncio.sleep(20) ########################################################### ВАЖНООООООООО
        await bot.send_video(chat_id=message.chat.id,video=video_bekir2,caption='Отправляй домашнее задание прямо сюда в бота\n\n'
                                                                                'Пример, как должно выглядеть твое сообщение\n\n'
                                                                                '@name_channel\n\n'
                                                                                'Если возникли сложности, то пиши в поддержку @JaysonAdmin')
        await state.update_data(pr1=0)
        await asyncio.sleep(time_dz_2)
        await state.update_data(pr1=1)

        await state.update_data(dz1=0)
        await asyncio.sleep(time_day)
        data = await state.get_data()
        if data['dz1'] == 0:
            await bot.send_message(chat_id=message.chat.id,text="""Блииин😟 у тебя все так хорошо шло!

Почему останавливаешься на пол пути?

Давай приступай к заданию🔥

Возникли трудности поддержка тут 👉 @JaysonAdmin""")
            await asyncio.sleep(time_day)
            if data['dz1'] == 0:
                await bot.send_photo(chat_id=message.chat.id, photo=photo1,caption="""Давай не останавливайся 💪

Я жду твоё задание.

Если возникли трудности пиши в поддержку: @JaysonAdmin""")


@dp.message_handler(state=regs.fnames, content_types='text')
async def domashka_2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text[:1] != '@' or data['pr1'] == 0:
        await bot.send_message(chat_id=message.chat.id,text='Либо ты меня пытаешься обмануть, либо ты неправильно скинул ссылку на свой телеграмм канал\n\n'
                                                            '1. Проверь что бы твой канал был публичным\n'
                                                            '2. Проверь что ты мне отправляешь свой канал в формате @name_channel\n'
                                                            '3. Повтори попытку снова!')
    else:
        await state.finish()
        update_user(message.chat.id)
        await state.update_data(dz1=1)
        await bot.send_video(chat_id=message.chat.id,video=video_finish,caption='🙋‍♂ @nikolanext')