from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, FadeTransition

# Importações dos módulos de banco de dados e telas
from database import create_tables, add_user, add_exercise
from screens.login import LoginScreen
from screens.forgot_password import ForgotPasswordScreen
from screens.trainer_menu import TrainerMenuScreen
from screens.student_list import StudentListScreen
from screens.student_register import StudentRegisterScreen
from screens.workout_list import WorkoutListScreen
from screens.workout_register import WorkoutRegisterScreen


class MainApp(App):
    def build(self):
        # Criação das tabelas no banco de dados (caso ainda não existam)
        create_tables()

        # Adiciona usuário exemplo, se não existir
        add_user("maxwellbarboza@hotmail.com", "Maxwell Barboza", "12345678", "PROFESSOR")

        # Adiciona exercícios padrão, se ainda não estiverem cadastrados
        add_exercise("Legs", "Leg Press", "leg_press.png")
        add_exercise("Arms", "Bicep Curl", "bicep_curl.png")

        # Carrega os arquivos KV
        Builder.load_file('screens/login.kv')
        Builder.load_file('screens/forgot_password.kv')
        Builder.load_file('screens/trainer_menu.kv')
        Builder.load_file('screens/student_list.kv')
        Builder.load_file('screens/student_register.kv')
        Builder.load_file('screens/workout_list.kv')
        Builder.load_file('screens/workout_register.kv')

        # Define as telas da aplicação
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(ForgotPasswordScreen(name="forgot_password"))
        sm.add_widget(TrainerMenuScreen(name="trainer_menu"))
        sm.add_widget(StudentListScreen(name="student_list"))
        sm.add_widget(StudentRegisterScreen(name="student_register"))
        sm.add_widget(WorkoutListScreen(name="workout_list"))
        sm.add_widget(WorkoutRegisterScreen(name="workout_register"))
        return sm


if __name__ == '__main__':
    MainApp().run()
