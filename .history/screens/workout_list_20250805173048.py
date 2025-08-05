from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, StringProperty
from kivy.uix.label import Label
import sqlite3

DB_PATH = "app_data.db"

class WorkoutListScreen(Screen):
    workouts = ListProperty([])
    user_email = StringProperty("")

    def on_pre_enter(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Obter dados do usuário logado
        cursor.execute("SELECT * FROM Pessoa WHERE email = ?", (self.user_email,))
        user = cursor.fetchone()

        if not user:
            conn.close()
            return

        # Buscar treinos conforme perfil
        if user['perfil_acesso'] == "PROFESSOR":
            cursor.execute("SELECT * FROM Treino")
        else:
            cursor.execute("SELECT * FROM Treino WHERE id_aluno = ? AND status = 'ATIVO'", (user['id'],))

        treinos = cursor.fetchall()
        conn.close()

        self.workouts = [treino['nome_treino'] for treino in treinos]

        grid = self.ids.workouts_grid
        grid.clear_widgets()
        for nome in self.workouts:
            grid.add_widget(Label(text=nome))

    def add_workout(self):
        self.manager.current = "workout_register"
