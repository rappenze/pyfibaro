"""Endpoint object to access the endpoint settings/info"""

import logging

from .common.const import (
    API_VERSION_MATCHER,
    MANUFACTURER_NAME_MATCHER,
    MODEL_NAME_MATCHER,
)
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
        return self.raw_data.get("softVersion")

    @property
    def serial_number(self) -> str:
        """Returns the serial number of the home center."""
        return self.raw_data.get("serialNumber")

    @property
    def hc_name(self) -> str:
        """Returns the serial number of the home center."""
        return self.raw_data.get("hcName")

    @property
    def mac_address(self) -> str:
        """Returns the mac address of the home center."""
        return self.raw_data.get("mac")

    @property
    def api_version(self) -> int:
        """Returns the API version. As of writing version 4 and 5 was supported.

        When the version cannot be evaluated, it will fallback to version 5.
        """
        serial_number = self.serial_number
        for item in API_VERSION_MATCHER.items():
            if serial_number.startswith(item[0]):
                _LOGGER.debug(
                    "API version %s found by pattern %s", item[1], item[0])
                return item[1]
        return 5

    @property
    def platform(self) -> str:
        """Returns the model abbreviation of the home center.

        One of HC3, HC3L, YH, HC2 or HCL.
        """
        # This API is only available on newer models, therefore
        # we simulate an answer for older models.
        return self.raw_data.get("platform", self.serial_number[:3])

    @property
    def model_name(self) -> str:
        """Returns the name of the hub model.

        When the model cannot be evaluated, it will fallback to Hub.
        """
        serial_number = self.serial_number
        for item in MODEL_NAME_MATCHER.items():
            if serial_number.startswith(item[0]):
                return item[1]
        return "Hub"

    @property
    def manufacturer_name(self) -> str:
        """Returns the name of the hub model.

        When the model cannot be evaluated, it will fallback to Fibaro.
        """
        serial_number = self.serial_number
        for item in MANUFACTURER_NAME_MATCHER.items():
            if serial_number.startswith(item[0]):
                return item[1]
        return "Fibaro"
