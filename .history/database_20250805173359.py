import sqlite3
import hashlib
from datetime import datetime

DB_NAME = "app.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL,
            status TEXT DEFAULT 'ATIVO',
            tentativas INTEGER DEFAULT 0,
            tipo TEXT NOT NULL,
            bloqueado_ate TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            image TEXT
        )
    ''')

    conn.commit()
    conn.close()

def add_user(email, nome, senha, tipo):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (email, nome, senha, tipo)
        VALUES (?, ?, ?, ?)
    ''', (email, nome, hash_password(senha), tipo))
    conn.commit()
    conn.close()

def get_user(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user_tentativas(email, tentativas, bloqueado_ate=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET tentativas = ?, bloqueado_ate = ? WHERE email = ?
    ''', (tentativas, bloqueado_ate, email))
    conn.commit()
    conn.close()

def reset_tentativas(email):
    update_user_tentativas(email, 0, None)

def get_exercises():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, category, name, image FROM exercises')
    exercises = cursor.fetchall()
    conn.close()
    return exercises

def add_exercise(category, name, image=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO exercises (category, name, image)
        VALUES (?, ?, ?)
    ''', (category, name, image))
    conn.commit()
    conn.close()
    
    
