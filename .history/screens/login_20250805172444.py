from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from datetime import datetime, timedelta
import hashlib
import sqlite3

DB_PATH = "app_data.db"  # Caminho do banco

class LoginScreen(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    message = StringProperty("")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def get_user_by_email(self, email):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pessoa WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        return user

    def update_failed_attempts(self, email, tentativas, status, data_bloqueio):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Pessoa
            SET tentativas = ?, status = ?, data_hora_bloqueio = ?
            WHERE email = ?
        """, (tentativas, status, data_bloqueio, email))
        conn.commit()
        conn.close()

    def reset_attempts(self, email):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Pessoa
            SET tentativas = 0, data_hora_bloqueio = NULL, status = 'ATIVO'
            WHERE email = ?
        """, (email,))
        conn.commit()
        conn.close()

    def do_login(self):
        email = self.ids.email.text.strip().lower()
        password = self.ids.password.text
        hashed_password = self.hash_password(password)
        now = datetime.now()

        user = self.get_user_by_email(email)

        if not user or user['senha'] != hashed_password:
            if user:
                tentativas = user['tentativas'] + 1
                status = user['status']
                data_bloqueio = user['data_hora_bloqueio']

                if tentativas >= 3:
                    status = "INATIVO"
                    data_bloqueio = now.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    data_bloqueio = user['data_hora_bloqueio']

                self.update_failed_attempts(email, tentativas, status, data_bloqueio)

            self.message = "Usuário ou senha incorreto."
            return

        if user['status'] == "INATIVO":
            if user['data_hora_bloqueio']:
                bloqueio = datetime.strptime(user['data_hora_bloqueio'], "%Y-%m-%d %H:%M:%S")
                if now < bloqueio + timedelta(minutes=30):
                    self.message = "Usuário bloqueado. Tente novamente em breve."
                    return

        # Login bem-sucedido
        self.reset_attempts(email)
        self.message = ""

        tipo = user['perfil_acesso']
        if tipo == "PROFESSOR":
            self.manager.current = "trainer_menu"
        else:
            self.manager.current = "student_list"
        self.manager.get_screen(self.manager.current).user_email = email

    def forgot_password(self):
        self.manager.current = "forgot_password"
