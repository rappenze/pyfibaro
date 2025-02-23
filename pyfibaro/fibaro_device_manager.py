"""High level controller to access devices over the Fibaro API.

This adds a structural layer over the plain fibaro API which does a lot of
device detection logic and exposes properties in a more understandable way.
"""

from __future__ import annotations

import logging
from collections.abc import Callable

from .fibaro_state_multiplexer import FibaroStateMultiplexer
from .fibaro_client import FibaroClient
from .fibaro_device import DeviceModel
from .fibaro_state_resolver import FibaroEvent

_LOGGER = logging.getLogger(__name__)


class FibaroDeviceManager:
    """Controller to access fibaro API in a more structured way."""

    def __init__(
        self, fibaro_client: FibaroClient, include_devices_from_plugins: bool = False
    ) -> None:
        """Construct the fibaro device manager.
        - Load initial data
        - Open push channel"""
        self._fibaro_client = fibaro_client
        self._fibaro_state_multiplexer = FibaroStateMultiplexer(
            fibaro_client, include_devices_from_plugins
        )
        self._fibaro_state_multiplexer.start()

    def add_change_listener(
        self, fibaro_id: int, listener: Callable[[DeviceModel], None]
    ) -> Callable[[], None]:
        """Add a listener to get property changes.
        Provides the updated device data.

        Returns: Callback which can be used to unregister the listener"""
        return self._fibaro_state_multiplexer.add_change_listener(fibaro_id, listener)

    def add_event_listener(
        self, fibaro_id: int, listener: Callable[[FibaroEvent], None]
    ) -> Callable[[], None]:
        """Add scene event listener.

        Returns: Callback which can be used to unregister the listener"""
        return self._fibaro_state_multiplexer.add_event_listener(fibaro_id, listener)

    def get_devices(self) -> list[DeviceModel]:
        """Get current devices from Fibaro Home Center."""
        return self._fibaro_state_multiplexer.get_devices()

    def close(self) -> None:
        """Close push channel."""
        self._fibaro_state_multiplexer.stop()
