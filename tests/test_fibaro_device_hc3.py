"""Test FibaroInfo class."""

import requests_mock

from pyfibaro.fibaro_client import FibaroClient

from .test_utils import TEST_BASE_URL, TEST_PASSWORD, TEST_USERNAME, load_fixture

device_payload = load_fixture("device-hc3.json")
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

        assert len(devices) == 4
        assert devices[0].fibaro_id == 1
        assert devices[0].name == "zwave"
        assert devices[0].parent_fibaro_id == 0
        assert devices[0].type == "com.fibaro.zwavePrimaryController"
        assert devices[0].base_type == ""
        assert devices[0].room_id == 219
        assert isinstance(devices[0].actions, dict)
        assert isinstance(devices[0].properties, dict)
        assert mock.call_count == 3
        assert devices[0].has_dead is True
        assert devices[0].dead is True
        assert devices[0].has_dead_reason is True
        assert devices[0].dead_reason == "Connection problem"


def test_fibaro_device_turn_on() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        mock.register_uri("GET", f"{TEST_BASE_URL}devices", json=device_payload)
        mock.register_uri("POST", f"{TEST_BASE_URL}devices/7/action/turnOn")
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
        mock.register_uri("POST", f"{TEST_BASE_URL}devices/7/action/XXXX")
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
        mock.register_uri("POST", f"{TEST_BASE_URL}devices/7/action/abortUpdate")
        mock.register_uri("GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
        mock.register_uri("GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

        client = FibaroClient(TEST_BASE_URL)
        client.set_authentication(TEST_USERNAME, TEST_PASSWORD)
        client.connect()

        devices = client.read_devices()

        assert mock.call_count == 3
        devices[2].execute_action("abortUpdate", [True])
        assert mock.call_count == 4
