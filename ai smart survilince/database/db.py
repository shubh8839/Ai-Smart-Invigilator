import hashlib
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


def get_connection():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  return conn


def init_db():
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT DEFAULT 'Exam Administrator',
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
  conn.commit()
  conn.close()


init_db()


def hash_password(password: str) -> str:
  return hashlib.sha256(password.encode()).hexdigest()


def register_user(
    email: str,
    password: str,
    full_name: str = "Exam Administrator",
    **kwargs,
):
  if "name" in kwargs and (
      not full_name or full_name == "Exam Administrator"
  ):
    full_name = kwargs["name"]

  try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (email, password, full_name) VALUES (?, ?, ?)",
        (email, hash_password(password), full_name),
    )
    conn.commit()
    conn.close()
    return True
  except sqlite3.IntegrityError:
    return False
  except Exception as e:
    print("Register error:", e)
    return False


def authenticate_user(email: str, password: str):
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
  user = cursor.fetchone()
  conn.close()

  if user and user["password"] == hash_password(password):
    return dict(user)
  return None