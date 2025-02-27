"""Fibaro state multiplexer receives all information from the push channel and
provides methods to register listeners for specific devices.
"""

import logging
from typing import Any
from collections.abc import Callable

from .fibaro_client import FibaroClient
from .fibaro_device import DeviceModel
from .fibaro_data_helper import read_devices
from .fibaro_state_resolver import FibaroEvent, FibaroStateChange, FibaroStateResolver


_LOGGER = logging.getLogger(__name__)


class FibaroStateMultiplexer:
    """State and event multiplexer."""

    def __init__(
        self, fibaro_client: FibaroClient, include_devices_from_plugins: bool = False
    ) -> None:
        """Initialize the fibaro state multiplexer."""
        self._fibaro_client = fibaro_client
        self._include_devices_from_plugins = include_devices_from_plugins
        self._devices: dict[int, DeviceModel] = {}

        self._change_listeners: dict[int,
                                     list[Callable[[DeviceModel], None]]] = {}
        self._event_listeners: dict[int,
                                    list[Callable[[FibaroEvent], None]]] = {}

    def start(self) -> None:
        """Connect push channel and load initial device state.
        This starts change and event dispatching."""
        self._devices = {
            device.fibaro_id: device
            for device in read_devices(
                self._fibaro_client, self._include_devices_from_plugins
            )
        }
        self._fibaro_client.register_update_handler(self._on_change)

    def stop(self) -> None:
        """Disconnect push channel so that no change and events are dispatched anymore."""
        self._fibaro_client.unregister_update_handler()
        self._devices = {}

    def add_change_listener(
        self, fibaro_id: int, listener: Callable[[DeviceModel], None]
    ) -> Callable[[], None]:
        """Add a listener to get property changes."""
        change_listeners = self._change_listeners.setdefault(fibaro_id, [])
        change_listeners.append(listener)

        return lambda: change_listeners.remove(listener)

    def add_event_listener(
        self, fibaro_id: int, listener: Callable[[FibaroEvent], None]
    ) -> Callable[[], None]:
        """Add event listener."""
        event_listeners = self._event_listeners.setdefault(fibaro_id, [])
        event_listeners.append(listener)

        return lambda: event_listeners.remove(listener)

    def get_devices(self) -> list[DeviceModel]:
        """Return the current device state."""
        return list(self._devices.values())

    def _on_change(self, state: Any) -> None:
        # update internal device model and notify registered listeners
        resolver = FibaroStateResolver(state)

        for state_change in resolver.get_state_updates():
            fibaro_id = state_change.fibaro_id
            device = self._devices.get(fibaro_id)
            if device:
                self._update_device_data(device, state_change)
                for listener in self._change_listeners.get(fibaro_id, []):
                    listener(device)

        for event in resolver.get_events():
            # event does not always have a fibaro id, therefore it is
            # essential that we first check for it
            fibaro_id = event.fibaro_id
            if fibaro_id:
                for listener in self._event_listeners.get(fibaro_id, []):
                    listener(event)

    def _update_device_data(
        self, device: DeviceModel, state_change: FibaroStateChange
    ) -> None:
        # update the internal data object to keep it always current
        for key, value in state_change.property_changes.items():
            device.properties[key] = value
            _LOGGER.debug(
                "New state %s[%s].%s = %s", device.name, device.fibaro_id, key, str(
                    value)
            )
