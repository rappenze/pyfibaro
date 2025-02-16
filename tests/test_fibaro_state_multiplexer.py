"""Test FibaroStateMultiplexer class."""

from unittest.mock import Mock
from pyfibaro.fibaro_device import DeviceModel
from pyfibaro.fibaro_state_multiplexer import FibaroStateMultiplexer

from .test_utils import load_fixture

refresh_payload = load_fixture("refresh.json")
device_payload = load_fixture("device.json")


def test_fibaro_state_multiplexer_start() -> None:
    """Test state multiplexer start."""
    devices = [
        DeviceModel(device_payload[2], Mock(), 4),
        DeviceModel(device_payload[3], Mock(), 4),
    ]

    fibaro_client = Mock()
    fibaro_client.read_devices.return_value = devices
    multiplexer = FibaroStateMultiplexer(fibaro_client)

    multiplexer.start()

    fibaro_client.register_update_handler.assert_called_once()


def test_fibaro_state_multiplexer_stop() -> None:
    """Test state multiplexer stop."""
    fibaro_client = Mock()
    multiplexer = FibaroStateMultiplexer(fibaro_client)

    multiplexer.stop()

    fibaro_client.unregister_update_handler.assert_called_once()


def test_fibaro_state_multiplexer_state_change_listener() -> None:
    """Test state multiplexer add state change listener."""
    devices = [
        DeviceModel(device_payload[2], Mock(), 4),
        DeviceModel(device_payload[3], Mock(), 4),
    ]

    fibaro_client = Mock()
    fibaro_client.read_devices.return_value = devices

    multiplexer = FibaroStateMultiplexer(fibaro_client)
    multiplexer.start()

    result_mock = Mock()
    multiplexer.add_change_listener(13, result_mock.call_method)
    assert len(multiplexer._change_listeners.get(13)) == 1

    multiplexer._on_change(refresh_payload)

    result_mock.call_method.assert_called_once()


def test_fibaro_state_multiplexer_get_devices() -> None:
    """Test state multiplexer add state change listener."""
    devices = [
        DeviceModel(device_payload[2], Mock(), 4),
        DeviceModel(device_payload[3], Mock(), 4),
    ]

    fibaro_client = Mock()
    fibaro_client.read_devices.return_value = devices

    multiplexer = FibaroStateMultiplexer(fibaro_client)
    multiplexer.start()
    devices = multiplexer.get_devices()
    assert len(devices) == 2


def test_fibaro_state_multiplexer_add_remove_state_change_listener() -> None:
    """Test state multiplexer add state change listener."""
    devices = [
        DeviceModel(device_payload[2], Mock(), 4),
        DeviceModel(device_payload[3], Mock(), 4),
    ]

    fibaro_client = Mock()
    fibaro_client.read_devices.return_value = devices

    multiplexer = FibaroStateMultiplexer(fibaro_client)

    result_mock = Mock()
    remove = multiplexer.add_change_listener(13, result_mock.call_method)
    assert len(multiplexer._change_listeners.get(13)) == 1

    remove()

    assert len(multiplexer._change_listeners.get(13)) == 0


def test_fibaro_state_multiplexer_event_listener() -> None:
    """Test state multiplexer add event listener."""

    fibaro_client = Mock()
    multiplexer = FibaroStateMultiplexer(fibaro_client)

    result_mock = Mock()
    multiplexer.add_event_listener(28, result_mock.call_method)

    multiplexer._on_change(refresh_payload)

    result_mock.call_method.assert_called_once()
