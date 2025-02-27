"""Test fibaro connection."""

import pytest
import requests_mock

from pyfibaro.fibaro_client import FibaroClient
from pyfibaro.fibaro_client import (
    FibaroAuthenticationFailed,
    FibaroConnectFailed
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

        client = FibaroClient(TEST_BASE_URL)

        with pytest.raises(FibaroConnectFailed):
            client.connect_with_credentials(TEST_USERNAME, TEST_PASSWORD)


def test_connect_failed_with_http_error() -> None:
    """Test http error."""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}loginStatus", status_code=500)
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

        client = FibaroClient(TEST_BASE_URL)

        with pytest.raises(FibaroConnectFailed):
            client.connect_with_credentials(TEST_USERNAME, TEST_PASSWORD)


def test_invalid_authentication() -> None:
    """Test invalid password."""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}loginStatus", status_code=403)
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

        client = FibaroClient(TEST_BASE_URL)

        with pytest.raises(FibaroAuthenticationFailed):
            client.connect_with_credentials(TEST_USERNAME, TEST_PASSWORD)


def test_connect_succeed() -> None:
    """Test connect succeeds."""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

        client = FibaroClient(TEST_BASE_URL)
        info = client.connect_with_credentials(TEST_USERNAME, TEST_PASSWORD)

        assert mock.call_count == 2
        assert info.raw_data == info_payload


def test_frontend_url() -> None:
    """Test frontend url getter."""
    client = FibaroClient(TEST_BASE_URL)
    assert client.frontend_url() == TEST_BASE_URL.removesuffix("/api/")
