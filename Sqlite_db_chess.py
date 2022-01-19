import datetime
import sqlite3

def save_game_in_db(name_of_the_winners, game_duration, game_history):
    try:

        sqlite_connection = sqlite3.connect('sqlite_python_chess.db')
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS chess_table (
                                       id INTEGER PRIMARY KEY autoincrement,
                                       name_of_the_winners TEXT NOT NULL,
                                       game_duration datetime NOT NULL,
                                       game_date datetime NOT NULL,
                                       game_history TEXT NOT NULL);'''

        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Таблица SQLite создана")




        sqlite_insert_query ="""INSERT INTO chess_table
        (name_of_the_winners, game_duration, game_date, game_history)
        VALUES(?, ?, ?, ?);"""
        data_tuple = ( name_of_the_winners, game_duration, datetime.datetime.now(), game_history)
        cursor.execute(sqlite_insert_query, data_tuple)
        sqlite_connection.commit()
        cursor.close()


    except sqlite3.Error as err:
        print("Ошибка при подключении к sqlite", err)

    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQlite закрыто")