from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

class TrainerMenuScreen(Screen):
    user_email = StringProperty("")

    def on_pre_enter(self):
        self.ids.welcome.text = f"Bem-vindo(a), {self.user_email}"

    def go_to_students(self):
        self.manager.current = "student_list"

    def go_to_workouts(self):
        self.manager.current = "workout_list"