from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from utils import send_email
import sqlite3

DB_PATH = "app_data.db"

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

        # Enviar a senha por e-mail (a senha já está com hash, portanto deve ser alterada na prática)
        send_email(
            email,
            "Recuperação de Senha",
            "Esta é sua senha atual (criptografada):\n" + user["senha"] + "\n\nRecomendamos alterá-la assim que possível."
        )

        # Desbloquear o usuário e zerar tentativas
        cursor.execute("""
            UPDATE Pessoa 
            SET tentativas = 0, data_hora_bloqueio = NULL, status = 'ATIVO'
            WHERE email = ?
        """, (email,))
        conn.commit()
        conn.close()

        self.message = "Senha enviada para seu e-mail."
