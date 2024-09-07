import asyncio
import json
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile

import config


# Объект бота
bot = Bot(token=config.BOT_API_TOKEN)
# Диспетчер
dp = Dispatcher()


@dp.message(Command("start", "старт"))
async def cmd_start(message: types.Message, bot: Bot):
    text = (f"Наш сайт:\n"
            f"https://aistrategiya.ru/\n\n"
            f"Наши Telegram-каналы:\n"
            f"@AI_Strategy_razrabotka_botov_tg\n"
            f"@AsHuman_AI\n\n"
            f"Наш ИИ-ассистент для подготовки ТЗ:\n"
            f"@As_HumanHelp\n\n"
            f"Наше портфолио:\n"
            f"https://www.fl.ru/users/antonthai2022/portfolio/\n"
            f"@As_HumanBot\n\n"
            f"Контакты для связи:\n\n"
            f"@vedename - Евгений Мамонтов\n"
            f"@Anton_AsHuman - Антон Борисенко\n")

    video_file = FSInputFile(path='files/DEMO.mp4')
    await bot.send_video(message.chat.id, video=video_file, caption=text)
    # Узнаем ид пользователя.
    user_id = message.from_user.id
    print("Читаем лог из json.")
    try:
        with open('start_log.json', 'r') as f:
            data_log = json.load(f)
    except FileNotFoundError:
        print("Список логов в формате json не обнаружен.")
    print("Лог из json прочитан.")
    date_now = datetime.now()
    # Запись в лог.
    # Ключ ид пользователя, соответсвенно остается только поселеднее время входа.
    data_log[f"{user_id}"] = {
        "user_id": user_id,
        "last_time": f"{date_now}",
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "username": message.from_user.username
    }
    try:
        with open("start_log.json", 'w') as f:
            json.dump(data_log, f, sort_keys=False, ensure_ascii=False, indent=4, separators=(',', ': '))
    except FileNotFoundError:
        print(f"Файл 'start_log.json' не найден")


# Чтение лога. Просмотр стучавшихся пользователей.
@dp.message(Command("log", "лог"))
async def cmd_log(message: types.Message):
    # Узнаем ид пользователя.
    user_id = message.from_user.id
    # Данный функционал доступен только админам.
    if user_id in config.admins:
        try:
            with open("start_log.json", "r") as f:
                data_json = json.load(f)
            for i in data_json.items():
                await bot.send_message(message.chat.id,
                                       f'Пользователь: {i[1]["first_name"]} {i[1]["last_name"]} {i[1]["username"]} \n'
                                       f'Последний вход: {i[1]["last_time"]} \n'
                                       f'id: `{i[1]["user_id"]}`', parse_mode="MARKDOWN")

        except FileNotFoundError:
            print("Список логов в формате json не обнаружен.")
        print(data_json)



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
