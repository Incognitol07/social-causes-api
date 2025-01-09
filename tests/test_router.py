# tests/test_router.py
from fastapi.testclient import TestClient
from app.models import Cause, Contribution

def test_create_cause(client: TestClient, test_cause_data):
    new_cause = test_cause_data

    response = client.post("/causes", json=new_cause)

    assert response.status_code == 200
    assert response.json()["title"] == new_cause["title"]
    assert response.json()["description"] == new_cause["description"]
    assert response.json()["image_url"] == new_cause["image_url"]
    assert "id" in response.json()

def test_create_duplicate_cause(client: TestClient, test_cause_data):
    new_cause = test_cause_data
    client.post("/causes", json=new_cause)  # Create the first cause

    # Attempt to create the same cause again
    response = client.post("/causes", json=new_cause)

    assert response.status_code == 400
    assert response.json()["detail"] == f"Cause '{new_cause["title"]}' already exists"

def test_get_causes(client: TestClient, test_cause: Cause):
    response = client.get("/causes")

    assert response.status_code == 200
    assert len(response.json()) > 0
    for entry in response.json():
        assert "title" in entry
        assert "description" in entry
        assert "image_url" in entry
        assert "id" in entry

def test_get_causes_no_data(client: TestClient):
    # Assuming no causes exist in the DB
    response = client.get("/causes")

    assert response.status_code == 404
    assert response.json()["detail"] == "No causes found"

def test_get_cause(client: TestClient, test_cause: Cause):
    new_cause = test_cause

    response = client.get(f"/causes/{new_cause.id}")

    assert response.status_code == 200
    assert response.json()["title"] == new_cause.title
    assert response.json()["description"] == new_cause.description
    assert response.json()["image_url"] == new_cause.image_url

def test_get_cause_not_found(client: TestClient):
    invalid_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(f"/causes/{invalid_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"No cause found with ID: {invalid_id}"

def test_update_cause(client: TestClient, test_cause: Cause, test_update_cause_data):
    new_cause = test_cause
    update_cause = test_update_cause_data

    response = client.put(f"/causes/{new_cause.id}", json=update_cause)

    assert response.status_code == 200
    assert response.json()["title"] == update_cause["title"]
    assert response.json()["description"] == update_cause["description"]
    assert response.json()["image_url"] == update_cause["image_url"]

def test_update_cause_not_found(client: TestClient, test_update_cause_data):
    invalid_id = "00000000-0000-0000-0000-000000000000"
    update_cause = test_update_cause_data

    response = client.put(f"/causes/{invalid_id}", json=update_cause)

    assert response.status_code == 404
    assert response.json()["detail"] == f"No cause found with ID: {invalid_id}"

def test_delete_cause(client: TestClient, test_cause: Cause):
    new_cause = test_cause

    response = client.delete(f"/causes/{new_cause.id}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Deleted cause with ID: {new_cause.id}"

def test_delete_cause_not_found(client: TestClient):
    invalid_id = "00000000-0000-0000-0000-000000000000"

    response = client.delete(f"/causes/{invalid_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"No cause found with ID: {invalid_id}"

def test_contribute_to_a_cause(client: TestClient, test_cause: Cause, test_contribution_data):
    cause = test_cause
    contribution_data = test_contribution_data

    response = client.post(f"/causes/{cause.id}/contribute", json=contribution_data)

    assert response.status_code == 200
    assert response.json()["name"] == contribution_data["name"]
    assert response.json()["email"] == contribution_data["email"]
    assert response.json()["amount"] == contribution_data["amount"]

def test_contribute_to_nonexistent_cause(client: TestClient, test_contribution_data):
    invalid_id = "00000000-0000-0000-0000-000000000000"
    contribution_data = test_contribution_data

    response = client.post(f"/causes/{invalid_id}/contribute", json=contribution_data)

    assert response.status_code == 404
    assert response.json()["detail"] == f"No cause found with ID: {invalid_id}"

def test_get_contributions(client: TestClient, test_cause: Cause, test_contribution_data):
    cause = test_cause
    contribution_data = test_contribution_data

    response = client.post(f"/causes/{cause.id}/contribute", json=contribution_data)
    response = client.get(f"/causes/{cause.id}/contribute")

    assert response.status_code == 200
    contributions = response.json()["contributions"]
    assert len(contributions) > 0
    for contribution in contributions:
        assert "name" in contribution
        assert "email" in contribution
        assert "amount" in contribution

def test_get_contributions_not_found(client: TestClient, test_cause):
    cause = test_cause

    response = client.get(f"/causes/{cause.id}/contribute")

    assert response.status_code == 404
    assert response.json()["detail"] == f"No contributions were found for cause with ID: {cause.id}"