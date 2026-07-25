import sqlite3

DB_NAME = "users.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        streak INTEGER DEFAULT 0,
        completed INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def add_user(user_id, username, first_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (id, username, first_name)
        VALUES (?, ?, ?)
    """, (user_id, username, first_name))

    conn.commit()
    conn.close()


def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE id=?",
        (user_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def add_xp(user_id, xp):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET
            xp = xp + ?,
            completed = completed + 1
        WHERE id=?
    """, (xp, user_id))

    cursor.execute(
        "SELECT xp FROM users WHERE id=?",
        (user_id,)
    )

    current_xp = cursor.fetchone()[0]

    level = current_xp // 100 + 1

    cursor.execute("""
        UPDATE users
        SET level=?
        WHERE id=?
    """, (level, user_id))

    conn.commit()
    conn.close()


def count_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")

    total = cursor.fetchone()[0]

    conn.close()

    return total
