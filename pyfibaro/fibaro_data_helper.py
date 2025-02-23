"""Fibaro data helper provides static method to read and
process data for the different fibaro API endpoints."""

from pyfibaro.fibaro_client import FibaroClient
from pyfibaro.fibaro_device import DeviceModel

CONTROLLER_TYPES = [
    "com.fibaro.zwavePrimaryController",
    "com.fibaro.zigbeePrimaryController",
    "com.fibaro.niceEngine",
]


def read_rooms(fibaro_client: FibaroClient) -> dict[int, str]:
    """Read dictionary mapping room ids to room name."""
    return {room.fibaro_id: room.name for room in fibaro_client.read_rooms()}


def read_devices(
    fibaro_client: FibaroClient, include_devices_from_plugins: bool = False
) -> list[DeviceModel]:
    """Read all enabled devices."""
    devices = fibaro_client.read_devices()

    return [
        device
        for device in devices
        if (not device.is_plugin or include_devices_from_plugins)
        and device.enabled
    ]


def find_master_devices(devices: list[DeviceModel]) -> list[DeviceModel]:
    """Find master devices only."""
    controller_ids = _get_controller_ids(devices)

    return [
        device for device in devices
        if _is_master_device(device, controller_ids)
    ]


def _get_controller_ids(devices: list[DeviceModel]) -> set[int]:
    return {device.fibaro_id for device in devices if device.type in CONTROLLER_TYPES}


def _is_master_device(device: DeviceModel, controller_ids: set[int]) -> bool:
    return device.parent_fibaro_id in controller_ids or (
        device.parent_fibaro_id == 0 and device.fibaro_id not in controller_ids
    )
