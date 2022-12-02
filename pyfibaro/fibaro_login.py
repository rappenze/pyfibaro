"""Endpoint object to access the endpoint settings/info"""

from .common.rest_client import RestClient


class LoginModel:
    """Fibaro login."""

    def __init__(self, rest_client: RestClient) -> None:
        """Load the data."""
        self.raw_data: dict = rest_client.get("loginStatus")

    @property
    def is_logged_in(self) -> bool:
        """Returns the software version."""
        return self.raw_data.get("status")
