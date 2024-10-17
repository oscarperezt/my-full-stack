from datetime import datetime, timezone

from sqlmodel import Session

from app import crud
from app.models import Device, DeviceCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_device(db: Session) -> Device:
    user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    device_name = random_lower_string()
    description = random_lower_string()
    last_online_timestamp = datetime.now(timezone.utc)

    provider_device_id = random_lower_string()  # Generate a random provider_device_id
    device_in = DeviceCreate(
        device_name=device_name,
        description=description,
        last_online_timestamp=last_online_timestamp,
        provider_device_id=provider_device_id,
    )
    return crud.create_device(session=db, device_in=device_in, owner_id=owner_id)
