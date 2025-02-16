"""High level connection for accessing the fibaro API."""
from __future__ import annotations

import logging

from requests import HTTPError

from .fibaro_client import FibaroClient
from .fibaro_info import InfoModel


_LOGGER = logging.getLogger(__name__)


class FibaroConnection:
    """Connection which simplifies connection to fibaro and provide access
    to the fibaro client once connected."""

    def __init__(self, url: str) -> None:
        """Construct the fibaro manager."""
        self._fibaro_client = FibaroClient(url)
        self._connected = False

    def connect(self, username: str, password: str) -> InfoModel:
        """Translate connect errors to easily differentiate auth and connect failures.

        Returns the hub info if successfully connected.
        """
        try:
            self._fibaro_client.set_authentication(username, password)
            self._fibaro_client.connect()
            self._connected = True
            return self._fibaro_client.read_info()
        except HTTPError as http_ex:
            if http_ex.response.status_code == 403:
                raise FibaroAuthenticationFailed from http_ex
            raise FibaroConnectFailed from http_ex
        except Exception as ex:
            raise FibaroConnectFailed from ex

    def fibaro_client(self) -> FibaroClient:
        """Return the connected fibaro client."""
        if not self._connected:
            raise FibaroConnectFailed()
        return self._fibaro_client


class FibaroConnectFailed(Exception):
    """Error to indicate we cannot connect to fibaro home center."""


class FibaroAuthenticationFailed(Exception):
    """Error to indicate that authentication failed on fibaro home center."""
