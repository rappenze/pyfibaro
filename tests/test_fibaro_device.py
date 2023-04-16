"""Test FibaroInfo class."""
from __future__ import annotations

from typing import Any

import pytest
import requests_mock

from pyfibaro.fibaro_client import FibaroClient
from pyfibaro.fibaro_device import ColorModel, DeviceModel, ValueModel

from .test_utils import TEST_BASE_URL, TEST_PASSWORD, TEST_USERNAME, load_fixture

device_payload = load_fixture("device.json")
login_payload = load_fixture("login_success.json")
info_payload = load_fixture("info.json")


def test_fibaro_device() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        mock.register_uri("GET", f"{TEST_BASE_URL}devices", json=device_payload)
        mock.register_uri("GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
        mock.register_uri("GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

        client = FibaroClient(TEST_BASE_URL)
        client.set_authentication(TEST_USERNAME, TEST_PASSWORD)
        client.connect()

        devices = client.read_devices()
        assert devices is not None

        assert len(devices) == 3
        assert devices[0].fibaro_id == 1
        assert devices[0].name == "zwave"
        assert devices[0].parent_fibaro_id == 0
        assert devices[0].type == "com.fibaro.zwavePrimaryController"
        assert devices[0].base_type == ""
        assert devices[0].room_id == 0
        assert devices[0].has_unit is False
        assert devices[0].unit is None
        assert devices[0].has_armed is False
        assert devices[0].armed is False
        assert devices[0].has_interface("invalid_interfce") is False
        assert devices[2].has_interface("energy") is True
        assert devices[0].has_battery_level is False
        assert devices[0].battery_level == 0
        assert devices[0].has_endpoint_id is True
        assert devices[0].endpoint_id == 0
        assert devices[0].enabled is True
        assert devices[0].visible is False
        assert devices[0].is_plugin is False
        assert devices[0].value.int_value() == 0
        assert devices[0].value_2.has_value is False
        assert devices[0].color.has_color is False
        assert devices[0].last_color_set.has_color is False
        assert devices[0].state.has_value is False
        assert devices[0].has_brightness is False
        assert devices[0].brightness == 0
        assert devices[0].current_program == 0
        assert devices[0].current_program_id == 0
        assert devices[0].has_mode is False
        assert devices[0].mode == 0
        assert devices[0].has_supported_modes is False
        assert devices[0].supported_modes == []
        assert devices[0].has_operating_mode is False
        assert devices[0].operating_mode == 0
        assert devices[0].has_supported_operating_modes is False
        assert devices[0].supported_operating_modes == []
        assert devices[0].has_thermostat_mode is False
        assert devices[0].thermostat_mode is None
        assert devices[0].has_thermostat_operating_state is False
        assert devices[0].thermostat_operating_state is None
        assert devices[0].has_supported_thermostat_modes is False
        assert devices[0].supported_thermostat_modes == []
        assert devices[0].has_heating_thermostat_setpoint is False
        assert devices[0].heating_thermostat_setpoint == 0
        assert devices[0].has_heating_thermostat_setpoint_future is False
        assert devices[0].heating_thermostat_setpoint_future == 0
        assert devices[0].target_level == 0
        assert devices[0].has_dead is True
        assert devices[0].dead is False
        assert devices[0].has_dead_reason is False
        assert devices[0].dead_reason is None

        assert isinstance(devices[0].actions, dict)
        assert isinstance(devices[0].properties, dict)
        assert mock.call_count == 3


@pytest.mark.parametrize("test_value", ["true", "True", True, 1, 0.1, "1", "0.1"])
def test_fibaro_value_true(test_value: Any) -> None:
    """Test value model"""
    value = ValueModel({"value": test_value}, "value")
    assert value.has_value is True
    assert value.bool_value() is True
    assert value.bool_value(False) is True


@pytest.mark.parametrize("test_value", ["false", "False", False, 0, 0.0, "0", "0.0"])
def test_fibaro_value_false(test_value: Any) -> None:
    """Test value model"""
    value = ValueModel({"value": test_value}, "value")
    assert value.has_value is True
    assert value.bool_value() is False
    assert value.bool_value(True) is False


@pytest.mark.parametrize("test_value", ["1", "1.1", 1, 1.1])
def test_fibaro_value_int(test_value: Any) -> None:
    """Test value model"""
    value = ValueModel({"value": test_value}, "value")
    assert value.has_value is True
    assert value.int_value() == 1


@pytest.mark.parametrize("test_value", ["1", 1])
def test_fibaro_value_float(test_value: Any) -> None:
    """Test value model"""
    value = ValueModel({"value": test_value}, "value")
    assert value.has_value is True
    assert value.float_value() == 1


@pytest.mark.parametrize("test_value", ["1", 1])
def test_fibaro_value_str(test_value: Any) -> None:
    """Test value model"""
    value = ValueModel({"value": test_value}, "value")
    assert value.has_value is True
    assert value.str_value() == "1"


@pytest.mark.parametrize("test_value", [{"x": 1}, '{"x":1}'])
def test_fibaro_value_dict(test_value: Any) -> None:
    """Test value model"""
    value = ValueModel({"value": test_value}, "value")
    assert value.has_value is True
    assert value.dict_value() == {"x": 1}


@pytest.mark.parametrize("test_value", ["1.1", 1.1])
def test_fibaro_value_float_2(test_value: Any) -> None:
    """Test value model"""
    value = ValueModel({"value": test_value}, "value")
    assert value.has_value is True
    assert value.float_value() == 1.1


def test_fibaro_value_default() -> None:
    """Test value model"""
    value = ValueModel({}, "value")
    assert value.has_value is False
    assert value.int_value(1) == 1
    assert value.float_value(1.1) == 1.1
    assert value.bool_value(True) is True
    assert value.str_value("test") == "test"
    assert value.dict_value({"x": 1}) == {"x": 1}


@pytest.mark.parametrize("test_value", ["true", "True", True, "false", "False", False])
def test_fibaro_value_is_bool(test_value: Any) -> None:
    """Test value model"""
    value = ValueModel({"value": test_value}, "value")
    assert value.is_bool_value is True


@pytest.mark.parametrize("test_value", [0, 1, "any_value"])
def test_fibaro_value_is_bool_negative(test_value: Any) -> None:
    """Test value model"""
    value = ValueModel({"value": test_value}, "value")
    assert value.is_bool_value is False


def test_fibaro_no_value() -> None:
    """Test value model"""
    value = ValueModel({}, "value")
    assert value.has_value is False
    with pytest.raises(TypeError):
        value.int_value()
    with pytest.raises(TypeError):
        value.float_value()
    with pytest.raises(TypeError):
        value.bool_value()
    with pytest.raises(TypeError):
        value.str_value()
    with pytest.raises(TypeError):
        value.dict_value()


def test_fibaro_color() -> None:
    """Test value model"""
    value = ColorModel({"color": "0,0,0,0"}, "color")
    assert value.has_color is True
    assert value.rgbw_color == (0, 0, 0, 0)

    value = ColorModel({"color": "234,244,255,0"}, "color")
    assert value.has_color is True
    assert value.rgbw_color == (234, 244, 255, 0)

    value = ColorModel({"color": "234,255,0"}, "color")
    assert value.has_color is False
    with pytest.raises(TypeError):
        value.rgbw_color

    value = ColorModel({"color": "234,255,0"}, "color_xxxx")
    assert value.has_color is False
    with pytest.raises(TypeError):
        value.rgbw_color


@pytest.mark.parametrize("test_value", ["1,2,3,4", ["1", "2", "3", "4"], [1, 2, 3, 4]])
def test_fibaro_supported_modes(test_value: Any) -> None:
    """Test modes"""
    device = DeviceModel({"properties": {"supportedModes": test_value}}, None, 4)
    assert device.supported_modes == [1, 2, 3, 4]


@pytest.mark.parametrize("test_value", ["1,2,3,4", ["1", "2", "3", "4"], [1, 2, 3, 4]])
def test_fibaro_supported_operating_modes(test_value: Any) -> None:
    """Test operating modes"""
    device = DeviceModel(
        {"properties": {"supportedOperatingModes": test_value}}, None, 4
    )
    assert device.supported_operating_modes == [1, 2, 3, 4]


def test_fibaro_supported_thermostat_modes() -> None:
    """Test thermostat modes"""
    device = DeviceModel(
        {"properties": {"supportedThermostatModes": ["heat", "auto"]}}, None, 4
    )
    assert device.supported_thermostat_modes == ["heat", "auto"]


def test_fibaro_device_turn_on() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        mock.register_uri("GET", f"{TEST_BASE_URL}devices", json=device_payload)
        mock.register_uri("POST", f"{TEST_BASE_URL}devices/13/action/turnOn")
        mock.register_uri("GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
        mock.register_uri("GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

        client = FibaroClient(TEST_BASE_URL)
        client.set_authentication(TEST_USERNAME, TEST_PASSWORD)
        client.connect()

        devices = client.read_devices()

        assert mock.call_count == 3
        devices[2].execute_action("turnOn")
        assert mock.call_count == 4


def test_fibaro_device_invalid_action() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        mock.register_uri("GET", f"{TEST_BASE_URL}devices", json=device_payload)
        mock.register_uri("POST", f"{TEST_BASE_URL}devices/13/action/XXXX")
        mock.register_uri("GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
        mock.register_uri("GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

        client = FibaroClient(TEST_BASE_URL)
        client.set_authentication(TEST_USERNAME, TEST_PASSWORD)
        client.connect()

        devices = client.read_devices()

        assert mock.call_count == 3
        devices[2].execute_action("XXXX")
        assert mock.call_count == 4


def test_fibaro_device_action_with_param() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        mock.register_uri("GET", f"{TEST_BASE_URL}devices", json=device_payload)
        mock.register_uri("POST", f"{TEST_BASE_URL}devices/13/action/abortUpdate")
        mock.register_uri("GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
        mock.register_uri("GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

        client = FibaroClient(TEST_BASE_URL)
        client.set_authentication(TEST_USERNAME, TEST_PASSWORD)
        client.connect()

        devices = client.read_devices()

        assert mock.call_count == 3
        devices[2].execute_action("abortUpdate", [True])
        assert mock.call_count == 4
