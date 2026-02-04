from fastapi import status


def _auth_header(client):
    payload = {"email": "tasks@example.com", "password": "supersecret"}
    client.post("/auth/register", json=payload)
    token = client.post("/auth/login", json=payload).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_and_list_tasks(client):
    headers = _auth_header(client)
    task_payload = {
        "title": "Preparar presentación",
        "description": "Slides y demo",
        "priority": "ALTA",
        "status": "PENDIENTE",
    }
    create_response = client.post("/tasks", json=task_payload, headers=headers)
    assert create_response.status_code == status.HTTP_201_CREATED
    assert create_response.json()["title"] == task_payload["title"]

    list_response = client.get("/tasks", headers=headers)
    assert list_response.status_code == status.HTTP_200_OK
    assert len(list_response.json()) == 1


def test_update_and_delete_task(client):
    headers = _auth_header(client)
    create_response = client.post(
        "/tasks",
        json={"title": "Escribir memoria", "priority": "MEDIA", "status": "PENDIENTE"},
        headers=headers,
    )
    task_id = create_response.json()["id"]

    update_response = client.put(
        f"/tasks/{task_id}",
        json={"status": "EN_PROGRESO"},
        headers=headers,
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json()["status"] == "EN_PROGRESO"

    delete_response = client.delete(f"/tasks/{task_id}", headers=headers)
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
