"""Test FibaroInfo class."""

import requests_mock

from pyfibaro.fibaro_client import FibaroClient

from .test_utils import TEST_BASE_URL, TEST_PASSWORD, TEST_USERNAME, load_fixture


def test_fibaro_connect_success() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        login_payload = load_fixture("login_success.json")
        info_payload = load_fixture("info.json")

        mock.register_uri("GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
        mock.register_uri("GET", f"{TEST_BASE_URL}settings/info", json=info_payload)
        client = FibaroClient(TEST_BASE_URL)
        client.set_authentication(TEST_USERNAME, TEST_PASSWORD)
        logged_in = client.connect()

        assert logged_in is True
        assert mock.call_count == 2


def test_fibaro_connect_fail() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        login_payload = load_fixture("login_fail.json")
        info_payload = load_fixture("info.json")

        mock.register_uri("GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
        mock.register_uri("GET", f"{TEST_BASE_URL}settings/info", json=info_payload)
        client = FibaroClient(TEST_BASE_URL)
        logged_in = client.connect()

        assert logged_in is False
        assert mock.call_count == 2
