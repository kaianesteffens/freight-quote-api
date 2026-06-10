ADDRESS_PAYLOAD = {
    "label": "Home",
    "street": "Main Street",
    "number": "100",
    "city": "Sao Paulo",
    "state": "SP",
    "zip_code": "01000-000",
    "country": "Brazil",
}


def test_addresses_require_authentication(client):
    assert client.get("/addresses").status_code == 401


def test_create_and_list_address(client, auth_headers):
    create = client.post("/addresses", json=ADDRESS_PAYLOAD, headers=auth_headers)
    assert create.status_code == 201
    assert create.json()["label"] == "Home"

    listing = client.get("/addresses", headers=auth_headers)
    assert listing.status_code == 200
    assert len(listing.json()) == 1


def test_update_address(client, auth_headers):
    address_id = client.post(
        "/addresses", json=ADDRESS_PAYLOAD, headers=auth_headers
    ).json()["id"]

    updated = client.put(
        f"/addresses/{address_id}",
        json={**ADDRESS_PAYLOAD, "label": "Office"},
        headers=auth_headers,
    )
    assert updated.status_code == 200
    assert updated.json()["label"] == "Office"


def test_delete_address(client, auth_headers):
    address_id = client.post(
        "/addresses", json=ADDRESS_PAYLOAD, headers=auth_headers
    ).json()["id"]

    assert client.delete(f"/addresses/{address_id}", headers=auth_headers).status_code == 204
    assert client.get(f"/addresses/{address_id}", headers=auth_headers).status_code == 404


def test_cannot_access_other_users_address(client, auth_headers):
    address_id = client.post(
        "/addresses", json=ADDRESS_PAYLOAD, headers=auth_headers
    ).json()["id"]

    other = {
        "email": "intruder@example.com",
        "full_name": "Intruder",
        "password": "supersecret",
    }
    client.post("/auth/register", json=other)
    other_token = client.post(
        "/auth/login",
        json={"email": other["email"], "password": other["password"]},
    ).json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}

    assert client.get(f"/addresses/{address_id}", headers=other_headers).status_code == 404
