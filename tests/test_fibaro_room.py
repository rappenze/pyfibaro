"""Test FibaroInfo class."""

import requests_mock

from pyfibaro.fibaro_client import FibaroClient

from .test_utils import TEST_BASE_URL, TEST_PASSWORD, TEST_USERNAME, load_fixture


def test_fibaro_room() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        room_payload = load_fixture("room.json")
        mock.register_uri("GET", f"{TEST_BASE_URL}rooms", json=room_payload)
        client = FibaroClient(TEST_BASE_URL)
        client.set_authentication(TEST_USERNAME, TEST_PASSWORD)

        rooms = client.read_rooms()
        assert rooms is not None

        assert len(rooms) == 2
        assert rooms[0].fibaro_id == 4
        assert rooms[0].name == "Wohnen"
        assert mock.call_count == 1
