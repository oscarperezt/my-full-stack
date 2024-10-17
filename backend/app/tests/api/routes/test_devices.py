import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.device import create_random_device


def test_create_device(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {
        "device_name": "Tracker Device",
        "description": "A GPS tracker",
        "last_online_timestamp": "2024-10-16T10:10:10Z",
    }
    response = client.post(
        f"{settings.API_V1_STR}/devices/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["device_name"] == data["device_name"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


def test_read_device(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    device = create_random_device(db)
    response = client.get(
        f"{settings.API_V1_STR}/devices/{device.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["device_name"] == device.device_name
    assert content["description"] == device.description
    assert content["id"] == str(device.id)
    assert content["owner_id"] == str(device.owner_id)


def test_read_device_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/devices/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Device not found"


def test_update_device(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    device = create_random_device(db)
    data = {"device_name": "Updated Device Name", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/devices/{device.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["device_name"] == data["device_name"]
    assert content["description"] == data["description"]
    assert content["id"] == str(device.id)
    assert content["owner_id"] == str(device.owner_id)
