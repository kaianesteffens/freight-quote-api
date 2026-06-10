def test_register_returns_user(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "new@example.com",
            "full_name": "New User",
            "password": "supersecret",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "new@example.com"
    assert "id" in body
    assert "password" not in body


def test_register_duplicate_email_conflicts(client):
    payload = {
        "email": "dup@example.com",
        "full_name": "Dup User",
        "password": "supersecret",
    }
    assert client.post("/auth/register", json=payload).status_code == 201
    assert client.post("/auth/register", json=payload).status_code == 409


def test_login_returns_token(client):
    payload = {
        "email": "login@example.com",
        "full_name": "Login User",
        "password": "supersecret",
    }
    client.post("/auth/register", json=payload)
    response = client.post(
        "/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_login_wrong_password_unauthorized(client):
    payload = {
        "email": "wrong@example.com",
        "full_name": "Wrong User",
        "password": "supersecret",
    }
    client.post("/auth/register", json=payload)
    response = client.post(
        "/auth/login",
        json={"email": payload["email"], "password": "bad-password"},
    )
    assert response.status_code == 401


def test_me_requires_authentication(client):
    assert client.get("/auth/me").status_code == 401


def test_me_returns_current_user(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"
