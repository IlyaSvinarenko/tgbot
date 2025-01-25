import sqlite3, os, logging
import time

log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=log_level, format='%(asctime)s %(levelname)s %(message)s')

bot_id: int = os.environ.get(
    'Son_of_Ilya_bot_id')  # Нужно для того чтобы бот сам себя случайно не добавлял в таблицу users

'''Класс для работы с базой данных'''


class UsersTable:
    def __init__(self):
        self.connect = sqlite3.connect('Telegram_Bot_DB.db')
        self.cursor = self.connect.cursor()

    def delete_table(self, table_name):
        logging.info(f'in SqlTables / def delete_table:  table_name == {table_name}')
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        logging.info(f" ТЫ ЗАЧЕМ УДАЛИЛ ТАБЛИЦУ {table_name} !!?!?!?")

    def clear_table(self, table_name):
        logging.info(f'in SqlTables / def clear_table: table_name == {table_name}')
        self.cursor.execute(f"DELETE FROM {table_name}")
        logging.info(f"table {table_name} cleared")
        return self.connect.commit()

    def create_table_users(self):
        ''' Шаблончик таблицы users  с полями
        (user_id, add_date_time, user_name, date_in_seс, user_first_name, chat_id)'''
        try:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INT NOT NULL UNIQUE,
            add_date_time DATETIME NOT NULL,
            user_name TEXT NOT NULL UNIQUE,
            date_in_sec REAL NOT NULL,
            user_first_name TEXT NOT NULL,
            chat_id INT NOT NULL);""")
            self.connect.commit()
        except sqlite3.Error as error:
            logging.info("ERROR", error)

    def add_user(self, user_id, username, user_first_name, chat_id):
        logging.info(f'in SqlTables / def add_user:  user_id, username, chat_id == '
                     f'{user_id, username, user_first_name, chat_id}')
        current_time_sec = time.time()
        add_date_time = time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime(current_time_sec))
        if user_id == bot_id:  # Это чтобы бот не добавлял сам себя в таблицу
            logging.info("Ой, я пытался сам себя занести в таблицу")
            return
        try:
            self.cursor.execute("INSERT INTO users "
                                "(user_id, add_date_time, user_name, date_in_sec, user_first_name, chat_id)"
                                " VALUES (?, ?, ?, ?, ?, ?)",
                                (user_id, add_date_time, username, current_time_sec, user_first_name, chat_id))
            logging.info(f'user {username}  id: {user_id} added to data base\n with datetime: {add_date_time}')
        except sqlite3.Error as error:
            logging.info("Error", error)
            return False
        return self.connect.commit()

    def get_user(self, user_id, chat_id):
        logging.info(f'in SqlTables / def get_user:  user_id== {user_id}')
        result = self.cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id} AND chat_id = {chat_id}")
        result = result.fetchone()
        if result is None:
            return False
        else:
            return result

    def get_users_in_chat(self, chat_id):
        logging.info(f'in SqlTables / def get_users_in_chat:  chat_id== {chat_id}')
        result = self.cursor.execute(f"SELECT * FROM users WHERE chat_id = {chat_id}")
        result = result.fetchall()
        if result is None or result == []:
            return False
        else:
            return result

    def get_users(self):
        logging.info(f'in SqlTables / def get_users:  ')
        result = self.cursor.execute(f"SELECT * FROM users")
        result = result.fetchall()
        if result is None or result == []:
            return False
        else:
            return result

    def del_user(self, user_id):
        self.cursor.execute(f"DELETE FROM users WHERE user_id = {user_id}")
        return self.connect.commit()

users_table = UsersTable()

users_table.create_table_users()
# users_table.delete_table("users")