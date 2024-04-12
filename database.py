import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()


class Connection_Closure:
    def __init__(self):
        self.connect = sqlite3.connect(os.getenv('db_file'))
        self.cursor = self.connect.cursor()

    async def close(self):
        self.connect.close()


class Database(Connection_Closure):
    def __init__(self):
        super().__init__()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS User(
                        id INTEGER PRIMARY KEY,
                        message_text TEXT,
                        tts_symbols INTEGER)""")
        self.connect.commit()

    async def check_user_exists(self, id):
        self.cursor.execute(
            "SELECT id FROM User "
            "WHERE id = ? ",
            (id,))
        data = self.cursor.fetchone()
        return data is not None

    async def add_user(self, id):
        self.cursor.execute("INSERT INTO User VALUES(?, ?, ?);",
                            (id, '', 300))
        self.connect.commit()


class tokens_user(Connection_Closure):
    def __init__(self):
        super().__init__()

    async def tts_symbols_user(self, id):
        self.cursor.execute(f"SELECT tts_symbols FROM User WHERE id = ?", (id,))
        row = self.cursor.fetchone()
        if not row[0]:
            return
        else:
            return row[0]


class tokens_add(Connection_Closure):
    def __init__(self):
        super().__init__()

    async def tts_symbols(self, id):
        self.cursor.execute("SELECT id, tts_symbols FROM User WHERE id = ?", (id,))
        result = self.cursor.fetchone()
        if result is None:
            return 'Ошибка, при запросе к БД.'
        return result

    async def add_tts_symbols(self, tokens, user_id):
        self.cursor.execute("UPDATE User SET tts_symbols = ? WHERE id = ?", (tokens, user_id))
        self.connect.commit()


class message_add(Connection_Closure):
    def __init__(self):
        super().__init__()

    async def text_add(self, id):
        self.cursor.execute("SELECT id, message_text FROM User WHERE id = ?", (id,))
        result = self.cursor.fetchone()
        if result is None:
            return 'Ошибка, при запросе к БД.'
        return result

    async def add_text(self, text, user_id):
        self.cursor.execute("UPDATE User SET message_text = ? WHERE id = ?", (text, user_id))
        self.connect.commit()
