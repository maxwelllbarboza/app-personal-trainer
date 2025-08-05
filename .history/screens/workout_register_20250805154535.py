from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from database import USERS, WORKOUTS
from uuid import uuid4
from datetime import datetime

class WorkoutRegisterScreen(Screen):
    student = ObjectProperty(None)
    workout_name = ObjectProperty(None)
    exercises = ListProperty([])
    message = StringProperty("")

    def save_workout(self):
        student_email = self.ids.student.text.strip().lower()
        student = USERS.get(student_email)
        if not student or student['access_profile'] != "Student":
            self.message = "Invalid student."
            return
        workout = {
            "id_workout": str(uuid4()),
            "id_student": student['id_person'],
            "workout_name": self.ids.workout_name.text,
            "creation_date": datetime.now().strftime("%Y-%m-%d"),
            "exercise_ids": self.exercises,
            "status": "Active"
        }
        WORKOUTS[workout['id_workout']] = workout
        self.message = "Workout registered."
        self.manager.current = "workout_list"