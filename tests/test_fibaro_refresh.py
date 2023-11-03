"""Test FibaroStateHandler class."""

import time

import pytest
import requests_mock

from pyfibaro.fibaro_client import FibaroClient

from .test_utils import (TEST_BASE_URL, TEST_PASSWORD, TEST_USERNAME,
                         load_fixture)

refresh_payload = load_fixture("refresh.json")
login_payload = load_fixture("login_success.json")
info_payload = load_fixture("info.json")


class TestRefresh:
    """Use a test class to get async state."""

    callback_result = None

    def callback_function(self, event) -> None:
        """The callback handler for this test."""
        self.callback_result = event

    def callback_exception(self, event) -> None:
        """The callback handler for this test."""
        self.callback_result = event
        raise TypeError()

    def test_fibaro_refresh(self) -> None:
        """Test get request"""
        with requests_mock.Mocker() as mock:
            assert isinstance(mock, requests_mock.Mocker)

            mock.register_uri(
                "GET", f"{TEST_BASE_URL}refreshStates", json=refresh_payload
            )
            mock.register_uri("GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
            mock.register_uri("GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

            client = FibaroClient(TEST_BASE_URL)
            client.set_authentication(TEST_USERNAME, TEST_PASSWORD)
            client.connect()

            client.register_update_handler(self.callback_function)
            time.sleep(0.1)
            client.unregister_update_handler()

            assert self.callback_result is not None
            assert mock.call_count > 2

    def test_fibaro_refresh_fail(self) -> None:
        """Test get request"""
        with requests_mock.Mocker() as mock:
            assert isinstance(mock, requests_mock.Mocker)

            mock.register_uri("GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
            mock.register_uri("GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

            client = FibaroClient(TEST_BASE_URL)
            client.set_authentication(TEST_USERNAME, TEST_PASSWORD)
            client.connect()

            client.register_update_handler(self.callback_function)
            time.sleep(1.1)
            client.unregister_update_handler()

            assert self.callback_result is None
            assert mock.call_count > 2

    def test_fibaro_refresh_double_register(self) -> None:
        """Test get request"""
        with requests_mock.Mocker() as mock:
            assert isinstance(mock, requests_mock.Mocker)

            mock.register_uri("GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
            mock.register_uri("GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

            client = FibaroClient(TEST_BASE_URL)
            client.set_authentication(TEST_USERNAME, TEST_PASSWORD)
            client.connect()
            client.register_update_handler(self.callback_function)

            with pytest.raises(Exception):
                client.register_update_handler(self.callback_function)

            client.unregister_update_handler()

    def test_fibaro_refresh_callback_exception(self) -> None:
        """Test get request"""
        with requests_mock.Mocker() as mock:
            assert isinstance(mock, requests_mock.Mocker)

            mock.register_uri(
                "GET", f"{TEST_BASE_URL}refreshStates", json=refresh_payload
            )
            mock.register_uri("GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
            mock.register_uri("GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

            client = FibaroClient(TEST_BASE_URL)
            client.set_authentication(TEST_USERNAME, TEST_PASSWORD)
            client.connect()

            client.register_update_handler(self.callback_exception)
            time.sleep(0.1)
            client.unregister_update_handler()

            assert self.callback_result is not None
            assert mock.call_count > 2
