from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_and_login_flow() -> None:
    register = client.post(
        "/api/auth/register",
        json={"username": "demo", "password": "secret123"},
    )
    assert register.status_code == 201, register.text

    login = client.post(
        "/api/auth/login",
        json={"username": "demo", "password": "secret123"},
    )
    assert login.status_code == 200, login.text
    data = login.json()
    assert data["token_type"] == "bearer"
    assert "access_token" in data

    me = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {data['access_token']}"},
    )
    assert me.status_code == 200, me.text
    assert me.json()["username"] == "demo"
