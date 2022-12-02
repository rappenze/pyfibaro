"""Rest client for accessing the fibaro API."""
from __future__ import annotations

import logging
from typing import Any

from requests import Response, Session
from requests.auth import HTTPBasicAuth
from requests.exceptions import JSONDecodeError

from .const import HTTP_HEADERS, TIMEOUT

_LOGGER = logging.getLogger(__name__)


class RestClient:
    """Rest client for fibaro home center."""

    def __init__(
        self, url: str, username: str | None = None, password: str | None = None
    ) -> None:
        """Init"""
        self._session = Session()
        self._session.headers = HTTP_HEADERS
        self._base_url = url
        if username and password:
            self.set_auth(username, password)

    def set_auth(self, username: str, password: str) -> None:
        """Set the credentials for the fibaro home center."""
        self._session.auth = HTTPBasicAuth(username, password)

    def get(self, endpoint: str, json: Any | None = None) -> Any:
        """Execute a get request."""
        response = self._session.get(
            f"{self._base_url}{endpoint}", json=json, timeout=TIMEOUT
        )

        return self._process_json_result(response)

    def post(self, endpoint: str, json: Any | None = None) -> Any:
        """Execute a post request."""
        response = self._session.post(
            f"{self._base_url}{endpoint}", json=json, timeout=TIMEOUT
        )

        return self._process_json_result(response)

    def close(self) -> None:
        """Close the session."""
        self._session.close()

    def _process_json_result(self, resp: Response) -> Any:
        """Do error handling and logging on a HTTP response and covert to json."""
        _LOGGER.debug(
            '%s "%s": %s', resp.request.method, resp.request.url, resp.status_code
        )

        resp.raise_for_status()

        try:
            json = resp.json()
            _LOGGER.debug("Response: %s", json)
            return json
        except JSONDecodeError:
            _LOGGER.debug("No response")
            return None
