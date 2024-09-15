import asyncio
import json
from datetime import datetime
import sqlite3

import emoji
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile

import config
from FDataBase import FDataBase
import main_text


# Объект бота
bot = Bot(token=config.BOT_API_TOKEN)
# Диспетчер
dp = Dispatcher()



# # Подключение к бд
def connect_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Формирование ответа в виде словаря, а не кортежа
    return conn


@dp.message(Command("start", "старт"))
async def cmd_start(message: types.Message):
    video_file = FSInputFile(path='files/DEMO.mp4')

    # TODO вынести текст в отдельный модуль, для удобства редактирования через админку.
    text = main_text.main_text
    await bot.send_video(message.chat.id, video=video_file, caption=text)

    # Узнаем ид пользователя.
    user_id = message.from_user.id

    # date_now = datetime.now()
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
