# tests/test_router.py
from fastapi.testclient import TestClient
from app.models import Cause

def test_create_cause(client: TestClient, test_cause_data):
    new_cause = test_cause_data

    response = client.post(
        "/causes",
        json = new_cause
    )

    assert response.status_code == 200
    assert response.json()["title"] == new_cause["title"]
    assert response.json()["description"] == new_cause["description"]
    assert response.json()["image_url"] == new_cause["image_url"]
    assert "id" in response.json()


def test_get_causes(client: TestClient, test_cause: Cause):
    new_cause1 = test_cause
    new_cause2 = test_cause

    response = client.get(
        "/causes"
    )

    assert response.status_code == 200
    for entry in response.json():
        assert entry["title"] == "Social Causes"
        assert entry["description"] == "A cause that is open to contributions"
        assert entry["image_url"] == "https://image.url"
        assert "id" in entry

def test_get_cause(client: TestClient, test_cause: Cause):
    new_cause = test_cause

    response = client.get(
        f"/causes/{new_cause.id}"
    )

    assert response.status_code == 200
    assert response.json()["title"] == new_cause.title
    assert response.json()["description"] == new_cause.description
    assert response.json()["image_url"] == new_cause.image_url
    assert "id" in response.json()

def test_update_cause(client: TestClient, test_cause: Cause, test_update_cause_data):
    new_cause = test_cause
    update_cause = test_update_cause_data

    response = client.put(
        f"/causes/{new_cause.id}",
        json=update_cause
    )

    assert response.status_code == 200
    assert response.json()["title"] == update_cause["title"]
    assert response.json()["description"] == update_cause["description"]
    assert response.json()["image_url"] == update_cause["image_url"]
    assert "id" in response.json()

def test_delete_cause(client: TestClient, test_cause: Cause):
    new_cause = test_cause

    response = client.delete(
        f"/causes/{new_cause.id}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Deleted cause with ID: {new_cause.id}"


def test_contribute_to_a_cause(client: TestClient, test_cause: Cause, test_contribution_data):
    cause = test_cause
    contribution_data = test_contribution_data

    response = client.post(
        f"/causes/{cause.id}/contribute",
        json=contribution_data
    )

    assert response.status_code == 200
    assert response.json()["name"] == contribution_data["name"]
    assert response.json()["email"] == contribution_data["email"]
    assert response.json()["amount"] == 1000000
    assert "cause_id" in response.json()