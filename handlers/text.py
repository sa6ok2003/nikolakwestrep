from aiogram import types
from misc import dp, bot
import sqlite3
from aiogram.dispatcher import FSMContext
from .sqlit import stata_user
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

@dp.message_handler(content_types=['video_note','video','photo'])
async def ka(message: types.Message):
    print(message.chat.id)