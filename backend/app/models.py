"""
Data models for the application
"""
import uuid
from datetime import datetime
from datetime import timezone as tz
from typing import Any

from pydantic import EmailStr
from sqlalchemy import Integer, PrimaryKeyConstraint
from sqlmodel import JSON, Column, Field, Relationship, SQLModel


def utcnow() -> datetime:
    """Return the current UTC time"""
    return datetime.now(tz.utc)


# Shared properties
class UserBase(SQLModel):
    """Base user properties"""

    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    """Properties to receive via API on user creation"""

    password: str = Field(min_length=8, max_length=40, regex=r"^(?=.*[A-Z])(?=.*\d).+$")


class UserRegister(SQLModel):
    """Properties to receive via API on user registration"""

    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    """Properties to receive via API on user update"""

    email: EmailStr = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    """Properties to receive via API on user update"""

    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    """Properties to receive via API on password update"""

    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    """Database model for users"""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    devices: list["Device"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    """Properties to return via API"""

    id: uuid.UUID


class UsersPublic(SQLModel):
    """Properties to return via API"""

    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    """Base item properties"""

    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    """Properties to receive on item creation"""


# Properties to receive on item update
class ItemUpdate(ItemBase):
    """Properties to receive on item update"""

    title: str = Field(default=None, min_length=1, max_length=255)


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    """Database model for items"""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    """Properties to return via API"""

    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    """Properties to return via API"""

    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    """Generic message"""

    message: str


# JSON payload containing access token
class Token(SQLModel):
    """JSON payload containing access token"""

    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    """Contents of JWT token"""

    sub: str | None = None


class NewPassword(SQLModel):
    """New password"""

    token: str
    new_password: str = Field(min_length=8, max_length=40)


# Shared properties
class DeviceBase(SQLModel):
    """Base device properties"""

    device_name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on device creation
class DeviceCreate(DeviceBase):
    """Properties to receive on device creation"""


# Properties to receive on device update
class DeviceUpdate(DeviceBase):
    """Properties to receive on device update"""

    device_name: str = Field(default=None, min_length=1, max_length=255)


# Database model, database table inferred from class name
class Device(DeviceBase, table=True):
    """Database model for devices"""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    provider_device_id: str | None = Field(
        None, description="Unique identifier of the external device"
    )
    device_name: str = Field(max_length=255)
    last_reported_latitude: float | None = None
    last_reported_longitude: float | None = None
    is_online: bool = True
    last_online_timestamp: datetime | None
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="devices")
    telemetry_data: list["TelemetryData"] = Relationship(back_populates="device")


# Properties to return via API, id is always required
class DevicePublic(DeviceBase):
    """Properties to return via API"""

    id: uuid.UUID
    owner_id: uuid.UUID


class DevicesPublic(SQLModel):
    """Properties to return via API"""

    data: list[DevicePublic]
    count: int


class TelemetryData(SQLModel, table=True):
    """Database model for telemetry data"""

    id: int = Field(default=None, sa_column=Column(Integer, autoincrement=True))
    storage_server_timestamp_utc: datetime = Field(default_factory=utcnow)
    ident: str = Field(default="unknown_device")
    position_altitude: float | None = None
    position_hdop: float | None = None
    position_latitude: float | None = None
    position_longitude: float | None = None
    position_satellites: int | None = None
    server_timestamp: datetime | None = Field(default=None, nullable=True)
    timestamp: datetime | None = Field(default=None, nullable=False)
    device_type_id: int | None = None
    channel_id: int | None = None
    protocol_id: int | None = None
    engine_ignition_status: bool | None = None
    provider_device_id: str | None = Field(
        None, description="Unique identifier of the external device"
    )
    device_name: str | None = Field(None, description="Name assigned to the device")
    din: int | None = Field(None, description="Digital input status")
    event_enum: int | None = Field(None, description="Event code in enumerated form")
    event_seqnum: int | None = Field(None, description="Event sequence number")
    gnss_antenna_status: str | None = Field(None, description="GNSS antenna status")
    gsm_network_roaming_status: str | None = Field(
        None, description="GSM network roaming status"
    )
    message_type_enum: int | None = Field(
        None, description="Message type in enumerated form"
    )
    peer: str | None = Field(
        None, description="Network peer information (e.g., IP address and port)"
    )
    position_direction: float | None = Field(
        None, description="Direction or heading of the device"
    )
    position_speed: float | None = Field(None, description="Speed of the device")
    position_valid: bool | None = Field(
        None, description="Boolean indicating if position data is valid"
    )
    timestamp_key: int | None = Field(
        None, description="Timestamp key for indexing or reference"
    )
    accumulator_0: float | None = None
    accumulator_1: float | None = None
    accumulator_2: float | None = None
    accumulator_3: float | None = None
    accumulator_4: float | None = None
    accumulator_5: float | None = None
    accumulator_6: float | None = None
    accumulator_7: float | None = None
    accumulator_8: float | None = None
    accumulator_9: float | None = None
    accumulator_10: float | None = None
    accumulator_11: float | None = None
    accumulator_12: float | None = None
    accumulator_13: float | None = None
    accumulator_14: float | None = None
    accumulator_15: float | None = None
    raw_data: dict[str, Any] | None = Field(sa_column=Column(JSON))
    device_id: uuid.UUID = Field(foreign_key="device.id", nullable=False)
    device: Device | None = Relationship(
        back_populates="telemetry_data", cascade_delete=True
    )

    __table_args__ = (PrimaryKeyConstraint("id", "timestamp"),)
