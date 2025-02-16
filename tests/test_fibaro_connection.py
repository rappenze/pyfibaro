"""Test fibaro connection."""

import pytest
import requests_mock

from pyfibaro.fibaro_connection import (
    FibaroAuthenticationFailed,
    FibaroConnection,
    FibaroConnectFailed,
)

from .test_utils import TEST_BASE_URL, TEST_PASSWORD, TEST_USERNAME, load_fixture

login_payload = load_fixture("login_success.json")
info_payload = load_fixture("info.json")


def test_connect_failed_with_exception() -> None:
    """Test any exception."""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

        connection = FibaroConnection(TEST_BASE_URL)

        with pytest.raises(FibaroConnectFailed):
            connection.connect(TEST_USERNAME, TEST_PASSWORD)


def test_connect_failed_with_http_error() -> None:
    """Test http error."""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}loginStatus", status_code=500)
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

        connection = FibaroConnection(TEST_BASE_URL)

        with pytest.raises(FibaroConnectFailed):
            connection.connect(TEST_USERNAME, TEST_PASSWORD)


def test_invalid_authentication() -> None:
    """Test invalid password."""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}loginStatus", status_code=403)
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

        connection = FibaroConnection(TEST_BASE_URL)

        with pytest.raises(FibaroAuthenticationFailed):
            connection.connect(TEST_USERNAME, TEST_PASSWORD)


def test_connect_succeed() -> None:
    """Test connect succeeds."""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

        connection = FibaroConnection(TEST_BASE_URL)
        info = connection.connect(TEST_USERNAME, TEST_PASSWORD)

        assert mock.call_count == 3
        assert info.raw_data == info_payload

        fibaro_client = connection.fibaro_client()
        assert fibaro_client is not None


def test_fibaro_client_exception_when_called_without_connect() -> None:
    """Test call sequence incorrect."""
    connection = FibaroConnection(TEST_BASE_URL)

    with pytest.raises(FibaroConnectFailed):
        connection.fibaro_client()
