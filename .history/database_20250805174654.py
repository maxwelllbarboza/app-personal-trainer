import sqlite3
import hashlib
from datetime import datetime

DB_NAME = "app.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tabela Pessoa (usuários)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pessoa (
            id_pessoa TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            data_nascimento TEXT,
            telefone TEXT,
            email TEXT UNIQUE NOT NULL,
            perfil_acesso TEXT NOT NULL,
            status TEXT DEFAULT 'ATIVO',
            senha TEXT NOT NULL,
            data_hora_bloqueio TEXT,
            tentativas INTEGER DEFAULT 0
        )
    ''')

    # Tabela de exercícios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            image TEXT
        )
    ''')

    # Tabela de treinos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id TEXT PRIMARY KEY,
            student_email TEXT NOT NULL,
            workout_name TEXT NOT NULL,
            creation_date TEXT NOT NULL,
            exercise_ids TEXT,
            status TEXT DEFAULT 'ATIVO',
            FOREIGN KEY (student_email) REFERENCES Pessoa(email)
        )
    ''')

    conn.commit()
    conn.close()

def add_user(id_pessoa, nome, data_nascimento, telefone, email, perfil_acesso, senha):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO Pessoa (id_pessoa, nome, data_nascimento, telefone, email, perfil_acesso, senha)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (id_pessoa, nome, data_nascimento, telefone, email, perfil_acesso, hash_password(senha)))
    conn.commit()
    conn.close()

def get_user(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Pessoa WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user_tentativas(email, tentativas, data_hora_bloqueio=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Pessoa SET tentativas = ?, data_hora_bloqueio = ? WHERE email = ?
    ''', (tentativas, data_hora_bloqueio, email))
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

def add_workout(id, student_email, workout_name, creation_date, exercise_ids, status="ATIVO"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO workouts (id, student_email, workout_name, creation_date, exercise_ids, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id, student_email, workout_name, creation_date, exercise_ids, status))
    conn.commit()
    conn.close()

def get_workouts_by_student(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, workout_name, creation_date, exercise_ids, status 
        FROM workouts 
        WHERE student_email = ? AND status = 'ATIVO'
    ''', (email,))
    results = cursor.fetchall()
    conn.close()
    return results