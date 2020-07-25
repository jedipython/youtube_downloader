from main import bot, dp
from aiogram.types import Message
from aiogram import types
from config import admin_id
from pytube import YouTube
from aiogram.dispatcher.filters import Text



async def send_to_admin(*args):
    await bot.send_message(chat_id=admin_id, text="Бот запущен")

@dp.message_handler(commands=['start'])
async def show_menu(message: types.Message):
    await message.answer("Привет! Пришли ссылку на видео с Youtube")

@dp.message_handler(Text(startswith="https://www.you"))
async def get_link(message: types.Message):
    """ Загружаем видео с YouTube в папку с приложением"""
    yt = YouTube(message.text)
    stream = yt.streams.filter(res='720p').first().download()
    await message.answer(stream)
