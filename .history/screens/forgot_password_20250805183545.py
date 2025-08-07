from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from utils import send_email
import sqlite3

DB_PATH = "app.db"

class ForgotPasswordScreen(Screen):
    email = ObjectProperty(None)
    message = StringProperty("")

    def send_password(self):
        email = self.ids.email.text.strip().lower()
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pessoa WHERE email = ?", (email,))
        user = cursor.fetchone()

        if not user:
            self.message = "E-mail não encontrado."
            conn.close()
            return

        # Desbloqueia usuário e zera tentativas
        cursor.execute("""
            UPDATE Pessoa 
            SET tentativas = 0, data_hora_bloqueio = NULL, status = 'ATIVO'
            WHERE email = ?
        """, (email,))
        conn.commit()
        conn.close()

        # Mensagem com orientação segura
        send_email(
            email,
            "Recuperação de Senha",
            "Olá!\n\nRecebemos uma solicitação para redefinir sua senha.\n\nPor motivos de segurança, recomendamos alterar sua senha ao fazer login.\n\nSe você não solicitou isso, ignore esta mensagem."
        )

        self.message = "Instruções enviadas para seu e-mail."
