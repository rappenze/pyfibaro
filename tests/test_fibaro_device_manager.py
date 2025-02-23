"""Test FibaroDeviceManager."""

from unittest.mock import Mock

from pyfibaro.fibaro_device import DeviceModel
from pyfibaro.fibaro_device_manager import FibaroDeviceManager

from .test_utils import load_fixture

device_payload = load_fixture("device.json")


def test_fibaro_device_manager_get_devices() -> None:
    """Test fibaro device manager."""
    devices = [
        DeviceModel(device_payload[2], Mock(), 4),
        DeviceModel(device_payload[3], Mock(), 4),
    ]

    fibaro_client = Mock()
    fibaro_client.read_devices.return_value = devices

    multiplexer = FibaroDeviceManager(fibaro_client)
    devices = multiplexer.get_devices()
    assert len(devices) == 2


def test_fibaro_device_manager_add_state_listener() -> None:
    """Test manager add state change listener."""
    devices = [
        DeviceModel(device_payload[2], Mock(), 4),
        DeviceModel(device_payload[3], Mock(), 4),
    ]

    listener = Mock()

    fibaro_client = Mock()
    fibaro_client.read_devices.return_value = devices

    manager = FibaroDeviceManager(fibaro_client)
    remove = manager.add_change_listener(13, listener.call_method)

    remove()

    manager.close()


def test_fibaro_device_manager_add_event_listener() -> None:
    """Test manager add event listener."""
    devices = [
        DeviceModel(device_payload[2], Mock(), 4),
        DeviceModel(device_payload[3], Mock(), 4),
    ]

    listener = Mock()

    fibaro_client = Mock()
    fibaro_client.read_devices.return_value = devices

    manager = FibaroDeviceManager(fibaro_client)
    remove = manager.add_event_listener(28, listener.call_method)

    remove()
