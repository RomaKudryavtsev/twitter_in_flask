import sqlite3


def prepare_db():
    with sqlite3.connect("user.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users 
            (id INTEGER PRIMARY KEY, screen_name TEXT, access_token TEXT, token_secret TEXT)"""
        )
        conn.commit()


def add_user(id: int, screen_name: str, access_token: str, token_secret: str):
    with sqlite3.connect("user.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (id, screen_name, access_token, token_secret) VALUES (?, ?, ?, ?)",
            (id, screen_name, access_token, token_secret),
        )
        conn.commit()


def get_user_by_screen_name(screen_name: str):
    with sqlite3.connect("user.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users AS u WHERE u.screen_name = ?", (screen_name,)
        )
        user_data = cursor.fetchone()
        return (
            {
                "id": user_data[0],
                "screen_name": user_data[1],
                "access_token": user_data[2],
                "token_secret": user_data[3],
            }
            if user_data
            else None
        )
