from uuid import uuid4

def populate_users():
    create_tables()

    add_user(
        id_pessoa=str(uuid4()),
        nome="Maxwell Barboza",
        data_nascimento="1980-01-01",
        telefone="21999999999",
        email="maxwellbarboza@hotmail.com",
        perfil_acesso="Professor",
        senha="12345678"
    )

    add_user(
        id_pessoa=str(uuid4()),
        nome="Aluno Teste",
        data_nascimento="2005-05-10",
        telefone="21988888888",
        email="aluno@teste.com",
        perfil_acesso="Aluno",
        senha="senhaaluno"
    )

populate_users()
