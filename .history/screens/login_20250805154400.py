from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from database import USERS
from datetime import datetime, timedelta

class LoginScreen(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    message = StringProperty("")

    def do_login(self):
        email = self.ids.email.text.strip().lower()
        password = self.ids.password.text
        user = USERS.get(email)
        now = datetime.now()
        if not user or user['password'] != password:
            if user:
                user['loginAttempts'] += 1
                if user['loginAttempts'] >= 3:
                    user['lockoutTime'] = now
                    user['status'] = "Inactive"
            self.message = "Incorrect username or password."
            return
        if user['status'] == "Inactive" and user.get('lockoutTime'):
            if now < user['lockoutTime'] + timedelta(minutes=30):
                self.message = "Account locked. Try again later."
                return
            else:
                user['status'] = "Active"
                user['loginAttempts'] = 0
        user['loginAttempts'] = 0
        self.manager.current = "trainer_menu" if user['access_profile'] == "Trainer" else "student_list"
        self.manager.get_screen(self.manager.current).user_email = email

    def forgot_password(self):
        self.manager.current = "forgot_password"