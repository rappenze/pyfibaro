"""Fibaro data class is a data reader for the different fibaro API endpoints."""

from pyfibaro.fibaro_client import FibaroClient, InfoModel
from pyfibaro.fibaro_device import DeviceModel
from pyfibaro.fibaro_scene import SceneModel

CONTROLLER_TYPES = [
    "com.fibaro.zwavePrimaryController",
    "com.fibaro.zigbeePrimaryController",
    "com.fibaro.niceEngine",
]


def read_rooms(fibaro_client: FibaroClient) -> dict[int, str]:
    """Read dictionary mapping room ids to room name."""
    return {room.fibaro_id: room.name for room in fibaro_client.read_rooms()}


def read_scenes(fibaro_client: FibaroClient) -> list[SceneModel]:
    """Get all scenes."""
    return fibaro_client.read_scenes()


def get_hub_information(fibaro_client: FibaroClient) -> InfoModel:
    """Get information about the hub."""
    return fibaro_client.read_info()


def read_devices(
    fibaro_client: FibaroClient, include_devices_from_plugins: bool = False
) -> list[DeviceModel]:
    """Read all enabled devices except the once representing the controllers."""
    devices = fibaro_client.read_devices()

    controller_ids = _get_controller_ids(devices)

    return [
        device
        for device in devices
        if device.fibaro_id not in controller_ids
        and (not device.is_plugin or include_devices_from_plugins)
    ]


def _get_controller_ids(devices: list[DeviceModel]) -> set[int]:
    return {device.fibaro_id for device in devices if device.type in CONTROLLER_TYPES}
