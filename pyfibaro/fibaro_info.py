"""Endpoint object to access the endpoint settings/info"""
import logging

from .common.const import API_VERSION_MATCHER
from .common.rest_client import RestClient

_LOGGER = logging.getLogger(__name__)


class InfoModel:
    """Fibaro info."""

    def __init__(self, rest_client: RestClient) -> None:
        """Load the data."""
        self.raw_data: dict = rest_client.get("settings/info")

    @property
    def current_version(self) -> str:
        """Returns the software version."""
        return self.raw_data.get("currentVersion").get("version")

    @property
    def serial_number(self) -> str:
        """Returns the serial number of the home center."""
        return self.raw_data.get("serialNumber")

    @property
    def hc_name(self) -> str:
        """Returns the serial number of the home center."""
        return self.raw_data.get("hcName")

    @property
    def api_version(self) -> int:
        """Returns the API version. As of writing version 4 and 5 was supported.

        When the version cannot be evaluated, it will fallback to version 4.
        """
        serial_number = self.serial_number
        for item in API_VERSION_MATCHER.items():
            if serial_number.startswith(item[0]):
                _LOGGER.debug("API version %s found by pattern %s", item[1], item[0])
                return item[1]
        return 4
