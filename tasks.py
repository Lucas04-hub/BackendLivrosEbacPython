from celery_app import celery_app
import time

@celery_app.task(name="tasks.somar", bind=True)
def somar(self, a, b):
    time.sleep(3)
    return a + b

@celery_app.task(name="tasks,fatorial", bind=True)
def fatorial(self, n):
    time.sleep(3)
    if n < 0:
        raise ValueError("Número negativo não permitido!")
    
    resultado = 1

    for i in range(2, n + 1):
        resultado *= i
    
    return resultado

# 1 - Vamos criar algumas tarefas
# 2 - Vamos rodar essas tarefas em background usando o Celery
# 3 - Vamos jogar essas  tarefas para o Redis usando-o como sistema de fila


#test_database.py

# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from main import Base, LivroDB, app
# from fastapi.testclient import TestClient
# from main import Usuario
# import os

# DATABASE_URL_TEST = "sqlite:///:memory:"
# engine = create_engine(DATABASE_URL_TEST, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(bind=engine)

# Base.metadata.create_all(bind=engine)

# client = TestClient(app)

# @pytest.fixture(autouse=True)
# def mock_redis(mocker):
    # mock_redis_client = mocker.patch("main.redis_client", autospec=True)
    # mock_redis_client.get.return_value = None

# @pytest.fixture(scope="function")
# def db():
    # db = TestingSessionLocal()
    # try:
        # yield db
    # finally:
        # db.close()

# def test_get_books(db, mocker):
    # admin_user = Usuario(username="admin", password="admin")
    # db.add(admin_user)
    # db.commit()
    
    # response = client.get("/livros", auth=("admin", "admin"))
    # assert response.status_code == 200

    # data = response.json()

    # assert len(data["livros"]) == 10
    # assert data["livros"][0]["nome_livro"] == "A Revolução dos Bichos"
    # assert data["livros"][0]["autor_livro"] == "George Orwell"
    # assert data["livros"][0]["ano_livro"] == 1945