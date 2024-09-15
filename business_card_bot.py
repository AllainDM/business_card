import asyncio
# import json
# from datetime import datetime
import sqlite3

# import emoji
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile, InputMediaVideo
# from aiohttp.web_fileresponse import content_type

import config
from FDataBase import FDataBase
import main_text


# Объект бота
bot = Bot(token=config.BOT_API_TOKEN)
# Диспетчер
dp = Dispatcher()

# Отдельно сохраним ид видео
video_id = main_text.main_video_id
# video_mg = InputMediaVideo(type='video', media=FSInputFile(r'files/DEMO.mp4'))
# print(video_mg)
# print(video_mg.media)

# # Подключение к бд
def connect_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Формирование ответа в виде словаря, а не кортежа
    return conn


@dp.message(Command("start", "старт"))
async def cmd_start(message: types.Message):
    global video_id
    # Узнаем ид пользователя.
    user_id = message.from_user.id
    # TODO вынести текст в отдельный модуль, для удобства редактирования через админку.
    text = main_text.main_text
    # await bot.send_video(message.chat.id, video=video_mg.media, caption=text)
    try:
        await bot.send_video(message.chat.id, video=video_id, caption=text)
        # await bot.send_video(message.chat.id, video=video_id, caption=text)
    except:
        # Запасной вариант выцепления ид файла.
        video_file = FSInputFile(path='files/DEMO2.mp4')
        msg = await bot.send_video(message.chat.id, video=video_file, caption=text)
        # Глобально перезапишем ид.
        video_id = msg.video.file_id
        # Временный тестовый функционал по отправке нового ид видео конкретному пользователю.
        if user_id == 976374565:
            await bot.send_message(976374565, text=video_id)

    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    # Запись в лог.
    # Перед обновлением необходимо проверить заходил ли этот пользователь ранее.
    db = FDataBase(connect_db())
    if db.get_user_log(user_id):  #
        db.update_log(user_id)
    else:
        db.add_log(user_id, first_name, last_name, username)


# Чтение лога. Просмотр стучавшихся пользователей.
@dp.message(Command("log", "лог"))
async def cmd_log(message: types.Message):
    # Узнаем ид пользователя.
    user_id = message.from_user.id
    # Данный функционал доступен только админам.
    if user_id in config.admins:
        db = FDataBase(connect_db())
        logs = db.get_log()
        for i in logs:
            await bot.send_message(message.chat.id,
                                   f'Пользователь: {i["first_name"]} {i["last_name"]} {i["username"]} \n'
                                   f'Последний вход: {i["date_last_in"]} \n'
                                   f'id: `{i["user_tg_id"]}`', parse_mode="MARKDOWN")

        print(f"logs {logs[0]['user_tg_id']}")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
