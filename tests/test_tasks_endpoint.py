import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_calcular_soma(mocker):
    mock_somar_delay = mocker.patch("tasks.somar.delay")

    mock_somar_delay.return_value.id = "fake-task-id"

    response = client.post("/calcular/soma", params={"a": 1, "b": 2})

    assert response.status_code == 200
    assert response.json() == {
        "task_id": "fake-task-id",
        "message": "Tarefa de soma enviada para execução!"
    }




def test_calcular_fatorial(mocker):
    mock_fatorial_delay = mocker.patch("tasks.fatorial.delay")
    
    mock_fatorial_delay.return_value.id = "fake-task-id"

    response = client.post("/calcular/fatorial", params={"n": 5})

    assert response.status_code == 200
    assert response.json() == {
        "task_id": "fake-task-id",
        "message": "Tarefa de fatorial enviada para execução!"
    }
    