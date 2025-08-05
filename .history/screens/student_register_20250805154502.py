from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from database import USERS
from utils import send_email
from uuid import uuid4

class StudentRegisterScreen(Screen):
    name = ObjectProperty(None)
    email = ObjectProperty(None)
    phone = ObjectProperty(None)
    birthdate = ObjectProperty(None)
    profile = ObjectProperty(None)
    message = StringProperty("")

    def save_student(self):
        email = self.ids.email.text.strip().lower()
        if '@' not in email:
            self.message = "Invalid email."
            return
        if email in USERS:
            self.message = "Email already registered."
            return
        temp_password = str(uuid4())[:8]
        user = {
            "id_person": str(uuid4()),
            "name": self.ids.name.text,
            "birthdate": self.ids.birthdate.text,
            "phone": self.ids.phone.text,
            "email": email,
            "access_profile": self.ids.profile.text,
            "status": "Active",
            "password": temp_password,
            "loginAttempts": 0,
            "lockoutTime": None
        }
        USERS[email] = user
        send_email(email, "Welcome", f"Download the app and login with password: {temp_password}")
        self.message = "Student registered and email sent."
        self.manager.current = "student_list"