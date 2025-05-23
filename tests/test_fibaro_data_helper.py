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
device3_payload = load_fixture("device-netatmo-plugin.json")


def test_read_rooms() -> None:
    """Test read rooms"""
    client = Mock()
    client.read_rooms.return_value = [RoomModel(room_payload[0])]

    rooms = read_rooms(client)

    assert len(rooms) == 1
    assert rooms[4] == "Wohnen"


def test_read_devices_main_devices() -> None:
    """Test read devices"""
    devices = [
        # z-wave controller is no device
        DeviceModel(device_payload[0], Mock(), 4),
        # main endpoint reported as device
        DeviceModel(device2_payload[2], Mock(), 4),
        # child endpoint not reported as device
        DeviceModel(device2_payload[3], Mock(), 4),
        # zigbee controller is no device
        DeviceModel(device_payload[4], Mock(), 4),
    ]
    client = Mock()
    client.read_devices.return_value = devices

    devices = find_master_devices(devices)

    assert len(devices) == 1
    assert devices[0].name == "Hifi Main"


def test_read_devices_main_devices_without_zwave_controller() -> None:
    """Test read z-wave devices without a zwave controller"""
    devices = [
        # main entity
        DeviceModel(device2_payload[2], Mock(), 4),
        # child entity
        DeviceModel(device2_payload[3], Mock(), 4),
    ]
    client = Mock()
    client.read_devices.return_value = devices

    devices = find_master_devices(devices)

    assert len(devices) == 1
    assert devices[0].name == "Hifi Main"


def test_read_devices_main_devices_netatmo() -> None:
    """Test read netatmo devices"""
    devices = [
        DeviceModel(device, Mock(), 4) for device in device3_payload
    ]
    client = Mock()
    client.read_devices.return_value = devices

    devices = find_master_devices(devices)

    assert len(devices) == 2
    assert devices[0].name == "Netatmo Weather Sation"
    assert devices[1].name == "Netatmo Weather Station 2"


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
