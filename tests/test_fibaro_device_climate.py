"""Test climate device properties."""
from __future__ import annotations


import requests_mock

from pyfibaro.fibaro_client import FibaroClient

from .test_utils import TEST_BASE_URL, TEST_PASSWORD, TEST_USERNAME, load_fixture

device_payload = load_fixture("device-climate.json")
login_payload = load_fixture("login_success.json")
info_payload = load_fixture("info.json")


def test_fibaro_climate_device() -> None:
    """Test climate properties"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        mock.register_uri(
            "GET", f"{TEST_BASE_URL}devices", json=device_payload)
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

        client = FibaroClient(TEST_BASE_URL)
        client.set_authentication(TEST_USERNAME, TEST_PASSWORD)
        client.connect()

        devices = client.read_devices()
        assert devices is not None

        assert len(devices) == 3
        assert devices[1].has_thermostat_fan_mode is True
        assert devices[1].thermostat_fan_mode == "Low"
        assert devices[1].has_supported_thermostat_fan_modes is True
        assert devices[1].supported_thermostat_fan_modes == [
            "Low", "High", "Medium"]
        assert devices[1].has_thermostat_mode is True
        assert devices[1].thermostat_mode == "Heat"
        assert devices[1].has_supported_thermostat_modes is True
        assert devices[1].supported_thermostat_modes == [
            "Off", "Heat", "Cool", "Fan"]
        assert devices[1].has_thermostat_operating_state is True
        assert devices[1].thermostat_operating_state == "Heating"
        assert devices[1].has_heating_thermostat_setpoint is True
        assert devices[1].heating_thermostat_setpoint == 20.5
        assert devices[1].has_heating_thermostat_setpoint_future is True
        assert devices[1].heating_thermostat_setpoint_future == 20.5
        assert devices[1].has_cooling_thermostat_setpoint is True
        assert devices[1].cooling_thermostat_setpoint == 25.0
        assert devices[1].has_cooling_thermostat_setpoint_future is True
        assert devices[1].cooling_thermostat_setpoint_future == 25.0
