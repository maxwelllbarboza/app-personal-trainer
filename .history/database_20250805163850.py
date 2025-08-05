USERS = {
    "usuario@exemplo.com": {
        "password": "senha123",
        "access_profile": "Trainer",  # ou "Student" dependendo do perfil desejado
        "status": "Active",
        "loginAttempts": 0,
        "lockoutTime": None
    }
}

WORKOUTS = {}

EXERCISES = [
    {"id": "1", "category": "Legs", "name": "Leg Press", "image": "leg_press.png"},
    {"id": "2", "category": "Arms", "name": "Bicep Curl", "image": "bicep_curl.png"},
    # Adicione mais exercícios conforme necessário
]
