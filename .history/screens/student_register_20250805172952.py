from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from utils import send_email
from uuid import uuid4
import hashlib
import sqlite3

DB_PATH = "app_data.db"

class StudentRegisterScreen(Screen):
    name = ObjectProperty(None)
    email = ObjectProperty(None)
    phone = ObjectProperty(None)
    birthdate = ObjectProperty(None)
    profile = ObjectProperty(None)
    message = StringProperty("")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def save_student(self):
        email = self.ids.email.text.strip().lower()
        nome = self.ids.name.text.strip()
        telefone = self.ids.phone.text.strip()
        nascimento = self.ids.birthdate.text.strip()
        perfil = self.ids.profile.text.strip().upper()  # ALUNO ou PROFESSOR

        if '@' not in email:
            self.message = "Email inválido."
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Verifica se o e-mail já está cadastrado
        cursor.execute("SELECT 1 FROM Pessoa WHERE email = ?", (email,))
        if cursor.fetchone():
            self.message = "Email já cadastrado."
            conn.close()
            return

        # Gera senha temporária
        temp_password = str(uuid4())[:8]
        hashed_password = self.hash_password(temp_password)

        # Insere no banco
        cursor.execute("""
            INSERT INTO Pessoa (
                id, nome, email, telefone, data_nascimento, perfil_acesso, senha, status, tentativas
            ) VALUES (?,
