"""
This module defines API routes for handling telemetry reports.
It includes endpoints for receiving and storing telemetry reports and
retrieving telemetry data from the database.
"""

from datetime import datetime
from datetime import timezone as tz
from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request
from sqlalchemy import exc
from sqlmodel import Session, select

from app.core.config import settings
from app.core.db import engine
from app.models import Device, TelemetryData, User

router = APIRouter()


def convert_timestamp(timestamp: float | None) -> datetime | None:
    """Convert a Unix timestamp to a datetime object"""
    if timestamp is not None:
        return datetime.fromtimestamp(timestamp, tz.utc)
    return None


def validate_report(report: dict[str, Any]) -> None:
    """Validate a report dictionary"""
    required_fields = ["timestamp", "server.timestamp", "device.id"]
    missing_fields = [field for field in required_fields if not report.get(field)]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")


@router.post("/reports/")
async def receive_report(request: Request) -> dict[str, str]:
    """Receive a report from a streaming telemetry source"""
    try:
        reports_json = await request.json()
        # Ensure reports is a list
        if isinstance(reports_json, dict):
            reports: list[dict[str, Any]] = [reports_json]
        else:
            reports = reports_json

        telemetry_data_list: list[TelemetryData] = []

        with Session(engine) as session:
            for report in reports:
                validate_report(report)

                # Fetch the device using the provider_device_id from the report
                provider_device_id = report.get("device.id")
                device_result = session.exec(
                    select(Device)
                    .where(Device.provider_device_id == provider_device_id)
                    .limit(1)
                )
                device: Device | None = device_result.first()

                if device is None:
                    user = session.exec(
                        select(User).where(User.email == settings.FIRST_SUPERUSER)
                    ).first()

                    if user is None:
                        raise ValueError("Superuser not found")

                    # CREATE A NEW DEVICE
                    device = Device(
                        provider_device_id=provider_device_id,
                        device_name=report.get("device.name", ""),
                        last_online_timestamp=convert_timestamp(
                            report.get("timestamp")
                        ),
                        owner_id=user.id,
                        last_reported_latitude=report.get("position.latitude"),
                        last_reported_longitude=report.get("position.longitude"),
                    )
                    session.add(device)
                    session.commit()
                    session.refresh(device)

                else:
                    # UPDATE EXISTING DEVICE
                    device.last_online_timestamp = convert_timestamp(
                        report.get("timestamp")
                    )
                    device.last_reported_latitude = report.get("position.latitude")
                    device.last_reported_longitude = report.get("position.longitude")
                    session.add(device)
                    session.commit()

                telemetry_data = TelemetryData(
                    storage_server_timestamp_utc=datetime.now(tz.utc),
                    ident=str(report.get("ident", "unknown_device")),
                    position_altitude=report.get("position.altitude"),
                    position_hdop=report.get("position.hdop"),
                    position_latitude=report.get("position.latitude"),
                    position_longitude=report.get("position.longitude"),
                    position_satellites=report.get("position.satellites"),
                    server_timestamp=convert_timestamp(report.get("server.timestamp")),
                    timestamp=convert_timestamp(report.get("timestamp")),
                    device_type_id=report.get("device.type.id"),
                    channel_id=report.get("channel.id"),
                    protocol_id=report.get("protocol.id"),
                    engine_ignition_status=report.get("engine.ignition.status", False),
                    provider_device_id=report.get("device.id"),
                    device_name=report.get("device.name"),
                    din=report.get("din"),
                    event_enum=report.get("event.enum"),
                    event_seqnum=report.get("event.seqnum"),
                    gnss_antenna_status=report.get("gnss.antenna.status"),
                    gsm_network_roaming_status=report.get("gsm.network.roaming.status"),
                    message_type_enum=report.get("message.type.enum"),
                    peer=report.get("peer"),
                    position_direction=report.get("position.direction"),
                    position_speed=report.get("position.speed"),
                    position_valid=report.get("position.valid"),
                    timestamp_key=report.get("timestamp.key"),
                    accumulator_0=report.get("accumulator.0"),
                    accumulator_1=report.get("accumulator.1"),
                    accumulator_2=report.get("accumulator.2"),
                    accumulator_3=report.get("accumulator.3"),
                    accumulator_4=report.get("accumulator.4"),
                    accumulator_5=report.get("accumulator.5"),
                    accumulator_6=report.get("accumulator.6"),
                    accumulator_7=report.get("accumulator.7"),
                    accumulator_8=report.get("accumulator.8"),
                    accumulator_9=report.get("accumulator.9"),
                    accumulator_10=report.get("accumulator.10"),
                    accumulator_11=report.get("accumulator.11"),
                    accumulator_12=report.get("accumulator.12"),
                    accumulator_13=report.get("accumulator.13"),
                    accumulator_14=report.get("accumulator.14"),
                    accumulator_15=report.get("accumulator.15"),
                    raw_data=report,
                    device_id=device.id,
                )
                telemetry_data_list.append(telemetry_data)

        with Session(engine) as session:
            session.bulk_save_objects(telemetry_data_list)
            session.commit()

        return {"status": "success", "message": f"{len(reports)} reports processed"}
    except exc.SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/reports/")
async def get_telemetry_data(
    limit: int = Query(default=10, description="Limit the number of records returned"),
    offset: int = Query(default=0, description="Offset for pagination"),
    ident: str | None = Query(None, description="Filter by device identifier (ident)"),
    position_latitude: float | None = Query(
        None, description="Filter by position latitude"
    ),
    position_longitude: float | None = Query(
        None, description="Filter by position longitude"
    ),
    engine_ignition_status: bool | None = Query(
        None, description="Filter by engine ignition status"
    ),
    timestamp_from: datetime | None = Query(
        None, description="Filter by timestamp from"
    ),
    timestamp_to: datetime | None = Query(None, description="Filter by timestamp to"),
) -> list[TelemetryData]:
    """Retrieve telemetry data from the database"""
    try:
        with Session(engine) as session:
            # Start building the query
            query = select(TelemetryData)

            # Apply filters if provided
            if ident:
                query = query.where(TelemetryData.ident == ident)
            if position_latitude:
                query = query.where(
                    TelemetryData.position_latitude == position_latitude
                )
            if position_longitude:
                query = query.where(
                    TelemetryData.position_longitude == position_longitude
                )
            if engine_ignition_status is not None:
                query = query.where(
                    TelemetryData.engine_ignition_status == engine_ignition_status
                )

            if timestamp_from and TelemetryData.timestamp:
                query = query.where(TelemetryData.timestamp >= timestamp_from)
            if timestamp_to and TelemetryData.timestamp:
                query = query.where(TelemetryData.timestamp <= timestamp_to)

            # Apply pagination
            query = query.offset(offset).limit(limit)

            # Execute the query and fetch results
            results = session.exec(query).all()
            return list(results)
    except exc.SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e
