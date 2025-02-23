"""Test data helpers."""

from unittest.mock import Mock

from pyfibaro.fibaro_data_helper import (
    read_devices,
    read_rooms,
    find_master_devices,
)
from pyfibaro.fibaro_device import DeviceModel
from pyfibaro.fibaro_room import RoomModel

from .test_utils import load_fixture

scene_payload = load_fixture("scene-hc3.json")
room_payload = load_fixture("room.json")
device_payload = load_fixture("device-hc3.json")
device2_payload = load_fixture("device.json")


def test_read_rooms() -> None:
    """Test read rooms"""
    client = Mock()
    client.read_rooms.return_value = [RoomModel(room_payload[0])]

    rooms = read_rooms(client)

    assert len(rooms) == 1
    assert rooms[4] == "Wohnen"


def test_read_devices_master_devices() -> None:
    """Test read devices"""
    devices = [
        DeviceModel(device_payload[0], Mock(), 4),
        DeviceModel(device2_payload[2], Mock(), 4),
        DeviceModel(device2_payload[3], Mock(), 4),
        DeviceModel(device_payload[4], Mock(), 4),
    ]
    client = Mock()
    client.read_devices.return_value = devices

    devices = find_master_devices(devices)

    assert len(devices) == 1


def test_read_devices() -> None:
    """Test read devices"""
    devices = [
        DeviceModel(device2_payload[2], Mock(), 4),
        DeviceModel(device2_payload[3], Mock(), 4),
    ]
    client = Mock()
    client.read_devices.return_value = devices

    devices = read_devices(client, True)

    assert len(devices) == 2
