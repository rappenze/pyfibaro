"""Test FibaroInfo class."""

import pytest
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
        assert fibaro_info.mac_address == "00:22:4d:b7:13:24"


@pytest.mark.parametrize(
    "serial_number,api_version", [
        ("HC3-111111", 5), ("HC2-111111", 4), ("INVALID", 5)]
)
def test_api_version(serial_number: str, api_version: int) -> None:
    """Test API version"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        test_payload_copy = info_payload.copy()
        test_payload_copy["serialNumber"] = serial_number
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}settings/info", json=test_payload_copy
        )
        client = RestClient(TEST_BASE_URL, TEST_USERNAME, TEST_PASSWORD)

        fibaro_info = InfoModel(client)

        assert mock.call_count == 1
        assert fibaro_info.api_version == api_version


@pytest.mark.parametrize(
    "serial_number,name",
    [
        ("HC3-111111", "Home Center 3"),
        ("HC2-111111", "Home Center 2"),
        ("INVALID", "Hub"),
    ],
)
def test_model_name_resolution(serial_number: str, name: int) -> None:
    """Test name resolution"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        test_payload_copy = info_payload.copy()
        test_payload_copy["serialNumber"] = serial_number
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}settings/info", json=test_payload_copy
        )
        client = RestClient(TEST_BASE_URL, TEST_USERNAME, TEST_PASSWORD)

        fibaro_info = InfoModel(client)

        assert mock.call_count == 1
        assert fibaro_info.model_name == name


@pytest.mark.parametrize(
    "serial_number,name",
    [
        ("HC3-111111", "Fibaro"),
        ("HC2-111111", "Fibaro"),
        ("ZB", "ZOOZ"),
        ("INVALID", "Fibaro"),
    ],
)
def test_manufacturer_name_resolution(serial_number: str, name: int) -> None:
    """Test name resolution"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        test_payload_copy = info_payload.copy()
        test_payload_copy["serialNumber"] = serial_number
        mock.register_uri(
            "GET", f"{TEST_BASE_URL}settings/info", json=test_payload_copy
        )
        client = RestClient(TEST_BASE_URL, TEST_USERNAME, TEST_PASSWORD)

        fibaro_info = InfoModel(client)

        assert mock.call_count == 1
        assert fibaro_info.manufacturer_name == name


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
