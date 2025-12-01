from fastapi.testclient import TestClient

from fastapi_learn.main import app

client = TestClient(app)


def test_create_user():
    with client:
        response = client.post(
            "/users",
            json={
                "name": "Ahri",
                "email": "Ahri@Ahri.com",
                "password": "DearAhri",
                "account": "Ahri",
                "description": "I am Ahri",
            },
        )
        assert response.status_code == 200


def test_get_user():
    with client:
        response = client.get("/users")
        assert response.status_code == 200
