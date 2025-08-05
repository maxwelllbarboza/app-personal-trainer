from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from database import USERS
from datetime import datetime, timedelta
import hashlib

class LoginScreen(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    message = StringProperty("")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def do_login(self):
        email = self.ids.email.text.strip().lower()
        password = self.ids.password.text
        hashed_password = self.hash_password(password)
        user = USERS.get(email)
        now = datetime.now()

        if not user or user['senha'] != hashed_password:
            if user:
                user['tentativas'] = user.get('tentativas', 0) + 1
                if user['tentativas'] >= 3:
                    user['data_hora_bloqueio'] = now
                    user['status'] = "INATIVO"
            self.message = "Usuário ou senha incorreto."
            return

        if user['status'] == "INATIVO":
            bloqueio = user.get('data_hora_bloqueio')
            if bloqueio and now < bloqueio + timedelta(minutes=30):
                self.message = "Usuário bloqueado. Tente novamente em breve."
                return
            else:
                user['status'] = "ATIVO"
                user['tentativas'] = 0

        # Login bem-sucedido
        user['tentativas'] = 0
        self.message = ""
        self.manager.current = "trainer_menu" if user['tipo'] == "PROFESSOR" else "student_list"
        self.manager.get_screen(self.manager.current).user_email = email

    def forgot_password(self):
        self.manager.current = "forgot_password"
