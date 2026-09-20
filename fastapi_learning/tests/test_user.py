import random
import uuid

import pytest
from fastapi.testclient import TestClient

from fastapi_learning.config import settings
from fastapi_learning.main import app

client = TestClient(app)

PASSWORD = "Test1234!"


def _rand_suffix() -> str:
    return uuid.uuid4().hex[:10]


def _rand_phone() -> str:
    return "1" + "".join(random.choice("0123456789") for _ in range(10))


def _register(email: str | None = None, phone: str | None = None, password: str = PASSWORD):
    payload = {"name": f"tester_{_rand_suffix()}", "password": password}
    if email is not None:
        payload["email"] = email
    if phone is not None:
        payload["phone"] = phone
    return client.post("/auth/register", json=payload)


def _login(username: str, password: str = PASSWORD):
    return client.post("/auth/jwt/login", data={"username": username, "password": password})


def test_register_with_email():
    with client:
        email = f"email_{_rand_suffix()}@example.com"
        resp = _register(email=email)
        assert resp.status_code == 201
        body = resp.json()
        assert body["email"] == email
        assert body["name"]
        assert body["uid"] >= settings.FIRST_UID


def test_register_with_phone_only():
    with client:
        phone = _rand_phone()
        resp = _register(phone=phone)
        assert resp.status_code == 201
        body = resp.json()
        assert body["phone"] == phone
        assert body["uid"] >= settings.FIRST_UID


def test_register_duplicate_email():
    with client:
        email = f"dup_{_rand_suffix()}@example.com"
        assert _register(email=email).status_code == 201
        resp = _register(email=email, phone=_rand_phone())
        assert resp.status_code == 400
        assert resp.json()["message"] == "REGISTER_USER_ALREADY_EXISTS"


def test_register_duplicate_phone():
    with client:
        phone = _rand_phone()
        assert _register(phone=phone).status_code == 201
        resp = _register(email=f"dup2_{_rand_suffix()}@example.com", phone=phone)
        assert resp.status_code == 400
        assert resp.json()["message"] == "REGISTER_USER_ALREADY_EXISTS"


def test_login_with_email():
    with client:
        email = f"login_{_rand_suffix()}@example.com"
        assert _register(email=email).status_code == 201
        resp = _login(email)
        assert resp.status_code == 200
        assert "access_token" in resp.json()


def test_login_with_phone():
    with client:
        phone = _rand_phone()
        assert _register(phone=phone).status_code == 201
        resp = _login(phone)
        assert resp.status_code == 200
        assert "access_token" in resp.json()


def test_login_with_uid():
    with client:
        email = f"uid_{_rand_suffix()}@example.com"
        reg = _register(email=email)
        assert reg.status_code == 201
        uid = reg.json()["uid"]
        resp = _login(str(uid))
        assert resp.status_code == 200
        assert "access_token" in resp.json()


def test_current_user_me():
    with client:
        email = f"me_{_rand_suffix()}@example.com"
        assert _register(email=email).status_code == 201
        token = _login(email).json()["access_token"]
        resp = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert resp.json()["email"] == email


def test_authenticated_route():
    with client:
        email = f"auth_{_rand_suffix()}@example.com"
        assert _register(email=email).status_code == 201
        token = _login(email).json()["access_token"]
        resp = client.get("/authenticated-route", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
