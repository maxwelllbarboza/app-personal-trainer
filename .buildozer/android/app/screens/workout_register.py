from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from uuid import uuid4
from datetime import datetime
import sqlite3

DB_PATH = "app.db"

class WorkoutRegisterScreen(Screen):
    student = ObjectProperty(None)
    workout_name = ObjectProperty(None)
    exercises = ListProperty([])
    message = StringProperty("")

    def save_workout(self):
        student_email = self.ids.student.text.strip().lower()
        workout_name = self.ids.workout_name.text.strip()

        if not workout_name:
            self.message = "Nome do treino obrigatório."
            return

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Verifica se o aluno existe e é do tipo ALUNO
        cursor.execute("SELECT * FROM Pessoa WHERE email = ?", (student_email,))
        student = cursor.fetchone()

        if not student or student["perfil_acesso"] != "ALUNO":
            self.message = "Aluno inválido."
            conn.close()
            return

        # Converte lista de IDs de exercícios em string separada por vírgula
        exercise_ids_str = ",".join(self.exercises)

        # Cria novo treino
        cursor.execute("""
            INSERT INTO Treino (
                id, id_aluno, nome_treino, data_criacao, id_exercicio, status
            ) VALUES (?, ?, ?, ?, ?, 'ATIVO')
        """, (
            str(uuid4()),
            student["id"],
            workout_name,
            datetime.now().strftime("%Y-%m-%d"),
            exercise_ids_str
        ))

        conn.commit()
        conn.close()

        self.message = "Treino cadastrado com sucesso."
        self.manager.current = "workout_list"
