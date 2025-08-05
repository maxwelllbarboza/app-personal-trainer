from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from database import USERS
from utils import send_email

class ForgotPasswordScreen(Screen):
    email = ObjectProperty(None)
    message = StringProperty("")

    def send_password(self):
        email = self.ids.email.text.strip().lower()
        user = USERS.get(email)
        if not user:
            self.message = "Email not found."
            return
        send_email(email, "Your Password", f"Your password is: {user['password']}")
        user['loginAttempts'] = 0
        user['lockoutTime'] = None
        user['status'] = "Active"
        self.message = "Password sent to your email."