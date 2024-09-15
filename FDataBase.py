import sqlite3
from datetime import datetime

"""Модуль общения с БД."""

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    # Получение одного пользователя из лога входа.
    def get_user_log(self, user_tg_id):
        try:
            self.__cur.execute(f"SELECT * FROM start_log WHERE user_tg_id = {user_tg_id} LIMIT 1")
            res = self.__cur.fetchone()
            return res
        except sqlite3.Error as e:
            print("get_user_log Ошибка поиска пользователя в логе БД " + str(e))
            return False

    # Добавить новую запись в лог входа пользователей.
    def add_log(self, user_tg_id, first_name="", last_name="", username=""):
        date = datetime.now()
        date = date.strftime("%d.%m.%Y %H:%M:%S")
        print("Запрос на добавление лога передан в модуль БД")
        try:
            query = (f"INSERT INTO start_log (user_tg_id, first_name, last_name, username, date_last_in) "
                     f"VALUES(?, ?, ?, ?, ?)")
            self.__cur.execute(query,
                     (user_tg_id, first_name, last_name, username, date))
            self.__db.commit()
            self.__cur.close()
            return "ok"

        except sqlite3.Error as e:
            print("update_log Ошибка записи данных в лог БД " + str(e))
            return False

    # Обвновить дату входа пользователя в таблице логов.
    def update_log(self, user_tg_id):
        date = datetime.now()
        date = date.strftime('%d.%m.%Y %H:%M:%S')
        print("Запрос на обновление лога передан в модуль БД")
        print(date)
        print(type(date))
        try:
            self.__cur.execute(f"UPDATE `start_log` SET `date_last_in` = ? WHERE user_tg_id = ?", (date, user_tg_id))
            self.__db.commit()
            self.__cur.close()
        except sqlite3.Error as e:
            print("update_log Ошибка обновления записи данных в логе БД " + str(e))
            return False

    # Получить все логи входов пользователей.
    def get_log(self):
        try:
            self.__cur.execute(f"SELECT * FROM start_log LIMIT 10")
            res = self.__cur.fetchall()
            return res
        except sqlite3.Error as e:
            print("get_user_log Ошибка сбора лога в БД " + str(e))
            return False


