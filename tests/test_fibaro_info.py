"""Test FibaroInfo class."""

import requests_mock

from pyfibaro.common.rest_client import RestClient
from pyfibaro.fibaro_client import FibaroClient
from pyfibaro.fibaro_info import InfoModel

from .test_utils import TEST_BASE_URL, TEST_PASSWORD, TEST_USERNAME, load_fixture

info_payload = load_fixture("info.json")


def test_extract_info() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}settings/info", json=info_payload)
        client = RestClient(TEST_BASE_URL, TEST_USERNAME, TEST_PASSWORD)

        fibaro_info = InfoModel(client)

        assert mock.call_count == 1
        assert fibaro_info.raw_data == info_payload
        assert fibaro_info.current_version == "4.630"
        assert fibaro_info.hc_name == "My Home"
        assert fibaro_info.serial_number == "HC2-011111"
        assert fibaro_info.platform == "HC2"


def test_api_version_hc2() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}settings/info", json=info_payload)
        client = RestClient(TEST_BASE_URL, TEST_USERNAME, TEST_PASSWORD)

        fibaro_info = InfoModel(client)

        assert mock.call_count == 1
        assert fibaro_info.api_version == 4


def test_api_version_hc3() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        test_payload_copy = info_payload.copy()
        test_payload_copy["serialNumber"] = "HC3-111111"
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}settings/info", json=test_payload_copy
        )
        client = RestClient(TEST_BASE_URL, TEST_USERNAME, TEST_PASSWORD)

        fibaro_info = InfoModel(client)

        assert mock.call_count == 1
        assert fibaro_info.api_version == 5


def test_api_version_invalid() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        test_payload_copy = info_payload.copy()
        test_payload_copy["serialNumber"] = "XXXXXXXXXXXX"
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}settings/info", json=test_payload_copy
        )
        client = RestClient(TEST_BASE_URL, TEST_USERNAME, TEST_PASSWORD)

        fibaro_info = InfoModel(client)

        assert mock.call_count == 1
        assert fibaro_info.api_version == 4


def test_fibaro_info() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        mock.register_uri(
            "GET", f"{TEST_BASE_URL}settings/info", json=info_payload)
        client = FibaroClient(TEST_BASE_URL)
        client.set_authentication(TEST_USERNAME, TEST_PASSWORD)

        assert client.read_info() is not None
        assert mock.call_count == 1
