from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, StringProperty
from kivy.uix.label import Label
import sqlite3

DB_PATH = "app.db"

class StudentListScreen(Screen):
    students = ListProperty([])
    user_email = StringProperty("")

    def on_pre_enter(self):
        self.refresh_list()

    def refresh_list(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM Pessoa '")
        alunos = cursor.fetchall()
        conn.close()

        self.students = [aluno['nome'] for aluno in alunos]

        grid = self.ids.students_grid
        grid.clear_widgets()
        for nome in self.students:
            grid.add_widget(Label(text=nome))

    def add_student(self):
        self.manager.current = "student_register"
