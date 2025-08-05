from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, StringProperty
from database import USERS, WORKOUTS

class WorkoutListScreen(Screen):
    workouts = ListProperty([])
    user_email = StringProperty("")

    def on_pre_enter(self):
        user = USERS.get(self.user_email)
        if user and user['access_profile'] == "Trainer":
            self.workouts = list(WORKOUTS.values())
        elif user:
            self.workouts = [w for w in WORKOUTS.values() if w['id_student'] == user['id_person'] and w['status'] == "Active"]
        grid = self.ids.workouts_grid
        grid.clear_widgets()
        for workout in self.workouts:
            from kivy.uix.label import Label
            grid.add_widget(Label(text=workout['workout_name']))

    def add_workout(self):
        self.manager.current = "workout_register"