from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.config import settings
from app.core.db import engine
from app.models import Device, TelemetryData


def test_receive_report(client: TestClient) -> None:
    # Sample real data reports
    report1: dict[str, int | float | str | bool] = {
        "accumulator.0": 27793898,
        "accumulator.1": 577,
        "accumulator.10": 1280,
        "accumulator.11": 211786565,
        "accumulator.12": 1361,
        "accumulator.13": 12970,
        "accumulator.14": 0,
        "accumulator.15": 0,
        "accumulator.2": 1436,
        "accumulator.3": 0,
        "accumulator.4": 0,
        "accumulator.5": 0,
        "accumulator.6": 16182,
        "accumulator.7": 118,
        "accumulator.8": 52,
        "accumulator.9": 14014,
        "channel.id": 1221609,
        "device.id": 6010846,
        "device.name": "FVO118",
        "device.type.id": 273,
        "din": 31,
        "engine.ignition.status": True,
        "event.enum": 4,
        "event.seqnum": 2753,
        "gisgraphy.address": "A 1464 m. de Hacienda Las Margaritas, Becerril, Cesar, Colombia",
        "gisgraphy.address.city": "Becerril",
        "gisgraphy.address.countryCode": "CO",
        "gisgraphy.address.state": "Cesar",
        "gisgraphy.address.streetName": "A 1464 m. de Hacienda Las Margaritas",
        "gnss.antenna.status": True,
        "gsm.network.roaming.status": True,
        "ident": "4764252939",
        "message.type.enum": 10,
        "peer": "200.7.102.210:43521",
        "position.direction": 53,
        "position.latitude": 9.734007,
        "position.longitude": -73.494497,
        "position.satellites": 14,
        "position.speed": 50,
        "position.valid": False,
        "protocol.id": 42,
        "server.timestamp": 1729132792.719063,
        "timestamp": 1729132792,
        "timestamp.key": 1729132792.002753,
    }

    report2: dict[str, int | float | str | bool] = {
        "accumulator.0": 27793898,
        "accumulator.1": 3051,
        "accumulator.10": 1488,
        "accumulator.11": 211788979,
        "accumulator.12": 1305,
        "accumulator.13": 7947,
        "accumulator.14": 0,
        "accumulator.15": 0,
        "accumulator.2": 1552,
        "accumulator.3": 0,
        "accumulator.4": 0,
        "accumulator.5": 0,
        "accumulator.6": 21417,
        "accumulator.7": 277,
        "accumulator.8": 52,
        "accumulator.9": 14105,
        "channel.id": 1221609,
        "device.id": 6010846,
        "device.name": "FVO118",
        "device.type.id": 273,
        "din": 31,
        "engine.ignition.status": True,
        "event.enum": 4,
        "event.seqnum": 2755,
        "gisgraphy.address": "A 1069 m. de Hacienda Las Margaritas, Becerril, Cesar, Colombia",
        "gisgraphy.address.city": "Becerril",
        "gisgraphy.address.countryCode": "CO",
        "gisgraphy.address.state": "Cesar",
        "gisgraphy.address.streetName": "A 1069 m. de Hacienda Las Margaritas",
        "gnss.antenna.status": True,
        "gsm.network.roaming.status": True,
        "ident": "4764252939",
        "message.type.enum": 10,
        "peer": "200.7.102.210:38948",
        "position.direction": 24,
        "position.latitude": 9.744994,
        "position.longitude": -73.475201,
        "position.satellites": 12,
        "position.speed": 47,
        "position.valid": False,
        "protocol.id": 42,
        "server.timestamp": 1729132952.593158,
        "timestamp": 1729132951,
        "timestamp.key": 1729132951.002755,
    }

    # Prepare the reports data
    reports = [report1, report2]

    # Send the POST request to the reports endpoint
    response = client.post(
        f"{settings.API_V1_STR}/reports/reports/",
        json=reports,
    )

    # Assert that the response is successful
    assert response.status_code == 200
    content = response.json()
    assert content["status"] == "success"
    assert content["message"] == f"{len(reports)} reports processed"

    # Verify that telemetry data is stored in the database
    with Session(engine) as session:
        # Fetch the device using provider_device_id
        device_provider_id = report1["device.id"]
        device = session.exec(
            select(Device).where(Device.provider_device_id == str(device_provider_id))
        ).first()
        assert device is not None
        assert device.device_name == report1["device.name"]

        # Check that telemetry data entries have been created
        telemetry_data_entries = session.exec(
            select(TelemetryData).where(TelemetryData.device_id == device.id)
        ).all()
        assert len(telemetry_data_entries) >= 2  # At least two entries

        # Optionally, verify the content of the telemetry data
        telemetry_data = telemetry_data_entries[-1]  # Get the last entry
        assert telemetry_data.position_latitude == report2["position.latitude"]
        assert telemetry_data.position_longitude == report2["position.longitude"]
        assert (
            telemetry_data.engine_ignition_status == report2["engine.ignition.status"]
        )
