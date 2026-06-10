QUOTE_PAYLOAD = {
    "origin": "Sao Paulo",
    "destination": "Rio de Janeiro",
    "weight_kg": 10.0,
    "volume_m3": 0.5,
}


def test_create_quote_requires_authentication(client):
    assert client.post("/quotes", json=QUOTE_PAYLOAD).status_code == 401


def test_create_quote_returns_options(client, auth_headers):
    response = client.post("/quotes", json=QUOTE_PAYLOAD, headers=auth_headers)
    assert response.status_code == 201
    body = response.json()
    assert body["origin"] == QUOTE_PAYLOAD["origin"]
    assert len(body["options"]) == 3
    for option in body["options"]:
        assert option["price"] > 0
        assert option["delivery_days"] > 0


def test_create_quote_validates_positive_weight(client, auth_headers):
    payload = {**QUOTE_PAYLOAD, "weight_kg": 0}
    response = client.post("/quotes", json=payload, headers=auth_headers)
    assert response.status_code == 422


def test_history_lists_only_own_quotes(client, auth_headers):
    client.post("/quotes", json=QUOTE_PAYLOAD, headers=auth_headers)
    client.post("/quotes", json=QUOTE_PAYLOAD, headers=auth_headers)

    other = {
        "email": "other@example.com",
        "full_name": "Other User",
        "password": "supersecret",
    }
    client.post("/auth/register", json=other)
    other_token = client.post(
        "/auth/login",
        json={"email": other["email"], "password": other["password"]},
    ).json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}
    client.post("/quotes", json=QUOTE_PAYLOAD, headers=other_headers)

    response = client.get("/quotes", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2

    other_response = client.get("/quotes", headers=other_headers)
    assert len(other_response.json()) == 1
