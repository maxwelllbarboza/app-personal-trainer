import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

USERS = {
    "maxwellbarboza@hotmail.com": {
        "nome": "Maxwell Barboza",
        "senha": hash_password("12345678"),
        "status": "ATIVO",
        "tentativas": 0,
        "tipo": "ALUNO"  # ou "ALUNO" se quiser que caia na tela "student_list"
    }
}

WORKOUTS = {}

EXERCISES = [
    {"id": "1", "category": "Legs", "name": "Leg Press", "image": "leg_press.png"},
    {"id": "2", "category": "Arms", "name": "Bicep Curl", "image": "bicep_curl.png"},
    # Adicione mais exercícios conforme necessário
]
