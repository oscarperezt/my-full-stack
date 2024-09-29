import uuid

from pydantic import EmailStr
from sqlmodel import SQLModel, Column, JSON, Relationship
from sqlmodel import Field
from typing import Any, Optional
from datetime import datetime
from datetime import timezone as tz


def utcnow() -> datetime:
    return datetime.now(tz.utc)


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr = Field(
        default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(
        back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str = Field(
        default=None, min_length=1, max_length=255)


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class TelemetryData(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    storage_server_timestamp_utc: datetime = Field(default_factory=utcnow)
    ident: str = Field(default="unknown_device")
    position_altitude: Optional[float] = None
    position_hdop: Optional[float] = None
    position_latitude: Optional[float] = None
    position_longitude: Optional[float] = None
    position_satellites: Optional[int] = None
    server_timestamp: Optional[datetime] = Field(default=None, nullable=True)
    timestamp: Optional[datetime] = Field(default=None, nullable=True)
    device_type_id: Optional[int] = None
    channel_id: Optional[int] = None
    protocol_id: Optional[int] = None
    engine_ignition_status: Optional[bool] = None
    device_id: Optional[str] = Field(
        None, description="Unique identifier of the device")
    device_name: Optional[str] = Field(
        None, description="Name assigned to the device")
    din: Optional[int] = Field(
        None, description="Digital input status")
    event_enum: Optional[int] = Field(
        None, description="Event code in enumerated form")
    event_seqnum: Optional[int] = Field(
        None, description="Event sequence number")
    gnss_antenna_status: Optional[str] = Field(
        None, description="GNSS antenna status")
    gsm_network_roaming_status: Optional[str] = Field(
        None, description="GSM network roaming status")
    message_type_enum: Optional[int] = Field(
        None, description="Message type in enumerated form")
    peer: Optional[str] = Field(
        None,
        description="Network peer information (e.g., IP address and port)")
    position_direction: Optional[float] = Field(
        None, description="Direction or heading of the device")
    position_speed: Optional[float] = Field(
        None, description="Speed of the device")
    position_valid: Optional[bool] = Field(
        None, description="Boolean indicating if position data is valid")
    timestamp_key: Optional[int] = Field(
        None, description="Timestamp key for indexing or reference")
    accumulator_0: Optional[float] = None
    accumulator_1: Optional[float] = None
    accumulator_2: Optional[float] = None
    accumulator_3: Optional[float] = None
    accumulator_4: Optional[float] = None
    accumulator_5: Optional[float] = None
    accumulator_6: Optional[float] = None
    accumulator_7: Optional[float] = None
    accumulator_8: Optional[float] = None
    accumulator_9: Optional[float] = None
    accumulator_10: Optional[float] = None
    accumulator_11: Optional[float] = None
    accumulator_12: Optional[float] = None
    accumulator_13: Optional[float] = None
    accumulator_14: Optional[float] = None
    accumulator_15: Optional[float] = None
    raw_data: Optional[dict[str, Any]] = Field(sa_column=Column(JSON))
