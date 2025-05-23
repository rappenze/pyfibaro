"""Fibaro data helper provides static method to read and
process data for the different fibaro API endpoints."""

from pyfibaro.fibaro_client import FibaroClient
from pyfibaro.fibaro_device import DeviceModel

ZWAVE_CONTROLLER = "com.fibaro.zwavePrimaryController"

CONTROLLER_TYPES = [
    ZWAVE_CONTROLLER,
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
    """Find main devices only."""
    controller_ids = _get_controller_ids(devices)

    return _main_devices(devices, controller_ids)


def _get_controller_ids(devices: list[DeviceModel]) -> set[int]:
    controller_ids = {
        device.fibaro_id for device in devices if device.type in CONTROLLER_TYPES}
    zwave_controller_id = {
        device.fibaro_id for device in devices if device.type == ZWAVE_CONTROLLER}
    if len(zwave_controller_id) == 0:
        # When choosing a user account without admin rights sometimes the controller device
        # is not visible on the API. In this case we assume it has id = 1.
        controller_ids.add(1)
    return controller_ids


def _main_devices(devices: list[DeviceModel], controller_ids: set[int]) -> bool:
    children_by_parent_id: dict[int, list[DeviceModel]] = {}
    for d in devices:
        children = children_by_parent_id.setdefault(d.parent_fibaro_id, [])
        children.append(d)

    main_devices = []

    for d in devices:
        if d.parent_fibaro_id in controller_ids or (
            d.parent_fibaro_id == 0 and d.fibaro_id not in controller_ids
        ):
            # Normally devices hanging on a controller or on nothing (id=0)
            # are representing a device.
            # Speical case are plugins which sometimes have an additional parent
            # representing the plugin itself, so devices are the first child level.
            count_of_children_level = 0
            direct_children = children_by_parent_id.get(d.fibaro_id)
            if direct_children:
                count_of_children_level = 1
                for child in direct_children:
                    if children_by_parent_id.get(child.fibaro_id):
                        count_of_children_level = 2

            if count_of_children_level == 2:
                main_devices.extend(direct_children)
            else:
                main_devices.append(d)
    return main_devices
