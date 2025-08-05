from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, StringProperty
from database import USERS

class StudentListScreen(Screen):
    students = ListProperty([])
    user_email = StringProperty("")

    def on_pre_enter(self):
        self.refresh_list()

    def refresh_list(self):
        self.students = [u for u in USERS.values() if u['access_profile'] == "Student"]
        grid = self.ids.students_grid
        grid.clear_widgets()
        for student in self.students:
            from kivy.uix.label import Label
            grid.add_widget(Label(text=student['name']))

    def add_student(self):
        self.manager.current = "student_register"