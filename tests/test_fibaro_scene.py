"""Test SceneModel class."""

import pytest
import requests_mock

from pyfibaro.fibaro_client import FibaroClient

from .test_utils import TEST_BASE_URL, TEST_PASSWORD, TEST_USERNAME, load_fixture

scene_payload = load_fixture("scene.json")
login_payload = load_fixture("login_success.json")
info_payload = load_fixture("info.json")


def test_fibaro_scene() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        mock.register_uri("GET", f"{TEST_BASE_URL}scenes", json=scene_payload)
        mock.register_uri("GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
        mock.register_uri("GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

        client = FibaroClient(TEST_BASE_URL)
        client.set_authentication(TEST_USERNAME, TEST_PASSWORD)
        client.connect()

        scenes = client.read_scenes()
        assert scenes is not None

        assert len(scenes) == 2
        assert scenes[0].fibaro_id == 2
        assert scenes[0].name == "Go to bed"
        assert scenes[0].room_id == 5
        assert scenes[0].visible is True
        assert mock.call_count == 3


def test_fibaro_scene_start() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        mock.register_uri("GET", f"{TEST_BASE_URL}scenes", json=scene_payload)
        mock.register_uri("POST", f"{TEST_BASE_URL}scenes/2/action/start")
        mock.register_uri("GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
        mock.register_uri("GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

        client = FibaroClient(TEST_BASE_URL)
        client.set_authentication(TEST_USERNAME, TEST_PASSWORD)
        client.connect()

        scenes = client.read_scenes()

        assert mock.call_count == 3
        scenes[0].start()
        assert mock.call_count == 4


def test_fibaro_scene_start_with_pin_raise_exception() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        mock.register_uri("GET", f"{TEST_BASE_URL}scenes", json=scene_payload)
        mock.register_uri("POST", f"{TEST_BASE_URL}scenes/2/action/start")
        mock.register_uri("GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
        mock.register_uri("GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

        client = FibaroClient(TEST_BASE_URL)
        client.set_authentication(TEST_USERNAME, TEST_PASSWORD)
        client.connect()

        scenes = client.read_scenes()

        assert mock.call_count == 3

        with pytest.raises(NotImplementedError):
            scenes[0].start("1234")
        assert mock.call_count == 3


def test_fibaro_scene_stop() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        mock.register_uri("GET", f"{TEST_BASE_URL}scenes", json=scene_payload)
        mock.register_uri("POST", f"{TEST_BASE_URL}scenes/2/action/stop")
        mock.register_uri("GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
        mock.register_uri("GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

        client = FibaroClient(TEST_BASE_URL)
        client.set_authentication(TEST_USERNAME, TEST_PASSWORD)
        client.connect()

        scenes = client.read_scenes()

        assert mock.call_count == 3
        scenes[0].stop()
        assert mock.call_count == 4


def test_fibaro_scene_stop_with_pin_raises_exception() -> None:
    """Test get request"""
    with requests_mock.Mocker() as mock:
        assert isinstance(mock, requests_mock.Mocker)

        mock.register_uri("GET", f"{TEST_BASE_URL}scenes", json=scene_payload)
        mock.register_uri("POST", f"{TEST_BASE_URL}scenes/2/action/stop")
        mock.register_uri("GET", f"{TEST_BASE_URL}loginStatus", json=login_payload)
        mock.register_uri("GET", f"{TEST_BASE_URL}settings/info", json=info_payload)

        client = FibaroClient(TEST_BASE_URL)
        client.set_authentication(TEST_USERNAME, TEST_PASSWORD)
        client.connect()

        scenes = client.read_scenes()

        assert mock.call_count == 3
        with pytest.raises(NotImplementedError):
            scenes[0].stop("1234")
        assert mock.call_count == 3
