"""
Devices routes.
"""

import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlalchemy import func
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Device,
    DeviceCreate,
    DevicePublic,
    DevicesPublic,
    DeviceUpdate,
    Message,
)

router = APIRouter()


@router.get("/", response_model=DevicesPublic)
def read_devices(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve devices.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Device)
        count = session.exec(count_statement).one()
        statement = select(Device).offset(skip).limit(limit)
        devices = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Device)
            .where(Device.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Device)
            .where(Device.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        devices = session.exec(statement).all()

    return DevicesPublic(data=devices, count=count)


@router.get("/{id}", response_model=DevicePublic)
def read_device(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get device by ID.
    """
    device = session.get(Device, id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    if not current_user.is_superuser and (device.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return device


@router.post("/", response_model=DevicePublic)
def create_device(
    *, session: SessionDep, current_user: CurrentUser, device_in: DeviceCreate
) -> Any:
    """
    Create new device.
    """
    device = Device.model_validate(device_in, update={"owner_id": current_user.id})
    session.add(device)
    session.commit()
    session.refresh(device)
    return device


@router.put("/{id}", response_model=DevicePublic)
def update_device(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    device_in: DeviceUpdate,
) -> Any:
    """
    Update an device.
    """
    device = session.get(Device, id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    if not current_user.is_superuser and (device.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = device_in.model_dump(exclude_unset=True)
    device.sqlmodel_update(update_dict)
    session.add(device)
    session.commit()
    session.refresh(device)
    return device


@router.delete("/{id}")
def delete_device(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an device.
    """
    device = session.get(Device, id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    if not current_user.is_superuser and (device.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(device)
    session.commit()
    return Message(message="Device deleted successfully")
