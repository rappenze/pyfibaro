"""Main class for accessing fibaro API."""

from .common.rest_client import RestClient
from .fibaro_device import DeviceModel
from .fibaro_info import InfoModel
from .fibaro_login import LoginModel
from .fibaro_room import RoomModel
from .fibaro_scene import SceneModel
from .fibaro_state_handler import FibaroStateHandler


class FibaroClient:
    """Fibaro client.

    This is the main entry point to access the fibaro API.

    Usage:
    Use set_authentication() to provide the credentials
    Use connect() to establish the connection and check if the credentials are valid
    Use any other method to access API data and actions
    """

    def __init__(self, url: str) -> None:
        """Init the fibaro client.

        The url needs to be in the format http://<HOST>/api/.
        """
        self._rest_client = RestClient(url)
        self._api_version: int = None
        self._state_handler: FibaroStateHandler = None

    def set_authentication(self, username: str, password: str) -> None:
        """Set the credentials."""
        self._rest_client.set_auth(username, password)

    def connect(self) -> bool:
        """Returns the login status.

        Returns:
        True if authenticated, False if not authenticated

        Raises:
        HTTPError: If there is a connection problem. Most important is HTTPError
        with status 403 which raised if invalid credentials are provided.
        """
        login = LoginModel(self._rest_client)

        # Read the API version as it is needed regularly
        self._api_version = self.read_info().api_version

        return login.is_logged_in

    def read_info(self) -> InfoModel:
        """Read the info endpoint from home center."""
        return InfoModel(self._rest_client)

    def read_rooms(self) -> list[RoomModel]:
        """Read the rooms endpoint from home center."""
        return RoomModel.read_rooms(self._rest_client)

    def read_scenes(self) -> list[SceneModel]:
        """Read the scenes endpoint from home center."""
        return SceneModel.read_scenes(self._rest_client, self._api_version)

    def read_devices(self) -> list[DeviceModel]:
        """Read the devices endpoint from home center."""
        return DeviceModel.read_devices(self._rest_client, self._api_version)

    def register_update_handler(self, callback: callable) -> None:
        """Register a state handler."""
        if self._state_handler:
            raise Exception("There is already a state handler registered")
        self._state_handler = FibaroStateHandler(self._rest_client, callback)

    def unregister_update_handler(self) -> None:
        """Unregister the state handler."""
        if self._state_handler:
            self._state_handler.stop()
            self._state_handler = None
