import sqlite3

"""Отдельный модуль для создания таблиц БД."""

def updates_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("create table if not exists start_log ("
                   "rowid integer primary key autoincrement,"
                   "user_tg_id integer not null,"
                   "first_name text,"
                   "last_name text,"
                   "username text,"
                   "date_last_in text not null);")
    print("Таблица start_log создана.")
    conn.commit()

    cursor.execute("create table if not exists admin ("
                   "rowid integer primary key autoincrement,"
                   "admin_tg_id integer not null);")
    print("Таблица admin создана.")
    conn.commit()
    cursor.close()

updates_tables()
