"""Test FibaroInfo class."""

import requests_mock

from pyfibaro.fibaro_client import FibaroClient

from .test_utils import TEST_BASE_URL, TEST_PASSWORD, TEST_USERNAME, load_fixture

device_payload = load_fixture("device-armed.json")
login_payload = load_fixture("login_success.json")
info_payload = load_fixture("info.json")


def test_fibaro_device_armed() -> None:
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

        assert devices[1].has_armed is True
        # Invalid value returns False
        assert devices[1].armed is False

        assert devices[2].has_armed is True
        assert devices[2].armed is True
