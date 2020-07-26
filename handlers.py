from main import bot, dp
from aiogram.types import Message
from aiogram import types
from config import admin_id
from pytube import YouTube
from aiogram.dispatcher.filters import Text
import ffmpeg



async def send_to_admin(*args):
    await bot.send_message(chat_id=admin_id, text="Бот запущен")

@dp.message_handler(commands=['start'])
async def show_menu(message: types.Message):
    await message.answer("Привет! Пришли ссылку на видео с Youtube")

@dp.message_handler(Text(startswith="https://www.you"))
async def get_link(message: types.Message):
    """ Загружаем видео с YouTubе и отдаем в чат """
    try:
        if YouTube(message.text).streams.filter(res="1080p"):
            video_stream = YouTube(message.text).streams.filter(res="1080p").order_by('resolution').desc().first().download()
        else:
            video_stream = YouTube(message.text).streams.filter(only_video=True).order_by('resolution').desc().first().download()
        audio_stream = YouTube(message.text).streams.filter(only_audio=True).order_by('abr').desc().first().download(filename_prefix="audio_")
        source_audio = ffmpeg.input(audio_stream)
        source_video = ffmpeg.input(video_stream)
        ffmpeg.concat(source_video, source_audio, v=1, a=1).output("video_name.mp4").run()
        await message.answer_video(open('video_name.mp4', 'rb'))
    except Exception as err:
        await message.text(f"Извините, произошла ошибка {err}")


    
