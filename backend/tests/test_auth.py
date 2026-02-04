from fastapi import status


def test_register_and_login(client):
    payload = {"email": "user@example.com", "password": "supersecret"}
    register_response = client.post("/auth/register", json=payload)
    assert register_response.status_code == status.HTTP_201_CREATED
    assert "access_token" in register_response.json()

    login_response = client.post("/auth/login", json=payload)
    assert login_response.status_code == status.HTTP_200_OK
    assert "access_token" in login_response.json()


def test_register_duplicate_email(client):
    payload = {"email": "dup@example.com", "password": "supersecret"}
    client.post("/auth/register", json=payload)
    second = client.post("/auth/register", json=payload)
    assert second.status_code == status.HTTP_400_BAD_REQUEST
