"""Main class for accessing fibaro API."""

from requests import HTTPError

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

    def __init__(self, url: str, ssl_verify: bool = False) -> None:
        """Init the fibaro client.

        The url needs to be in the format http(s)://<HOST>/api/.

        You can use ssl_verify to enable SSL certificate validation, but be
        aware that you need to register the fibaro certificates yourself
        to make it work. Also please be aware that the InsecureRequestWarning
        is not suppressed by default, so if you need to suppress warnings you
        need something like:

        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        """
        self._rest_client = RestClient(url, ssl_verify)
        self._frontend_url = url.removesuffix("/api/")
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
        login, _ = self._login()
        return login.is_logged_in

    def connect_with_credentials(self, username: str, password: str) -> InfoModel:
        """Connect with given credentials.
        Translate connect errors to easily differentiate auth and connect failures.

        Returns the hub info if successfully connected.
        Raises:
        FibaroAuthenticationFailed: If credentials are invalid
        FibaroConnectFailed: If connection is not possible
        """
        try:
            self.set_authentication(username, password)
            _, info = self._login()
            return info
        except HTTPError as http_ex:
            if http_ex.response.status_code == 403:
                raise FibaroAuthenticationFailed from http_ex
            raise FibaroConnectFailed from http_ex
        except Exception as ex:
            raise FibaroConnectFailed from ex

    def _login(self) -> tuple[LoginModel, InfoModel]:
        login = LoginModel(self._rest_client)
        info = self.read_info()

        # Read the API version as it is needed regularly
        self._api_version = info.api_version

        return (login, info)

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

    def frontend_url(self) -> str:
        """Return the url to the web frontend of the fibaro hub."""
        return self._frontend_url


class FibaroConnectFailed(Exception):
    """Error to indicate we cannot connect to fibaro home center."""


class FibaroAuthenticationFailed(Exception):
    """Error to indicate that authentication failed on fibaro home center."""
