"""Test rest client."""

import requests_mock

from pyfibaro.common.rest_client import RestClient

from .test_utils import TEST_BASE_URL, TEST_PASSWORD, TEST_USERNAME, load_fixture

info_payload = load_fixture("info.json")


def test_get_request() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)
        mock.register_uri("GET", f"{TEST_BASE_URL}settings/info", json=info_payload)
        client = RestClient(TEST_BASE_URL, False, TEST_USERNAME, TEST_PASSWORD)
        response = client.get("settings/info")

        assert mock.call_count == 1
        assert response == info_payload


def test_https_get_request() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)
        url = "https://192.169.1.40/api/"
        mock.register_uri("GET", f"{url}settings/info", json=info_payload)
        client = RestClient(url, True, TEST_USERNAME, TEST_PASSWORD)
        response = client.get("settings/info")

        assert mock.call_count == 1
        assert response == info_payload


def test_post_request() -> None:
    """Test post request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)
        mock.register_uri("POST", f"{TEST_BASE_URL}settings/info", json=info_payload)
        client = RestClient(TEST_BASE_URL, False, TEST_USERNAME, TEST_PASSWORD)
        response = client.post("settings/info", info_payload)

        assert mock.call_count == 1
        assert response == info_payload
