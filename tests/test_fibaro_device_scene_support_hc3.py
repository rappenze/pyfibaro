"""Test FibaroInfo class."""

import requests_mock

from pyfibaro.fibaro_client import FibaroClient

from .test_utils import TEST_BASE_URL, TEST_PASSWORD, TEST_USERNAME, load_fixture

device_payload = load_fixture("device-scene-support-hc3.json")
login_payload = load_fixture("login_success.json")
info_payload = load_fixture("info.json")


def test_fibaro_device_scene_support() -> None:
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

        assert devices[2].has_central_scene_event is True
        # Invalid value returns False
        central_scene_event = devices[2].central_scene_event
        assert len(central_scene_event) == 2
        assert central_scene_event[0].key_id == 1
        assert central_scene_event[0].key_event_types == [
            "Pressed",
            "Released",
            "HeldDown",
            "Pressed2",
            "Pressed3",
        ]

        assert devices[1].has_central_scene_event is False
        assert devices[1].central_scene_event == []
